# Arquitectura del sistema (CLI funcional)

## Alcance

Este documento describe la arquitectura tecnica, la organizacion del codigo y el modelo de datos. El manual de usuario contiene los pasos de uso y las capturas.

## Requisitos tecnicos

- Python 3.x
- Ejecucion en consola (CLI)

## Principios

- Enfoque funcional: funciones, diccionarios y listas; sin clases ni dataclasses.
- Estado global minimo: `usuario_actual` en `nucleo/sesion.py`.
- Persistencia simple con JSON (tres archivos en `datos/`).
- Separacion modular por responsabilidad.
- Compatibilidad conceptual con el HTML (campos y flujo).

## Estructura de carpetas

- `principal.py`: punto de entrada y arranque del flujo.
- `nucleo/`: constantes, utilidades, validaciones, persistencia y sesion.
- `autenticacion/`: registro, inicio de sesion y autorizacion.
- `denuncias/`: crear, listar, filtrar, denuncias publicas y actualizar estado.
- `mensajes/`: buzon, envio y listado.
- `menus/`: navegacion y menus CLI.
- `datos/`: `usuarios.json`, `denuncias.json`, `mensajes.json`.
- `pruebas/`: pruebas basicas (funcionales, sin frameworks complejos).
- `documentacion/`: este archivo y el manual de usuario.

## Flujo general

1. Menu inicio
2. Autenticacion (registro / inicio de sesion)
3. Menu usuario o menu autoridad
4. Accion -> funcion -> persistencia -> retorno
5. Salida del sistema

## Componentes y responsabilidades

### Nucleo

- `constantes.py`: rutas JSON, tipos de denuncia, estados, provincias y catalogo de ciudades por provincia.
- `persistencia.py`: lectura/escritura de listas JSON (sin logica de negocio).
- `utilidades.py`: IDs, fechas, limpieza de pantalla, titulos, parseo de fechas y formateo de listas en columnas.
- `validaciones.py`: reglas de entrada (usuario, clave, fecha, ciudad/provincia y tipo).
- `sesion.py`: `usuario_actual` y helpers basicos.

### Autenticacion

- `registro.py`: crea usuarios con validaciones y confirma disponibilidad del nombre.
- `inicio_sesion.py`: valida credenciales y retorna el usuario.
- `autorizacion.py`: crea autoridad demo de forma idempotente.

### Denuncias

- `crear_denuncia.py`: valida datos y guarda denuncia.
- `listar_denuncias.py`: listados por usuario y generales (ordenados por fecha).
- `denuncias_publicas.py`: filtro por periodo y orden por fecha.
- `filtros.py`: filtros por periodo, tipo y estado.
- `actualizar_estado.py`: cambio de estado por autoridad.

### Mensajes

- `enviar_mensaje.py`: crea mensajes y persiste.
- `listar_mensajes.py`: lista y marca como leidos.
- `buzon.py`: determina denuncias disponibles y autoridad destino.

### Menus

- `menu_inicio.py`: menu principal.
- `menu_usuario.py`: menu ciudadano con contador de no leidos.
- `menu_autoridad.py`: menu autoridad con contador de no leidos.
- `navegacion.py`: orquesta el flujo, confirma clave en registro y muestra provincias/ciudades en columnas.

## Modelo de datos (diccionarios)

### Usuario

```
{
  "id": "u_...",
  "nombre_usuario": "alias",
  "clave": "...",
  "es_autoridad": false,
  "creado_en": "DD-MM-AAAA"
}
```

### Denuncia

```
{
  "id": "d_...",
  "usuario_id": "u_...",
  "nombre_usuario": "alias",
  "titulo": "...",
  "descripcion": "...",
  "fecha_evento": "DD-MM-AAAA",
  "ciudad_provincia": "Provincia - Ciudad",
  "tipo": "Aseo y Ornato | Transito Vial | Delito",
  "es_publica": true,
  "estado": "Recibida | En Proceso | Resuelta | Rechazada",
  "creada_en": "DD-MM-AAAA"
}
```

### Mensaje

```
{
  "id": "m_...",
  "denuncia_id": "d_...",
  "remitente_id": "u_...",
  "remitente_nombre": "alias",
  "destinatario_id": "u_...",
  "contenido": "...",
  "creado_en": "DD-MM-AAAA",
  "leido": false
}
```

## Reglas de negocio

- `nombre_usuario` es unico (case-insensitive).
- `clave` minimo 6 caracteres.
- `fecha_evento` se ingresa como DD-MM-AAAA (se acepta YYYY-MM-DD si se requiere).
- `creada_en` se genera automaticamente en DD-MM-AAAA.
- `tipo` y `estado` deben pertenecer a las listas oficiales.
- `ciudad_provincia` se valida como "Provincia - Ciudad" usando el catalogo de provincias y ciudades.
- El registro solicita confirmacion de clave antes de crear el usuario.
- El filtro de denuncias publicas usa `creada_en`.

## Persistencia JSON

- Cada archivo en `datos/` contiene una lista de diccionarios.
- La lectura tolera archivos inexistentes o invalidos y retorna listas vacias.
- Se guarda despues de acciones clave (registro, denuncia, mensaje, estado).

## Seguridad (alcance academico)

- La clave se guarda en texto plano (requerimiento academico).
- La entrada de clave se oculta en consola con `getpass`.
- No hay cifrado ni control de concurrencia.

## Manejo de errores

- Entradas invalidas retornan mensajes y vuelven al menu.
- Archivos JSON invalidos se reemplazan por listas vacias al leer.

## Estado actual (avance)

- Autenticacion completa con registro e inicio de sesion.
- Denuncias completas (crear, listar, publicas, filtros, estado).
- Mensajes completos (buzon, envio, lectura, no leidos).
- Autoridad demo idempotente.
- Pulidos: orden por fecha, filtros de autoridad, seleccion provincia -> ciudad en columnas.
- Consola: espaciado y saltos de linea para mejor lectura.
