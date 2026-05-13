from denuncias.listar_denuncias import listar_denuncias_por_usuario, listar_todas_las_denuncias
from nucleo.constantes import RUTA_USUARIOS
from nucleo.persistencia import leer_lista_json


def obtener_denuncias_buzon(usuario):
	if usuario.get("es_autoridad"):
		return listar_todas_las_denuncias()
	return listar_denuncias_por_usuario(usuario.get("id"))


def obtener_autoridad_destinatario():
	usuarios = leer_lista_json(RUTA_USUARIOS)
	return next((u for u in usuarios if u.get("es_autoridad")), None)
