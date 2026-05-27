import pytest
from unittest.mock import patch
from services.pedido_state import PedidoStateContext

@patch("services.pedido_state.pedido_db")
def test_pedido_state_happy_path(mock_pedido_db):
    # Iniciar en estado pendiente
    contexto = PedidoStateContext(pedido_id=1, estado_actual_nombre="pendiente")
    assert contexto.get_estado_nombre() == "pendiente"

    # Pendiente -> Pagado
    contexto.pagar()
    assert contexto.get_estado_nombre() == "pagado"
    mock_pedido_db.actualizar_estado_pedido.assert_called_with(1, "pagado")

    # Pagado -> Enviado
    contexto.despachar()
    assert contexto.get_estado_nombre() == "enviado"
    mock_pedido_db.actualizar_estado_pedido.assert_called_with(1, "enviado")

    # Enviado -> Entregado
    contexto.entregar()
    assert contexto.get_estado_nombre() == "entregado"
    mock_pedido_db.actualizar_estado_pedido.assert_called_with(1, "entregado")


@patch("services.pedido_state.pedido_db")
def test_pedido_state_invalid_transitions(mock_pedido_db):
    # Caso 1: Despachar un pedido pendiente de pago
    contexto = PedidoStateContext(pedido_id=1, estado_actual_nombre="pendiente")
    with pytest.raises(ValueError, match="No se puede despachar un pedido que está pendiente de pago."):
        contexto.despachar()

    # Caso 2: Entregar un pedido que aún no ha sido enviado
    contexto_pagado = PedidoStateContext(pedido_id=2, estado_actual_nombre="pagado")
    with pytest.raises(ValueError, match="No se puede entregar un pedido que no ha sido enviado."):
        contexto_pagado.entregar()

    # Caso 3: Cancelar un pedido que ya está entregado
    contexto_entregado = PedidoStateContext(pedido_id=3, estado_actual_nombre="entregado")
    with pytest.raises(ValueError, match="No se puede cancelar un pedido que ya fue entregado exitosamente."):
        contexto_entregado.cancelar()


@patch("services.pedido_state.pedido_db")
def test_pedido_state_cancel_scenarios(mock_pedido_db):
    # Caso 1: Cancelar pedido pendiente
    c1 = PedidoStateContext(pedido_id=4, estado_actual_nombre="pendiente")
    c1.cancelar()
    assert c1.get_estado_nombre() == "cancelado"
    mock_pedido_db.actualizar_estado_pedido.assert_called_with(4, "cancelado")

    # Caso 2: Cancelar pedido pagado (ejecuta lógica de reembolso)
    c2 = PedidoStateContext(pedido_id=5, estado_actual_nombre="pagado")
    c2.cancelar()
    assert c2.get_estado_nombre() == "cancelado"
    mock_pedido_db.actualizar_estado_pedido.assert_called_with(5, "cancelado")
