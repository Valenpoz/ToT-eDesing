import sys
from CRUD import pedido as original_pedido_db

class MockablePedidoDbProxy:
    """
    Intermediario dinámico que permite a los tests mockear 'pedido_service.pedido_db'
    y redirigir de forma transparente todas las llamadas hacia el módulo real o hacia
    el mock inyectado por pytest.
    """
    def __getattr__(self, name):
        # Si un test mockeó pedido_service.pedido_db, redirige la consulta al mock
        # de lo contrario, delega al original de la base de datos
        from services.pedido_service import pedido_db as current_active_db
        if current_active_db is not self:
            return getattr(current_active_db, name)
        return getattr(original_pedido_db, name)
