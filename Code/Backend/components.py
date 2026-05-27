"""
Composite Pattern Implementation for ToT-eDesign
Allows treating simple components (Camiseta, Estampa) and 
composite structures (ProductoPersonalizado) uniformly.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Component(ABC):
    """
    Abstract base class defining the interface for all components
    in the composite structure.
    """
    
    @abstractmethod
    def get_price(self) -> float:
        """Return the price of this component."""
        pass
    
    @abstractmethod
    def get_quantity(self) -> int:
        """Return the quantity of this component."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return a description of this component."""
        pass
    
    @abstractmethod
    def get_component_info(self) -> Dict[str, Any]:
        """Return detailed information about this component."""
        pass


class SimpleComponent(Component):
    """
    Leaf node in the composite tree. Represents an indivisible product
    like a Camiseta or Estampa.
    """
    
    def __init__(self, component_id: int, name: str, price: float, 
                 quantity: int = 1, component_type: str = "producto"):
        self.component_id = component_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.component_type = component_type  # 'camiseta', 'estampa', etc.
    
    def get_price(self) -> float:
        """Return total price (unit price * quantity)."""
        return self.price * self.quantity
    
    def get_quantity(self) -> int:
        """Return quantity of this component."""
        return self.quantity
    
    def get_description(self) -> str:
        """Return component name and price."""
        return f"{self.name} (${self.price} x{self.quantity})"
    
    def get_component_info(self) -> Dict[str, Any]:
        """Return detailed info about this component."""
        return {
            "id": self.component_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "type": self.component_type,
            "total_price": self.get_price()
        }
    
    def __repr__(self) -> str:
        return f"SimpleComponent({self.name}, ${self.price})"


class CompositeComponent(Component):
    """
    Composite node that can contain multiple components (simple or composite).
    Represents a complex product like a PersonalizedProduct (Camiseta + Estampa).
    """
    
    def __init__(self, composite_id: int, name: str, quantity: int = 1):
        self.composite_id = composite_id
        self.name = name
        self.quantity = quantity
        self.children: List[Component] = []
    
    def add_component(self, component: Component) -> None:
        """Add a child component."""
        if component not in self.children:
            self.children.append(component)
    
    def remove_component(self, component: Component) -> None:
        """Remove a child component."""
        if component in self.children:
            self.children.remove(component)
    
    def get_children(self) -> List[Component]:
        """Return list of child components."""
        return self.children.copy()
    
    def get_price(self) -> float:
        """Return total price of all children combined, multiplied by quantity."""
        children_price = sum(child.get_price() for child in self.children)
        return children_price * self.quantity
    
    def get_quantity(self) -> int:
        """Return quantity of this composite."""
        return self.quantity
    
    def get_description(self) -> str:
        """Return description with list of components."""
        children_desc = ", ".join([child.get_description() for child in self.children])
        return f"{self.name} (x{self.quantity}): [{children_desc}]"
    
    def get_component_info(self) -> Dict[str, Any]:
        """Return detailed info including all children."""
        return {
            "id": self.composite_id,
            "name": self.name,
            "quantity": self.quantity,
            "type": "composite",
            "children": [child.get_component_info() for child in self.children],
            "total_price": self.get_price()
        }
    
    def __repr__(self) -> str:
        return f"CompositeComponent({self.name}, {len(self.children)} items)"


class Camiseta(SimpleComponent):
    """
    Concrete implementation of a Camiseta (T-shirt).
    Represents a simple leaf component.
    """
    
    def __init__(self, camiseta_id: int, talla: str, color: str, 
                 material: str, precio: float, cantidad: int = 1):
        super().__init__(
            component_id=camiseta_id,
            name=f"Camiseta {talla} ({color})",
            price=precio,
            quantity=cantidad,
            component_type="camiseta"
        )
        self.talla = talla
        self.color = color
        self.material = material
    
    def get_component_info(self) -> Dict[str, Any]:
        """Return detailed camiseta info."""
        info = super().get_component_info()
        info.update({
            "talla": self.talla,
            "color": self.color,
            "material": self.material
        })
        return info


class Estampa(SimpleComponent):
    """
    Concrete implementation of an Estampa (Design/Print).
    Represents a simple leaf component.
    """
    
    def __init__(self, estampa_id: int, titulo: str, descripcion: str, 
                 artista_id: int, precio: float, cantidad: int = 1):
        super().__init__(
            component_id=estampa_id,
            name=f"Estampa: {titulo}",
            price=precio,
            quantity=cantidad,
            component_type="estampa"
        )
        self.titulo = titulo
        self.descripcion = descripcion
        self.artista_id = artista_id
    
    def get_component_info(self) -> Dict[str, Any]:
        """Return detailed estampa info."""
        info = super().get_component_info()
        info.update({
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "artista_id": self.artista_id
        })
        return info


class ProductoPersonalizado(CompositeComponent):
    """
    Concrete implementation of a personalized product.
    Combines a Camiseta with one or more Estampas.
    This is a composite component representing a complex product.
    """
    
    def __init__(self, producto_id: int, cantidad: int = 1, descuento: float = 0.0):
        super().__init__(
            composite_id=producto_id,
            name=f"Producto Personalizado #{producto_id}",
            quantity=cantidad
        )
        self.descuento = descuento  # Discount as percentage (0-100)
    
    def apply_discount(self, descuento_pct: float) -> None:
        """Apply a discount percentage to this product."""
        self.descuento = max(0, min(100, descuento_pct))
    
    def get_price(self) -> float:
        """Return total price with discount applied."""
        base_price = super().get_price()
        discount_amount = (base_price * self.descuento) / 100
        return base_price - discount_amount
    
    def get_component_info(self) -> Dict[str, Any]:
        """Return detailed info with discount applied."""
        info = super().get_component_info()
        info["descuento_pct"] = self.descuento
        info["precio_sin_descuento"] = sum(child.get_price() for child in self.children) * self.quantity
        return info


class CartItem(CompositeComponent):
    """
    Represents an item in the shopping cart.
    Can be a simple product or a personalized composite product.
    """
    
    def __init__(self, cart_item_id: int, cantidad: int = 1):
        super().__init__(
            composite_id=cart_item_id,
            name=f"Cart Item #{cart_item_id}",
            quantity=cantidad
        )
        self.added_at = None
    
    def __repr__(self) -> str:
        return f"CartItem({len(self.children)} items, Total: ${self.get_price():.2f})"
