from bs4 import BeautifulSoup
import httpx
import json
import pandas as pd
from datetime import datetime

def scrapear_paginas():

    contador = 0

    etiquetas = ["script", "style", "noscript",
                 "svg", "iframe", "header", "footer"]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
    }

    with httpx.Client(headers=headers) as client:
        df_resultados = pd.read_csv(
            f"./data/resultados_limpios_20251128.csv", sep=";")

        with open("./data/páginas_escrapeadas.jsonl", "a", encoding="utf-8") as f:

            for row in df_resultados.itertuples(index=False):
                try:
                    response = client.get(row.link)
                    response.raise_for_status()
                    html = response.text
                    soup = BeautifulSoup(html, "html.parser")

                    for etiqueta in etiquetas:
                        for elemento in soup(etiqueta):
                            elemento.decompose()

                    contenido = soup.get_text(separator=" ", strip=True)
                    contenido_recortado = contenido[0:10000]

                    if soup.title and soup.title.string:
                        title = soup.title.string.strip()
                    else:
                        title = row.title

                    data = {"link": row.link, "title": title,
                            "content": contenido_recortado}

                    json_line = json.dumps(data, ensure_ascii=False)

                    f.write(json_line + "\n")
                    f.flush()
                    contador += 1
                    print(f"Links scrapeados: {contador}")

                except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.NetworkError) as e:
                    print(
                        f"Error al intentar obtener el HTML de esta página: {row.link}")
                    print(f"Error: {e}")
                    print("No se registrará en el JSONL.")

scrapear_paginas()