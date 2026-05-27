"""
Ejemplos de Uso - Composite Pattern en ToT-eDesign
Demostraciones prácticas de cómo usar el patrón en diferentes escenarios
"""

# ============================================================================
# EJEMPLO 1: Crear un Carrito Simple
# ============================================================================

def ejemplo_carrito_simple():
    """
    Flujo: Usuario agrega solo camisetas simples
    """
    from services.carrito_composite_service import (
        crear_carrito_composite,
        agregar_producto_simple_composite,
        obtener_carrito_composite,
        calcular_total_composite
    )
    
    print("\n" + "="*60)
    print("EJEMPLO 1: Carrito Simple (Solo Camisetas)")
    print("="*60)
    
    # Paso 1: Crear carrito
    carrito_result = crear_carrito_composite(usuario_id=1)
    carrito_id = carrito_result["carrito_id"]
    print(f"✓ Carrito creado: {carrito_id}")
    
    # Paso 2: Agregar camisetas simples
    agregar_producto_simple_composite(carrito_id, camiseta_id=1, cantidad=2)
    print("✓ Agregada camiseta #1 (cantidad: 2)")
    
    agregar_producto_simple_composite(carrito_id, camiseta_id=2, cantidad=1)
    print("✓ Agregada camiseta #2 (cantidad: 1)")
    
    # Paso 3: Obtener detalles
    carrito = obtener_carrito_composite(carrito_id)
    print(f"\n📦 Carrito Summary:")
    print(f"   - Items: {carrito['cantidad_items']}")
    print(f"   - Total: ${carrito['total_precio']:.2f}")
    
    # Paso 4: Ver total
    total = calcular_total_composite(carrito_id)
    print(f"\n💰 Total Final: ${total['total']:.2f}")
    
    return carrito_id


# ============================================================================
# EJEMPLO 2: Crear Producto Personalizado en Carrito
# ============================================================================

def ejemplo_carrito_personalizado():
    """
    Flujo: Usuario personaliza una camiseta con estampas
    """
    from services.carrito_composite_service import (
        crear_carrito_composite,
        agregar_producto_personalizado_composite,
        obtener_carrito_composite
    )
    
    print("\n" + "="*60)
    print("EJEMPLO 2: Carrito con Producto Personalizado")
    print("="*60)
    
    # Paso 1: Crear carrito
    carrito_result = crear_carrito_composite(usuario_id=2)
    carrito_id = carrito_result["carrito_id"]
    print(f"✓ Carrito creado: {carrito_id}")
    
    # Paso 2: Agregar producto personalizado (Camiseta + Estampas)
    result = agregar_producto_personalizado_composite(
        carrito_id=carrito_id,
        camiseta_id=1,              # Base: Camiseta M Rojo ($25)
        estampa_ids=[5, 6],         # Estampa Gato Ninja ($10) + Rayas ($5)
        cantidad=1,
        descuento=10.0              # 10% descuento por promoción
    )
    print("✓ Producto personalizado agregado")
    print("  - Camiseta M Rojo ($25)")
    print("  - Estampa: Gato Ninja ($10)")
    print("  - Estampa: Rayas ($5)")
    print("  - Descuento: 10%")
    
    # Paso 3: Obtener detalles
    carrito = obtener_carrito_composite(carrito_id)
    
    print(f"\n📦 Estructura del Producto:")
    for item in carrito['items']:
        print(f"   - {item['name']}: ${item['total_price']:.2f}")
        if 'children' in item:
            for child in item['children']:
                print(f"     └─ {child['name']}: ${child['total_price']:.2f}")
    
    print(f"\n💰 Total: ${carrito['total_precio']:.2f}")


# ============================================================================
# EJEMPLO 3: Carrito Mixto (Simple + Personalizado)
# ============================================================================

def ejemplo_carrito_mixto():
    """
    Flujo: Usuario tiene camisetas simples y personalizadas en el carrito
    """
    from services.carrito_composite_service import (
        crear_carrito_composite,
        agregar_producto_simple_composite,
        agregar_producto_personalizado_composite,
        obtener_carrito_composite
    )
    
    print("\n" + "="*60)
    print("EJEMPLO 3: Carrito Mixto")
    print("="*60)
    
    # Crear carrito
    carrito_result = crear_carrito_composite(usuario_id=3)
    carrito_id = carrito_result["carrito_id"]
    print(f"✓ Carrito creado: {carrito_id}\n")
    
    # Agregar camiseta simple
    print("1️⃣  Agregando camiseta simple...")
    agregar_producto_simple_composite(carrito_id, camiseta_id=3, cantidad=2)
    print("   ✓ 2x Camiseta L Negro ($27 c/u = $54)\n")
    
    # Agregar producto personalizado #1
    print("2️⃣  Agregando producto personalizado #1...")
    agregar_producto_personalizado_composite(
        carrito_id, camiseta_id=1, estampa_ids=[5],
        cantidad=1, descuento=0.0
    )
    print("   ✓ Camiseta M Rojo + Estampa Gato ($35)\n")
    
    # Agregar producto personalizado #2 con descuento
    print("3️⃣  Agregando producto personalizado #2 (con descuento)...")
    agregar_producto_personalizado_composite(
        carrito_id, camiseta_id=2, estampa_ids=[6, 7],
        cantidad=1, descuento=15.0
    )
    print("   ✓ Camiseta L Blanco + Estampas ($37.59 con 15% desc)\n")
    
    # Obtener resumen
    carrito = obtener_carrito_composite(carrito_id)
    print("="*60)
    print("📋 RESUMEN DEL CARRITO")
    print("="*60)
    print(f"Items: {carrito['cantidad_items']}")
    for i, item in enumerate(carrito['items'], 1):
        print(f"\n{i}. {item['name']}")
        print(f"   Precio: ${item['total_price']:.2f}")
        if 'children' in item:
            print(f"   Componentes:")
            for child in item['children']:
                print(f"     • {child['name']}: ${child['total_price']:.2f}")
    
    print(f"\n{'='*60}")
    print(f"TOTAL CARRITO: ${carrito['total_precio']:.2f}")
    print(f"{'='*60}")


# ============================================================================
# EJEMPLO 4: Crear Pedido desde Carrito
# ============================================================================

def ejemplo_pedido_desde_carrito():
    """
    Flujo: Usuario hace checkout y crea un pedido
    """
    from services.carrito_composite_service import (
        crear_carrito_composite,
        agregar_producto_personalizado_composite,
        _carrito_manager
    )
    from services.pedido_composite_service import (
        crear_pedido_composite,
        obtener_resumen_pedido_composite,
        calcular_subtotales_pedido_composite
    )
    
    print("\n" + "="*60)
    print("EJEMPLO 4: Crear Pedido desde Carrito")
    print("="*60)
    
    # Crear carrito con productos
    print("\n1️⃣  Preparando carrito...")
    carrito_result = crear_carrito_composite(usuario_id=4)
    carrito_id = carrito_result["carrito_id"]
    
    agregar_producto_personalizado_composite(
        carrito_id, camiseta_id=1, estampa_ids=[5, 6],
        cantidad=2, descuento=5.0
    )
    print(f"✓ Carrito preparado con 2 productos personalizados\n")
    
    # Obtener carrito del manager
    carrito = _carrito_manager.obtener_carrito(carrito_id)
    
    # Crear pedido
    print("2️⃣  Procesando pedido...")
    pedido_result = crear_pedido_composite(
        usuario_id=4,
        carrito=carrito,
        metodo_pago_id=1  # Tarjeta de crédito
    )
    pedido_id = pedido_result["pedido_id"]
    print(f"✓ Pedido creado: #{pedido_id}\n")
    
    # Obtener resumen
    print("3️⃣  Obteniendo resumen del pedido...")
    resumen = obtener_resumen_pedido_composite(pedido_id)
    
    print("\n" + "="*60)
    print("📦 RESUMEN DEL PEDIDO")
    print("="*60)
    print(f"Número de Pedido: #{resumen['numero_pedido']}")
    print(f"Usuario ID: {resumen['usuario_id']}")
    print(f"Fecha: {resumen['fecha']}")
    print(f"Estado: {resumen['estado'].upper()}")
    print(f"Método de Pago: {resumen['metodo_pago']}")
    print(f"\nCantidad de Items: {resumen['items']['cantidad_total']}")
    
    print(f"\nSubtotales por Tipo:")
    for tipo, subtotal in resumen['resumen_precios']['subtotales_por_tipo'].items():
        print(f"  • {tipo.capitalize()}: ${subtotal:.2f}")
    
    print(f"\n{'='*60}")
    print(f"TOTAL: ${resumen['resumen_precios']['total']:.2f}")
    print(f"{'='*60}")
    
    # Calcular subtotales
    print("\n4️⃣  Análisis de subtotales por componente...")
    subtotales = calcular_subtotales_pedido_composite(pedido_id)
    if subtotales['success']:
        print("Subtotales:")
        for tipo, monto in subtotales['subtotales_por_tipo'].items():
            print(f"  • {tipo}: ${monto:.2f}")


# ============================================================================
# EJEMPLO 5: Gestión Avanzada - Aplicar Descuentos
# ============================================================================

def ejemplo_descuentos():
    """
    Flujo: Usuario aplica descuentos al carrito
    """
    from services.carrito_composite_service import (
        crear_carrito_composite,
        agregar_producto_personalizado_composite,
        obtener_carrito_composite
    )
    
    print("\n" + "="*60)
    print("EJEMPLO 5: Aplicar Descuentos")
    print("="*60)
    
    # Crear carrito
    carrito_result = crear_carrito_composite(usuario_id=5)
    carrito_id = carrito_result["carrito_id"]
    
    # Agregar producto
    agregar_producto_personalizado_composite(
        carrito_id, camiseta_id=1, estampa_ids=[5],
        cantidad=1, descuento=0.0  # Sin descuento inicialmente
    )
    
    # Ver total sin descuento
    carrito = obtener_carrito_composite(carrito_id)
    print(f"Total SIN descuento: ${carrito['total_precio']:.2f}")
    
    # Agregar otro producto con descuento
    print("\nAplicando 20% de descuento al nuevo producto...")
    agregar_producto_personalizado_composite(
        carrito_id, camiseta_id=2, estampa_ids=[6],
        cantidad=1, descuento=20.0  # 20% descuento
    )
    
    # Ver detalle con descuento
    carrito = obtener_carrito_composite(carrito_id)
    print("\nDetalles del carrito:")
    for item in carrito['items']:
        if item['type'] == 'composite':
            print(f"  - {item['name']}")
            print(f"    Precio sin descuento: ${item.get('precio_sin_descuento', item['total_price']):.2f}")
            if 'descuento_pct' in item:
                print(f"    Descuento: {item['descuento_pct']:.0f}%")
            print(f"    Total: ${item['total_price']:.2f}")
    
    print(f"\nTotal FINAL del carrito: ${carrito['total_precio']:.2f}")


# ============================================================================
# EJECUTOR DE EJEMPLOS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🎨 " * 20)
    print("EJEMPLOS DE USO - COMPOSITE PATTERN")
    print("🎨 " * 20)
    
    try:
        # Ejecutar todos los ejemplos
        ejemplo_carrito_simple()
        ejemplo_carrito_personalizado()
        ejemplo_carrito_mixto()
        ejemplo_pedido_desde_carrito()
        ejemplo_descuentos()
        
        print("\n" + "✅ " * 20)
        print("TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("✅ " * 20 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error ejecutando ejemplos: {e}")
        import traceback
        traceback.print_exc()
