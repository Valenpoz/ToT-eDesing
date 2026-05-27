import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        # Intentamos conectar a la base de datos directamente
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='tienda_totebags',
            user='root',
            password='password1'
        )
        return connection
    except Error as e:
        # Error 1049: Unknown database (la base de datos no existe)
        if e.errno == 1049:
            try:
                # Conectamos al servidor MySQL sin especificar base de datos para poder crearla
                print("La base de datos 'tienda_totebags' no existe. Intentando crearla...")
                temp_connection = mysql.connector.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='password1'
                )
                cursor = temp_connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS tienda_totebags")
                cursor.close()
                temp_connection.close()
                
                # Volvemos a intentar la conexión con la base de datos ya creada
                connection = mysql.connector.connect(
                    host='localhost',
                    port=3306,
                    database='tienda_totebags',
                    user='root',
                    password='password1'
                )
                print("Base de datos 'tienda_totebags' creada e inicializada con éxito.")
                return connection
            except Error as err:
                print(f"\n[ERROR] No se pudo crear la base de datos automáticamente: {err}")
                print("Asegúrate de que tu usuario y contraseña de MySQL en Code/Backend/db.py sean correctos.")
                return None
        else:
            print(f"\n[ERROR] Error al conectar a la base de datos: {e}")
            if e.errno == 1045:
                print("-> Error de acceso denegado (usuario o contraseña incorrectos).")
                print("   Modifica Code/Backend/db.py con tus credenciales correctas de MySQL local.\n")
            elif e.errno == 2003:
                print("-> No se pudo conectar al servidor MySQL. Asegúrate de que el servicio MySQL esté activo y corriendo en el puerto 3306.\n")
            return None
