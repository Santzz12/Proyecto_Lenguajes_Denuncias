from nucleo.constantes import RUTA_USUARIOS
from nucleo.persistencia import leer_lista_json, guardar_lista_json
from nucleo.utilidades import generar_id, fecha_iso


def registrar_usuario(nombre_usuario, clave):
	nombre_usuario = (nombre_usuario or "").strip()
	clave = clave or ""

	if len(nombre_usuario) < 3:
		return False, None, "El nombre de usuario debe tener minimo 3 caracteres."

	if len(clave) < 6:
		return False, None, "La clave debe tener minimo 6 caracteres."

	usuarios = leer_lista_json(RUTA_USUARIOS)
	nombre_normalizado = nombre_usuario.lower()

	if any((u.get("nombre_usuario") or "").lower() == nombre_normalizado for u in usuarios):
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
