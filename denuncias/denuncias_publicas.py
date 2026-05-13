from datetime import datetime

from denuncias.filtros import filtrar_publicas_por_periodo
from nucleo.constantes import RUTA_DENUNCIAS
from nucleo.persistencia import leer_lista_json
from nucleo.utilidades import parsear_fecha


def obtener_denuncias_publicas(periodo):
	denuncias = leer_lista_json(RUTA_DENUNCIAS)
	publicas = filtrar_publicas_por_periodo(denuncias, periodo)
	return sorted(
		publicas,
		key=lambda d: parsear_fecha(d.get("creada_en")) or datetime.min,
		reverse=True,
	)
