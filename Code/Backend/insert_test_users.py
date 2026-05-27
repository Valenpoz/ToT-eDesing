import db

def insert_data():
    conn = db.get_connection()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return
    
    cursor = conn.cursor(dictionary=True)
    
    # 1. Insertar usuarios de prueba si no existen
    users = [
        {"nombre": "Cliente Test", "correo": "cliente@test.com", "contrasena": "password1", "rol_id": 1},
        {"nombre": "Artista Test", "correo": "artista@test.com", "contrasena": "password1", "rol_id": 2},
        {"nombre": "Admin Test", "correo": "admin@test.com", "contrasena": "password1", "rol_id": 3}
    ]
    
    for u in users:
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (u["correo"],))
        res = cursor.fetchone()
        if not res:
            cursor.execute(
                "INSERT INTO usuarios (nombre, correo, contrasena, rol_id) VALUES (%s, %s, %s, %s)",
                (u["nombre"], u["correo"], u["contrasena"], u["rol_id"])
            )
            print(f"Usuario {u['correo']} insertado.")
            
            # Si es artista, insertar también en tabla de artistas
            if u["rol_id"] == 2:
                cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (u["correo"],))
                art_user = cursor.fetchone()
                cursor.execute(
                    "INSERT INTO artistas (usuario_id, biografia) VALUES (%s, %s)",
                    (art_user["id"], "Biografía de artista de prueba.")
                )
                print("Artista asociado en la tabla 'artistas'.")
        else:
            print(f"Usuario {u['correo']} ya existe.")
            
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    insert_data()
