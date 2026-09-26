import requests
from collections import Counter
from requests.exceptions import HTTPError, Timeout, RequestException

"""
Extracción de datos de perfil y métricas con requests.get() y manejo de excepciones.
"""

def get_profile(username:str) -> None:

    url = f"https://api.github.com/users/{username}"

    response = requests.get(url)

    #print (response.json())
    #print (response.status_code)
    #print (response.headers)

def get_repos(username:str) -> None:

    url = f"https://api.github.com/users/{username}/repos"

    params = {
        "sort": "created",
        "direction": "desc"
    }

    response = requests.get(url, params=params, timeout=10)

    repos = response.json()
    print(f"Repos of {username}:")
    for repo in repos:
        print(f"- {repo['name']} - {repo['language'] or 'Sin definir'} (Created at: {repo['created_at']})")

def get_languages(username:str) -> None:

    url = f"https://api.github.com/users/{username}/repos"

    query_params = {"per_page": 100}

    try :
        response = requests.get(url, params=query_params, timeout=10)
        response.raise_for_status()
        repos = response.json()
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

    languages = [repo['language'] or "Sin Especificar" for repo in repos]

    counter = Counter(languages)

    print(f"Languages used by {username}:")
    for lang, count in counter.items():
        if lang is None:
            lang = "Sin Especificar"
        print(f"- {lang}: {count}")

if __name__ == "__main__":
    #username = input("Enter a GitHub username: ")
    #get_profile(username)
    #get_repos("torvalds")
    get_languages("bio")