import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from enum import Enum
from typing import Sequence, Optional

# Habilitar trazabilidad de reintentos en consola
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger("urllib3").setLevel(logging.DEBUG)

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


def create_session(
    num_retries: int = 3,
    backoff_factor: float = 1.0,
    status_forcelist: Sequence[int] = (429, 500, 502, 503, 504),
    allowed_methods: Optional[Sequence[str]] = None
) -> requests.Session:

    if allowed_methods is None:
        allowed_methods = (HTTPMethod.GET.value, HTTPMethod.POST.value)

    session = requests.Session()

    retry_strategy = Retry(
        total=num_retries,
        backoff_factor=backoff_factor,
        status_forcelist=list(status_forcelist),
        allowed_methods=list(allowed_methods)
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    session.headers.update({
        "Accept": "application/json",
        "User-Agent": "LearningToUse/0.1"
    })

    return session


if __name__ == "__main__":
    session = create_session()
    url = "https://httpbin.org/status/500"

    try:
        logging.info(f"Iniciando petición a {url}...")
        response = session.get(url, timeout=(3.05, 10))
        response.raise_for_status()
        print(response.json())

    except requests.exceptions.RetryError:
        logging.error("Se agotaron los reintentos automáticos con Exponential Backoff.")
    except requests.exceptions.HTTPError as err:
        logging.error(f"Error HTTP final devuelto tras los reintentos: {err}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Fallo crítico de red: {err}")