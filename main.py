from scripts.busqueda import busqueda_eventos
from scripts.procesar_resultados import limpiar_resultados

def run():
    print("Iniciando búsqueda.")
    busqueda_eventos()
    print("Limpiando resultados.")
    limpiar_resultados()

if __name__ == "__main__":
    run()