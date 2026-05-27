from abc import ABC, abstractmethod

class IPedidoService(ABC):
    """
    Interfaz común (Subject) para el patrón Proxy de Seguridad.
    Garantiza que tanto el servicio real como el proxy tengan el mismo contrato.
    """

    @abstractmethod
    def cambiar_estado_pedido_accion(self, pedido_id: int, accion: str, usuario_rol: str) -> dict:
        pass

    @abstractmethod
    def pagar_pedido(self, pedido_id: int, tipo_pago: str, detalles: dict, usuario_rol: str) -> dict:
        pass

    @abstractmethod
    def despachar_pedido(self, pedido_id: int, usuario_rol: str) -> dict:
        pass

    @abstractmethod
    def entregar_pedido(self, pedido_id: int, usuario_rol: str) -> dict:
        pass

    @abstractmethod
    def cancelar_pedido(self, pedido_id: int, usuario_rol: str) -> dict:
        pass
