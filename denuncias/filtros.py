from datetime import datetime, timedelta

from nucleo.utilidades import parsear_fecha


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

		fecha_creacion = parsear_fecha(creada_en)
		if not fecha_creacion:
			continue

		if limite and fecha_creacion < limite:
			continue

		resultado.append(denuncia)

	return resultado


def filtrar_por_tipo_estado(denuncias, tipo=None, estado=None):
	resultado = []
	for denuncia in denuncias:
		if tipo and denuncia.get("tipo") != tipo:
			continue
		if estado and denuncia.get("estado") != estado:
			continue
		resultado.append(denuncia)

	return resultado
