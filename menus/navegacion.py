from autenticacion.autorizacion import asegurar_autoridad_demo
from autenticacion.inicio_sesion import iniciar_sesion_usuario
from autenticacion.registro import registrar_usuario
from denuncias.crear_denuncia import crear_denuncia
from denuncias.denuncias_publicas import obtener_denuncias_publicas
from denuncias.listar_denuncias import listar_denuncias_por_usuario
from mensajes.buzon import obtener_denuncias_buzon, obtener_autoridad_destinatario
from mensajes.enviar_mensaje import enviar_mensaje
from mensajes.listar_mensajes import listar_mensajes_por_denuncia, marcar_mensajes_leidos
from menus.menu_autoridad import menu_autoridad
from menus.menu_inicio import menu_inicio
from menus.menu_usuario import menu_usuario
from nucleo.constantes import TIPOS_DENUNCIA
from nucleo.sesion import iniciar_sesion, cerrar_sesion, esta_autenticado, es_autoridad
from nucleo.utilidades import limpiar_pantalla, pausa, formatear_fecha
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
            elif opcion == "2":
                limpiar_pantalla()
                print("BUZON DE MENSAJES")

                denuncias_buzon = obtener_denuncias_buzon(sesion.usuario_actual)
                if not denuncias_buzon:
                    print("No hay denuncias registradas.")
                    pausa()
                    continue

                for indice, denuncia in enumerate(denuncias_buzon, start=1):
                    print(
                        f"{indice}. {denuncia.get('titulo')} | "
                        f"Usuario: {denuncia.get('nombre_usuario')}"
                    )

                seleccion = input("Seleccione una denuncia (0 para volver): ").strip()
                if not seleccion.isdigit() or int(seleccion) == 0:
                    continue

                indice = int(seleccion) - 1
                if indice < 0 or indice >= len(denuncias_buzon):
                    print("Opcion invalida.")
                    pausa()
                    continue

                denuncia = denuncias_buzon[indice]
                mensajes = listar_mensajes_por_denuncia(denuncia.get("id"))
                marcar_mensajes_leidos(denuncia.get("id"), sesion.usuario_actual.get("id"))

                limpiar_pantalla()
                print(f"CONVERSACION: {denuncia.get('titulo')}")
                if not mensajes:
                    print("No hay mensajes aun.")
                else:
                    for mensaje in mensajes:
                        fecha = formatear_fecha(mensaje.get("creado_en"))
                        remitente = mensaje.get("remitente_nombre")
                        contenido = mensaje.get("contenido")
                        print(f"[{fecha}] {remitente}: {contenido}")

                contenido = input("Escriba un mensaje (Enter para volver): ").strip()
                if contenido:
                    ok, _, mensaje = enviar_mensaje(
                        denuncia.get("id"),
                        sesion.usuario_actual.get("id"),
                        sesion.usuario_actual.get("nombre_usuario"),
                        denuncia.get("usuario_id"),
                        contenido,
                    )
                    print(mensaje)
                    pausa()
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
            fecha_evento = input("Fecha del evento (DD-MM-AAAA): ").strip()
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
                    fecha_creada = formatear_fecha(denuncia.get("creada_en"))
                    print(
                        f"- {denuncia.get('titulo')} | {denuncia.get('tipo')} | "
                        f"Estado: {denuncia.get('estado')} | Creada: {fecha_creada}"
                    )
            pausa()
        elif opcion == "3":
            limpiar_pantalla()
            print("BUZON PERSONAL")

            denuncias_buzon = obtener_denuncias_buzon(sesion.usuario_actual)
            if not denuncias_buzon:
                print("No hay denuncias disponibles para el buzon.")
                pausa()
                continue

            for indice, denuncia in enumerate(denuncias_buzon, start=1):
                print(f"{indice}. {denuncia.get('titulo')} | {denuncia.get('estado')}")

            seleccion = input("Seleccione una denuncia (0 para volver): ").strip()
            if not seleccion.isdigit() or int(seleccion) == 0:
                continue

            indice = int(seleccion) - 1
            if indice < 0 or indice >= len(denuncias_buzon):
                print("Opcion invalida.")
                pausa()
                continue

            denuncia = denuncias_buzon[indice]
            mensajes = listar_mensajes_por_denuncia(denuncia.get("id"))
            marcar_mensajes_leidos(denuncia.get("id"), sesion.usuario_actual.get("id"))

            limpiar_pantalla()
            print(f"CONVERSACION: {denuncia.get('titulo')}")
            if not mensajes:
                print("No hay mensajes aun.")
            else:
                for mensaje in mensajes:
                    fecha = formatear_fecha(mensaje.get("creado_en"))
                    remitente = mensaje.get("remitente_nombre")
                    contenido = mensaje.get("contenido")
                    print(f"[{fecha}] {remitente}: {contenido}")

            destinatario = obtener_autoridad_destinatario()
            if not destinatario:
                print("No hay autoridad disponible para este buzon.")
                pausa()
                continue

            contenido = input("Escriba un mensaje (Enter para volver): ").strip()
            if contenido:
                ok, _, mensaje = enviar_mensaje(
                    denuncia.get("id"),
                    sesion.usuario_actual.get("id"),
                    sesion.usuario_actual.get("nombre_usuario"),
                    destinatario.get("id"),
                    contenido,
                )
                print(mensaje)
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
                    fecha_creada = formatear_fecha(denuncia.get("creada_en"))
                    print(
                        f"- {denuncia.get('titulo')} | {denuncia.get('ciudad_provincia')} | "
                        f"Creada: {fecha_creada}"
                    )
            pausa()
        elif opcion == "5":
            cerrar_sesion()
        else:
            print("Opcion invalida.")
            pausa()
