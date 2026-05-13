from nucleo.constantes import RUTA_DENUNCIAS
from nucleo.persistencia import leer_lista_json


def listar_denuncias_por_usuario(usuario_id):
    denuncias = leer_lista_json(RUTA_DENUNCIAS)
    return [d for d in denuncias if d.get("usuario_id") == usuario_id]


def listar_todas_las_denuncias():
    return leer_lista_json(RUTA_DENUNCIAS)


def obtener_denuncia_por_id(denuncia_id):
    denuncias = leer_lista_json(RUTA_DENUNCIAS)
    return next((d for d in denuncias if d.get("id") == denuncia_id), None)
