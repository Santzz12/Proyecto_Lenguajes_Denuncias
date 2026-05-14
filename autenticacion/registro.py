from nucleo.constantes import RUTA_USUARIOS
from nucleo.persistencia import leer_lista_json, guardar_lista_json
from nucleo.utilidades import generar_id, fecha_actual
from nucleo.validaciones import validar_nombre_usuario, validar_clave, usuario_existe


def validar_nombre_usuario_disponible(nombre_usuario):
	nombre_usuario = (nombre_usuario or "").strip()

	ok, mensaje = validar_nombre_usuario(nombre_usuario)
	if not ok:
		return False, None, mensaje

	usuarios = leer_lista_json(RUTA_USUARIOS)
	if usuario_existe(usuarios, nombre_usuario):
		return False, None, "\nEl nombre de usuario ya existe."

	return True, usuarios, ""


def registrar_usuario(nombre_usuario, clave):
	nombre_usuario = (nombre_usuario or "").strip()
	clave = clave or ""

	ok, usuarios, mensaje = validar_nombre_usuario_disponible(nombre_usuario)
	if not ok:
		return False, None, mensaje

	ok, mensaje = validar_clave(clave)
	if not ok:
		return False, None, mensaje

	nuevo_usuario = {
		"id": generar_id("u"),
		"nombre_usuario": nombre_usuario,
		"clave": clave,
		"es_autoridad": False,
		"creado_en": fecha_actual(),
	}

	usuarios.append(nuevo_usuario)
	guardar_lista_json(RUTA_USUARIOS, usuarios)

	return True, nuevo_usuario, "\nUsuario registrado correctamente."
