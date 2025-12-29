import requests

BASE_URL = "http://127.0.0.1:5000"


# AUTENTICACIÓN DE USUARIO

def registrar_usuario(nombre, password, user_id, id_pais, id_historial):
    url = f"{BASE_URL}/auth/register"
    payload = {
        "nombre": nombre, "password": password,
        "id": user_id, "id_pais": id_pais, "id_historial": id_historial
    }
    requests.post(url, json=payload)
    print(f" Usuario {nombre} registrado correctamente")

def login_usuario(nombre, password):
    url = f"{BASE_URL}/auth/login"
    resp = requests.post(url, json={"nombre": nombre, "password": password})
    if resp.status_code == 200:
        print(f"Login correcto: {nombre}")
        return resp.json().get('access_token')
    else:
        print(f"Login fallido: {resp.json()}")
        return None


# OPERACIONES DE USUARIO

def op_editar_cuenta(token, nuevos_datos):
    url = f"{BASE_URL}/api/usuarios/me"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.put(url, json=nuevos_datos, headers=headers)
    print("Respuesta:", resp.json())

def op_borrar_cuenta(token):
    url = f"{BASE_URL}/api/usuarios/me"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(url, headers=headers)
    print("Respuesta:", resp.json())

def op_pagar_suscripcion(token):
    url = f"{BASE_URL}/api/usuarios/subscription"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.put(url, headers=headers)
    print("Respuesta:", resp.json())

def op_cancelar_suscripcion(token):
    url = f"{BASE_URL}/api/usuarios/subscription"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(url, headers=headers)
    print("Respuesta:", resp.json())

def op_reproducir_video(token, vid_id):
    url = f"{BASE_URL}/api/videos/{vid_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(f"Viendo: '{resp.json().get('titulo')}'")
    else:
        print(f"Error: {resp.json()}")

def op_listar_videos_pais(token):
    url = f"{BASE_URL}/api/videos"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    print("Videos disponibles en tu país:")
    for video in resp.json():
        print(f"- {video.get('titulo')} (Paises: {video.get('id_paises')})")

def op_listar_videos_fecha(token, fecha):
    url = f"{BASE_URL}/api/videos?fecha_inicio={fecha}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    print(f" Videos posteriores a {fecha}:")
    for v in resp.json():
        print(f"- {v.get('titulo')} (Fecha: {v.get('fecha')})")

def op_consultar_historial(token):
    url = f"{BASE_URL}/api/usuarios/me/historial"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    print(" Historial:", resp.json())


# OPERACIONES DE ADMIN

def admin_añadir_video(token, id_vid, titulo, fecha, paises):
    url = f"{BASE_URL}/admin/videos"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"id": id_vid, "titulo": titulo, "fecha": fecha, "id_paises": paises}
    resp = requests.post(url, json=payload, headers=headers)
    print(" Admin añadido:", resp.json())

def admin_borrar_video(token, id_vid):
    url = f"{BASE_URL}/admin/videos/{id_vid}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(url, headers=headers)
    print(" Admin eliminado:", resp.json())

def admin_listar_todos(token):
    url = f"{BASE_URL}/admin/videos/all"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    print(f"Todos los videos disponibles:")
    for v in resp.json():
        print(f"- {v.get('titulo')}")

def admin_editar_video(token, id_vid, nuevos_datos):
    url = f"{BASE_URL}/admin/videos/{id_vid}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.put(url, json=nuevos_datos, headers=headers)
    print(" Admin edita video:", resp.json())

def admin_listar_usuarios(token):
    url = f"{BASE_URL}/admin/users"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers)
    print(" Admin lista usuarios:")
    for u in list(resp.json().keys()):
        print(f"- {u}")

def admin_editar_usuario(token, target_user, nuevos_datos):
    url = f"{BASE_URL}/admin/users/{target_user}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.put(url, json=nuevos_datos, headers=headers)
    print(" Admin edita usuario:", resp.json())

def admin_ban_usuario(token, target_user):
    url = f"{BASE_URL}/admin/users/{target_user}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(url, headers=headers)
    print(" Admin banea usuario:", resp.json())



# EJECUCIÓN DE PRUEBA

if __name__ == "__main__":
    
    
    # 1. Registrar
    print("\nRegistrar cuenta de usuario")
    registrar_usuario("Carol", "contrasenia_segura", 88888, 1, 77777)
    print("\n")

    # Login usuario
    token_user = login_usuario("Carol", "contrasenia_segura")
    
    if token_user:
        # 2. Editar cuenta
        print("\nEditar cuenta de usuario")
        op_editar_cuenta(token_user, {"password": "contrasenia_nueva"})

        # 3. Pagar suscripción
        print("\nPagar suscripción")
        op_pagar_suscripcion(token_user)

        # 4. Cancelar suscripción
        print("\nCancelar suscripción")
        op_cancelar_suscripcion(token_user)

        # 5. Reproducir un video
        print("\nReproducir un video")
        op_reproducir_video(token_user, 103)

        # 6. Listar videos disponibles en su país
        print("\nLista de videos disponibles en su país")
        op_listar_videos_pais(token_user)

        # 7. Listar videos filtrados por fecha
        print("\nLista de videos filtrada por fecha")
        op_listar_videos_fecha(token_user, "01/01/2022")

        # 8. Consultar historial
        print("\nConsultar historial de reproducción")
        op_consultar_historial(token_user)

        # 9. Borrar cuenta
        print("\nBorrar cuenta de usuario")
        op_borrar_cuenta(token_user)
        
        # 10. Volver a registrar
        print("\nRegistrar cuenta de usuario de nuevo")
        registrar_usuario("Carol", "contrasenia_segura", 88888, 1, 77777)


    print("\nOperaciones de Administrador")
    
    # Login Admin
    token_admin = login_usuario("Karites06", "pass_segura")

    if token_admin:
        # 11. Añadir video
        print("\nAñadir un nuevo video")
        admin_añadir_video(token_admin, 106, "Nuremberg", "25/06/2025", [1, 4, 6, 9])

        # 12. Borrar videoo
        print("\nBorrar un video")
        admin_borrar_video(token_admin, 106)

        # 13. Obtener lista de todos los videos
        print("\nObtener lista de todos los videos")
        admin_listar_todos(token_admin)

        # 14. Editar video
        print("\nEditar un video")
        admin_editar_video(token_admin, 101, {"id_paises": [1, 2, 3, 5, 7, 10]})

        # 15. Listar usuarios
        print("\nLista de usuarios registrados")
        admin_listar_usuarios(token_admin)

        # 16. Editar usuario
        print("\nEditar atributos de un usuario")
        admin_editar_usuario(token_admin, "Carol", {"esta_suscrito": True})
        # 17. Banear usuario
        print("\nBanear un usuario")
        admin_ban_usuario(token_admin, "Carol")