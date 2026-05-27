from abc import ABC, abstractmethod
from CRUD import pedido as pedido_db

class EstadoPedido(ABC):
    """Interfaz abstracta para definir el comportamiento de cada estado del pedido."""
    @property
    @abstractmethod
    def nombre(self) -> str:
        pass

    @abstractmethod
    def pagar(self, contexto: 'PedidoStateContext'):
        pass

    @abstractmethod
    def despachar(self, contexto: 'PedidoStateContext'):
        pass

    @abstractmethod
    def entregar(self, contexto: 'PedidoStateContext'):
        pass

    @abstractmethod
    def cancelar(self, contexto: 'PedidoStateContext'):
        pass


class EstadoPendiente(EstadoPedido):
    @property
    def nombre(self) -> str:
        return "pendiente"

    def pagar(self, contexto: 'PedidoStateContext'):
        print(f"Pedido {contexto.pedido_id} pagado exitosamente.")
        contexto.set_state(EstadoPagado())

    def despachar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede despachar un pedido que está pendiente de pago.")

    def entregar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede entregar un pedido que está pendiente de pago.")

    def cancelar(self, contexto: 'PedidoStateContext'):
        print(f"Pedido {contexto.pedido_id} cancelado.")
        contexto.set_state(EstadoCancelado())


class EstadoPagado(EstadoPedido):
    @property
    def nombre(self) -> str:
        return "pagado"

    def pagar(self, contexto: 'PedidoStateContext'):
        raise ValueError("El pedido ya ha sido pagado.")

    def despachar(self, contexto: 'PedidoStateContext'):
        print(f"Pedido {contexto.pedido_id} despachado / enviado.")
        contexto.set_state(EstadoEnviado())

    def entregar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede entregar un pedido que no ha sido enviado.")

    def cancelar(self, contexto: 'PedidoStateContext'):
        print(f"Pedido {contexto.pedido_id} cancelado y reembolsado.")
        contexto.set_state(EstadoCancelado())


class EstadoEnviado(EstadoPedido):
    @property
    def nombre(self) -> str:
        return "enviado"

    def pagar(self, contexto: 'PedidoStateContext'):
        raise ValueError("El pedido ya está pagado e incluso enviado.")

    def despachar(self, contexto: 'PedidoStateContext'):
        raise ValueError("El pedido ya fue despachado.")

    def entregar(self, contexto: 'PedidoStateContext'):
        print(f"Pedido {contexto.pedido_id} entregado al cliente.")
        contexto.set_state(EstadoEntregado())

    def cancelar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede cancelar un pedido que ya está en ruta de envío.")


class EstadoEntregado(EstadoPedido):
    @property
    def nombre(self) -> str:
        return "entregado"

    def pagar(self, contexto: 'PedidoStateContext'):
        raise ValueError("El pedido ya fue entregado y pagado.")

    def despachar(self, contexto: 'PedidoStateContext'):
        raise ValueError("El pedido ya fue entregado.")

    def entregar(self, contexto: 'PedidoStateContext'):
        raise ValueError("El pedido ya está entregado.")

    def cancelar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede cancelar un pedido que ya fue entregado exitosamente.")


class EstadoCancelado(EstadoPedido):
    @property
    def nombre(self) -> str:
        return "cancelado"

    def pagar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede pagar un pedido cancelado.")

    def despachar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede despachar un pedido cancelado.")

    def entregar(self, contexto: 'PedidoStateContext'):
        raise ValueError("No se puede entregar un pedido cancelado.")

    def cancelar(self, contexto: 'PedidoStateContext'):
        raise ValueError("El pedido ya está cancelado.")


class PedidoStateContext:
    """Clase contexto que mantiene la instancia del estado actual y actualiza la base de datos."""
    def __init__(self, pedido_id: int, estado_actual_nombre: str):
        self.pedido_id = pedido_id
        self._estado = self._obtener_instancia_estado(estado_actual_nombre)

    def _obtener_instancia_estado(self, nombre_estado: str) -> EstadoPedido:
        estados = {
            "pendiente": EstadoPendiente(),
            "pagado": EstadoPagado(),
            "enviado": EstadoEnviado(),
            "entregado": EstadoEntregado(),
            "cancelado": EstadoCancelado()
        }
        # Fallback por defecto a EstadoPendiente si el estado en la base de datos es inválido o vacío
        return estados.get(nombre_estado.lower(), EstadoPendiente())

    def get_estado_nombre(self) -> str:
        return self._estado.nombre

    def set_state(self, nuevo_estado: EstadoPedido):
        self._estado = nuevo_estado
        # Persistir el cambio en la base de datos
        pedido_db.actualizar_estado_pedido(self.pedido_id, nuevo_estado.nombre)

    def pagar(self):
        self._estado.pagar(self)

    def despachar(self):
        self._estado.despachar(self)

    def entregar(self):
        self._estado.entregar(self)

    def cancelar(self):
        self._estado.cancelar(self)
