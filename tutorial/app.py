from flask import Flask
from flask_jwt_extended import JWTManager
# Importamos los Blueprints
from auth import auth_bp
from texts import texts_bp
from admin import admin_bp

app = Flask(__name__)

# Configuración JWT (Variables de entorno son mejores, pero hardcodeado para ejemplo)
app.config['JWT_SECRET_KEY'] = 'super-secret-key' 
jwt = JWTManager(app)

# Registro de Blueprints con sus prefijos (URL Tree Slide 67)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(texts_bp, url_prefix='/texts')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return "API REST con Blueprints funcionando"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
