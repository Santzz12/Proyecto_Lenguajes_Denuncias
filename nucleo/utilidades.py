import os
import uuid
from datetime import datetime


def generar_id(prefijo):
    return f"{prefijo}_{uuid.uuid4()}"


def fecha_actual():
    return datetime.now().strftime("%d-%m-%Y")


def fecha_iso():
    return datetime.now().isoformat(timespec="seconds")


def parsear_fecha(fecha_texto):
    if not fecha_texto:
        return None

    for formato in ("%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(fecha_texto, formato)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(fecha_texto)
    except ValueError:
        return None


def formatear_fecha(fecha_texto):
    if not fecha_texto:
        return ""

    for formato in ("%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(fecha_texto, formato).strftime("%d-%m-%Y")
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(fecha_texto).strftime("%d-%m-%Y")
    except ValueError:
        return fecha_texto


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausa():
    input("Presione Enter para continuar...")


def imprimir_titulo(texto):
    linea = "=" * 32
    print(linea)
    print(texto.center(32))
    print(linea)


def imprimir_salto(cantidad=1):
	for _ in range(cantidad):
		print()
