import csv
import sqlite3
from app.user_management import hash_password

def column_exists(csv_reader, column_name):
    return column_name in csv_reader.fieldnames

def main():
    # Conectar a la base de datos
    with sqlite3.connect('inventario.db') as conn:
        cursor = conn.cursor()

        # Crear tablas
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            ID_Producto TEXT PRIMARY KEY,
            Nombre TEXT,
            Stock_Actual INTEGER,
            Stock_Minimo INTEGER,
            Precio_Unitario REAL
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Producto TEXT,
            Cantidad INTEGER,
            Tipo_Movimiento TEXT,
            Usuario TEXT,
            Descripción TEXT,
            Documento_Referencia TEXT,
            Fecha TIMESTAMP
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            Correo TEXT PRIMARY KEY,
            Contraseña TEXT,
            Nombre TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (
            ID_Compra TEXT PRIMARY KEY,
            ID_Producto TEXT,
            Fecha TIMESTAMP,
            Proveedor TEXT,
            Total REAL,
            Estado TEXT,
            Usuario TEXT,
            Observaciones TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
            ID_Venta TEXT PRIMARY KEY,
            ID_Producto TEXT,
            Fecha TIMESTAMP,
            Cliente TEXT,
            Total REAL,
            Estado TEXT,
            Usuario TEXT,
            Método_Pago TEXT,
            Observaciones TEXT
        )''')

        # Importar productos        
        # cursor.execute('''ALTER TABLE purchases ADD COLUMN ID_Producto TEXT;''')
        cursor.execute('''ALTER TABLE purchases ADD COLUMN Cantidad INTEGER;''')

        cursor.execute('''ALTER TABLE purchases ADD COLUMN Cantidad INTEGER;''')


    try:
        with open('data/products.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            required_columns = ['ID_Producto', 'Nombre', 'Stock_Actual', 'Stock_Minimo', 'Precio_Unitario']
            for column in required_columns:
                if not column_exists(csv_reader, column):
                    print(f"Error: La columna '{column}' no se encuentra en el archivo products.csv")
                    return
            
            file.seek(0)  # Reiniciar el archivo
            next(csv_reader)  # Saltar la línea de encabezado
            
            for row in csv_reader:
                try:
                    cursor.execute('''INSERT INTO products (ID_Producto, Nombre, Stock_Actual, Stock_Minimo, Precio_Unitario)
                                      VALUES (?, ?, ?, ?, ?)''', (
                        row['ID_Producto'],
                        row['Nombre'],
                        int(row['Stock_Actual']),
                        int(row['Stock_Minimo']),
                        float(row['Precio_Unitario'])
                    ))
                except sqlite3.IntegrityError:
                    print(f"Error: El producto con ID {row['ID_Producto']} ya existe en la base de datos.")
    except Exception as e:
        print(f"Error importando productos: {e}")

    # Importar usuarios
    try:
        with open('data/users.csv', mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    hashed_password = hash_password(row['Contraseña'])
                    cursor.execute('''INSERT INTO users (Correo, Contraseña, Nombre)
                                      VALUES (?, ?, ?)''', (row['Correo'], hashed_password, row['Nombre']))
                except sqlite3.IntegrityError:
                    print(f"Error: El usuario con correo {row['Correo']} ya existe en la base de datos.")
                except KeyError as e:
                    print(f"Error: La columna {e} no se encuentra en el archivo users.csv")
    except Exception as e:
        print(f"Error importando usuarios: {e}")

    # Importar compras, ventas e inventario (similar a los anteriores)
    # [Aquí se puede agregar el código para importar compras, ventas e inventario]

if __name__ == "__main__":
    main()
