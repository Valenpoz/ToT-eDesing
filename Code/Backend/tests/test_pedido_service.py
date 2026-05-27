import pytest
from unittest.mock import patch
from datetime import datetime
from services import pedido_service

@pytest.fixture
def items():
    return [
        {"camiseta_personalizada_id": 1, "cantidad": 2, "subtotal": 30000},
        {"camiseta_personalizada_id": 2, "cantidad": 1, "subtotal": 20000},
    ]

@patch("services.pedido_service.pedido_db")
def test_registrar_pedido(mock_pedido_db, items):
    mock_pedido_db.crear_pedido.return_value = 123

    pedido_id = pedido_service.registrar_pedido(1, 2, items)

    assert pedido_id == 123
    mock_pedido_db.crear_pedido.assert_called_once()
    assert mock_pedido_db.agregar_detalle_pedido.call_count == len(items)

@patch("services.pedido_service.pedido_db")
def test_obtener_pedidos_de_usuario(mock_pedido_db):
    mock_pedido_db.obtener_pedidos_por_usuario.return_value = [{"id": 1}, {"id": 2}]
    pedidos = pedido_service.obtener_pedidos_de_usuario(1)

    assert isinstance(pedidos, list)
    assert len(pedidos) == 2
    mock_pedido_db.obtener_pedidos_por_usuario.assert_called_once_with(1)

@patch("services.pedido_service.pedido_db")
def test_obtener_detalles_de_pedido(mock_pedido_db):
    mock_pedido_db.obtener_detalles_pedido.return_value = [{"detalle": "camiseta"}]
    detalles = pedido_service.obtener_detalles_de_pedido(123)

    assert detalles == [{"detalle": "camiseta"}]
    mock_pedido_db.obtener_detalles_pedido.assert_called_once_with(123)

from services.pedido_builder import PedidoBuilder

def test_pedido_builder_success():
    builder = PedidoBuilder()
    pedido = (builder
              .para_usuario(10)
              .con_metodo_pago(2)
              .con_estado("completado")
              .con_fecha(datetime(2026, 5, 27, 10, 0, 0))
              .agregar_item(1, 2, 15.0)
              .agregar_item(2, 1, 20.0)
              .build())

    assert pedido.usuario_id == 10
    assert pedido.metodo_pago_id == 2
    assert pedido.estado == "completado"
    assert pedido.fecha == "2026-05-27 10:00:00"
    assert pedido.total == 35.0  # Suma de subtotales: 15.0 + 20.0
    assert len(pedido.items) == 2

def test_pedido_builder_missing_usuario():
    builder = PedidoBuilder()
    builder.con_metodo_pago(2)
    with pytest.raises(ValueError, match="El pedido requiere un usuario_id válido."):
        builder.build()

def test_pedido_builder_missing_metodo_pago():
    builder = PedidoBuilder()
    builder.para_usuario(10)
    with pytest.raises(ValueError, match="El pedido requiere un metodo_pago_id válido."):
        builder.build()

