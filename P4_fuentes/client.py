import requests

BASE_URL = "http://127.0.0.1:5000"
TOKEN = None
ADMIN_TOKEN = None

def registrar_usuario():
    url = f"{BASE_URL}/auth/register"
    # Datos según UserRegisterSchema y usuario.json
    payload = {
        "nombre": "Karites06",
        "password": "pass_segura",
        "id": "156749",
        "id_pais": "01",
        "id_historial": "145689"
    }
    resp = requests.post(url, json=payload)
    print("Registro:", resp.json())

def login_usuario():
    global TOKEN
    url = f"{BASE_URL}/auth/login"
    resp = requests.post(url, json={"nombre": "Karites06", "password": "pass_segura"})
    if resp.status_code == 200:
        TOKEN = resp.json().get('access_token')
        print("Login Usuario: Éxito")
    else:
        print("Login Usuario: Error", resp.json())

def pagar_suscripcion():
    url = f"{BASE_URL}/api/usuarios/Karites06/subscription"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    resp = requests.put(url, headers=headers)
    print("Pagar Suscripción:", resp.json())

def agregar_video_admin(token_admin):
    url = f"{BASE_URL}/admin/videos"
    headers = {"Authorization": f"Bearer {token_admin}"}
    # Payload según VideoSchema
    payload = {
        "id": 15674906,
        "titulo": "Avengers",
        "fecha": "14/11/2026",
        "id_paises": [1, 2, 3] # Incluye país 1 (del usuario)
    }
    resp = requests.post(url, json=payload, headers=headers)
    print("Admin Agregar Video:", resp.json())

def listar_videos_usuario():
    url = f"{BASE_URL}/api/videos"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    resp = requests.get(url, headers=headers)
    print("Listar Videos (Usuario):", resp.json())

# --- FLUJO DE PRUEBA ---
if __name__ == "__main__":
    # 1. Registrar usuario normal
    registrar_usuario()
    
    # 2. Login
    login_usuario()
    
    # 3. Pagar suscripción
    pagar_suscripcion()
    
    # 4. Crear un admin temporal (truco: regístralo manualmente en código o base de datos con es_admin=True para probar esto)
    # Por ahora, intentaremos listar videos con el usuario normal (estará vacío hasta que se agreguen)
    listar_videos_usuario()
    
    print("\nNota: Para probar funciones de ADMIN, necesitas registrar un usuario y cambiar manualmente 'es_admin': true en users.json, luego loguearte con él.")