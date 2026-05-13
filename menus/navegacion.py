from getpass import getpass

from autenticacion.autorizacion import asegurar_autoridad_demo
from autenticacion.inicio_sesion import iniciar_sesion_usuario
from autenticacion.registro import registrar_usuario
from denuncias.actualizar_estado import actualizar_estado_denuncia
from denuncias.crear_denuncia import crear_denuncia
from denuncias.denuncias_publicas import obtener_denuncias_publicas
from denuncias.filtros import filtrar_por_tipo_estado
from denuncias.listar_denuncias import listar_denuncias_por_usuario, listar_todas_las_denuncias
from mensajes.buzon import obtener_denuncias_buzon, obtener_autoridad_destinatario
from mensajes.enviar_mensaje import enviar_mensaje
from mensajes.listar_mensajes import (
    listar_mensajes_por_denuncia,
    marcar_mensajes_leidos,
    contar_no_leidos,
)
from menus.menu_autoridad import menu_autoridad
from menus.menu_inicio import menu_inicio
from menus.menu_usuario import menu_usuario
from nucleo.constantes import TIPOS_DENUNCIA, ESTADOS_DENUNCIA, PROVINCIAS
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
                clave = getpass("Clave: ")
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
                clave = getpass("Clave (minimo 6 caracteres): ")
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
            no_leidos = contar_no_leidos(sesion.usuario_actual.get("id"))
            opcion = menu_autoridad(no_leidos)
            if opcion == "3":
                cerrar_sesion()
            elif opcion == "1":
                limpiar_pantalla()
                print("DENUNCIAS REGISTRADAS")

                denuncias = listar_todas_las_denuncias()
                print("\nFiltro por tipo:")
                print("0. Todos")
                for indice_tipo, tipo_opcion in enumerate(TIPOS_DENUNCIA, start=1):
                    print(f"{indice_tipo}. {tipo_opcion}")
                opcion_tipo = input("Seleccione: ").strip()
                tipo_filtro = None
                if opcion_tipo.isdigit() and int(opcion_tipo) > 0:
                    indice_tipo = int(opcion_tipo) - 1
                    if 0 <= indice_tipo < len(TIPOS_DENUNCIA):
                        tipo_filtro = TIPOS_DENUNCIA[indice_tipo]

                print("\nFiltro por estado:")
                print("0. Todos")
                for indice_estado, estado_opcion in enumerate(ESTADOS_DENUNCIA, start=1):
                    print(f"{indice_estado}. {estado_opcion}")
                opcion_estado = input("Seleccione: ").strip()
                estado_filtro = None
                if opcion_estado.isdigit() and int(opcion_estado) > 0:
                    indice_estado = int(opcion_estado) - 1
                    if 0 <= indice_estado < len(ESTADOS_DENUNCIA):
                        estado_filtro = ESTADOS_DENUNCIA[indice_estado]

                denuncias = filtrar_por_tipo_estado(denuncias, tipo_filtro, estado_filtro)
                if not denuncias:
                    if tipo_filtro and estado_filtro:
                        print("No hay denuncias con el tipo y estado seleccionados.")
                    elif tipo_filtro:
                        print("No hay denuncias del tipo seleccionado.")
                    elif estado_filtro:
                        print("No hay denuncias con el estado seleccionado.")
                    else:
                        print("No hay denuncias registradas.")
                    pausa()
                    continue

                for indice, denuncia in enumerate(denuncias, start=1):
                    fecha_creada = formatear_fecha(denuncia.get("creada_en"))
                    fecha_evento = formatear_fecha(denuncia.get("fecha_evento"))
                    print(
                        f"{indice}. {denuncia.get('titulo')} | {denuncia.get('tipo')} | "
                        f"Evento: {fecha_evento} | Creada: {fecha_creada} | "
                        f"Estado: {denuncia.get('estado')}"
                    )

                seleccion = input("Seleccione una denuncia (0 para volver): ").strip()
                if not seleccion.isdigit() or int(seleccion) == 0:
                    continue

                indice = int(seleccion) - 1
                if indice < 0 or indice >= len(denuncias):
                    print("Opcion invalida.")
                    pausa()
                    continue

                denuncia = denuncias[indice]
                limpiar_pantalla()
                print("DETALLE DE DENUNCIA")
                print(f"Titulo: {denuncia.get('titulo')}")
                print(f"Usuario: {denuncia.get('nombre_usuario')}")
                print(f"Ciudad/Provincia: {denuncia.get('ciudad_provincia')}")
                print(f"Fecha del evento: {formatear_fecha(denuncia.get('fecha_evento'))}")
                print(f"Fecha de creacion: {formatear_fecha(denuncia.get('creada_en'))}")
                print(f"Descripcion: {denuncia.get('descripcion')}")
                print(f"Estado actual: {denuncia.get('estado')}")

                print("\nEstados disponibles:")
                for indice_estado, estado in enumerate(ESTADOS_DENUNCIA, start=1):
                    print(f"{indice_estado}. {estado}")

                opcion_estado = input("Seleccione nuevo estado (0 para mantener): ").strip()
                if not opcion_estado.isdigit() or int(opcion_estado) == 0:
                    continue

                indice_estado = int(opcion_estado) - 1
                if indice_estado < 0 or indice_estado >= len(ESTADOS_DENUNCIA):
                    print("Opcion invalida.")
                    pausa()
                    continue

                nuevo_estado = ESTADOS_DENUNCIA[indice_estado]
                ok, _, mensaje = actualizar_estado_denuncia(denuncia.get("id"), nuevo_estado)
                print(mensaje)
                pausa()
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
                fecha_evento = formatear_fecha(denuncia.get("fecha_evento"))
                fecha_creada = formatear_fecha(denuncia.get("creada_en"))
                print(f"CONVERSACION: {denuncia.get('titulo')}")
                print(f"Evento: {fecha_evento} | Creada: {fecha_creada}")
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

        no_leidos = contar_no_leidos(sesion.usuario_actual.get("id"))
        opcion = menu_usuario(no_leidos)
        if opcion == "1":
            limpiar_pantalla()
            print("NUEVA DENUNCIA")
            titulo = input("Titulo: ").strip()
            descripcion = input("Descripcion: ").strip()
            fecha_evento = input("Fecha del evento (DD-MM-AAAA): ").strip()
            print("Ciudad/Provincia:")
            for indice, provincia in enumerate(PROVINCIAS, start=1):
                print(f"{indice}. {provincia}")
            opcion_provincia = input("Seleccione (numero) o escriba el nombre: ").strip()
            ciudad_provincia = None
            if opcion_provincia.isdigit():
                indice = int(opcion_provincia)
                if 1 <= indice <= len(PROVINCIAS):
                    ciudad_provincia = PROVINCIAS[indice - 1]
            else:
                ciudad_provincia = opcion_provincia

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
                    fecha_evento = formatear_fecha(denuncia.get("fecha_evento"))
                    fecha_creada = formatear_fecha(denuncia.get("creada_en"))
                    print(
                        f"- {denuncia.get('titulo')} | {denuncia.get('tipo')} | "
                        f"Evento: {fecha_evento} | Creada: {fecha_creada} | "
                        f"Estado: {denuncia.get('estado')}"
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
            fecha_evento = formatear_fecha(denuncia.get("fecha_evento"))
            fecha_creada = formatear_fecha(denuncia.get("creada_en"))
            print(f"CONVERSACION: {denuncia.get('titulo')}")
            print(f"Evento: {fecha_evento} | Creada: {fecha_creada}")
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
                    fecha_evento = formatear_fecha(denuncia.get("fecha_evento"))
                    print(
                        f"- {denuncia.get('titulo')} | {denuncia.get('ciudad_provincia')} | "
                        f"Evento: {fecha_evento} | Creada: {fecha_creada}"
                    )
            pausa()
        elif opcion == "5":
            cerrar_sesion()
        else:
            print("Opcion invalida.")
            pausa()
