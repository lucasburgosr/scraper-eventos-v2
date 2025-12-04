from groq import Groq
import pandas as pd
import json, os, time, sys, instructor

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)
    
from utils.dependencias import iterador, paginas_scrapeadas, paginas_filtradas, eventos_clasificados, prompt_filtro, prompt_clasificacion
from models.evento_schema import Evento

client_filtro = Groq()

client_clasificacion = Groq()
client_clasificacion = instructor.from_provider("groq/llama-3.1-8b-instant")

def filtrar():

    with open(paginas_filtradas, 'a', encoding='utf-8') as f:
        for pagina in iterador(paginas_scrapeadas):
            response = client_filtro.chat.completions.create(
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
                json_line = json.dumps(evento_dict, ensure_ascii=False)
                f.write(json_line + '\n')
                f.flush()
                print(f"Evento guardado: {pagina['link']}")

filtrar()