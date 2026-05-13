from nucleo.constantes import RUTA_USUARIOS
from nucleo.persistencia import leer_lista_json


def iniciar_sesion_usuario(nombre_usuario, clave):
	nombre_usuario = (nombre_usuario or "").strip()
	clave = clave or ""

	if not nombre_usuario or not clave:
		return False, None, "Debe ingresar usuario y clave."

	usuarios = leer_lista_json(RUTA_USUARIOS)
	nombre_normalizado = nombre_usuario.lower()

	usuario = next(
		(
			u
			for u in usuarios
			if (u.get("nombre_usuario") or "").lower() == nombre_normalizado
			and u.get("clave") == clave
		),
		None,
	)

	if not usuario:
		return False, None, "Usuario o clave incorrectos."

	return True, usuario, "Inicio de sesion correcto."
