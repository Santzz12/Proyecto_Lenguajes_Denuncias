from nucleo.constantes import RUTA_DENUNCIAS, ESTADOS_DENUNCIA
from nucleo.persistencia import leer_lista_json, guardar_lista_json


def actualizar_estado_denuncia(denuncia_id, nuevo_estado):
	if nuevo_estado not in ESTADOS_DENUNCIA:
		return False, None, "El estado seleccionado no es valido."

	denuncias = leer_lista_json(RUTA_DENUNCIAS)
	for denuncia in denuncias:
		if denuncia.get("id") == denuncia_id:
			denuncia["estado"] = nuevo_estado
			guardar_lista_json(RUTA_DENUNCIAS, denuncias)
			return True, denuncia, "Estado actualizado correctamente."

	return False, None, "No se encontro la denuncia seleccionada."
