from flask import Flask
from flask_jwt_extended import JWTManager
from auth import auth_bp
from user_ops import user_ops_bp
from admin import admin_bp

app = Flask(__name__)

# Configuración JWT
app.config['JWT_SECRET_KEY'] = 'streaming-catalog-secret-key' 
jwt = JWTManager(app)

# Registro de Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_ops_bp, url_prefix='/api') # Prefijo general para usuario
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return "StreamingCatalog API REST Running"

if __name__ == '__main__':
    app.run(debug=True, port=5000)