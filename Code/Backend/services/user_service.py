import hashlib
from CRUD import user
from datetime import datetime, timedelta

intentos_fallidos = {}

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(nombre, correo, contrasena, rol_id):
    success = user.create_user(nombre, correo, contrasena, rol_id)
    if success:
        return {"message": "Usuario registrado correctamente", "success": True}
    else:
        return {"message": "Error al registrar usuario", "success": False}


def login_user(correo, contrasena):

    ahora = datetime.now()

    # Si está bloqueado
    if correo in intentos_fallidos:
        info = intentos_fallidos[correo]
        if info.get("bloqueado_hasta", datetime.min) > ahora:
            return {
                "message": "Usuario bloqueado por intentos fallidos. Intenta en unos minutos.",
                "success": False
            }

    # Intentar login con el CRUD
    user_data = user.login_user(correo, contrasena)

    if user_data:
        # Si es correcto, eliminar errores pasados
        intentos_fallidos.pop(correo, None)
        return {
            "message": "Login exitoso",
            "user": {
                "id": user_data["id"], 
                "nombre": user_data["nombre"]
            },
            "success": True
        }
    else:
        # Falló el login, registrar intento
        if correo not in intentos_fallidos:
            intentos_fallidos[correo] = {"intentos": 1, "bloqueado_hasta": datetime.min}
        else:
            intentos_fallidos[correo]["intentos"] += 1

        # Si llegó a 3 intentos, bloquear 10 minutos
        if intentos_fallidos[correo]["intentos"] >= 3:
            intentos_fallidos[correo]["bloqueado_hasta"] = ahora + timedelta(minutes=10)
            return {
                "message": "Demasiados intentos. Usuario bloqueado por 10 minutos.",
                "success": False
            }

        return {
            "message": "Correo o contraseña incorrectos.",
            "success": False
        }
