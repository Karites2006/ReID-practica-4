import requests

BASE_URL = "http://127.0.0.1:5000"
TOKEN = None

def registrar(user, pwd):
    url = f"{BASE_URL}/auth/register"
    resp = requests.post(url, json={"username": user, "password": pwd})
    print(f"Registro {user}:", resp.json())

def login(user, pwd):
    global TOKEN
    url = f"{BASE_URL}/auth/login"
    resp = requests.post(url, json={"username": user, "password": pwd})
    if resp.status_code == 200:
        TOKEN = resp.json().get('access_token')
        print(f"Login {user}: Éxito (Token recibido)")
    else:
        print(f"Login {user}: Error", resp.json())

def enviar_mensaje(frase):
    if not TOKEN:
        print("No hay token, inicia sesión primero.")
        return
    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{BASE_URL}/texts/send"
    resp = requests.post(url, json={"sentence": frase}, headers=headers)
    print("Enviar mensaje:", resp.json())

def ver_mensajes():
    url = f"{BASE_URL}/texts/messages"
    resp = requests.get(url)
    print("Mensajes:", resp.json())

def registrar_admin(user, pwd):
    url = f"{BASE_URL}/admin/register"
    resp = requests.post(url, json={"username": user, "password": pwd})
    print(f"Registro Admin {user}:", resp.json())

if __name__ == "__main__":
    print("--- TEST USUARIO NORMAL ---")
    registrar("usuario1", "pass1")
    login("usuario1", "pass1")
    enviar_mensaje("Hola mundo desde Blueprints")
    ver_mensajes()
    
    print("\n--- TEST ADMIN ---")
    registrar_admin("admin1", "adminpass")
