import json
import os

FILE_VIDEOS = "videos.json"
FILE_HISTORIAL = "historial.json"
FILE_PAIS = "pais.json"

def leer_json(archivo):
    if not os.path.exists(archivo):
        return []
    with open(archivo, "r", encoding="utf-8") as f:
        try:
            content = json.load(f)
            if isinstance(content, dict): 
                return [content] 
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
    str_vid_id = str(vid_id)
    for v in videos:
        if str(v.get('id')) == str_vid_id:
            return v
    return None

def agregar_video_db(nuevo_video):
    videos = leer_json(FILE_VIDEOS)
    for v in videos:
        if str(v['id']) == str(nuevo_video['id']):
            return False
    videos.append(nuevo_video)
    guardar_json(FILE_VIDEOS, videos)
    return True

def borrar_video_db(vid_id):
    videos = leer_json(FILE_VIDEOS)
    str_vid_id = str(vid_id)
    filtrados = [v for v in videos if str(v['id']) != str_vid_id]
    if len(videos) == len(filtrados): return False
    guardar_json(FILE_VIDEOS, filtrados)
    return True

def editar_video_db(vid_id, datos_nuevos):
    videos = leer_json(FILE_VIDEOS)
    str_vid_id = str(vid_id)
    for i, v in enumerate(videos):
        if str(v['id']) == str_vid_id:
            videos[i].update(datos_nuevos)
            videos[i]['id'] = vid_id # Mantener ID
            guardar_json(FILE_VIDEOS, videos)
            return True
    return False

# --- HISTORIAL ---
def crear_historial_db(id_historial, id_usuario):
    historiales = leer_json(FILE_HISTORIAL)
    if any(h.get('id_usuario') == id_usuario for h in historiales):
        return
    nuevo = {"id": id_historial, "id_usuario": id_usuario, "id_videos": []}
    historiales.append(nuevo)
    guardar_json(FILE_HISTORIAL, historiales)

def obtener_historial_por_usuario(id_usuario):
    historiales = leer_json(FILE_HISTORIAL)
    for h in historiales:
        if h.get('id_usuario') == id_usuario:
            return h
    return None

def agregar_video_a_historial(id_usuario, id_video):
    historiales = leer_json(FILE_HISTORIAL)
    encontrado = False
    for h in historiales:
        if h.get('id_usuario') == id_usuario:
            if "id_videos" not in h: h["id_videos"] = []
            h["id_videos"].append(id_video)
            encontrado = True
            break
    if encontrado:
        guardar_json(FILE_HISTORIAL, historiales)
        return True
    return False