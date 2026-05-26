from Code.Backend.CRUD import bolsa

def listar_bolsas():
    return bolsa.get_all_bolsas()

def registrar_bolsa(talla, color, material, precio, stock):
    success = bolsa.create_bolsa(talla, color, material, precio, stock)
    if success:
        return {"message": "Totebag creada correctamente", "success": True}
    else:
        return {"message": "Error al crear Totebag", "success": False}
