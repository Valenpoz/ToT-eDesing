import db
import os

def init():
    conn = db.get_connection()
    if not conn:
        print("\n[ERROR] No se pudo conectar a la base de datos MySQL en el puerto 3307.")
        print("Asegúrate de que Docker Desktop esté abierto y que hayas iniciado el contenedor con 'docker-compose up -d'.\n")
        return
    
    cursor = conn.cursor()
    
    # Leer querydb.txt
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    query_file_path = os.path.join(backend_dir, 'querydb.txt')
    
    if not os.path.exists(query_file_path):
        print(f"\n[ERROR] No se encontró el archivo querydb.txt en {query_file_path}\n")
        return
        
    print(f"Leyendo consultas desde {query_file_path}...")
    with open(query_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
        
    # Limpiar y separar las consultas por punto y coma
    queries = sql_content.split(';')
    
    success_count = 0
    error_count = 0
    
    for query in queries:
        query = query.strip()
        if not query:
            continue
        try:
            cursor.execute(query)
            success_count += 1
        except Exception as e:
            # Algunas consultas de inserción o tablas ya creadas pueden arrojar advertencias/errores controlados
            print(f"[ADVERTENCIA/ERROR] Error al ejecutar consulta:\n{query[:100]}...\nDetalle: {e}\n")
            error_count += 1
            
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"\n[OK] Inicialización de la base de datos completada.")
    print(f" - Consultas ejecutadas con éxito: {success_count}")
    print(f" - Errores/Advertencias: {error_count}\n")

if __name__ == '__main__':
    init()
