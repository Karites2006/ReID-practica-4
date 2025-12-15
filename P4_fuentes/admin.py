from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from db import agregar_video_db, borrar_video_db, editar_video_db, obtener_todos_videos
from users_db import cargar_usuarios, borrar_usuario_db, actualizar_usuario_db
from schemas import VideoSchema

admin_bp = Blueprint('admin', __name__)

# Decorador auxiliar para verificar admin
def admin_required():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return False
    return True

# --- GESTIÓN DE VIDEOS ---

@admin_bp.route('/videos', methods=['POST'])
@jwt_required()
def add_video():
    if not admin_required(): return jsonify({"error": "Admin required"}), 403
    
    data = request.json
    try:
        VideoSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
    if agregar_video_db(data):
        return jsonify({"message": "Video añadido"}), 201
    return jsonify({"error": "ID de video duplicado"}), 409

@admin_bp.route('/videos/<int:vid_id>', methods=['DELETE'])
@jwt_required()
def delete_video(vid_id):
    if not admin_required(): return jsonify({"error": "Admin required"}), 403
    
    if borrar_video_db(vid_id):
        return jsonify({"message": "Video eliminado"}), 200
    return jsonify({"error": "Video no encontrado"}), 404

@admin_bp.route('/videos/<int:vid_id>', methods=['PUT'])
@jwt_required()
def edit_video(vid_id):
    if not admin_required(): return jsonify({"error": "Admin required"}), 403
    
    data = request.json
    if editar_video_db(vid_id, data):
        return jsonify({"message": "Video actualizado"}), 200
    return jsonify({"error": "Video no encontrado"}), 404

# Listar TODOS los videos (sin filtro de país, vista admin)
@admin_bp.route('/videos/all', methods=['GET'])
@jwt_required()
def list_all_videos():
    if not admin_required(): return jsonify({"error": "Admin required"}), 403
    return jsonify(obtener_todos_videos()), 200

# --- GESTIÓN DE USUARIOS ---

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    if not admin_required(): return jsonify({"error": "Admin required"}), 403
    # Devolvemos todos los usuarios (sin contraseñas por seguridad)
    users = cargar_usuarios()
    safe_users = []
    for k, v in users.items():
        user_copy = v.copy()
        user_copy.pop("password", None)
        safe_users.append(user_copy)
    return jsonify(safe_users), 200

# Banear usuario
@admin_bp.route('/users/<username>', methods=['DELETE'])
@jwt_required()
def ban_user(username):
    if not admin_required(): return jsonify({"error": "Admin required"}), 403
    if borrar_usuario_db(username):
        return jsonify({"message": "Usuario baneado (eliminado)"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

# Editar usuario (ej. forzar cancelar suscripción)
@admin_bp.route('/users/<username>', methods=['PUT'])
@jwt_required()
def edit_user(username):
    if not admin_required(): return jsonify({"error": "Admin required"}), 403
    data = request.json # Ej: {"esta_suscripto": false}
    if actualizar_usuario_db(username, data):
        return jsonify({"message": "Usuario modificado"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404