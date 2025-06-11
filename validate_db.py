import sqlite3

def validate_database(db_name):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        
        # Obtener la estructura de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            print(f"Tabla: {table[0]}")
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()
            for column in columns:
                print(f"  Columna: {column[1]}, Tipo: {column[2]}, No Nulo: {column[3]}, Predeterminado: {column[4]}")
            
            # Obtener los datos de la tabla
            cursor.execute(f"SELECT * FROM {table[0]};")
            rows = cursor.fetchall()
            for row in rows:
                print(f"  Datos: {row}")
            print()
        
        connection.close()
    except Exception as e:
        print(f"Error al validar la base de datos: {e}")

if __name__ == "__main__":
    validate_database('inventario.db')
