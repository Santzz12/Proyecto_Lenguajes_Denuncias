from nucleo.utilidades import imprimir_titulo, imprimir_salto


def menu_inicio():
    imprimir_titulo("DENUNCIAS ECUADOR")
    imprimir_salto()
    print("1. Iniciar sesion")
    print("2. Registrarse")
    print("3. Salir")
    imprimir_salto()
    return input("Seleccione: ").strip()
