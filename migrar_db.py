import csv
import logging
import sqlite3
import pandas as pd

def connect_db():
    try:
        connection = sqlite3.connect('inventario.db')
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.Error as e:
        print(f"Ocurrió un error al conectar a la base de datos: {e}")
        logging.error(f"Ocurrió un error al conectar a la base de datos: {e}")

        return None, None


def main():
    connection, cursor = connect_db()
    try:
        create_tables(cursor)
        if load_products(cursor) or load_users(cursor) or load_purchases(cursor) or load_sales(cursor):
            connection.commit()
    except sqlite3.Error as e:
        print(f"Ocurrió un error de base de datos: {e}")
        logging.error(f"Ocurrió un error de base de datos: {e}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        logging.error(f"Ocurrió un error: {e}")

    finally:
        print("Cerrando conexión...")
        cursor.close()
        connection.close()

def create_tables(cursor):
    cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    ID_Producto TEXT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Stock_Actual INTEGER NOT NULL,
    Stock_Minimo INTEGER NOT NULL,
    Precio_Unitario REAL NOT NULL
)
''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    Correo TEXT PRIMARY KEY NOT NULL,
    Contraseña TEXT NOT NULL,
    Nombre TEXT NOT NULL
)
''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS purchases (
    ID_Compra TEXT PRIMARY KEY NOT NULL,
    Fecha TIMESTAMP,
    Proveedor TEXT NOT NULL,
    Total REAL NOT NULL,
    Estado TEXT NOT NULL,
    Usuario TEXT NOT NULL,
    Observaciones TEXT
)
''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS sales (
    ID_Venta TEXT PRIMARY KEY NOT NULL,
    Fecha TIMESTAMP,
    Cliente TEXT NOT NULL,
    Total REAL NOT NULL,
    Estado TEXT NOT NULL,
    Usuario TEXT NOT NULL,
    Método_Pago TEXT,
    Observaciones TEXT
)
''')

def load_products(cursor):
    """Carga los productos desde un archivo CSV a la base de datos."""
    try:
        with open('data/products.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            cursor.execute('DELETE FROM products')  # Limpiar datos existentes
            for row in reader:
                try:
                    id_producto = row['ID_Producto']
                    nombre = row['Nombre']
                    stock_actual = int(row['Stock_Actual'])
                    stock_minimo = int(row['Stock_Minimo'])
                    precio_unitario = float(row['Precio_Unitario'])
                    cursor.execute(
                        'INSERT INTO products (ID_Producto, Nombre, Stock_Actual, Stock_Minimo, Precio_Unitario) VALUES (?, ?, ?, ?, ?)',
                        (id_producto, nombre, stock_actual, stock_minimo, precio_unitario))
                except (sqlite3.IntegrityError, ValueError) as e:
                    print(f"Error al insertar el producto {row}: {e}")
                    logging.error(f"Error al insertar el producto {row}: {e}")

            return False
    except FileNotFoundError:
        print("No se encontró el archivo 'data/products.csv'.")
        logging.error("No se encontró el archivo 'data/products.csv'.")

        return True


def load_users(cursor):
    """Carga los usuarios desde un archivo CSV a la base de datos."""
    try:
        with open('data/users.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            cursor.execute('DELETE FROM users')  # Limpiar datos existentes
            for row in reader:
                try:
                    cursor.execute(
                        'INSERT INTO users (Correo, Contraseña, Nombre) VALUES (?, ?, ?)',
                        (row['Correo'], row['Contraseña'], row['Nombre']))
                except sqlite3.IntegrityError:
                    print(f"Error: El usuario con correo {row['Correo']} ya existe en la base de datos.")
            return False
    except FileNotFoundError:
        print("No se encontró el archivo 'data/users.csv'.")
        logging.error("No se encontró el archivo 'data/users.csv'.")

        return True


def load_purchases(cursor):
    try:
        df = pd.read_csv('data/purchases.csv')
    except Exception as e:
        print(f"Error al cargar el archivo 'purchases.csv': {e}")
        logging.error(f"Error al cargar el archivo 'purchases.csv': {e}")

        return True

    cursor.execute('DELETE FROM purchases')
    for index, row in df.iterrows():
        try:
                cursor.execute(
                    'INSERT INTO purchases (ID_Compra, Fecha, Proveedor, Total, Estado, Usuario, Observaciones) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (row['ID_Compra'], row['Fecha'], row['Proveedor'], float(row['Total']), row['Estado'], row['Usuario'], row['Observaciones']))

        except sqlite3.IntegrityError:
            print(f"Error: La compra con ID {row['ID_Compra']} ya existe en la base de datos.")
            continue
    return False

def load_sales(cursor):
    try:
        df = pd.read_csv('data/sales.csv')
    except Exception as e:
        print(f"Error al cargar el archivo 'sales.csv': {e}")
        logging.error(f"Error al cargar el archivo 'sales.csv': {e}")

        return True

    cursor.execute('DELETE FROM sales')
    for index, row in df.iterrows():
        try:
                cursor.execute(
                    'INSERT INTO sales (ID_Venta, Fecha, Cliente, Total, Estado, Usuario, Método_Pago, Observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (row['ID_Venta'], row['Fecha'], row['Cliente'], float(row['Total']), row['Estado'], row['Usuario'], row['Método_Pago'], row['Observaciones']))

        except sqlite3.IntegrityError:
            print(f"Error: La venta con ID {row['ID_Venta']} ya existe en la base de datos.")
            continue
        except sqlite3.IntegrityError:
            print(f"Error: La venta con ID {row['ID_Venta']} ya existe en la base de datos.")
            continue
    return False

if __name__ == '__main__':
    main()
