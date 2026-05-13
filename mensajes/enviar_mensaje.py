from nucleo.constantes import RUTA_MENSAJES
from nucleo.persistencia import leer_lista_json, guardar_lista_json
from nucleo.utilidades import generar_id, fecha_actual
from nucleo.validaciones import validar_texto_obligatorio


def enviar_mensaje(denuncia_id, remitente_id, remitente_nombre, destinatario_id, contenido):
	ok, mensaje = validar_texto_obligatorio(contenido, "mensaje")
	if not ok:
		return False, None, mensaje

	mensaje_nuevo = {
		"id": generar_id("m"),
		"denuncia_id": denuncia_id,
		"remitente_id": remitente_id,
		"remitente_nombre": remitente_nombre,
		"destinatario_id": destinatario_id,
		"contenido": contenido.strip(),
		"leido": False,
		"creado_en": fecha_actual(),
	}

	mensajes = leer_lista_json(RUTA_MENSAJES)
	mensajes.append(mensaje_nuevo)
	guardar_lista_json(RUTA_MENSAJES, mensajes)

	return True, mensaje_nuevo, "Mensaje enviado correctamente."
