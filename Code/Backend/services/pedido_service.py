from services.pedido_service_proxy import PedidoServiceProxy
from CRUD import pedido as pedido_db

# Instanciamos el Proxy en lugar del servicio real.
# Esto mantiene la retrocompatibilidad: cualquier módulo que importe services.pedido_service
# obtendrá la instancia del Proxy transparente que intercepta y protege las acciones.
_proxy = PedidoServiceProxy()

def registrar_pedido(usuario_id, metodo_pago_id, items):
    return _proxy.registrar_pedido(usuario_id, metodo_pago_id, items)

def obtener_pedidos_de_usuario(usuario_id):
    return _proxy.obtener_pedidos_de_usuario(usuario_id)

def obtener_detalles_de_pedido(pedido_id):
    return _proxy.obtener_detalles_de_pedido(pedido_id)

def crear_nuevo_pedido(data):
    return _proxy.crear_nuevo_pedido(data)

def obtener_pedidos_usuario(usuario_id):
    return _proxy.obtener_pedidos_usuario(usuario_id)

def cambiar_estado_pedido_accion(pedido_id, accion, usuario_rol="cliente"):
    return _proxy.cambiar_estado_pedido_accion(pedido_id, accion, usuario_rol)

def pagar_pedido(pedido_id, tipo_pago="efectivo", detalles=None, usuario_rol="cliente"):
    return _proxy.pagar_pedido(pedido_id, tipo_pago, detalles, usuario_rol)

def despachar_pedido(pedido_id, usuario_rol="cliente"):
    return _proxy.despachar_pedido(pedido_id, usuario_rol)

def entregar_pedido(pedido_id, usuario_rol="cliente"):
    return _proxy.entregar_pedido(pedido_id, usuario_rol)

def cancelar_pedido(pedido_id, usuario_rol="cliente"):
    return _proxy.cancelar_pedido(pedido_id, usuario_rol)