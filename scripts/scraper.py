from bs4 import BeautifulSoup
import httpx
import pandas as pd
from datetime import datetime


def scrapear_paginas():

    with httpx.Client() as client:
        df_resultados = pd.read_csv(
            f"./data/resultados_{datetime.today().strftime('%Y%m%d')}.csv")

        for index, row in df_resultados.iterrows():
            response = client.get(row["link"])
            response.raise_for_status()
            html = response.text
