# Arquitectura del sistema (CLI funcional)

## Alcance de este documento

Este archivo describe la arquitectura tecnica y las decisiones de diseno. El manual de usuario es un documento separado con pasos y capturas.

## Principios

- Enfoque funcional: funciones, diccionarios y listas; sin clases ni dataclasses.
- Estado global minimo: `usuario_actual` en `nucleo/sesion.py`.
- Persistencia simple con JSON (tres archivos en `datos/`).
- Separacion modular por responsabilidad.
- Compatibilidad conceptual con el HTML (campos y flujo).

## Estructura de carpetas

- `principal.py`: punto de entrada.
- `nucleo/`: constantes, utilidades, validaciones, persistencia y sesion.
- `autenticacion/`: registro, inicio de sesion y autorizacion.
- `denuncias/`: crear, listar, filtrar y denuncias publicas.
- `mensajes/`: buzon, envio y listado.
- `menus/`: navegacion y menus CLI.
- `datos/`: `usuarios.json`, `denuncias.json`, `mensajes.json`.
- `pruebas/`: pruebas basicas (funcionales, sin frameworks complejos).
- `documentacion/`: este archivo y el manual de usuario.

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
	"ciudad_provincia": "...",
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

## Sesion

- `nucleo/sesion.py` define `usuario_actual = None`.
- La capa de menus consulta y actualiza esta variable global.

## Filtro de denuncias publicas

- El filtro de "ultimo dia / ultima semana" usa `creada_en`.
- `fecha_evento` es informativa y se muestra en el detalle.

## Persistencia JSON

- `nucleo/persistencia.py` ofrece funciones para leer y guardar JSON.
- Se trabaja en memoria y se guarda tras acciones clave (registro, denuncia, mensaje).

## Validaciones minimas

- Registro: usuario unico, longitud minima y clave minima.
- Denuncia: campos obligatorios completos.
- Mensaje: contenido no vacio.

## Flujo general

1. Menu inicio
2. Autenticacion (registro / inicio de sesion)
3. Menu usuario o menu autoridad
4. Accion -> funcion -> persistencia -> retorno
5. Salida del sistema

## Estado actual (avance)

- Constantes, persistencia, utilidades y sesion implementadas.
- Menus base listos con opciones en construccion.
- Autenticacion real implementada (registro e inicio de sesion).
- Validaciones minimas centralizadas en el nucleo.
- Autoridad demo se asegura al inicio del sistema.
- Denuncias: crear, listar propias y consultar publicas.
- Mensajes: buzon personal y envio basico implementados.
- Autoridad: listado general y actualizacion de estado.
- Pulidos: orden por fecha, filtros en autoridad y conteo de no leidos.
