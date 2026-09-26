import requests
import json
from requests.exceptions import HTTPError, Timeout, RequestException
from urllib.parse import urlparse, parse_qs


"""
Paginación iterativa y streaming de registros JSONLines a disco.
"""


def get_repository_commits(username:str, repository:str) -> None:
    url = f"https://api.github.com/repos/{username}/{repository}/commits"

    params = {
        "per_page": 30,
        "page": 1
    }

    commit_count = 0

    while True:
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            commits = response.json()

        except HTTPError as e:
            if response.status_code == 404:
                print(f"Error: El usuario '{username}' no existe en GitHub.")
            else:
                print(f"Error HTTP: {e}")
            return
        except Timeout as e:
            print(f"Request timed out: {e}")
            return
        except RequestException as e:
            print(f"Error fetching repositories: {e}")
            return

        if not commits:
            break

        with open("commits.jsonl", "a") as f:

            for commit in commits:
                if commit_count >= 100:
                    print("Se ha alcanzado el límite de 100 commits. Deteniendo la extracción.")
                    return
                f.write(json.dumps(commit) + "\n")
                commit_count += 1

        # verificar si hay enlaces de paginacion en los encabezados de la respuesta
        if 'Link' not in response.headers:
            break

        links = response.headers['Link'].split(',')
        link = next((link.split(';')[0].strip('<>') for link in links if 'rel="next"' in link), None)

        if link:
            parsed_url = urlparse(link)
            query_params = parse_qs(parsed_url.query)
            params['page'] = int(query_params.get('page', [1])[0])  # actualizar el número de página para la siguiente solicitud
        else:
            break


if __name__ == "__main__":
    username = "octocat"
    repository = "Hello-World"
    get_repository_commits(username, repository)