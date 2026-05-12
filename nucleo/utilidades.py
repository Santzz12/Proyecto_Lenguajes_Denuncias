import os
import uuid
from datetime import datetime


def generar_id(prefijo):
	return f"{prefijo}_{uuid.uuid4()}"


def fecha_iso():
	return datetime.now().isoformat(timespec="seconds")


def limpiar_pantalla():
	os.system("cls" if os.name == "nt" else "clear")


def pausa():
	input("Presione Enter para continuar...")


def imprimir_titulo(texto):
	linea = "=" * 32
	print(linea)
	print(texto.center(32))
	print(linea)
