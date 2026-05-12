import json
from pathlib import Path


def asegurar_archivo_lista(ruta):
	archivo = Path(ruta)
	if not archivo.exists():
		archivo.parent.mkdir(parents=True, exist_ok=True)
		archivo.write_text("[]", encoding="utf-8")
	return archivo


def leer_lista_json(ruta):
	archivo = asegurar_archivo_lista(ruta)
	try:
		contenido = archivo.read_text(encoding="utf-8").strip()
		datos = json.loads(contenido) if contenido else []
		return datos if isinstance(datos, list) else []
	except json.JSONDecodeError:
		return []


def guardar_lista_json(ruta, datos):
	archivo = asegurar_archivo_lista(ruta)
	with archivo.open("w", encoding="utf-8") as salida:
		json.dump(datos, salida, indent=4, ensure_ascii=False)
