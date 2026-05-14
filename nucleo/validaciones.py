from datetime import datetime

from nucleo.constantes import PROVINCIAS, CIUDADES_POR_PROVINCIA

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


def validar_texto_obligatorio(valor, nombre_campo):
	texto = (valor or "").strip()
	if not texto:
		return False, f"El campo {nombre_campo} es obligatorio."
	return True, ""


def validar_fecha_evento(fecha_evento):
	texto = (fecha_evento or "").strip()
	if not texto:
		return False, "La fecha del evento es obligatoria."

	if not normalizar_fecha_evento(texto):
		return False, "La fecha del evento debe tener formato DD-MM-AAAA."

	return True, ""


def normalizar_fecha_evento(fecha_evento):
	texto = (fecha_evento or "").strip()
	if not texto:
		return None

	for formato in ("%d-%m-%Y", "%Y-%m-%d"):
		try:
			return datetime.strptime(texto, formato).strftime("%d-%m-%Y")
		except ValueError:
			continue

	return None


def validar_tipo_denuncia(tipo, tipos_validos):
	if tipo not in tipos_validos:
		return False, "El tipo de denuncia no es valido."
	return True, ""


def validar_ciudad_provincia(ciudad_provincia):
	texto = (ciudad_provincia or "").strip()
	if not texto:
		return False, "La ciudad/provincia es obligatoria."

	if " - " not in texto:
		return False, "Debe seleccionar una provincia y una ciudad."

	provincia, ciudad = [parte.strip() for parte in texto.split(" - ", 1)]
	provincia_normalizada = next(
		(p for p in PROVINCIAS if p.lower() == provincia.lower()),
		None,
	)
	if not provincia_normalizada:
		return False, "La provincia no es valida."

	ciudades = CIUDADES_POR_PROVINCIA.get(provincia_normalizada, [])
	if not ciudades:
		return False, "No hay ciudades registradas para la provincia seleccionada."

	if ciudad.lower() not in [c.lower() for c in ciudades]:
		return False, "La ciudad no es valida para la provincia seleccionada."

	return True, ""


def normalizar_ciudad_provincia(ciudad_provincia):
	texto = (ciudad_provincia or "").strip()
	if not texto:
		return None

	if " - " not in texto:
		return None

	provincia, ciudad = [parte.strip() for parte in texto.split(" - ", 1)]
	provincia_normalizada = next(
		(p for p in PROVINCIAS if p.lower() == provincia.lower()),
		None,
	)
	if not provincia_normalizada:
		return None

	ciudades = CIUDADES_POR_PROVINCIA.get(provincia_normalizada, [])
	ciudad_normalizada = next(
		(c for c in ciudades if c.lower() == ciudad.lower()),
		None,
	)
	if not ciudad_normalizada:
		return None

	return f"{provincia_normalizada} - {ciudad_normalizada}"
