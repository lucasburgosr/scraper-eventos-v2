from groq import Groq
import pandas as pd
import json, os, time, sys, instructor
from rapidfuzz import process
from rapidfuzz import fuzz
from instructor.core import InstructorError
from textwrap import dedent

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)
    
from utils.dependencias import iterador, paginas_scrapeadas, paginas_filtradas, eventos_clasificados, prompt_filtro, prompt_clasificacion, prompt_revision_sede
from models.evento_schema import Evento

client_estandar = Groq()
client_clasificacion = instructor.from_provider("groq/llama-3.1-8b-instant")

def filtrar():

    with open(paginas_filtradas, 'a', encoding='utf-8') as f:
        for pagina in iterador(paginas_scrapeadas):
            response = client_estandar.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_filtro
                    },
                    {
                        "role": "user",
                        "content": f"Contenido web: {pagina['content']}"
                    }
                ],
                model="llama-3.1-8b-instant"
            )

            check = (response.choices[0].message.content).strip().upper().replace(".", "")

            if "SI" in check:
                json_line = json.dumps(pagina, ensure_ascii=False)
                f.write(json_line + "\n")
                f.flush()
                print(f"Evento guardado: {pagina["link"]}")
            else:
                print(f"Evento descartado: {pagina["link"]}")

            time.sleep(2)

def clasificar():
    
    with open(eventos_clasificados, 'a', encoding='utf-8') as f:
        for pagina in iterador(paginas_filtradas):
            try:
                response = client_clasificacion.create(
                    messages=[
                        {
                            'role': 'system',
                            'content': prompt_clasificacion
                        },
                        {
                            'role': 'user',
                            'content': f'Contenido web: {pagina['content']}'
                        }
                    ],
                    response_model=Evento
                )
            
                if response:
                    evento_dict = response.model_dump(mode='json')
                    evento_dict['link'] = pagina['link']
                    json_line = json.dumps(evento_dict, ensure_ascii=False)
                    f.write(json_line + '\n')
                    f.flush()
                    print(f"Evento guardado: {pagina['link']}")
            except InstructorError as e:
                print(f'Error intentando procesar el evento {pagina['title']}')
                print(f'{e}')


def revisar_sede():

    df_sedes = pd.read_csv("./data/csv/sedes.csv", sep=";", encoding="utf-8", low_memory=False)
    lista_sedes = df_sedes["Nombre"].to_list()

    print(f"Lista de sedes obtenida: {lista_sedes[0]}")

    with open("./data/jsonl/eventos_con_sede_corregida.jsonl", "a", encoding="utf-8") as f:

        print(f"Iterando sobre los eventos disponibles")

        for evento in iterador("./data/jsonl/eventos_clasificados_prueba.jsonl"):

            print(f"Revisando evento: {evento['nombre']}")

            sedes_fuzzy = process.extract(evento['sede'], lista_sedes, scorer=fuzz.WRatio)

            score_posible_sede = sedes_fuzzy[0][1]

            if score_posible_sede > 85:
                print("Sede definida por similitud con fuzzy matching")
                evento["sede"] = sedes_fuzzy[0][0]

            else:
                sedes_aux = []
                for sede in sedes_fuzzy:
                    sedes_aux.append(sede[0])

                sedes_string = ", ".join(sedes_aux)
                response = client_estandar.chat.completions.create(
                    messages=[
                        {
                            'role': 'system',
                            'content': prompt_revision_sede
                        },
                        {
                            'role': 'user',
                            'content': dedent(f"""\
                                        JSON evento: {json.dumps(evento)}
                                        Lista de posibles sedes: {sedes_string} 
                                        """)
                        }
                    ],
                    model="llama-3.1-8b-instant"
                )

                print("Sede definida con LLM")
                evento["sede"] = (response.choices[0].message.content).strip()

            
            print(f"Sede definida para el evento: {evento["sede"]}")
            json_line = json.dumps(evento, ensure_ascii=False)
            f.write(json_line + "\n")

filtrar()