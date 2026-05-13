from nucleo.constantes import RUTA_DENUNCIAS
from nucleo.persistencia import leer_lista_json
from denuncias.filtros import filtrar_publicas_por_periodo


def obtener_denuncias_publicas(periodo):
	denuncias = leer_lista_json(RUTA_DENUNCIAS)
	return filtrar_publicas_por_periodo(denuncias, periodo)
