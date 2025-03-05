import csv
import sqlite3

def main():
    # Conectar a la base de datos
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    # Crear tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        ID_Producto TEXT PRIMARY KEY,
        Nombre TEXT,
        Stock_Actual INTEGER,
        Stock_Minimo INTEGER,
        Precio_Unitario REAL
    )
    ''')

    # Crear tabla de inventario
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Producto TEXT,
        Cantidad INTEGER,
        Tipo_Movimiento TEXT,
        Usuario TEXT,
        Descripción TEXT,
        Documento_Referencia TEXT,
        Fecha TIMESTAMP
    )
    ''')

    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        Correo TEXT PRIMARY KEY,
        Contraseña TEXT,
        Nombre TEXT
    )
    ''')

    # Crear tabla de compras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS purchases (
        ID_Compra TEXT PRIMARY KEY,
        Fecha TIMESTAMP,
        Proveedor TEXT,
        Total REAL,
        Estado TEXT,
        Usuario TEXT,
        Observaciones TEXT
    )
    ''')

    # Crear tabla de ventas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        ID_Venta TEXT PRIMARY KEY,
        Fecha TIMESTAMP,
        Cliente TEXT,
        Total REAL,
        Estado TEXT,
        Usuario TEXT,
        Método_Pago TEXT,
        Observaciones TEXT
    )
    ''')

    # Insertar datos en la tabla de productos
    with open('data/products.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO products (ID_Producto, Nombre, Stock_Actual, Stock_Minimo, Precio_Unitario)
                VALUES (?, ?, ?, ?, ?)
                ''', (row['ID_Producto'], row['Nombre'], int(row['Stock_Actual']), int(row['Stock_Minimo']), float(row['Precio_Unitario'])))
            except sqlite3.IntegrityError:
                print(f"Error: El producto con ID {row['ID_Producto']} ya existe en la base de datos.")

    # Insertar datos en la tabla de usuarios
    with open('data/users.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO users (Correo, Contraseña, Nombre)
                VALUES (?, ?, ?)
                ''', (row['Correo'], row['Contraseña'], row['Nombre']))
            except sqlite3.IntegrityError:
                print(f"Error: El usuario con correo {row['Correo']} ya existe en la base de datos.")

    # Insertar datos en la tabla de compras
    with open('data/purchases.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO purchases (ID_Compra, Fecha, Proveedor, Total, Estado, Usuario, Observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row['ID_Compra'], row['Fecha'], row['Proveedor'], float(row['Total']), row['Estado'], row['Usuario'], row['Observaciones']))
            except KeyError as e:
                print(f"Error: La columna {e} no se encuentra en el archivo purchases.csv")
            except sqlite3.IntegrityError:
                print(f"Error: La compra con ID {row['ID_Compra']} ya existe en la base de datos.")

    # Insertar datos en la tabla de ventas
    with open('data/sales.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            try:
                cursor.execute('''
                INSERT INTO sales (ID_Venta, Fecha, Cliente, Total, Estado, Usuario, Método_Pago, Observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row['ID_Venta'], row['Fecha'], row['Cliente'], float(row['Total']), row['Estado'], row['Usuario'], row['Método_Pago'], row['Observaciones']))
            except KeyError as e:
                print(f"Error: La columna {e} no se encuentra en el archivo sales.csv")
            except sqlite3.IntegrityError:
                print(f"Error: La venta con ID {row['ID_Venta']} ya existe en la base de datos.")

    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()