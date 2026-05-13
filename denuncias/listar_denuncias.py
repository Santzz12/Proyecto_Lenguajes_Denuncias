from datetime import datetime

from nucleo.constantes import RUTA_DENUNCIAS
from nucleo.persistencia import leer_lista_json
from nucleo.utilidades import parsear_fecha


def _ordenar_por_fecha(denuncias):
    return sorted(
        denuncias,
        key=lambda d: parsear_fecha(d.get("creada_en")) or datetime.min,
        reverse=True,
    )


def listar_denuncias_por_usuario(usuario_id):
    denuncias = leer_lista_json(RUTA_DENUNCIAS)
    filtradas = [d for d in denuncias if d.get("usuario_id") == usuario_id]
    return _ordenar_por_fecha(filtradas)


def listar_todas_las_denuncias():
    denuncias = leer_lista_json(RUTA_DENUNCIAS)
    return _ordenar_por_fecha(denuncias)


def obtener_denuncia_por_id(denuncia_id):
    denuncias = leer_lista_json(RUTA_DENUNCIAS)
    return next((d for d in denuncias if d.get("id") == denuncia_id), None)
