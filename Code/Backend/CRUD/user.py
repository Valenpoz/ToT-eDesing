from db import get_connection

def create_user(nombre, correo, contrasena, rol_id):
    try:
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, rol_id, fecha_creacion) VALUES (%s, %s, %s, %s, NOW())",
                (nombre, correo, contrasena, rol_id)
            )
            connection.commit()
        connection.close()
        return True
    except Exception as e:
        print("Error al crear usuario:", e)
        return False

def get_user_by_email(correo):
    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE correo = %s"
        cursor.execute(query, (correo,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error en get_user_by_email: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def login_user(correo, contrasena):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s", (correo, contrasena))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
