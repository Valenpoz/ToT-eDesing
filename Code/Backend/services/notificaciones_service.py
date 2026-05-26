#observable
class notificaciones_service(object):
    #esta es una interfaz que haran uso los users para ser notificados administradores por
    #añadiduras a la db de users, diseñadores por pedidos completados con sus diseños y 
    # clientes por el estado de sus pedidos

    #la interfaz entonces sera usada por los users e implementada por db y pedido
    def add(user):
        pass
    def delete(user):
        pass
    def notify(user):
        pass
