from autenticacion.autorizacion import asegurar_autoridad_demo
from menus.menu_autoridad import menu_autoridad
from menus.menu_inicio import menu_inicio
from menus.menu_usuario import menu_usuario
from nucleo.sesion import iniciar_sesion, cerrar_sesion, esta_autenticado, es_autoridad
from nucleo.utilidades import limpiar_pantalla, pausa


def iniciar_sesion_demo():
	limpiar_pantalla()
	print("INICIO DE SESION (DEMO)")
	print("1. Ciudadano")
	print("2. Autoridad")
	opcion = input("Seleccione: ").strip()

	if opcion == "1":
		iniciar_sesion({
			"id": "u_demo",
			"nombre_usuario": "ciudadano_demo",
			"es_autoridad": False,
		})
		return True

	if opcion == "2":
		iniciar_sesion({
			"id": "u_demo_aut",
			"nombre_usuario": "autoridad_demo",
			"es_autoridad": True,
		})
		return True

	return False


def ejecutar():
	asegurar_autoridad_demo()

	while True:
		limpiar_pantalla()

		if not esta_autenticado():
			opcion = menu_inicio()
			if opcion == "1":
				if not iniciar_sesion_demo():
					print("Opcion invalida.")
					pausa()
			elif opcion == "2":
				print("Funcionalidad en construccion.")
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
