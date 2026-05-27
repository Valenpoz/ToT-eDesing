from abc import ABC, abstractmethod


class EstrategiaPago(ABC):
    """Interfaz común para todas las estrategias de pago."""

    @abstractmethod
    def procesar(self, pedido_id: int, monto: float, detalles: dict) -> dict:
        """
        Procesa el pago para un pedido dado.

        Args:
            pedido_id: Identificador del pedido a cobrar.
            monto: Monto total a cobrar.
            detalles: Datos adicionales específicos de cada estrategia.

        Returns:
            dict con 'success' (bool) y 'message' (str).
        """
        pass

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Nombre identificador de la estrategia."""
        pass


# ─────────────────────────────────────────
#  Estrategias Concretas
# ─────────────────────────────────────────

class PagoTarjetaStrategy(EstrategiaPago):
    """Pago mediante tarjeta de crédito/débito (integración con Stripe o similar)."""

    @property
    def nombre(self) -> str:
        return "tarjeta"

    def procesar(self, pedido_id: int, monto: float, detalles: dict) -> dict:
        token = detalles.get("token_tarjeta")
        if not token:
            raise ValueError("Se requiere un token_tarjeta para procesar el pago con tarjeta.")

        # Aquí iría la integración real con la pasarela (ej. Stripe)
        print(f"[Tarjeta] Cobrando ${monto:.2f} al pedido #{pedido_id} con token '{token}'.")
        return {
            "success": True,
            "message": f"Pago con tarjeta de ${monto:.2f} procesado exitosamente.",
            "estrategia": self.nombre
        }


class PagoPayPalStrategy(EstrategiaPago):
    """Pago mediante cuenta de PayPal."""

    @property
    def nombre(self) -> str:
        return "paypal"

    def procesar(self, pedido_id: int, monto: float, detalles: dict) -> dict:
        correo = detalles.get("correo_paypal")
        if not correo:
            raise ValueError("Se requiere un correo_paypal para procesar el pago con PayPal.")

        print(f"[PayPal] Cobrando ${monto:.2f} al pedido #{pedido_id} vía cuenta '{correo}'.")
        return {
            "success": True,
            "message": f"Pago con PayPal de ${monto:.2f} autorizado exitosamente.",
            "estrategia": self.nombre
        }


class PagoEfectivoStrategy(EstrategiaPago):
    """Pago en efectivo contra entrega."""

    @property
    def nombre(self) -> str:
        return "efectivo"

    def procesar(self, pedido_id: int, monto: float, detalles: dict) -> dict:
        print(f"[Efectivo] Pedido #{pedido_id} registrado para cobro en efectivo de ${monto:.2f}.")
        return {
            "success": True,
            "message": f"Pedido #{pedido_id} pendiente de cobro en efectivo por ${monto:.2f}.",
            "estrategia": self.nombre
        }


# ─────────────────────────────────────────
#  Contexto del Procesador de Pagos
# ─────────────────────────────────────────

# Mapa público para seleccionar estrategia desde un string
ESTRATEGIAS_DISPONIBLES: dict[str, EstrategiaPago] = {
    "tarjeta": PagoTarjetaStrategy(),
    "paypal":  PagoPayPalStrategy(),
    "efectivo": PagoEfectivoStrategy(),
}


class ProcesadorPago:
    """
    Clase contexto del patrón Strategy.
    Recibe la estrategia en tiempo de ejecución y delega el procesamiento.
    """

    def __init__(self, estrategia: EstrategiaPago):
        self._estrategia = estrategia

    def set_estrategia(self, estrategia: EstrategiaPago):
        self._estrategia = estrategia

    def ejecutar(self, pedido_id: int, monto: float, detalles: dict) -> dict:
        return self._estrategia.procesar(pedido_id, monto, detalles)
