from datetime import datetime, timedelta


def _parsear_fecha_creada(fecha_texto):
	for formato in ("%d-%m-%Y", "%Y-%m-%d"):
		try:
			return datetime.strptime(fecha_texto, formato)
		except ValueError:
			continue

	try:
		return datetime.fromisoformat(fecha_texto)
	except ValueError:
		return None


def filtrar_publicas_por_periodo(denuncias, periodo):
	ahora = datetime.now()
	if periodo == "dia":
		limite = ahora - timedelta(days=1)
	elif periodo == "semana":
		limite = ahora - timedelta(days=7)
	else:
		limite = None

	resultado = []
	for denuncia in denuncias:
		if not denuncia.get("es_publica"):
			continue

		creada_en = denuncia.get("creada_en")
		if not creada_en:
			continue

		fecha_creacion = _parsear_fecha_creada(creada_en)
		if not fecha_creacion:
			continue

		if limite and fecha_creacion < limite:
			continue

		resultado.append(denuncia)

	return resultado
