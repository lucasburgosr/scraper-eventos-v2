from datetime import datetime
import pandas as pd
import json
import time
from rapidfuzz import process
from rapidfuzz import fuzz

def limpiar_resultados():
    resultados_df = pd.read_csv(
        f"./data/csv/resultados_{datetime.today().strftime('%Y%m%d')}.csv", low_memory=False, sep=";")

    output_df = resultados_df[["title", "link", "snippet"]]
    output_df = output_df.drop_duplicates(subset=["link"], keep="first")

    output_df.to_csv(
        f"./data/csv/resultados_limpios_{datetime.today().strftime('%Y%m%d')}.csv",
        sep=";",
        index=False,
        encoding="utf-8")
    
limpiar_resultados()