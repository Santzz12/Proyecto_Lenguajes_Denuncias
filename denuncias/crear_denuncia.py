from nucleo.constantes import RUTA_DENUNCIAS, ESTADOS_DENUNCIA, TIPOS_DENUNCIA
from nucleo.persistencia import leer_lista_json, guardar_lista_json
from nucleo.utilidades import generar_id, fecha_iso
from nucleo.validaciones import (
    validar_texto_obligatorio,
    validar_fecha_evento,
    validar_tipo_denuncia,
)


def crear_denuncia(datos_denuncia):
    ok, mensaje = validar_texto_obligatorio(datos_denuncia.get("titulo"), "titulo")
    if not ok:
        return False, None, mensaje

    ok, mensaje = validar_texto_obligatorio(datos_denuncia.get("descripcion"), "descripcion")
    if not ok:
        return False, None, mensaje

    ok, mensaje = validar_texto_obligatorio(
        datos_denuncia.get("ciudad_provincia"),
        "ciudad/provincia",
    )
    if not ok:
        return False, None, mensaje

    ok, mensaje = validar_fecha_evento(datos_denuncia.get("fecha_evento"))
    if not ok:
        return False, None, mensaje

    ok, mensaje = validar_tipo_denuncia(datos_denuncia.get("tipo"), TIPOS_DENUNCIA)
    if not ok:
        return False, None, mensaje

    denuncia = {
        "id": generar_id("d"),
        "usuario_id": datos_denuncia.get("usuario_id"),
        "nombre_usuario": datos_denuncia.get("nombre_usuario"),
        "titulo": datos_denuncia.get("titulo"),
        "descripcion": datos_denuncia.get("descripcion"),
        "fecha_evento": datos_denuncia.get("fecha_evento"),
        "ciudad_provincia": datos_denuncia.get("ciudad_provincia"),
        "tipo": datos_denuncia.get("tipo"),
        "es_publica": bool(datos_denuncia.get("es_publica")),
        "estado": ESTADOS_DENUNCIA[0],
        "creada_en": fecha_iso(),
    }

    denuncias = leer_lista_json(RUTA_DENUNCIAS)
    denuncias.append(denuncia)
    guardar_lista_json(RUTA_DENUNCIAS, denuncias)

    return True, denuncia, "Denuncia registrada correctamente."