from datetime import datetime, timedelta


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

		try:
			fecha_creacion = datetime.fromisoformat(creada_en)
		except ValueError:
			continue

		if limite and fecha_creacion < limite:
			continue

		resultado.append(denuncia)

	return resultado
