from groq import Groq
import pandas as pd
import json
import os
import time
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(ROOT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.append(PARENT_DIR)
    
from utils.dependencias import iterador, ruta_jsonl_crudo, ruta_jsonl_filtrado, prompt_filtro

client = Groq()

def filtrar():

    with open(ruta_jsonl_filtrado, 'a', encoding='utf-8') as f:
        for pagina in iterador(ruta_jsonl_crudo):
            response = client.chat.completions.create(
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
    pass

filtrar()