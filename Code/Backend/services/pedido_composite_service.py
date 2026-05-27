"""
Enhanced Pedido (Order) Service with Composite Pattern Integration
Manages orders using the Composite Pattern for flexible order composition.
Allows tracking of simple and complex products within orders.
"""

from CRUD import pedido as pedido_db
from CRUD import camiseta as camiseta_db
from CRUD import estampa as estampa_db
from datetime import datetime
from typing import Dict, List, Any, Optional
from components import (
    Component, Camiseta, Estampa, ProductoPersonalizado, CartItem
)


class PedidoCompositeManager:
    """
    Manager class for handling orders with Composite Pattern.
    Provides methods to work with both simple and complex product compositions.
    """
    
    def __init__(self):
        """Initialize the order manager."""
        self.pedidos: Dict[int, Dict[str, Any]] = {}
    
    def crear_pedido_desde_carrito(self, usuario_id: int, carrito: CartItem,
                                   metodo_pago_id: int, estado: str = "pendiente") -> Dict[str, Any]:
        """
        Create an order from a shopping cart.
        
        Args:
            usuario_id: User ID
            carrito: CartItem composite with all products
            metodo_pago_id: Payment method ID
            estado: Order status (default: "pendiente")
            
        Returns:
            Dict with order details
        """
        try:
            pedido_id = self._get_next_pedido_id()
            
            # Create order structure
            pedido = {
                "pedido_id": pedido_id,
                "usuario_id": usuario_id,
                "carrito": carrito,
                "metodo_pago_id": metodo_pago_id,
                "estado": estado,
                "fecha_creacion": datetime.now(),
                "detalles": self._extraer_detalles_carrito(carrito)
            }
            
            # Calculate totals
            pedido["total"] = carrito.get_price()
            pedido["cantidad_items"] = len(carrito.get_children())
            
            self.pedidos[pedido_id] = pedido
            
            return {
                "success": True,
                "pedido_id": pedido_id,
                "total": pedido["total"],
                "estado": estado,
                "cantidad_items": pedido["cantidad_items"]
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def obtener_pedido(self, pedido_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve an order by ID.
        
        Args:
            pedido_id: Order ID
            
        Returns:
            Order dict or None if not found
        """
        return self.pedidos.get(pedido_id)
    
    def obtener_pedidos_usuario(self, usuario_id: int) -> List[Dict[str, Any]]:
        """
        Retrieve all orders for a user.
        
        Args:
            usuario_id: User ID
            
        Returns:
            List of order dicts
        """
        return [p for p in self.pedidos.values() if p["usuario_id"] == usuario_id]
    
    def actualizar_estado_pedido(self, pedido_id: int, nuevo_estado: str) -> bool:
        """
        Update order status.
        
        Args:
            pedido_id: Order ID
            nuevo_estado: New status
            
        Returns:
            bool: Success status
        """
        if pedido_id in self.pedidos:
            self.pedidos[pedido_id]["estado"] = nuevo_estado
            return True
        return False
    
    def obtener_detalles_pedido(self, pedido_id: int) -> Dict[str, Any]:
        """
        Get detailed information about an order including component hierarchy.
        
        Args:
            pedido_id: Order ID
            
        Returns:
            Dict with detailed order information
        """
        pedido = self.obtener_pedido(pedido_id)
        if not pedido:
            return {"error": "Order not found"}
        
        return {
            "pedido_id": pedido["pedido_id"],
            "usuario_id": pedido["usuario_id"],
            "estado": pedido["estado"],
            "fecha_creacion": pedido["fecha_creacion"].isoformat(),
            "total": pedido["total"],
            "cantidad_items": pedido["cantidad_items"],
            "metodo_pago_id": pedido["metodo_pago_id"],
            "detalles_items": pedido["detalles"],
            "composicion_carrito": pedido["carrito"].get_component_info()
        }
    
    def calcular_subtotal_por_tipo(self, pedido_id: int) -> Dict[str, float]:
        """
        Calculate subtotals by product type (Camisetas, Estampas, etc).
        
        Args:
            pedido_id: Order ID
            
        Returns:
            Dict with subtotals by product type
        """
        pedido = self.obtener_pedido(pedido_id)
        if not pedido:
            return {}
        
        subtotales = {}
        self._calcular_subtotales_recursivo(pedido["carrito"], subtotales)
        return subtotales
    
    def generar_resumen_pedido(self, pedido_id: int) -> Dict[str, Any]:
        """
        Generate a complete order summary.
        
        Args:
            pedido_id: Order ID
            
        Returns:
            Dict with order summary
        """
        pedido = self.obtener_pedido(pedido_id)
        if not pedido:
            return {"error": "Order not found"}
        
        subtotales = self.calcular_subtotal_por_tipo(pedido_id)
        
        return {
            "numero_pedido": pedido["pedido_id"],
            "usuario_id": pedido["usuario_id"],
            "fecha": pedido["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S"),
            "estado": pedido["estado"],
            "metodo_pago": f"Metodo {pedido['metodo_pago_id']}",
            "items": {
                "cantidad_total": pedido["cantidad_items"],
                "detalles": pedido["detalles"]
            },
            "resumen_precios": {
                "subtotales_por_tipo": subtotales,
                "total": pedido["total"]
            }
        }
    
    def aplicar_descuento_pedido(self, pedido_id: int, descuento_pct: float) -> bool:
        """
        Apply a global discount to all personalized products in the order.
        
        Args:
            pedido_id: Order ID
            descuento_pct: Discount percentage
            
        Returns:
            bool: Success status
        """
        pedido = self.obtener_pedido(pedido_id)
        if not pedido:
            return False
        
        try:
            carrito = pedido["carrito"]
            for item in carrito.get_children():
                if isinstance(item, ProductoPersonalizado):
                    item.apply_discount(descuento_pct)
            
            # Recalculate total
            pedido["total"] = carrito.get_price()
            return True
        except Exception as e:
            print(f"Error applying discount: {e}")
            return False
    
    def _extraer_detalles_carrito(self, carrito: CartItem) -> List[Dict[str, Any]]:
        """
        Extract detailed information from cart items recursively.
        
        Args:
            carrito: CartItem to process
            
        Returns:
            List of item details
        """
        detalles = []
        for item in carrito.get_children():
            detalles.append(item.get_component_info())
        return detalles
    
    def _calcular_subtotales_recursivo(self, componente: Component, 
                                       subtotales: Dict[str, float]) -> None:
        """
        Recursively calculate subtotals by component type.
        
        Args:
            componente: Component to process
            subtotales: Dictionary to accumulate subtotals
        """
        if isinstance(componente, ProductoPersonalizado) or isinstance(componente, CartItem):
            for child in componente.get_children():
                self._calcular_subtotales_recursivo(child, subtotales)
        else:
            comp_type = componente.component_type
            if comp_type not in subtotales:
                subtotales[comp_type] = 0.0
            subtotales[comp_type] += componente.get_price()
    
    def _get_next_pedido_id(self) -> int:
        """Generate the next order ID."""
        return max(self.pedidos.keys(), default=0) + 1


# Global manager instance
_pedido_manager = PedidoCompositeManager()


# Legacy function signatures (backward compatibility)

def registrar_pedido(usuario_id, metodo_pago_id, items):
    """
    Legacy function: Register order with items.
    items: list of dicts with keys:
    - camiseta_personalizada_id
    - cantidad
    - subtotal
    """
    try:
        fecha = datetime.now()
        total = sum(item["subtotal"] for item in items)
        estado = "pendiente"
        
        pedido_id = pedido_db.crear_pedido(usuario_id, total, metodo_pago_id, estado, fecha)
        
        for item in items:
            pedido_db.agregar_detalle_pedido(
                pedido_id,
                item["camiseta_personalizada_id"],
                item["cantidad"],
                item["subtotal"]
            )
        
        return pedido_id
    except Exception as e:
        print(f"Error registrando pedido: {e}")
        return None


def obtener_pedidos_de_usuario(usuario_id):
    """Legacy function: Get user's orders."""
    return pedido_db.obtener_pedidos_por_usuario(usuario_id)


def obtener_detalles_de_pedido(pedido_id):
    """Legacy function: Get order details."""
    return pedido_db.obtener_detalles_pedido(pedido_id)


def crear_nuevo_pedido(data):
    """Legacy function: Create new order."""
    try:
        usuario_id = data["usuario_id"]
        total = data["total"]
        metodo_pago_id = data["metodo_pago_id"]
        estado = data.get("estado", "pendiente")
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        pedido_db.crear_pedido(usuario_id, total, metodo_pago_id, estado, fecha)
        return {"message": "Pedido creado exitosamente", "success": True}
    except Exception as e:
        return {"message": str(e), "success": False}


def obtener_pedidos_usuario(usuario_id):
    """Legacy function: Get user's orders."""
    try:
        pedidos = pedido_db.obtener_pedidos_por_usuario(usuario_id)
        return {"pedidos": pedidos, "success": True}
    except Exception as e:
        return {"message": str(e), "success": False}


# New Composite Pattern API

def crear_pedido_composite(usuario_id: int, carrito: CartItem, 
                           metodo_pago_id: int) -> Dict[str, Any]:
    """
    Create order using Composite Pattern.
    
    Args:
        usuario_id: User ID
        carrito: CartItem with products
        metodo_pago_id: Payment method ID
        
    Returns:
        Order creation status
    """
    return _pedido_manager.crear_pedido_desde_carrito(usuario_id, carrito, metodo_pago_id)


def obtener_pedido_composite(pedido_id: int) -> Dict[str, Any]:
    """
    Get order details using Composite Pattern.
    
    Args:
        pedido_id: Order ID
        
    Returns:
        Order details dict
    """
    return _pedido_manager.obtener_detalles_pedido(pedido_id)


def obtener_pedidos_usuario_composite(usuario_id: int) -> Dict[str, Any]:
    """
    Get all user's orders using Composite Pattern.
    
    Args:
        usuario_id: User ID
        
    Returns:
        Dict with list of orders
    """
    try:
        pedidos = _pedido_manager.obtener_pedidos_usuario(usuario_id)
        return {
            "success": True,
            "cantidad_pedidos": len(pedidos),
            "pedidos": [_pedido_manager.obtener_detalles_pedido(p["pedido_id"]) for p in pedidos]
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


def obtener_resumen_pedido_composite(pedido_id: int) -> Dict[str, Any]:
    """
    Get order summary using Composite Pattern.
    
    Args:
        pedido_id: Order ID
        
    Returns:
        Order summary dict
    """
    return _pedido_manager.generar_resumen_pedido(pedido_id)


def actualizar_estado_pedido_composite(pedido_id: int, nuevo_estado: str) -> Dict[str, Any]:
    """
    Update order status.
    
    Args:
        pedido_id: Order ID
        nuevo_estado: New status
        
    Returns:
        Status dict
    """
    try:
        success = _pedido_manager.actualizar_estado_pedido(pedido_id, nuevo_estado)
        if success:
            return {
                "success": True,
                "message": f"Estado actualizado a {nuevo_estado}",
                "pedido_id": pedido_id
            }
        else:
            return {"success": False, "message": "Pedido no encontrado"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def calcular_subtotales_pedido_composite(pedido_id: int) -> Dict[str, Any]:
    """
    Calculate subtotals by product type.
    
    Args:
        pedido_id: Order ID
        
    Returns:
        Dict with subtotals
    """
    try:
        subtotales = _pedido_manager.calcular_subtotal_por_tipo(pedido_id)
        return {
            "success": True,
            "pedido_id": pedido_id,
            "subtotales_por_tipo": subtotales
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
