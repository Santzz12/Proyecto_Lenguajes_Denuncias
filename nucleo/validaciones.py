def normalizar_nombre_usuario(nombre_usuario):
	return (nombre_usuario or "").strip().lower()


def validar_nombre_usuario(nombre_usuario):
	nombre_usuario = (nombre_usuario or "").strip()
	if len(nombre_usuario) < 3:
		return False, "El nombre de usuario debe tener minimo 3 caracteres."
	return True, ""


def validar_clave(clave):
	clave = clave or ""
	if len(clave) < 6:
		return False, "La clave debe tener minimo 6 caracteres."
	return True, ""


def validar_credenciales(nombre_usuario, clave):
	nombre_usuario = (nombre_usuario or "").strip()
	clave = clave or ""
	if not nombre_usuario or not clave:
		return False, "Debe ingresar usuario y clave."
	return True, ""


def usuario_existe(usuarios, nombre_usuario):
	nombre_normalizado = normalizar_nombre_usuario(nombre_usuario)
	return any(
		(u.get("nombre_usuario") or "").lower() == nombre_normalizado
		for u in usuarios
	)
