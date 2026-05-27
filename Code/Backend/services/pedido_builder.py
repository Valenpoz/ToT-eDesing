from datetime import datetime

class Pedido:
    """Clase que representa un pedido listo para guardarse en la base de datos."""
    def __init__(self):
        self.usuario_id = None
        self.total = 0.0
        self.metodo_pago_id = None
        self.estado = "pendiente"
        self.fecha = None
        self.items = []

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "total": self.total,
            "metodo_pago_id": self.metodo_pago_id,
            "estado": self.estado,
            "fecha": self.fecha,
            "items": self.items
        }


class PedidoBuilder:
    """Builder para construir un Pedido de forma fluida y validar sus campos requeridos."""
    def __init__(self):
        self.reset()

    def reset(self):
        self._pedido = Pedido()
        return self

    def para_usuario(self, usuario_id):
        self._pedido.usuario_id = usuario_id
        return self

    def con_metodo_pago(self, metodo_pago_id):
        self._pedido.metodo_pago_id = metodo_pago_id
        return self

    def con_estado(self, estado):
        if estado:
            self._pedido.estado = estado
        return self

    def con_fecha(self, fecha):
        if not fecha:
            return self
        if isinstance(fecha, datetime):
            self._pedido.fecha = fecha.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self._pedido.fecha = str(fecha)
        return self

    def con_total(self, total):
        if total is not None:
            self._pedido.total = float(total)
        return self

    def agregar_item(self, camiseta_personalizada_id, cantidad, subtotal):
        self._pedido.items.append({
            "camiseta_personalizada_id": int(camiseta_personalizada_id),
            "cantidad": int(cantidad),
            "subtotal": float(subtotal)
        })
        return self

    def build(self):
        """Valida las reglas de negocio y construye el pedido final."""
        if self._pedido.usuario_id is None:
            raise ValueError("El pedido requiere un usuario_id válido.")
        if self._pedido.metodo_pago_id is None:
            raise ValueError("El pedido requiere un metodo_pago_id válido.")
        
        # Generar fecha por defecto si no fue asignada
        if not self._pedido.fecha:
            self._pedido.fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        # Calcular total acumulado de ítems si no se configuró un total manual
        if self._pedido.items and self._pedido.total == 0.0:
            self._pedido.total = sum(item["subtotal"] for item in self._pedido.items)

        return self._pedido
