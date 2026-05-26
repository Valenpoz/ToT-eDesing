import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='tienda_camisetas',
            user='root',
            password='12345'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
