import pytest
from unittest.mock import patch, MagicMock
from services.pedido_service_proxy import PedidoServiceProxy

@pytest.fixture
def proxy():
    return PedidoServiceProxy()

@patch("services.pedido_service_real.pedido_db")
@patch("services.pedido_state.pedido_db")
def test_proxy_pagar_allowed(mock_state_db, mock_real_db, proxy):
    # Setup del mock
    mock_real_db.obtener_pedido_por_id.return_value = {"id": 1, "total": 100.0, "estado": "pendiente"}
    
    # Un cliente puede pagar
    with patch("services.pago_strategy.ProcesadorPago.ejecutar") as mock_ejecutar:
        mock_ejecutar.return_value = {"success": True, "transaction_id": "tx_123"}
        resultado = proxy.pagar_pedido(pedido_id=1, tipo_pago="efectivo", detalles={}, usuario_rol="cliente")
        assert resultado["success"] is True
        assert resultado["pago"]["transaction_id"] == "tx_123"

@patch("services.pedido_service_real.pedido_db")
def test_proxy_pagar_denied(mock_real_db, proxy):
    # Un artista no debería pagar pedidos
    resultado = proxy.pagar_pedido(pedido_id=1, tipo_pago="efectivo", detalles={}, usuario_rol="artista")
    assert resultado["success"] is False
    assert "Acceso Denegado" in resultado["message"]

@patch("services.pedido_service_real.pedido_db")
@patch("services.pedido_state.pedido_db")
def test_proxy_despachar_admin_allowed(mock_state_db, mock_real_db, proxy):
    # Setup de mock
    mock_real_db.obtener_pedido_por_id.return_value = {"id": 1, "estado": "pagado"}
    
    # Un administrador puede despachar
    resultado = proxy.despachar_pedido(pedido_id=1, usuario_rol="admin")
    assert resultado["success"] is True
    assert resultado["nuevo_estado"] == "enviado"

@patch("services.pedido_service_real.pedido_db")
def test_proxy_despachar_cliente_denied(mock_real_db, proxy):
    # Un cliente no puede despachar
    resultado = proxy.despachar_pedido(pedido_id=1, usuario_rol="cliente")
    assert resultado["success"] is False
    assert "Acceso Denegado" in resultado["message"]

@patch("services.pedido_service_real.pedido_db")
@patch("services.pedido_state.pedido_db")
def test_proxy_entregar_admin_allowed(mock_state_db, mock_real_db, proxy):
    # Setup de mock
    mock_real_db.obtener_pedido_por_id.return_value = {"id": 1, "estado": "enviado"}
    
    # Un administrador puede entregar
    resultado = proxy.entregar_pedido(pedido_id=1, usuario_rol="admin")
    assert resultado["success"] is True
    assert resultado["nuevo_estado"] == "entregado"

@patch("services.pedido_service_real.pedido_db")
def test_proxy_entregar_cliente_denied(mock_real_db, proxy):
    # Un cliente no puede entregar
    resultado = proxy.entregar_pedido(pedido_id=1, usuario_rol="cliente")
    assert resultado["success"] is False
    assert "Acceso Denegado" in resultado["message"]

@patch("services.pedido_service_real.pedido_db")
@patch("services.pedido_state.pedido_db")
def test_proxy_cancelar_allowed(mock_state_db, mock_real_db, proxy):
    # Setup de mock
    mock_real_db.obtener_pedido_por_id.return_value = {"id": 1, "estado": "pendiente"}
    
    # Un cliente puede cancelar su propio pedido
    resultado = proxy.cancelar_pedido(pedido_id=1, usuario_rol="cliente")
    assert resultado["success"] is True
    assert resultado["nuevo_estado"] == "cancelado"

@patch("services.pedido_service_real.pedido_db")
def test_proxy_cancelar_denied(mock_real_db, proxy):
    # Un rol no autorizado (por ejemplo, artista) no puede cancelar
    resultado = proxy.cancelar_pedido(pedido_id=1, usuario_rol="artista")
    assert resultado["success"] is False
    assert "Acceso Denegado" in resultado["message"]
