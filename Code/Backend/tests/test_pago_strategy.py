import pytest
from unittest.mock import patch, MagicMock

from services.pago_strategy import (
    PagoTarjetaStrategy,
    PagoPayPalStrategy,
    PagoEfectivoStrategy,
    ProcesadorPago,
    ESTRATEGIAS_DISPONIBLES,
)
from services import pedido_service


# ─────────────────────────────────────────────────────────
#  Tests de las Estrategias Concretas (sin base de datos)
# ─────────────────────────────────────────────────────────

def test_estrategia_tarjeta_success():
    estrategia = PagoTarjetaStrategy()
    resultado = estrategia.procesar(pedido_id=10, monto=75.0, detalles={"token_tarjeta": "tok_test_123"})
    assert resultado["success"] is True
    assert resultado["estrategia"] == "tarjeta"
    assert "75" in resultado["message"]


def test_estrategia_tarjeta_sin_token():
    estrategia = PagoTarjetaStrategy()
    with pytest.raises(ValueError, match="Se requiere un token_tarjeta"):
        estrategia.procesar(pedido_id=10, monto=75.0, detalles={})


def test_estrategia_paypal_success():
    estrategia = PagoPayPalStrategy()
    resultado = estrategia.procesar(pedido_id=11, monto=50.0, detalles={"correo_paypal": "user@paypal.com"})
    assert resultado["success"] is True
    assert resultado["estrategia"] == "paypal"


def test_estrategia_paypal_sin_correo():
    estrategia = PagoPayPalStrategy()
    with pytest.raises(ValueError, match="Se requiere un correo_paypal"):
        estrategia.procesar(pedido_id=11, monto=50.0, detalles={})


def test_estrategia_efectivo_success():
    estrategia = PagoEfectivoStrategy()
    resultado = estrategia.procesar(pedido_id=12, monto=30.0, detalles={})
    assert resultado["success"] is True
    assert resultado["estrategia"] == "efectivo"


# ─────────────────────────────────────────────────────────
#  Tests del ProcesadorPago (Contexto)
# ─────────────────────────────────────────────────────────

def test_procesador_delega_a_estrategia():
    mock_estrategia = MagicMock()
    mock_estrategia.procesar.return_value = {"success": True, "message": "ok", "estrategia": "mock"}

    procesador = ProcesadorPago(mock_estrategia)
    resultado = procesador.ejecutar(pedido_id=99, monto=100.0, detalles={"dato": "x"})

    mock_estrategia.procesar.assert_called_once_with(99, 100.0, {"dato": "x"})
    assert resultado["success"] is True


def test_procesador_puede_cambiar_estrategia():
    procesador = ProcesadorPago(PagoEfectivoStrategy())
    procesador.set_estrategia(PagoPayPalStrategy())

    with pytest.raises(ValueError, match="Se requiere un correo_paypal"):
        procesador.ejecutar(pedido_id=5, monto=20.0, detalles={})


def test_estrategias_disponibles_contiene_claves():
    assert "tarjeta"  in ESTRATEGIAS_DISPONIBLES
    assert "paypal"   in ESTRATEGIAS_DISPONIBLES
    assert "efectivo" in ESTRATEGIAS_DISPONIBLES


# ─────────────────────────────────────────────────────────
#  Tests de integración con pedido_service.pagar_pedido
# ─────────────────────────────────────────────────────────

@patch("services.pedido_service.pedido_db")
@patch("services.pedido_service.cambiar_estado_pedido_accion")
def test_pagar_pedido_efectivo_completo(mock_cambiar_estado, mock_pedido_db):
    mock_pedido_db.obtener_pedido_por_id.return_value = {"id": 1, "total": 50.0, "estado": "pendiente"}
    mock_cambiar_estado.return_value = {"success": True, "nuevo_estado": "pagado", "message": "ok"}

    resultado = pedido_service.pagar_pedido(pedido_id=1, tipo_pago="efectivo", detalles={})

    assert resultado["success"] is True
    assert resultado["nuevo_estado"] == "pagado"
    assert resultado["pago"]["estrategia"] == "efectivo"


@patch("services.pedido_service.pedido_db")
def test_pagar_pedido_tipo_invalido(mock_pedido_db):
    resultado = pedido_service.pagar_pedido(pedido_id=1, tipo_pago="bitcoin", detalles={})
    assert resultado["success"] is False
    assert "no soportado" in resultado["message"]


@patch("services.pedido_service.pedido_db")
def test_pagar_pedido_no_encontrado(mock_pedido_db):
    mock_pedido_db.obtener_pedido_por_id.return_value = None
    resultado = pedido_service.pagar_pedido(pedido_id=999, tipo_pago="efectivo", detalles={})
    assert resultado["success"] is False
    assert "no encontrado" in resultado["message"]
