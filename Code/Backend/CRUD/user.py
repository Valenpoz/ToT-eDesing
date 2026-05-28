from db import get_connection

class user:
    pass


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
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return user_data


def create_user(nombre, correo, contrasena, rol_id):
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        nombre: Nombre del usuario
        correo: Correo electrónico (único)
        contrasena: Contraseña del usuario
        rol_id: ID del rol (0=Admin, 1=Diseñador, 2=Cliente)
    
    Returns:
        True si se creó correctamente, False en caso de error
    """
    try:
        conn = get_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return False
        
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena, rol_id, fecha_creacion) VALUES (%s, %s, %s, %s, NOW())",
            (nombre, correo, contrasena, rol_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False

