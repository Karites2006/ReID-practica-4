from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from db import agregar_video_db, borrar_video_db, editar_video_db, obtener_todos_videos
from users_db import cargar_usuarios, borrar_usuario_db, actualizar_usuario_db

admin_bp = Blueprint('admin', __name__)

def admin_required():
    claims = get_jwt()
    return claims.get("is_admin") == True

# --- VIDEOS ---

@admin_bp.route('/videos', methods=['POST'])
@jwt_required()
def add_video():
    if not admin_required(): return jsonify({"error": "No eres admin"}), 403
    data = request.json
    if agregar_video_db(data):
        return jsonify({"msg":"Video añadido"}), 201
    return jsonify({"error": "ID duplicado"}), 409

@admin_bp.route('/videos/<int:vid_id>', methods=['DELETE'])
@jwt_required()
def delete_video(vid_id):
    if not admin_required(): return jsonify({"error": "No eres admin"}), 403
    if borrar_video_db(vid_id):
        return jsonify({"msg":"Video borrado"}), 200
    return jsonify({"error": "No encontrado"}), 404

@admin_bp.route('/videos/all', methods=['GET'])
@jwt_required()
def list_all():
    if not admin_required(): return jsonify({"error": "No eres admin"}), 403
    return jsonify(obtener_todos_videos()), 200

@admin_bp.route('/videos/<int:vid_id>', methods=['PUT'])
@jwt_required()
def edit_video(vid_id):
    if not admin_required(): return jsonify({"error": "No eres admin"}), 403
    data = request.json
    if editar_video_db(vid_id, data):
        return jsonify({"msg":"Video editado"}), 200
    return jsonify({"error": "No encontrado"}), 404

# --- USUARIOS ---

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    if not admin_required(): return jsonify({"error": "No eres admin"}), 403
    users = cargar_usuarios()
    # Quitamos passwords para que quede limpio en la captura
    safe_users = {k: v for k, v in users.items() if k != "password"}
    return jsonify(safe_users), 200

@admin_bp.route('/users/<username>', methods=['PUT'])
@jwt_required()
def edit_user(username):
    if not admin_required(): return jsonify({"error": "No eres admin"}), 403
    data = request.json
    if actualizar_usuario_db(username, data):
        return jsonify({"msg":"Usuario modificado"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@admin_bp.route('/users/<username>', methods=['DELETE'])
@jwt_required()
def ban_user(username):
    if not admin_required(): return jsonify({"error": "No eres admin"}), 403
    if borrar_usuario_db(username):
        return jsonify({"msg":"Usuario baneado"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404