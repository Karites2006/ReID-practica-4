import json
import os

FILE_VIDEOS = "videos.json"
FILE_HISTORIAL = "historial.json"
FILE_PAIS = "pais.json"

# --- UTILIDADES GENÉRICAS ---
def leer_json(archivo):
    if not os.path.exists(archivo):
        return [] if archivo != "pais.json" else [] # Retornamos lista para videos/historiales
    with open(archivo, "r", encoding="utf-8") as f:
        try:
            content = json.load(f)
            # Aseguramos que sea una lista para facilitar búsquedas, 
            # aunque en P3 ejemplo videos.json parece un objeto único, lo lógico es una lista de objetos.
            if isinstance(content, dict): 
                return [content] # Si solo hay uno, lo metemos en lista
            return content
        except json.JSONDecodeError:
            return []

def guardar_json(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

# --- VIDEOS ---
def obtener_todos_videos():
    return leer_json(FILE_VIDEOS)

def obtener_video_por_id(vid_id):
    videos = leer_json(FILE_VIDEOS)
    for v in videos:
        if v['id'] == vid_id:
            return v
    return None

def agregar_video_db(nuevo_video):
    videos = leer_json(FILE_VIDEOS)
    # Verificar ID duplicado
    for v in videos:
        if v['id'] == nuevo_video['id']:
            return False
    videos.append(nuevo_video)
    guardar_json(FILE_VIDEOS, videos)
    return True

def borrar_video_db(vid_id):
    videos = leer_json(FILE_VIDEOS)
    videos_filtrados = [v for v in videos if v['id'] != vid_id]
    if len(videos) == len(videos_filtrados):
        return False
    guardar_json(FILE_VIDEOS, videos_filtrados)
    return True

def editar_video_db(vid_id, datos_nuevos):
    videos = leer_json(FILE_VIDEOS)
    for i, v in enumerate(videos):
        if v['id'] == vid_id:
            videos[i].update(datos_nuevos)
            guardar_json(FILE_VIDEOS, videos)
            return True
    return False

# --- HISTORIAL ---
def crear_historial_db(id_historial, id_usuario):
    historiales = leer_json(FILE_HISTORIAL)
    nuevo = {
        "id": id_historial,
        "id_usuario": id_usuario,
        "id_videos": []
    }
    historiales.append(nuevo)
    guardar_json(FILE_HISTORIAL, historiales)

def obtener_historial_por_usuario(id_usuario):
    historiales = leer_json(FILE_HISTORIAL)
    for h in historiales:
        if h['id_usuario'] == id_usuario:
            return h
    return None