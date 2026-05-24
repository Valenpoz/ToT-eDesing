from CRUD import estampa

def listar_estampas():
    return estampa.get_all_estampas()

def registrar_estampa(titulo, descripcion, artista_id, estado):
    success = estampa.create_estampa(titulo, descripcion, artista_id, estado)
    if success:
        return {"message": "Estampa creada correctamente", "success": True}
    else:
        return {"message": "Error al crear estampa", "success": False}
