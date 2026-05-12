from nucleo.utilidades import imprimir_titulo


def menu_autoridad():
    imprimir_titulo("PANEL AUTORIDAD")
    print("1. Ver denuncias")
    print("2. Buzon de mensajes")
    print("3. Cerrar sesion")
    return input("Seleccione: ").strip()
