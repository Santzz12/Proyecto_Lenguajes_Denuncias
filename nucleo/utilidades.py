import os
import shutil
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
    input("\nPresione Enter para continuar...")


def imprimir_titulo(texto):
    linea = "=" * 32
    print(linea)
    print(texto.center(32))
    print(linea)


def imprimir_salto(cantidad=1):
	for _ in range(cantidad):
		print()


def imprimir_lista_en_columnas(items, columnas=None, separacion=2):
    if not items:
        return

    etiquetas = [f"{indice}. {item}" for indice, item in enumerate(items, start=1)]
    ancho_max = max(len(etiqueta) for etiqueta in etiquetas)
    ancho_columna = ancho_max + separacion

    if not columnas or columnas < 1:
        ancho_terminal = shutil.get_terminal_size(fallback=(80, 20)).columns
        columnas = max(1, ancho_terminal // ancho_columna)

    filas = (len(etiquetas) + columnas - 1) // columnas
    for fila in range(filas):
        partes = []
        for columna in range(columnas):
            indice = fila + columna * filas
            if indice >= len(etiquetas):
                continue
            etiqueta = etiquetas[indice]
            if columna < columnas - 1:
                partes.append(etiqueta.ljust(ancho_columna))
            else:
                partes.append(etiqueta)
        print("".join(partes).rstrip())
