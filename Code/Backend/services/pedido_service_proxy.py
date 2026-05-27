from services.pedido_interface import IPedidoService
from services.pedido_service_real import PedidoServiceReal

class PedidoServiceProxy(IPedidoService):
    """
    Clase Proxy (Proxy) para el control de acceso y seguridad sobre el PedidoServiceReal.
    Controla el acceso según el rol del usuario ('admin', 'cliente', 'artista', etc.)
    antes de delegar la llamada al servicio real.
    """

    def __init__(self):
        # Inicialización perezosa (Lazy loading): no instanciamos el RealSubject
        # hasta que realmente se requiera realizar una operación autorizada.
        self._real_service = None

    def _get_real_service(self) -> PedidoServiceReal:
        if self._real_service is None:
            self._real_service = PedidoServiceReal()
        return self._real_service

    def cambiar_estado_pedido_accion(self, pedido_id: int, accion: str, usuario_rol: str = "cliente") -> dict:
        # Lógica de Seguridad (Control de Acceso)
        # Solo 'admin' puede despachar o entregar pedidos
        acciones_administrativas = ["despachar", "entregar"]
        
        if accion in acciones_administrativas and usuario_rol != "admin":
            return {
                "message": f"Acceso Denegado: El rol '{usuario_rol}' no tiene permisos para realizar la acción '{accion}'",
                "success": False
            }

        # Clientes, Artistas y Admins pueden cancelar o pagar (siempre y cuando pasen las reglas de negocio)
        return self._get_real_service().cambiar_estado_pedido_accion(pedido_id, accion, usuario_rol)

    def pagar_pedido(self, pedido_id: int, tipo_pago: str = "efectivo", detalles: dict = None, usuario_rol: str = "cliente") -> dict:
        # Los clientes y administradores pueden pagar pedidos. Los artistas no deberían pagar pedidos ajenos.
        if usuario_rol not in ["cliente", "admin"]:
            return {
                "message": f"Acceso Denegado: El rol '{usuario_rol}' no está autorizado para realizar pagos.",
                "success": False
            }
        
        return self._get_real_service().pagar_pedido(pedido_id, tipo_pago, detalles, usuario_rol)

    def despachar_pedido(self, pedido_id: int, usuario_rol: str = "cliente") -> dict:
        if usuario_rol != "admin":
            return {
                "message": f"Acceso Denegado: El rol '{usuario_rol}' no tiene permisos para despachar pedidos.",
                "success": False
            }
        return self._get_real_service().despachar_pedido(pedido_id, usuario_rol)

    def entregar_pedido(self, pedido_id: int, usuario_rol: str = "cliente") -> dict:
        if usuario_rol != "admin":
            return {
                "message": f"Acceso Denegado: El rol '{usuario_rol}' no tiene permisos para entregar pedidos.",
                "success": False
            }
        return self._get_real_service().entregar_pedido(pedido_id, usuario_rol)

    def cancelar_pedido(self, pedido_id: int, usuario_rol: str = "cliente") -> dict:
        # Cualquiera (cliente o admin) puede solicitar una cancelación, pero un artista no.
        if usuario_rol not in ["cliente", "admin"]:
            return {
                "message": f"Acceso Denegado: El rol '{usuario_rol}' no puede cancelar este pedido.",
                "success": False
            }
        return self._get_real_service().cancelar_pedido(pedido_id, usuario_rol)

    # Delegación transparente de métodos auxiliares/de consulta
    def registrar_pedido(self, usuario_id, metodo_pago_id, items):
        return self._get_real_service().registrar_pedido(usuario_id, metodo_pago_id, items)

    def obtener_pedidos_de_usuario(self, usuario_id):
        return self._get_real_service().obtener_pedidos_de_usuario(usuario_id)

    def obtener_detalles_de_pedido(self, pedido_id):
        return self._get_real_service().obtener_detalles_de_pedido(pedido_id)

    def crear_nuevo_pedido(self, data):
        return self._get_real_service().crear_nuevo_pedido(data)

    def obtener_pedidos_usuario(self, usuario_id):
        return self._get_real_service().obtener_pedidos_usuario(usuario_id)
