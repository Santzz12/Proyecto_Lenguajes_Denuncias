from nucleo.utilidades import imprimir_titulo, imprimir_salto


def menu_usuario(no_leidos=0):
    imprimir_titulo("PANEL CIUDADANO")
    imprimir_salto()
    print("1. Nueva denuncia")
    print("2. Mis denuncias")
    if no_leidos:
        print(f"3. Buzon personal ({no_leidos} nuevos)")
    else:
        print("3. Buzon personal")
    print("4. Denuncias publicas")
    print("5. Cerrar sesion")
    imprimir_salto()
    return input("\nSeleccione: ").strip()
