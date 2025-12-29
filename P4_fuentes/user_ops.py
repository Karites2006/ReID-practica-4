from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from users_db import actualizar_usuario_db, borrar_usuario_db
from db import obtener_todos_videos, obtener_video_por_id, obtener_historial_por_usuario, agregar_video_a_historial
from datetime import datetime

user_ops_bp = Blueprint('user_ops', __name__)

# --- CUENTA ---

@user_ops_bp.route('/usuarios/me', methods=['PUT'])
@jwt_required()
def editar_mi_usuario():
    username = get_jwt_identity()
    if actualizar_usuario_db(username, request.json):
        return jsonify({"message": "Actualizado correctamente"}), 200
    return jsonify({"error": "Error al actualizar"}), 400

@user_ops_bp.route('/usuarios/me', methods=['DELETE'])
@jwt_required()
def borrar_mi_usuario():
    username = get_jwt_identity()
    if borrar_usuario_db(username):
        return jsonify({"message": "Cuenta borrada"}), 200
    return jsonify({"error": "Error al borrar"}), 400

# --- SUSCRIPCION ---

@user_ops_bp.route('/usuarios/subscription', methods=['PUT'])
@jwt_required()
def pagar_suscripcion():
    username = get_jwt_identity()
    actualizar_usuario_db(username, {"esta_suscripto": True})
    return jsonify({"message": "Suscripción ACTIVA"}), 200

@user_ops_bp.route('/usuarios/subscription', methods=['DELETE'])
@jwt_required()
def cancelar_suscripcion():
    username = get_jwt_identity()
    actualizar_usuario_db(username, {"esta_suscripto": False})
    return jsonify({"message": "Suscripción CANCELADA"}), 200

# --- VIDEOS ---

@user_ops_bp.route('/videos', methods=['GET'])
@jwt_required()
def listar_videos():
    claims = get_jwt()
    # Obtenemos el ID tal cual (entero)
    pais_usuario = claims.get("id_pais") 

    todos = obtener_todos_videos()
    resultado = []
    fecha_filtro = request.args.get('fecha_inicio')

    for v in todos:
        # Filtro País: comparamos entero con lista de enteros
        if pais_usuario not in v.get('id_paises', []):
            continue

        # Filtro Fecha
        if fecha_filtro:
            try:
                # Tu JSON tiene fechas DD/MM/YYYY
                f_vid = datetime.strptime(v['fecha'], "%d/%m/%Y")
                f_req = datetime.strptime(fecha_filtro, "%d/%m/%Y")
                if f_vid < f_req: continue
            except: 
                continue 
        resultado.append(v)
    return jsonify(resultado), 200

@user_ops_bp.route('/videos/<int:vid_id>', methods=['GET'])
@jwt_required()
def ver_video(vid_id):
    video = obtener_video_por_id(vid_id)
    if not video: return jsonify({"error": "No encontrado"}), 404
    
    claims = get_jwt()
    pais_usuario = claims.get("id_pais")
    
    if pais_usuario not in video.get('id_paises', []):
        return jsonify({"error": "Bloqueado en tu país"}), 403
    
    # Añadir al historial
    user_id = claims.get("user_id")
    if user_id:
        agregar_video_a_historial(user_id, vid_id)
    
    return jsonify(video), 200

@user_ops_bp.route('/usuarios/me/historial', methods=['GET'])
@jwt_required()
def ver_historial():
    claims = get_jwt()
    user_id = claims.get("user_id")
    hist = obtener_historial_por_usuario(user_id)
    # Si no hay historial, devolvemos estructura vacía válida
    if not hist:
        return jsonify({"id_usuario": user_id, "id_videos": []}), 200
    return jsonify(hist), 200