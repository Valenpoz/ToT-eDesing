import pytest
from unittest.mock import patch
from services import carrito_service  # ajusta si tu archivo se llama diferente

@patch("services.carrito_service.carrito_db")
def test_crear_carrito_para_usuario(mock_carrito_db):
    mock_carrito_db.crear_carrito.return_value = 10

    result = carrito_service.crear_carrito_para_usuario(1)

    assert result == 10
    mock_carrito_db.crear_carrito.assert_called_once()

@patch("services.carrito_service.carrito_db")
def test_obtener_carrito_de_usuario(mock_carrito_db):
    mock_carrito_db.obtener_carrito_por_usuario.return_value = {"id": 1, "usuario_id": 1}

    result = carrito_service.obtener_carrito_de_usuario(1)

    assert result["usuario_id"] == 1
    mock_carrito_db.obtener_carrito_por_usuario.assert_called_once_with(1)

@patch("services.carrito_service.carrito_db")
def test_obtener_items_de_carrito(mock_carrito_db):
    mock_carrito_db.obtener_items_carrito.return_value = [{"id": 1}, {"id": 2}]

    result = carrito_service.obtener_items_de_carrito(5)

    assert isinstance(result, list)
    assert len(result) == 2
    mock_carrito_db.obtener_items_carrito.assert_called_once_with(5)

@patch("services.carrito_service.carrito_db")
def test_agregar_item(mock_carrito_db):
    mock_carrito_db.agregar_item_al_carrito.return_value = True

    result = carrito_service.agregar_item(3, 99, 2)

    assert result is True
    mock_carrito_db.agregar_item_al_carrito.assert_called_once_with(3, 99, 2)

@patch("services.carrito_service.carrito_db")
def test_eliminar_item(mock_carrito_db):
    mock_carrito_db.eliminar_item_del_carrito.return_value = True

    result = carrito_service.eliminar_item(42)

    assert result is True
    mock_carrito_db.eliminar_item_del_carrito.assert_called_once_with(42)

@patch("services.carrito_service.carrito_db")
def test_eliminar_carrito(mock_carrito_db):
    mock_carrito_db.eliminar_carrito.return_value = True

    result = carrito_service.eliminar_carrito(7)

    assert result is True
    mock_carrito_db.eliminar_carrito.assert_called_once_with(7)
