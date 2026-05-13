from datetime import datetime

from nucleo.constantes import RUTA_MENSAJES
from nucleo.persistencia import leer_lista_json, guardar_lista_json
from nucleo.utilidades import parsear_fecha


def listar_mensajes_por_denuncia(denuncia_id):
	mensajes = leer_lista_json(RUTA_MENSAJES)
	filtrados = [m for m in mensajes if m.get("denuncia_id") == denuncia_id]
	return sorted(
		filtrados,
		key=lambda m: parsear_fecha(m.get("creado_en")) or datetime.min,
	)


def marcar_mensajes_leidos(denuncia_id, destinatario_id):
	mensajes = leer_lista_json(RUTA_MENSAJES)
	cambios = 0
	for mensaje in mensajes:
		if (
			mensaje.get("denuncia_id") == denuncia_id
			and mensaje.get("destinatario_id") == destinatario_id
			and not mensaje.get("leido")
		):
			mensaje["leido"] = True
			cambios += 1

	if cambios:
		guardar_lista_json(RUTA_MENSAJES, mensajes)
	return cambios


def contar_no_leidos(destinatario_id):
	mensajes = leer_lista_json(RUTA_MENSAJES)
	return sum(
		1
		for m in mensajes
		if m.get("destinatario_id") == destinatario_id and not m.get("leido")
	)
