from db import get_connection

def crear_pedido(usuario_id, total, metodo_pago_id, estado, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pedidos (usuario_id, total, metodo_pago_id, estado, fecha)
        VALUES (%s, %s, %s, %s, %s)
    """, (usuario_id, total, metodo_pago_id, estado, fecha))
    conn.commit()
    conn.close()

def agregar_detalle_pedido(pedido_id, camiseta_personalizada_id, cantidad, subtotal):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO detalles_pedido (pedido_id, camiseta_personalizada_id, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
        (pedido_id, camiseta_personalizada_id, cantidad, subtotal)
    )
    conn.commit()
    cursor.close()
    conn.close()

def obtener_pedidos_por_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos WHERE usuario_id = %s", (usuario_id,))
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def obtener_detalles_pedido(pedido_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT dp.cantidad, dp.subtotal, c.talla, c.color, c.material, c.precio, e.titulo
        FROM detalles_pedido dp
        JOIN camisetas_personalizadas cp ON dp.camiseta_personalizada_id = cp.id
        JOIN camisetas c ON cp.camiseta_id = c.id
        JOIN estampas e ON cp.estampa_id = e.id
        WHERE dp.pedido_id = %s
        """,
        (pedido_id,)
    )
    detalles = cursor.fetchall()
    cursor.close()
    conn.close()
    return detalles
