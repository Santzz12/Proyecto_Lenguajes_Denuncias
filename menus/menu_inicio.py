from nucleo.utilidades import imprimir_titulo


def menu_inicio():
    imprimir_titulo("DENUNCIAS ECUADOR")
    print("1. Iniciar sesion")
    print("2. Registrarse")
    print("3. Salir")
    return input("Seleccione: ").strip()
