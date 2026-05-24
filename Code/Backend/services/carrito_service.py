from CRUD import carrito as carrito_db
from datetime import datetime
from db import get_connection

def crear_carrito_si_no_existe(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Verificar si ya hay un carrito para el usuario
        cursor.execute("SELECT id FROM carrito WHERE usuario_id = %s", (usuario_id,))
        existente = cursor.fetchone()

        if existente:
            print(f"Ya existe carrito para usuario {usuario_id} con id {existente[0]}")
            return {"message": "El carrito ya existe", "success": True, "carrito_id": existente[0]}

        # Insertar nuevo carrito
        cursor.execute("INSERT INTO carrito (usuario_id) VALUES (%s)", (usuario_id,))
        conn.commit()  # ¡IMPORTANTE!
        nuevo_id = cursor.lastrowid

        print(f"Carrito creado para usuario {usuario_id} con id {nuevo_id}")
        return {"message": "Carrito creado correctamente", "success": True, "carrito_id": nuevo_id}

    except Exception as e:
        print("Error al crear carrito:", str(e))
        return {"message": "Error al crear carrito", "success": False}

    finally:
        cursor.close()
        conn.close()

def crear_carrito_para_usuario(usuario_id):
    fecha = datetime.now()
    return carrito_db.crear_carrito(usuario_id, fecha)

def obtener_carrito_de_usuario(usuario_id):
    return carrito_db.obtener_carrito_por_usuario(usuario_id)

def obtener_items_de_carrito(carrito_id):
    return carrito_db.obtener_items_carrito(carrito_id)

def agregar_item(carrito_id, camiseta_personalizada_id, cantidad):
    return carrito_db.agregar_item_al_carrito(carrito_id, camiseta_personalizada_id, cantidad)

def eliminar_item(item_id):
    return carrito_db.eliminar_item_del_carrito(item_id)

def eliminar_carrito(carrito_id):
    return carrito_db.eliminar_carrito(carrito_id)

def crear_carrito_si_no_existe(usuario_id):
    carrito_existente = carrito_db.obtener_carrito_por_usuario(usuario_id)
    if carrito_existente:
        return {"message": "Ya tiene un carrito", "carrito": carrito_existente, "success": True}
    fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    carrito_db.crear_carrito(usuario_id, fecha_creacion)
    nuevo_carrito = carrito_db.obtener_carrito_por_usuario(usuario_id)
    return {"message": "Carrito creado", "carrito": nuevo_carrito, "success": True}
