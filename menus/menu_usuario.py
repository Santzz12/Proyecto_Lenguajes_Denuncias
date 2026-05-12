from nucleo.utilidades import imprimir_titulo


def menu_usuario():
    imprimir_titulo("PANEL CIUDADANO")
    print("1. Nueva denuncia")
    print("2. Mis denuncias")
    print("3. Buzon personal")
    print("4. Denuncias publicas")
    print("5. Cerrar sesion")
    return input("Seleccione: ").strip()
