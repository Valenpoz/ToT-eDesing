"""
Unit tests for the Composite Pattern implementation.
Tests simple components, composites, and price calculations.
"""

import unittest
from components import (
    SimpleComponent, CompositeComponent, Camiseta, Estampa,
    ProductoPersonalizado, CartItem
)


class TestSimpleComponent(unittest.TestCase):
    """Test cases for SimpleComponent leaf nodes."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.simple = SimpleComponent(
            component_id=1,
            name="Test Component",
            price=10.0,
            quantity=2
        )
    
    def test_simple_component_price(self):
        """Test that SimpleComponent calculates price correctly."""
        self.assertEqual(self.simple.get_price(), 20.0)
    
    def test_simple_component_quantity(self):
        """Test that SimpleComponent returns correct quantity."""
        self.assertEqual(self.simple.get_quantity(), 2)
    
    def test_simple_component_description(self):
        """Test description generation."""
        desc = self.simple.get_description()
        self.assertIn("Test Component", desc)
        self.assertIn("$10", desc)
    
    def test_simple_component_info(self):
        """Test get_component_info method."""
        info = self.simple.get_component_info()
        self.assertEqual(info["id"], 1)
        self.assertEqual(info["name"], "Test Component")
        self.assertEqual(info["total_price"], 20.0)


class TestCamiseta(unittest.TestCase):
    """Test cases for Camiseta (T-shirt) component."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.camiseta = Camiseta(
            camiseta_id=1,
            talla="L",
            color="Rojo",
            material="Algodón",
            precio=25.0,
            cantidad=1
        )
    
    def test_camiseta_creation(self):
        """Test Camiseta object creation."""
        self.assertEqual(self.camiseta.component_id, 1)
        self.assertEqual(self.camiseta.talla, "L")
        self.assertEqual(self.camiseta.price, 25.0)
    
    def test_camiseta_price(self):
        """Test Camiseta price calculation."""
        self.assertEqual(self.camiseta.get_price(), 25.0)
    
    def test_camiseta_info(self):
        """Test Camiseta info includes specific fields."""
        info = self.camiseta.get_component_info()
        self.assertEqual(info["talla"], "L")
        self.assertEqual(info["color"], "Rojo")
        self.assertEqual(info["material"], "Algodón")


class TestEstampa(unittest.TestCase):
    """Test cases for Estampa (Design/Print) component."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.estampa = Estampa(
            estampa_id=5,
            titulo="Diseño Galaxy",
            descripcion="Un bonito diseño del espacio",
            artista_id=2,
            precio=15.0,
            cantidad=1
        )
    
    def test_estampa_creation(self):
        """Test Estampa object creation."""
        self.assertEqual(self.estampa.component_id, 5)
        self.assertEqual(self.estampa.titulo, "Diseño Galaxy")
    
    def test_estampa_price(self):
        """Test Estampa price."""
        self.assertEqual(self.estampa.get_price(), 15.0)
    
    def test_estampa_info(self):
        """Test Estampa info includes specific fields."""
        info = self.estampa.get_component_info()
        self.assertEqual(info["titulo"], "Diseño Galaxy")
        self.assertEqual(info["artista_id"], 2)


class TestProductoPersonalizado(unittest.TestCase):
    """Test cases for ProductoPersonalizado composite component."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.camiseta = Camiseta(
            camiseta_id=1,
            talla="M",
            color="Blanco",
            material="Algodón",
            precio=25.0,
            cantidad=1
        )
        self.estampa = Estampa(
            estampa_id=5,
            titulo="Gato Ninja",
            descripcion="Un gato ninja",
            artista_id=2,
            precio=10.0,
            cantidad=1
        )
        self.producto = ProductoPersonalizado(producto_id=100, cantidad=1)
    
    def test_add_component(self):
        """Test adding components to composite."""
        self.producto.add_component(self.camiseta)
        self.assertEqual(len(self.producto.get_children()), 1)
    
    def test_composite_price_no_discount(self):
        """Test composite price without discount."""
        self.producto.add_component(self.camiseta)
        self.producto.add_component(self.estampa)
        expected_price = 25.0 + 10.0
        self.assertEqual(self.producto.get_price(), expected_price)
    
    def test_composite_with_discount(self):
        """Test composite price with discount."""
        self.producto.add_component(self.camiseta)
        self.producto.add_component(self.estampa)
        self.producto.apply_discount(10)  # 10% discount
        
        base_price = 35.0
        discount_amount = base_price * 0.10
        expected_price = base_price - discount_amount
        
        self.assertAlmostEqual(self.producto.get_price(), expected_price, places=2)
    
    def test_composite_description(self):
        """Test composite description."""
        self.producto.add_component(self.camiseta)
        self.producto.add_component(self.estampa)
        desc = self.producto.get_description()
        
        self.assertIn("Producto Personalizado", desc)
        self.assertIn("Camiseta", desc)
        self.assertIn("Estampa", desc)
    
    def test_composite_info(self):
        """Test composite info method."""
        self.producto.add_component(self.camiseta)
        self.producto.add_component(self.estampa)
        info = self.producto.get_component_info()
        
        self.assertEqual(len(info["children"]), 2)
        self.assertEqual(info["type"], "composite")
        self.assertEqual(info["descuento_pct"], 0.0)
    
    def test_remove_component(self):
        """Test removing components from composite."""
        self.producto.add_component(self.camiseta)
        self.producto.add_component(self.estampa)
        self.assertEqual(len(self.producto.get_children()), 2)
        
        self.producto.remove_component(self.estampa)
        self.assertEqual(len(self.producto.get_children()), 1)


class TestNestedComposites(unittest.TestCase):
    """Test cases for nested composite structures."""
    
    def setUp(self):
        """Set up nested composite structure."""
        self.camiseta1 = Camiseta(1, "M", "Blanco", "Algodón", 25.0, 1)
        self.camiseta2 = Camiseta(2, "L", "Negro", "Algodón", 27.0, 1)
        self.estampa = Estampa(5, "Logo", "Logo de la empresa", 1, 10.0, 1)
        
        self.producto1 = ProductoPersonalizado(100, cantidad=1)
        self.producto1.add_component(self.camiseta1)
        self.producto1.add_component(self.estampa)
        
        self.producto2 = ProductoPersonalizado(101, cantidad=1)
        self.producto2.add_component(self.camiseta2)
        self.producto2.add_component(self.estampa)
        
        self.carrito = CartItem(200, cantidad=1)
    
    def test_nested_composite_structure(self):
        """Test adding composite to composite."""
        self.carrito.add_component(self.producto1)
        self.carrito.add_component(self.producto2)
        
        self.assertEqual(len(self.carrito.get_children()), 2)
    
    def test_nested_composite_price(self):
        """Test price calculation through nested composites."""
        self.carrito.add_component(self.producto1)
        self.carrito.add_component(self.producto2)
        
        expected_price = (25.0 + 10.0) + (27.0 + 10.0)
        self.assertEqual(self.carrito.get_price(), expected_price)
    
    def test_nested_composite_description(self):
        """Test description of nested composites."""
        self.carrito.add_component(self.producto1)
        desc = self.carrito.get_description()
        
        self.assertIn("Cart Item", desc)
        self.assertIn("Producto Personalizado", desc)


class TestCartItem(unittest.TestCase):
    """Test cases for CartItem composite."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.camiseta = Camiseta(1, "S", "Rojo", "Algodón", 20.0, 2)
        self.cart_item = CartItem(300, cantidad=1)
    
    def test_cart_item_creation(self):
        """Test CartItem creation."""
        self.assertEqual(self.cart_item.composite_id, 300)
        self.assertEqual(self.cart_item.get_quantity(), 1)
    
    def test_cart_item_add_component(self):
        """Test adding components to cart item."""
        self.cart_item.add_component(self.camiseta)
        self.assertEqual(len(self.cart_item.get_children()), 1)
    
    def test_cart_item_price(self):
        """Test cart item price calculation."""
        self.cart_item.add_component(self.camiseta)
        self.assertEqual(self.cart_item.get_price(), 40.0)  # 20 * 2
    
    def test_cart_item_repr(self):
        """Test CartItem string representation."""
        self.cart_item.add_component(self.camiseta)
        repr_str = repr(self.cart_item)
        self.assertIn("CartItem", repr_str)
        self.assertIn("$40.00", repr_str)


class TestDiscountEdgeCases(unittest.TestCase):
    """Test edge cases for discount application."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.producto = ProductoPersonalizado(producto_id=500, cantidad=1)
        self.camiseta = Camiseta(1, "M", "Azul", "Algodón", 50.0, 1)
        self.producto.add_component(self.camiseta)
    
    def test_zero_discount(self):
        """Test that 0% discount doesn't change price."""
        original_price = self.producto.get_price()
        self.producto.apply_discount(0)
        self.assertEqual(self.producto.get_price(), original_price)
    
    def test_max_discount(self):
        """Test 100% discount."""
        self.producto.apply_discount(100)
        self.assertEqual(self.producto.get_price(), 0.0)
    
    def test_over_max_discount(self):
        """Test that discount > 100% is capped at 100%."""
        self.producto.apply_discount(150)
        self.assertEqual(self.producto.get_price(), 0.0)
    
    def test_negative_discount(self):
        """Test that negative discount is set to 0."""
        self.producto.apply_discount(-50)
        original_price = self.camiseta.get_price()
        self.assertEqual(self.producto.get_price(), original_price)


class TestQuantityHandling(unittest.TestCase):
    """Test quantity handling in composites."""
    
    def test_quantity_in_simple_component(self):
        """Test quantity calculation in simple components."""
        camiseta = Camiseta(1, "M", "Verde", "Algodón", 25.0, cantidad=3)
        self.assertEqual(camiseta.get_quantity(), 3)
        self.assertEqual(camiseta.get_price(), 75.0)
    
    def test_quantity_in_composite(self):
        """Test quantity in composite with simple components."""
        producto = ProductoPersonalizado(100, cantidad=2)
        camiseta = Camiseta(1, "M", "Rojo", "Algodón", 25.0, 1)
        producto.add_component(camiseta)
        
        self.assertEqual(producto.get_quantity(), 2)
        self.assertEqual(producto.get_price(), 50.0)  # 25 * 2


if __name__ == '__main__':
    unittest.main()
