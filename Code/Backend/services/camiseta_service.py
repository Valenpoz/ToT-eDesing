from CRUD import camiseta

def listar_camisetas():
    return camiseta.get_all_camisetas()

def registrar_camiseta(talla, color, material, precio, stock):
    success = camiseta.create_camiseta(talla, color, material, precio, stock)
    if success:
        return {"message": "Camiseta creada correctamente", "success": True}
    else:
        return {"message": "Error al crear camiseta", "success": False}
