from db import get_connection

def get_all_estampas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM estampas")
        result = cursor.fetchall()
        return result
    except Exception as e:
        print("Error al obtener estampas:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def create_estampa(titulo, descripcion, artista_id, estado):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO estampas (titulo, descripcion, artista_id, estado) VALUES (%s, %s, %s, %s)",
                (titulo, descripcion, artista_id, estado)
            )
            conn.commit()
            return True
    except Exception as e:
        print("Error al crear estampa:", e)
        return False
    finally:
        conn.close()
