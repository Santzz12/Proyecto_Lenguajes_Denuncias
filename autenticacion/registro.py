from nucleo.constantes import RUTA_USUARIOS
from nucleo.persistencia import leer_lista_json, guardar_lista_json
from nucleo.utilidades import generar_id, fecha_iso
from nucleo.validaciones import validar_nombre_usuario, validar_clave, usuario_existe


def registrar_usuario(nombre_usuario, clave):
	nombre_usuario = (nombre_usuario or "").strip()
	clave = clave or ""

	ok, mensaje = validar_nombre_usuario(nombre_usuario)
	if not ok:
		return False, None, mensaje

	ok, mensaje = validar_clave(clave)
	if not ok:
		return False, None, mensaje

	usuarios = leer_lista_json(RUTA_USUARIOS)
	if usuario_existe(usuarios, nombre_usuario):
		return False, None, "El nombre de usuario ya existe."

	nuevo_usuario = {
		"id": generar_id("u"),
		"nombre_usuario": nombre_usuario,
		"clave": clave,
		"es_autoridad": False,
		"creado_en": fecha_iso(),
	}

	usuarios.append(nuevo_usuario)
	guardar_lista_json(RUTA_USUARIOS, usuarios)

	return True, nuevo_usuario, "Usuario registrado correctamente."
