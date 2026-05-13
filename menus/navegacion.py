from autenticacion.autorizacion import asegurar_autoridad_demo
from autenticacion.inicio_sesion import iniciar_sesion_usuario
from autenticacion.registro import registrar_usuario
from menus.menu_autoridad import menu_autoridad
from menus.menu_inicio import menu_inicio
from menus.menu_usuario import menu_usuario
from nucleo.sesion import iniciar_sesion, cerrar_sesion, esta_autenticado, es_autoridad
from nucleo.utilidades import limpiar_pantalla, pausa


def ejecutar():
    asegurar_autoridad_demo()

    while True:
        limpiar_pantalla()

        if not esta_autenticado():
            opcion = menu_inicio()
            if opcion == "1":
                limpiar_pantalla()
                print("INICIO DE SESION")
                nombre_usuario = input("Nombre de usuario: ").strip()
                clave = input("Clave: ")
                ok, usuario, mensaje = iniciar_sesion_usuario(nombre_usuario, clave)
                if ok:
                    iniciar_sesion(usuario)
                else:
                    print(mensaje)
                    pausa()
            elif opcion == "2":
                limpiar_pantalla()
                print("REGISTRO DE USUARIO")
                nombre_usuario = input("Nombre de usuario: ").strip()
                clave = input("Clave (minimo 6 caracteres): ")
                ok, usuario, mensaje = registrar_usuario(nombre_usuario, clave)
                if ok:
                    iniciar_sesion(usuario)
                else:
                    print(mensaje)
                    pausa()
            elif opcion == "3":
                break
            else:
                print("Opcion invalida.")
                pausa()
            continue

        if es_autoridad():
            opcion = menu_autoridad()
            if opcion == "3":
                cerrar_sesion()
            else:
                print("Funcionalidad en construccion.")
                pausa()
            continue

        opcion = menu_usuario()
        if opcion == "5":
            cerrar_sesion()
        else:
            print("Funcionalidad en construccion.")
            pausa()
