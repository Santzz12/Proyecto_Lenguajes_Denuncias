import datetime

def agregar_denuncia(lista_denuncias, titulo, descripcion, ciudad, tipo, es_publica):
    nueva_denuncia = {
        "titulo": titulo,
        "descripcion": descripcion,
        "ciudad": ciudad,
        "tipo": tipo,
        "es_publica": es_publica,
        "fecha": datetime.date.today().isoformat()
    }
    return lista_denuncias + [nueva_denuncia]

def consultar_publicas(lista_denuncias, filtro_dias):
    fecha_limite = datetime.date.today() - datetime.timedelta(days=filtro_dias)
    
    def cumple_condiciones(denuncia):
        fecha_denuncia = datetime.date.fromisoformat(denuncia["fecha"])
        return denuncia["es_publica"] is True and fecha_denuncia >= fecha_limite

    denuncias_filtradas = filter(cumple_condiciones, lista_denuncias)
    return list(denuncias_filtradas)