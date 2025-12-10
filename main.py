from scripts.busqueda import busqueda_eventos
from scripts.limpieza_de_datos import limpiar_resultados
from scripts.scraper import scrapear_paginas
from scripts.llm import filtrar, clasificar
from dotenv import load_dotenv

load_dotenv()

def run():
    print("Iniciando búsqueda.")
    busqueda_eventos()
    print("Limpiando resultados.")
    limpiar_resultados()
    print("Scrapeando páginas.")
    scrapear_paginas()
    print("Filtrando resultados.")
    filtrar()
    print("Clasificando eventos.")
    clasificar()

if __name__ == "__main__":
    run()