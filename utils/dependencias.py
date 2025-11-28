import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

GCS_API_KEY = os.getenv("EMETUR_SEARCH_API_KEY")
ENGINE_ID = os.getenv("EMETUR_SEARCH_ENGINE")

sedes_df = pd.read_csv("./data/sedes.csv", sep=";")
sedes = sedes_df["Nombre"].dropna().tolist()
tipos_evento = ["Jornada", "Encuentro", "Congreso", "Conferencia", "Exposición", "Seminario",
                "Evento Deportivo Internacional", "Simposio", "Convencion", "Feria"]

start = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]