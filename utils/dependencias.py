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

paginas_scrapeadas = "./data/paginas_scrapeadas.jsonl"
paginas_filtradas = "./data/paginas_filtradas.jsonl"
eventos_clasificados = "./data/eventos_clasificados.jsonl"

prompt_filtro = """Sos un **clasificador de contenido web**. Tu tarea es revisar el texto que te proporcionan y **definir si se trata sobre un evento de reuniones realizado en la provincia de Mendoza o no**. Para realizarlo, te comparto las características de un evento de reuniones:
- Debe realizarse en un periodo de tiempo determinado. Puede ser una única fecha o un periodo comprendido entre una fecha y otra.
- Debe tener una sede física definida. Por esto mismo, quedan descartados eventos realizados vía web como webinars y conferencias vía plataformas como Google Meet.
- Debe tener un organizador definido. Este organizador debe ser un ente o entidad, no puede ser una persona física.
- Debe realizarse en la provincia de Mendoza, Argentina. Todo evento que tenga lugar en otra provincia o país queda automáticamente descartado.

**No cuentan como eventos de reuniones los siguientes sucesos**:
- Anuncios institucionales (inicio de clases, apertura de convocatorias para cargos públicos)
- Acontecimientos climáticos (tormentas, etc.)
- Actos de colación
- Eventos culturales (obras de teatro, conciertos, festivales, exposiciones de arte, etc.)
- Eventos deportivos **nacionales**, aquellos que sean internacionales son válidos
- Audiencias gubernamentales
- Turismo educativo (por ejemplo: un curso de posgrado)
- Sesiones o debates en la Cámara de Diputados/Senadores

Cuando el contenido corresponda a un evento, tu respuesta tiene que ser 'SI', y cuando no corresponda tenés que responder 'NO'. **Tu respuesta debe limitarse únicamente a esas dos palabras**, ni una sola más."""

prompt_clasificacion = """
Eres un analista de datos experto especializado en estructurar información de eventos de reuniones.

Tu tarea es analizar el contenido web y extraer los datos para completar el esquema JSON requerido.

El tipo del evento solo puede ser uno de estos:
- Jornada
- Encuentro
- Congreso
- Conferencia
- Exposición
- Seminario
- Evento Deportivo Internacional
- Simposio
- Convención
- Feria

La agrupación a la que pertenece el evento está definida por el tipo de evento:
CONGRESOS Y CONVENCIONES: Asamblea, Conferencia, Congreso, Convención, Encuentro, Foro, Jornada, Seminario, Simposio
FERIAS Y EXPOSICIONES: Exposición, Feria, Workshop
FUERA DEL ALCANCE DEL OETR: Evento Deportivo Internacional, Incentivo, Evento Cultural, Evento Deportivo Nacional, Otro tipo de evento

Los valores del tipo de rotación solo pueden ser los de esta lista:
Local, Provincial, Nacional - Regional (Patagonia), Nacional - Regional (NOA), Nacional - Regional (Litoral),
Nacional - Regional (Centro), Nacional - Regional (Cuyo), Nacional, Internacional - Iberoamérica, Internacional - Panamérica,
Internacional - Latinoamérica, Internacional - Sudamérica, Internacional - Mercosur, Internacional, Único, NS/NC.

El tema del evento tiene que ser uno de los que está en está lista:
Acuático, Agricultura y ganadería, Ajedrez, Alimentos, Arquitectura, Arte y diseño, Artes marciales y peleas, Automotores, 
Básquet, Bibliotecología, Ciclismo, Ciencias históricas y sociales, Ciencias naturales y exactas, Comercio, Comunicación, 
Cosmética y tratamientos estéticos, Cultura, Danza, Deporte y ocio, Derecho, Diseño de indumentaria y moda, Ecología y medio ambiente, 
Economía, Educación, Energía, Entretenimiento, parques y atracciones, Farmacia, Fisicoculturismo, Fútbol, Gastronomía, Geografia, 
Gobierno/Sindical, Golf, Handball, Hockey, Industria/Industrial, Lingüística, Literatura, Logística, Management y negocios, 
Maratón, Matemática y estadística, Medicina, Multideportes, Multisectorial, Ns/Nc, Odontología, Otro, Packaging y regalería, 
Polo, Psicología, Religión, Rugby, Seguridad, Seguros, Servicios, Sóftbol, Tecnología, Tenis, paddel o paleta, Tiro con arco y flecha, 
Transporte, Turismo y hotelería, Veterinaria, Vóley.

La categoría tiene que ser una de estas:
- Académico
- Asociativo
- Corporativo
- Gubernamental

La frecuencia del evento tiene que ser una de estas:
- Único
- Trimestral
- Cuatrimestral
- Semestral
- Anual
- Bienal
- Trienal
- Cuatrienal
- Irregular
- NS/NC

REGLAS DE EXTRACCIÓN:
1. PRECISIÓN: Extrae solo la información explícita en el texto. No inventes datos.
2. FECHAS: Convierte siempre las fechas al formato estandar ISO 8601 (YYYY-MM-DD). Si el año no es explícito, asume el año actual o el próximo lógico según el contexto del evento pero **NUNCA insertes un valor que no cumpla con el formato específico de fecha**.
3. NOMBRES: Limpia los nombres de eventos (elimina "Bienvenido al...", "Home - ...").
4. BOOLEANOS: El campo 'requiere_revision' debe ser True si la información clave (fecha o lugar) es ambigua o no se encuentra.

"""

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
