# 🚀 Mastering Python Requests

Este repositorio contiene el codigo para el aprendizaje progresivo de la librería `requests` de Python.
---

## 🛠️ Estructura del Proyecto

El repositorio tiene tres niveles de complejidad:

| Nivel | Archivo / Script | ConceptosClave |
| :--- | :--- | :--- |
| **Nivel 1** | `github_user_analyzer.py` | Métodos HTTP (`GET`), parámetros de consulta (`params`), inspección de cabeceras, formato JSON y manejo de errores con `raise_for_status()`. |
| **Nivel 2** | `github_commits_streamer.py` | Descargas en streaming a disco, formateo e ingesta en **JSONLines (`.jsonl`)**, control de límites y paginación iterativa con encabezados `Link` (`RFC 5988`). |
| **Nivel 3** | `resilient_api_ingestor.py` | Reuso de conexiones TCP con `requests.Session()`, reintentos automáticos con **Exponential Backoff** (`urllib3.util.Retry`), timeouts dinámicos `(connect, read)` y trazabilidad de logs. |

---

## ⚙️ Requisitos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/rcotilla/python_lib_requests.git](https://github.com/rcotilla/python_lib_requests.git)
   cd python_lib_requests