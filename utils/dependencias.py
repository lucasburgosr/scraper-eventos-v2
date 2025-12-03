import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()

# --- DATA ---

GCS_API_KEY = os.getenv("EMETUR_SEARCH_API_KEY")
ENGINE_ID = os.getenv("EMETUR_SEARCH_ENGINE")

sedes_df = pd.read_csv("./data/sedes.csv", sep=";")
sedes = sedes_df["Nombre"].dropna().tolist()
tipos_evento = ["Jornada", "Encuentro", "Congreso", "Conferencia", "Exposición", "Seminario",
                "Evento Deportivo Internacional", "Simposio", "Convencion", "Feria"]

start = [1, 11, 21, 31, 41, 51, 61, 71, 81, 91]

ruta_jsonl_crudo = "./data/páginas_escrapeadas.jsonl"
ruta_jsonl_filtrado = "./data/paginas_filtradas.jsonl"

prompt_filtro = (
    "Sos un **clasificador de contenido web**. Tu tarea es revisar el texto que te proporcionan "
    "y **definir si se trata sobre un evento de reuniones realizado en la provincia de Mendoza o no**. "
    "Para realizarlo, te comparto las características de un evento de reuniones:\n"
    "- Debe realizarse en un periodo de tiempo determinado. Puede ser una única fecha o un periodo "
    "comprendido entre una fecha y otra.\n"
    "- Debe tener una sede física definida. Por esto mismo, quedan descartados eventos realizados vía web como "
    "webinars y conferencias vía plataformas como Google Meet.\n"
    "- Debe tener un organizador definido. Este organizador debe ser un ente o entidad, no puede ser una persona "
    "física.\n"
    "- Debe realizarse en la provincia de Mendoza, Argentina. Todo evento que tenga lugar en otra provincia o país "
    "queda automáticamente descartado.\n"
    "**No cuentan como eventos de reuniones los siguientes sucesos**:\n"
    "- Anuncios institucionales (inicio de clases, apertura de convocatorias para cargos públicos) \n"
    "- Acontecimientos climáticos (tormentas, etc.) \n"
    "- Actos de colación \n"
    "- Eventos culturales (obras de teatro, conciertos, festivales, exposiciones de arte, etc.)\n"
    "- Eventos deportivos **nacionales**, aquellos que sean internacionales son válidos\n"
    "- Audiencias gubernamentales \n"
    "- Turismo educativo (por ejemplo: un curso de posgrado) \n"
    "- Sesiones o debates en la Cámara de Diputados/Senadores \n"
    "Cuando el contenido corresponda a un evento, tu respuesta tiene que ser 'SI', y cuando no corresponda tenés que "
    "responder 'NO'. **Tu respuesta debe limitarse únicamente a esas dos palabras**, ni una sola más."
)

# --- FUNCIONES ---

def iterador(ruta: str):

    if not os.path.exists(ruta):
        print(f"No hay archivos en la ruta {ruta}")
        return
    
    with open(ruta, 'r', encoding='utf-8') as f:
        for numero_linea, linea in enumerate(f, 1):
            linea = linea.strip()

            if not linea:
                continue

            try:
                yield json.loads(linea)
            except json.JSONDecodeError:
                print(f"Error de formato JSON en la línea {numero_linea}")