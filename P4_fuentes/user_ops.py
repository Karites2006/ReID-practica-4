from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from users_db import obtener_usuario_por_username, actualizar_usuario_db
from db import obtener_todos_videos, obtener_video_por_id, obtener_historial_por_usuario
from datetime import datetime

user_ops_bp = Blueprint('user_ops', __name__)

# Pagar suscripción
@user_ops_bp.route('/usuarios/<username>/subscription', methods=['PUT'])
@jwt_required()
def pagar_suscripcion(username):
    # Lógica: cambiar esta_suscripto a True
    if actualizar_usuario_db(username, {"esta_suscripto": True}):
        return jsonify({"message": "Suscripción activada"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# Cancelar suscripción
@user_ops_bp.route('/usuarios/<username>/subscription', methods=['DELETE'])
@jwt_required()
def cancelar_suscripcion(username):
    if actualizar_usuario_db(username, {"esta_suscripto": False}):
        return jsonify({"message": "Suscripción cancelada"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# Obtener lista de videos (Filtro por país y fecha opcional)
@user_ops_bp.route('/videos', methods=['GET'])
@jwt_required()
def listar_videos():
    claims = get_jwt()
    user_pais = claims.get("id_pais")
    
    videos = obtener_todos_videos()
    
    # Filtrar por país (P4 Req: disponibles en su país)
    # Si id_paises en video es lista de enteros, verificamos pertenencia
    videos_disponibles = [v for v in videos if user_pais in v.get('id_paises', [])]
    
    # Filtrar por fecha (Query param ?fecha=YYYY)
    fecha_filtro = request.args.get('fecha')
    if fecha_filtro:
        # Asumimos formato fecha en video "DD/MM/YYYY" y filtro solo año "YYYY"
        # O coincidencia exacta de string
        videos_disponibles = [v for v in videos_disponibles if fecha_filtro in v.get('fecha', '')]

    return jsonify(videos_disponibles), 200

# Reproducir (obtener) video
@user_ops_bp.route('/videos/<int:vid_id>', methods=['GET'])
@jwt_required()
def ver_video(vid_id):
    video = obtener_video_por_id(vid_id)
    if video:
        return jsonify(video), 200
    return jsonify({"error": "Video no encontrado"}), 404

# Consultar historial
@user_ops_bp.route('/usuarios/me/historial', methods=['GET'])
@jwt_required()
def ver_historial():
    claims = get_jwt()
    user_id = claims.get("user_id")
    historial = obtener_historial_por_usuario(user_id)
    if historial:
        return jsonify(historial), 200
    return jsonify({"error": "Historial no encontrado"}), 404