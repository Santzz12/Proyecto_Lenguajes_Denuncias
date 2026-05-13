from autenticacion.autorizacion import asegurar_autoridad_demo
from autenticacion.inicio_sesion import iniciar_sesion_usuario
from autenticacion.registro import registrar_usuario
from denuncias.crear_denuncia import crear_denuncia
from denuncias.denuncias_publicas import obtener_denuncias_publicas
from denuncias.listar_denuncias import listar_denuncias_por_usuario
from menus.menu_autoridad import menu_autoridad
from menus.menu_inicio import menu_inicio
from menus.menu_usuario import menu_usuario
from nucleo.constantes import TIPOS_DENUNCIA
from nucleo.sesion import iniciar_sesion, cerrar_sesion, esta_autenticado, es_autoridad
from nucleo.utilidades import limpiar_pantalla, pausa
import nucleo.sesion as sesion


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
        if opcion == "1":
            limpiar_pantalla()
            print("NUEVA DENUNCIA")
            titulo = input("Titulo: ").strip()
            descripcion = input("Descripcion: ").strip()
            fecha_evento = input("Fecha del evento (YYYY-MM-DD): ").strip()
            ciudad_provincia = input("Ciudad/Provincia: ").strip()

            print("Tipo de denuncia:")
            for indice, tipo in enumerate(TIPOS_DENUNCIA, start=1):
                print(f"{indice}. {tipo}")
            opcion_tipo = input("Seleccione: ").strip()
            tipo = None
            if opcion_tipo.isdigit():
                indice = int(opcion_tipo)
                if 1 <= indice <= len(TIPOS_DENUNCIA):
                    tipo = TIPOS_DENUNCIA[indice - 1]

            visibilidad = input("Publica (s/n): ").strip().lower()
            es_publica = visibilidad == "s"

            datos = {
                "usuario_id": sesion.usuario_actual.get("id"),
                "nombre_usuario": sesion.usuario_actual.get("nombre_usuario"),
                "titulo": titulo,
                "descripcion": descripcion,
                "fecha_evento": fecha_evento,
                "ciudad_provincia": ciudad_provincia,
                "tipo": tipo,
                "es_publica": es_publica,
            }

            ok, _, mensaje = crear_denuncia(datos)
            print(mensaje)
            pausa()
        elif opcion == "2":
            limpiar_pantalla()
            print("MIS DENUNCIAS")
            denuncias = listar_denuncias_por_usuario(sesion.usuario_actual.get("id"))
            if not denuncias:
                print("No hay denuncias registradas.")
            else:
                for denuncia in denuncias:
                    print(
                        f"- {denuncia.get('titulo')} | {denuncia.get('tipo')} | "
                        f"Estado: {denuncia.get('estado')} | Creada: {denuncia.get('creada_en')}"
                    )
            pausa()
        elif opcion == "3":
            print("Funcionalidad en construccion.")
            pausa()
        elif opcion == "4":
            limpiar_pantalla()
            print("DENUNCIAS PUBLICAS")
            print("1. Ultimo dia")
            print("2. Ultima semana")
            print("3. Todo")
            opcion_periodo = input("Seleccione: ").strip()
            if opcion_periodo == "1":
                periodo = "dia"
            elif opcion_periodo == "2":
                periodo = "semana"
            else:
                periodo = "todo"

            denuncias = obtener_denuncias_publicas(periodo)
            if not denuncias:
                print("No hay denuncias publicas en el periodo seleccionado.")
            else:
                for denuncia in denuncias:
                    print(
                        f"- {denuncia.get('titulo')} | {denuncia.get('ciudad_provincia')} | "
                        f"Creada: {denuncia.get('creada_en')}"
                    )
            pausa()
        elif opcion == "5":
            cerrar_sesion()
        else:
            print("Opcion invalida.")
            pausa()
