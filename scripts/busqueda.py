import httpx, os, sys
import time
from datetime import datetime
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)

from utils.dependencias import start, tipos_evento, GCS_API_KEY, ENGINE_ID


def google_search(query, api_key, cse_id, **params):
    url_base = "https://customsearch.googleapis.com/customsearch/v1"
    parametros = {'key': api_key, 'cx': cse_id, 'q': query, **params}

    with httpx.Client() as client:
        response = client.get(url=url_base, params=parametros)
        response.raise_for_status()
        return response.json()


def busqueda_eventos():
    resultados_acumulados = []
    limite_agotado = False
    for tipo in tipos_evento:
        for i in start:
            try:
                query = f"{tipo} 2025 Mendoza -site:.cl -site:.uy -site:.mx"

                response = google_search(
                    api_key=GCS_API_KEY,
                    cse_id=ENGINE_ID,
                    query=query,
                    gl="ar", cr="countryAR", lr="lang_es",
                    sort="date:r:20250501:20250531",
                    start=i
                )

                resultados = response.get("items", [])

                if resultados:
                    resultados_acumulados.extend(resultados)
                    print(f"Se añadieron {len(resultados)} resultados.")
                else:
                    print("No se encontraron resultados.")
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    print("Límite de consultas diarias agotado.")
                    limite_agotado = True
                    break
                else:
                    print(f"Error inesperado: {e}")
                    return

            time.sleep(2)

        if limite_agotado:
            break

    if not resultados_acumulados:
        return

    df = pd.DataFrame(resultados_acumulados)
    df.to_csv(f"./data/csv/resultados_{datetime.today().strftime('%Y%m%d')}.csv",
              index=False,
              sep=";",
              encoding="utf-8")
    
busqueda_eventos()