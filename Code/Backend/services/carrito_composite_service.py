"""
Enhanced Carrito Service with Composite Pattern Integration
Manages shopping carts using the Composite Pattern for flexible product composition.
Allows simple products (Camiseta) and complex personalized products (Camiseta + Estampa).
"""

from CRUD import carrito as carrito_db
from CRUD import camiseta as camiseta_db
from CRUD import estampa as estampa_db
from datetime import datetime
from db import get_connection
from components import (
    CartItem, Camiseta, Estampa, ProductoPersonalizado, Component
)
from typing import Dict, List, Any, Optional


class CarritoCompositeManager:
    """
    Manager class for handling shopping cart with Composite Pattern.
    Provides methods to work with both simple and complex product compositions.
    """
    
    def __init__(self):
        """Initialize the cart manager."""
        self.carts: Dict[int, CartItem] = {}
    
    def crear_carrito(self, usuario_id: int) -> CartItem:
        """
        Create a new cart for a user using Composite Pattern.
        
        Args:
            usuario_id: ID of the user owning the cart
            
        Returns:
            CartItem: New cart composite component
        """
        cart_id = self._get_next_cart_id(usuario_id)
        cart = CartItem(cart_id, cantidad=1)
        self.carts[cart_id] = cart
        return cart
    
    def obtener_carrito(self, carrito_id: int) -> Optional[CartItem]:
        """
        Retrieve a cart by ID.
        
        Args:
            carrito_id: ID of the cart to retrieve
            
        Returns:
            CartItem or None if not found
        """
        return self.carts.get(carrito_id)
    
    def agregar_producto_simple(self, carrito_id: int, camiseta_id: int, 
                                cantidad: int = 1) -> bool:
        """
        Add a simple product (Camiseta) to the cart.
        
        Args:
            carrito_id: ID of the cart
            camiseta_id: ID of the Camiseta to add
            cantidad: Quantity to add
            
        Returns:
            bool: Success status
        """
        cart = self.obtener_carrito(carrito_id)
        if not cart:
            return False
        
        try:
            camiseta_data = camiseta_db.get_camiseta_by_id(camiseta_id)
            if not camiseta_data:
                return False
            
            camiseta = Camiseta(
                camiseta_id=camiseta_id,
                talla=camiseta_data[1],
                color=camiseta_data[2],
                material=camiseta_data[3],
                precio=camiseta_data[4],
                cantidad=cantidad
            )
            cart.add_component(camiseta)
            return True
        except Exception as e:
            print(f"Error agregando producto simple: {e}")
            return False
    
    def agregar_producto_personalizado(self, carrito_id: int, camiseta_id: int,
                                       estampa_ids: List[int], cantidad: int = 1,
                                       descuento: float = 0.0) -> bool:
        """
        Add a personalized product (Camiseta + Estampas) to the cart.
        
        Args:
            carrito_id: ID of the cart
            camiseta_id: ID of the base Camiseta
            estampa_ids: List of Estampa IDs to add to the product
            cantidad: Quantity of this product to add
            descuento: Optional discount percentage (0-100)
            
        Returns:
            bool: Success status
        """
        cart = self.obtener_carrito(carrito_id)
        if not cart:
            return False
        
        try:
            # Create the personalized product composite
            producto_id = self._get_next_producto_id()
            producto = ProductoPersonalizado(producto_id, cantidad, descuento)
            
            # Add Camiseta as base component
            camiseta_data = camiseta_db.get_camiseta_by_id(camiseta_id)
            if not camiseta_data:
                return False
            
            camiseta = Camiseta(
                camiseta_id=camiseta_id,
                talla=camiseta_data[1],
                color=camiseta_data[2],
                material=camiseta_data[3],
                precio=camiseta_data[4],
                cantidad=1
            )
            producto.add_component(camiseta)
            
            # Add Estampas
            for estampa_id in estampa_ids:
                estampa_data = estampa_db.get_estampa_by_id(estampa_id)
                if estampa_data:
                    estampa = Estampa(
                        estampa_id=estampa_id,
                        titulo=estampa_data[1],
                        descripcion=estampa_data[2],
                        artista_id=estampa_data[3],
                        precio=estampa_data[5],
                        cantidad=1
                    )
                    producto.add_component(estampa)
            
            # Add the personalized product to the cart
            cart.add_component(producto)
            return True
        except Exception as e:
            print(f"Error agregando producto personalizado: {e}")
            return False
    
    def calcular_total_carrito(self, carrito_id: int) -> float:
        """
        Calculate total price of all items in the cart.
        Uses recursive calculation through composite structure.
        
        Args:
            carrito_id: ID of the cart
            
        Returns:
            float: Total price of the cart
        """
        cart = self.obtener_carrito(carrito_id)
        if not cart:
            return 0.0
        return cart.get_price()
    
    def obtener_detalles_carrito(self, carrito_id: int) -> Dict[str, Any]:
        """
        Get detailed information about the cart and its components.
        
        Args:
            carrito_id: ID of the cart
            
        Returns:
            Dict with cart details and component hierarchy
        """
        cart = self.obtener_carrito(carrito_id)
        if not cart:
            return {"error": "Cart not found"}
        
        return {
            "carrito_id": cart.composite_id,
            "cantidad_items": len(cart.get_children()),
            "total_precio": cart.get_price(),
            "items": [child.get_component_info() for child in cart.get_children()]
        }
    
    def remover_item(self, carrito_id: int, item_index: int) -> bool:
        """
        Remove an item from the cart by index.
        
        Args:
            carrito_id: ID of the cart
            item_index: Index of the item to remove
            
        Returns:
            bool: Success status
        """
        cart = self.obtener_carrito(carrito_id)
        if not cart or item_index >= len(cart.get_children()):
            return False
        
        try:
            children = cart.get_children()
            cart.remove_component(children[item_index])
            return True
        except Exception as e:
            print(f"Error removiendo item: {e}")
            return False
    
    def limpiar_carrito(self, carrito_id: int) -> bool:
        """
        Remove all items from the cart.
        
        Args:
            carrito_id: ID of the cart
            
        Returns:
            bool: Success status
        """
        cart = self.obtener_carrito(carrito_id)
        if not cart:
            return False
        
        try:
            for child in cart.get_children():
                cart.remove_component(child)
            return True
        except Exception as e:
            print(f"Error limpiando carrito: {e}")
            return False
    
    def aplicar_descuento_global(self, carrito_id: int, descuento_pct: float) -> bool:
        """
        Apply a discount to all personalized products in the cart.
        
        Args:
            carrito_id: ID of the cart
            descuento_pct: Discount percentage (0-100)
            
        Returns:
            bool: Success status
        """
        cart = self.obtener_carrito(carrito_id)
        if not cart:
            return False
        
        try:
            for item in cart.get_children():
                if isinstance(item, ProductoPersonalizado):
                    item.apply_discount(descuento_pct)
            return True
        except Exception as e:
            print(f"Error aplicando descuento: {e}")
            return False
    
    def _get_next_cart_id(self, usuario_id: int) -> int:
        """Generate the next cart ID."""
        return int(f"{usuario_id}{len(self.carts) + 1}")
    
    def _get_next_producto_id(self) -> int:
        """Generate the next product ID."""
        return max([c.composite_id for c in self.carts.values() 
                   for item in c.get_children()], default=0) + 1


# Global manager instance
_carrito_manager = CarritoCompositeManager()


# Legacy function signatures (backward compatibility with existing API)

def crear_carrito_si_no_existe(usuario_id):
    """
    Legacy function: Create a cart if it doesn't exist.
    Now uses Composite Pattern internally.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM carrito WHERE usuario_id = %s", (usuario_id,))
        existente = cursor.fetchone()
        
        if existente:
            print(f"Ya existe carrito para usuario {usuario_id} con id {existente[0]}")
            return {
                "message": "El carrito ya existe",
                "success": True,
                "carrito_id": existente[0]
            }
        
        cursor.execute("INSERT INTO carrito (usuario_id) VALUES (%s)", (usuario_id,))
        conn.commit()
        nuevo_id = cursor.lastrowid
        
        print(f"Carrito creado para usuario {usuario_id} con id {nuevo_id}")
        return {
            "message": "Carrito creado correctamente",
            "success": True,
            "carrito_id": nuevo_id
        }
    
    except Exception as e:
        print("Error al crear carrito:", str(e))
        return {"message": "Error al crear carrito", "success": False}
    
    finally:
        cursor.close()
        conn.close()


def crear_carrito_para_usuario(usuario_id):
    """Legacy function: Create cart for user."""
    fecha = datetime.now()
    return carrito_db.crear_carrito(usuario_id, fecha)


def obtener_carrito_de_usuario(usuario_id):
    """Legacy function: Get cart by user."""
    return carrito_db.obtener_carrito_por_usuario(usuario_id)


def obtener_items_de_carrito(carrito_id):
    """Legacy function: Get items from cart."""
    return carrito_db.obtener_items_carrito(carrito_id)


def agregar_item(carrito_id, camiseta_personalizada_id, cantidad):
    """Legacy function: Add item to cart."""
    return carrito_db.agregar_item_al_carrito(carrito_id, camiseta_personalizada_id, cantidad)


def eliminar_item(item_id):
    """Legacy function: Remove item from cart."""
    return carrito_db.eliminar_item_del_carrito(item_id)


def eliminar_carrito(carrito_id):
    """Legacy function: Delete cart."""
    return carrito_db.eliminar_carrito(carrito_id)


# New Composite Pattern API

def crear_carrito_composite(usuario_id: int) -> Dict[str, Any]:
    """
    Create a new cart using Composite Pattern.
    
    Returns:
        Dict with status and carrito_id
    """
    try:
        cart = _carrito_manager.crear_carrito(usuario_id)
        return {
            "success": True,
            "message": "Carrito creado con Composite Pattern",
            "carrito_id": cart.composite_id
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


def agregar_producto_simple_composite(carrito_id: int, camiseta_id: int,
                                     cantidad: int = 1) -> Dict[str, Any]:
    """
    Add a simple product to cart.
    
    Args:
        carrito_id: Cart ID
        camiseta_id: Camiseta ID
        cantidad: Quantity
        
    Returns:
        Success status dict
    """
    try:
        success = _carrito_manager.agregar_producto_simple(carrito_id, camiseta_id, cantidad)
        if success:
            return {
                "success": True,
                "message": "Producto simple agregado al carrito"
            }
        else:
            return {"success": False, "message": "No se pudo agregar el producto"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def agregar_producto_personalizado_composite(carrito_id: int, camiseta_id: int,
                                            estampa_ids: List[int], cantidad: int = 1,
                                            descuento: float = 0.0) -> Dict[str, Any]:
    """
    Add a personalized product to cart.
    
    Args:
        carrito_id: Cart ID
        camiseta_id: Base Camiseta ID
        estampa_ids: List of Estampa IDs
        cantidad: Quantity
        descuento: Discount percentage
        
    Returns:
        Success status dict
    """
    try:
        success = _carrito_manager.agregar_producto_personalizado(
            carrito_id, camiseta_id, estampa_ids, cantidad, descuento
        )
        if success:
            return {
                "success": True,
                "message": "Producto personalizado agregado al carrito"
            }
        else:
            return {"success": False, "message": "No se pudo agregar el producto personalizado"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def obtener_carrito_composite(carrito_id: int) -> Dict[str, Any]:
    """
    Get detailed cart information using Composite Pattern.
    
    Args:
        carrito_id: Cart ID
        
    Returns:
        Dict with cart details and items
    """
    try:
        return _carrito_manager.obtener_detalles_carrito(carrito_id)
    except Exception as e:
        return {"error": str(e)}


def calcular_total_composite(carrito_id: int) -> Dict[str, Any]:
    """
    Calculate cart total using Composite Pattern.
    
    Args:
        carrito_id: Cart ID
        
    Returns:
        Dict with total amount
    """
    try:
        total = _carrito_manager.calcular_total_carrito(carrito_id)
        return {
            "success": True,
            "carrito_id": carrito_id,
            "total": total
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


def limpiar_carrito_composite(carrito_id: int) -> Dict[str, Any]:
    """
    Clear all items from cart.
    
    Args:
        carrito_id: Cart ID
        
    Returns:
        Success status dict
    """
    try:
        success = _carrito_manager.limpiar_carrito(carrito_id)
        if success:
            return {"success": True, "message": "Carrito limpiado"}
        else:
            return {"success": False, "message": "No se pudo limpiar el carrito"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def guardar_carrito_completo(usuario_id, items):
    """
    Legacy function: Save complete cart.
    Note: Database persistence would be implemented here.
    """
    try:
        carrito_id = user_id  # Simplified mapping
        cart = _carrito_manager.crear_carrito(usuario_id)
        
        for item in items:
            if item.get('type') == 'simple':
                _carrito_manager.agregar_producto_simple(
                    cart.composite_id,
                    item['camiseta_id'],
                    item.get('cantidad', 1)
                )
            elif item.get('type') == 'personalizado':
                _carrito_manager.agregar_producto_personalizado(
                    cart.composite_id,
                    item['camiseta_id'],
                    item.get('estampa_ids', []),
                    item.get('cantidad', 1),
                    item.get('descuento', 0.0)
                )
        
        return {
            "success": True,
            "message": "Carrito guardado correctamente",
            "carrito_id": cart.composite_id,
            "total": cart.get_price()
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
