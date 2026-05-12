from nucleo.constantes import RUTA_USUARIOS
from nucleo.persistencia import leer_lista_json, guardar_lista_json
from nucleo.utilidades import generar_id, fecha_iso


USUARIO_AUTORIDAD_DEMO = "autoridad_ec"
CLAVE_AUTORIDAD_DEMO = "Autoridad2026"


def asegurar_autoridad_demo():
	usuarios = leer_lista_json(RUTA_USUARIOS)
	if any(u.get("es_autoridad") for u in usuarios):
		return False

	usuario_demo = {
		"id": generar_id("u"),
		"nombre_usuario": USUARIO_AUTORIDAD_DEMO,
		"clave": CLAVE_AUTORIDAD_DEMO,
		"es_autoridad": True,
		"creado_en": fecha_iso(),
	}

	usuarios.append(usuario_demo)
	guardar_lista_json(RUTA_USUARIOS, usuarios)
	return True
