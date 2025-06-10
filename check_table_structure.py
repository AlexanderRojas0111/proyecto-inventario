import sqlite3

DATABASE = 'inventario.db'

def check_table_structure():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    tables = ['users', 'products', 'purchases', 'sales']
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        print(f"Estructura de la tabla {table}:")
        for column in columns:
            print(f" - {column[1]} (Tipo: {column[2]})")
        print()

    conn.close()

if __name__ == "__main__":
    check_table_structure()
