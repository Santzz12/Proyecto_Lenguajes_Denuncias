from nucleo.constantes import RUTA_USUARIOS
from nucleo.persistencia import leer_lista_json
from nucleo.validaciones import validar_credenciales, normalizar_nombre_usuario


def iniciar_sesion_usuario(nombre_usuario, clave):
    ok, mensaje = validar_credenciales(nombre_usuario, clave)
    if not ok:
        return False, None, mensaje

    usuarios = leer_lista_json(RUTA_USUARIOS)
    nombre_normalizado = normalizar_nombre_usuario(nombre_usuario)

    usuario = next(
        (
            u
            for u in usuarios
            if (u.get("nombre_usuario") or "").lower() == nombre_normalizado
            and u.get("clave") == clave
        ),
        None,
    )

    if not usuario:
        return False, None, "Usuario o clave incorrectos."

    return True, usuario, "Inicio de sesion correcto."
