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
