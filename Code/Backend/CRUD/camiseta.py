from db import get_connection

def get_all_camisetas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM camisetas")
        return cursor.fetchall()
    except Exception as e:
        print("Error al obtener camisetas:", e)
        return []
    finally:
        cursor.close()
        conn.close()

def create_camiseta(talla, color, material, precio, stock):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO camisetas (talla, color, material, precio, stock) VALUES (%s, %s, %s, %s, %s)",
                (talla, color, material, precio, stock)
            )
            conn.commit()
            return True
    except Exception as e:
        print("Error al crear camiseta:", e)
        return False
    finally:
        conn.close()
