from datetime import datetime
import pandas as pd

def limpiar_resultados():
    resultados_df = pd.read_csv(
        f"./data/resultados_20251128.csv", low_memory=False, sep=";")

    output_df = resultados_df[["title", "link", "snippet"]]
    output_df = output_df.drop_duplicates(subset=["link"], keep="first")

    output_df.to_csv(
        f"./data/resultados_limpios_20251128.csv",
        sep=";",
        index=False,
        encoding="utf-8")
    
limpiar_resultados()