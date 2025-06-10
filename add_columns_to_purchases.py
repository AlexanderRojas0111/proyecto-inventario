import sqlite3

DATABASE = 'inventario.db'

def main():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Check if ID_Producto column exists
        cursor.execute("PRAGMA table_info(purchases);")
        columns = [column[1] for column in cursor.fetchall()]

        if 'ID_Producto' not in columns:
            cursor.execute('''ALTER TABLE purchases ADD COLUMN ID_Producto TEXT;''')

        if 'Cantidad' not in columns:
            cursor.execute('''ALTER TABLE purchases ADD COLUMN Cantidad INTEGER;''')
        
        if 'Costo' not in columns:
            cursor.execute('''ALTER TABLE purchases ADD COLUMN Costo REAL;''')


        if 'ID_Proveedor' not in columns:
            cursor.execute('''ALTER TABLE purchases ADD COLUMN ID_Proveedor TEXT;''')


if __name__ == "__main__":
    main()
