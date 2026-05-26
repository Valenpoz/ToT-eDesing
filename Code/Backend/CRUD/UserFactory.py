
class UserFactory():
    def create_user(nombre, correo, contrasena, rol_id):
        try:
            connection = get_connection()
            if rol_id ==0 :
                #crearAdmin
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "INSERT INTO usuarios (nombre, correo, contrasena, rol_id, fecha_creacion) VALUES (%s, %s, %s, %s, NOW())",
                        (nombre, correo, contrasena,"Admin")
                    )
                connection.commit()
            connection.close()
            return True
            if rol_id ==1:
                #crearDiseñador
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "INSERT INTO usuarios (nombre, correo, contrasena, rol_id, fecha_creacion) VALUES (%s, %s, %s, %s, NOW())",
                        (nombre, correo, contrasena,"Diseñador")
                    )
                    connection.commit()
            connection.close()
            return True                
            if rol_id ==2:
                #crearCliente
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute(
                        "INSERT INTO usuarios (nombre, correo, contrasena, rol_id, fecha_creacion) VALUES (%s, %s, %s, %s, NOW())",
                        (nombre, correo, contrasena,"Cliente")
                    )
                    connection.commit()
            connection.close()
            return True    
        except Exception as e:
            print("Error al crear usuario:", e)
            return False
