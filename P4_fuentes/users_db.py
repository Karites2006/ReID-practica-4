import json
import os

FILE_USERS = "users.json"

def cargar_usuarios():
    if not os.path.exists(FILE_USERS):
        return {}
    with open(FILE_USERS, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            return {}

def guardar_usuarios_json(datos):
    with open(FILE_USERS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)

# --- FUNCIONES DE LECTURA/ESCRITURA ESPECÍFICAS ---

def obtener_usuario_por_username(username):
    datos = cargar_usuarios()
    return datos.get(username)

def crear_usuario_db(username, password, id_num, id_pais, id_historial, es_admin=False):
    datos = cargar_usuarios()
    if username in datos:
        return False
    
    datos[username] = {
        "id": id_num,
        "nombre": username,
        "password": password,
        "id_pais": id_pais,
        "id_historial": id_historial,
        "esta_suscripto": False,
        "es_admin": es_admin
    }
    guardar_usuarios_json(datos)
    return True

def actualizar_usuario_db(username, campos_a_actualizar):
    datos = cargar_usuarios()
    if username in datos:
        datos[username].update(campos_a_actualizar)
        guardar_usuarios_json(datos)
        return True
    return False

def borrar_usuario_db(username):
    datos = cargar_usuarios()
    if username in datos:
        del datos[username]
        guardar_usuarios_json(datos)
        return True
    return False