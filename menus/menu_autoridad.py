from nucleo.utilidades import imprimir_titulo


def menu_autoridad(no_leidos=0):
    imprimir_titulo("PANEL AUTORIDAD")
    print("1. Ver denuncias")
    if no_leidos:
        print(f"2. Buzon de mensajes ({no_leidos} nuevos)")
    else:
        print("2. Buzon de mensajes")
    print("3. Cerrar sesion")
    return input("Seleccione: ").strip()
