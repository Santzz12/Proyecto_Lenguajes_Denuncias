import json
import os
import denuncias

ARCHIVO_DATOS = os.path.join("datos", "datos.json")

def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        return {"usuarios": {}, "denuncias": [], "mensajes": []}
    with open(ARCHIVO_DATOS, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardar_datos(estado_actual):
    with open(ARCHIVO_DATOS, 'w', encoding='utf-8') as archivo:
        json.dump(estado_actual, archivo, indent=4)

def iniciar_sistema():
    
    estado_sistema = cargar_datos()

    while True:
        print("\n=== SISTEMA DE DENUNCIAS ANONIMAS ===")
        print("1. Registrar usuario")
        print("2. Ingresar al sistema (Login)")
        print("3. Consultar denuncias publicas")
        print("4. Crear nueva denuncia (Test)")
        print("5. Salir")
        
        opcion = input("\nElige una opcion (1-5): ")
        
        if opcion == "1":
            print("\n=> [Modulo de registro en construccion...]")
            
        elif opcion == "2":
            print("\n=> [Modulo de login en construccion...]")
            
        elif opcion == "3":
            print("\n--- DENUNCIAS PUBLICAS RECIENTES ---")
            publicas = denuncias.consultar_publicas(estado_sistema["denuncias"], 7)
            
            if not publicas:
                print("No hay denuncias publicas en los ultimos 7 dias.")
            else:
                for d in publicas:
                    print(f"- {d['titulo']} ({d['ciudad']}) | Fecha: {d['fecha']}")
                    
        elif opcion == "4":
            print("\n--- FORMULARIO DE NUEVA DENUNCIA ---")
            titulo = input("Titulo de la denuncia: ")
            descripcion = input("Breve descripcion: ")
            ciudad = input("Ciudad del incidente: ")
            tipo = input("Tipo (Ej. Robo, Fraude, Ruido): ")
            es_publica_str = input("¿Deseas que sea visible al publico? (s/n): ").lower()
            
           
            es_publica = True if es_publica_str == 's' else False
            
            
            lista_actualizada = denuncias.agregar_denuncia(
                estado_sistema["denuncias"], 
                titulo, descripcion, ciudad, tipo, es_publica
            )
            
            
            estado_sistema["denuncias"] = lista_actualizada
            print("\n[Exito] Denuncia registrada correctamente.")
            
        elif opcion == "5":
            print("\nGuardando informacion y cerrando el sistema...")
            guardar_datos(estado_sistema)
            break
            
        else:
            print("\n[Error] Opcion invalida. Intenta nuevamente.")

if __name__ == "__main__":
    iniciar_sistema()