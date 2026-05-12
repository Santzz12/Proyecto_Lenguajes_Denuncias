usuario_actual = None


def iniciar_sesion(usuario):
	global usuario_actual
	usuario_actual = usuario


def cerrar_sesion():
	global usuario_actual
	usuario_actual = None


def esta_autenticado():
	return usuario_actual is not None


def es_autoridad():
	return bool(usuario_actual and usuario_actual.get("es_autoridad"))
