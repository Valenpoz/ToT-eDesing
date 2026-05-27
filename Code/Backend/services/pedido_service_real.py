from services.pedido_interface import IPedidoService
from services.db_proxy import MockablePedidoDbProxy
from services.pedido_builder import PedidoBuilder

pedido_db = MockablePedidoDbProxy()
from services.pedido_state import PedidoStateContext
from services.pago_strategy import ProcesadorPago, ESTRATEGIAS_DISPONIBLES
from datetime import datetime

class PedidoServiceReal(IPedidoService):
    """
    Clase que contiene la implementación real (RealSubject) de las operaciones
    de negocio de los pedidos. Implementa IPedidoService.
    """

    def registrar_pedido(self, usuario_id, metodo_pago_id, items):
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

    def obtener_pedidos_de_usuario(self, usuario_id):
        return pedido_db.obtener_pedidos_por_usuario(usuario_id)

    def obtener_detalles_de_pedido(self, pedido_id):
        return pedido_db.obtener_detalles_pedido(pedido_id)

    def crear_nuevo_pedido(self, data):
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

    def obtener_pedidos_usuario(self, usuario_id):
        pedidos = pedido_db.obtener_pedidos_por_usuario(usuario_id)
        return {"pedidos": pedidos, "success": True}

    def cambiar_estado_pedido_accion(self, pedido_id: int, accion: str, usuario_rol: str = "cliente") -> dict:
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

    def pagar_pedido(self, pedido_id: int, tipo_pago: str = "efectivo", detalles: dict = None, usuario_rol: str = "cliente") -> dict:
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
        resultado_estado = self.cambiar_estado_pedido_accion(pedido_id, "pagar", usuario_rol)
        resultado_estado["pago"] = resultado_pago
        return resultado_estado

    def despachar_pedido(self, pedido_id: int, usuario_rol: str = "cliente") -> dict:
        return self.cambiar_estado_pedido_accion(pedido_id, "despachar", usuario_rol)

    def entregar_pedido(self, pedido_id: int, usuario_rol: str = "cliente") -> dict:
        return self.cambiar_estado_pedido_accion(pedido_id, "entregar", usuario_rol)

    def cancelar_pedido(self, pedido_id: int, usuario_rol: str = "cliente") -> dict:
        return self.cambiar_estado_pedido_accion(pedido_id, "cancelar", usuario_rol)
