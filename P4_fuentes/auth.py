from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from users_db import crear_usuario_db, obtener_usuario_por_username
from db import crear_historial_db
from schemas import UserRegisterSchema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    # Validar entrada
    try:
        UserRegisterSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    username = data.get("nombre")
    password = data.get("password")
    user_id = data.get("id")
    id_pais = data.get("id_pais")
    id_historial = data.get("id_historial")

    if obtener_usuario_por_username(username):
        return jsonify({"error": "Usuario ya existe"}), 400

    hashed_pw = generate_password_hash(password)
    
    # P4: Crear usuario
    creado = crear_usuario_db(username, hashed_pw, user_id, id_pais, id_historial)
    
    if creado:
        # P3/P4: Crear historial asociado automáticamente
        crear_historial_db(id_historial, user_id)
        return jsonify({"message": "Usuario registrado y historial creado"}), 201
    else:
        return jsonify({"error": "Error al crear usuario"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("nombre") # Según tu schema usas "nombre" como login
    password = data.get("password")
    
    user_data = obtener_usuario_por_username(username)
    
    if not user_data or not check_password_hash(user_data['password'], password):
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    # Creamos token con identidad y claims extra (admin, id, pais)
    access_token = create_access_token(identity=username, additional_claims={
        "is_admin": user_data['es_admin'],
        "user_id": user_data['id'],
        "id_pais": user_data['id_pais']
    })
    return jsonify({"access_token": access_token}), 200