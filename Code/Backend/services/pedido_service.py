from CRUD import pedido as pedido_db
from services.pedido_builder import PedidoBuilder
from datetime import datetime

def registrar_pedido(usuario_id, metodo_pago_id, items):
    """
    items: lista de diccionarios con keys:
    - camiseta_personalizada_id
    - cantidad
    - subtotal
    """
    builder = (PedidoBuilder()
               .para_usuario(usuario_id)
               .con_metodo_pago(metodo_pago_id)
               .con_estado("pendiente")
               .con_fecha(datetime.now()))

    for item in items:
        builder.agregar_item(
            camiseta_personalizada_id=item["camiseta_personalizada_id"],
            cantidad=item["cantidad"],
            subtotal=item["subtotal"]
        )

    pedido_objeto = builder.build()

    pedido_id = pedido_db.crear_pedido(
        pedido_objeto.usuario_id,
        pedido_objeto.total,
        pedido_objeto.metodo_pago_id,
        pedido_objeto.estado,
        pedido_objeto.fecha
    )

    for item in pedido_objeto.items:
        pedido_db.agregar_detalle_pedido(
            pedido_id,
            item["camiseta_personalizada_id"],
            item["cantidad"],
            item["subtotal"]
        )

    return pedido_id

def obtener_pedidos_de_usuario(usuario_id):
    return pedido_db.obtener_pedidos_por_usuario(usuario_id)

def obtener_detalles_de_pedido(pedido_id):
    return pedido_db.obtener_detalles_pedido(pedido_id)

def crear_nuevo_pedido(data):
    builder = (PedidoBuilder()
               .para_usuario(data["usuario_id"])
               .con_metodo_pago(data["metodo_pago_id"])
               .con_total(data.get("total"))
               .con_estado(data.get("estado", "pendiente"))
               .con_fecha(datetime.now()))

    pedido_objeto = builder.build()

    pedido_db.crear_pedido(
        pedido_objeto.usuario_id,
        pedido_objeto.total,
        pedido_objeto.metodo_pago_id,
        pedido_objeto.estado,
        pedido_objeto.fecha
    )
    return {"message": "Pedido creado exitosamente", "success": True}

def obtener_pedidos_usuario(usuario_id):
    pedidos = pedido_db.obtener_pedidos_por_usuario(usuario_id)
    return {"pedidos": pedidos, "success": True}