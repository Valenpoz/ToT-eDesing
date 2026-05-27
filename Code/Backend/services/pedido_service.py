from CRUD import pedido as pedido_db
from services.pedido_builder import PedidoBuilder
from services.pedido_state import PedidoStateContext
from services.pago_strategy import ProcesadorPago, ESTRATEGIAS_DISPONIBLES
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

def cambiar_estado_pedido_accion(pedido_id, accion):
    pedido = pedido_db.obtener_pedido_por_id(pedido_id)
    if not pedido:
        return {"message": "Pedido no encontrado", "success": False}

    contexto = PedidoStateContext(pedido_id, pedido["estado"])
    try:
        if accion == "pagar":
            contexto.pagar()
        elif accion == "despachar":
            contexto.despachar()
        elif accion == "entregar":
            contexto.entregar()
        elif accion == "cancelar":
            contexto.cancelar()
        else:
            return {"message": f"Acción inválida: {accion}", "success": False}

        return {
            "message": f"Pedido actualizado con éxito a estado: {contexto.get_estado_nombre()}",
            "success": True,
            "nuevo_estado": contexto.get_estado_nombre()
        }
    except ValueError as e:
        return {"message": str(e), "success": False}

def pagar_pedido(pedido_id, tipo_pago="efectivo", detalles=None):
    """
    Procesa el pago de un pedido utilizando la estrategia seleccionada (Strategy)
    y, si tiene éxito, realiza la transición de estado (State).

    Args:
        pedido_id: ID del pedido a pagar.
        tipo_pago: 'tarjeta', 'paypal' o 'efectivo' (por defecto).
        detalles: Datos extra requeridos por la estrategia (token, correo, etc.).
    """
    if detalles is None:
        detalles = {}

    # Seleccionar la estrategia de pago correcta
    estrategia = ESTRATEGIAS_DISPONIBLES.get(tipo_pago)
    if not estrategia:
        return {
            "message": f"Método de pago '{tipo_pago}' no soportado. Use: {list(ESTRATEGIAS_DISPONIBLES.keys())}",
            "success": False
        }

    # Obtener el pedido para conocer el monto
    pedido = pedido_db.obtener_pedido_por_id(pedido_id)
    if not pedido:
        return {"message": "Pedido no encontrado", "success": False}

    monto = float(pedido.get("total", 0))

    # Ejecutar la estrategia de pago
    try:
        procesador = ProcesadorPago(estrategia)
        resultado_pago = procesador.ejecutar(pedido_id, monto, detalles)
    except ValueError as e:
        return {"message": str(e), "success": False}

    if not resultado_pago.get("success"):
        return resultado_pago

    # Si el pago fue exitoso → transicionar el estado del pedido (State)
    resultado_estado = cambiar_estado_pedido_accion(pedido_id, "pagar")
    resultado_estado["pago"] = resultado_pago
    return resultado_estado

def despachar_pedido(pedido_id):
    return cambiar_estado_pedido_accion(pedido_id, "despachar")

def entregar_pedido(pedido_id):
    return cambiar_estado_pedido_accion(pedido_id, "entregar")

def cancelar_pedido(pedido_id):
    return cambiar_estado_pedido_accion(pedido_id, "cancelar")