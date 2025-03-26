import sqlite3

DATABASE = 'inventario.db'

def execute_query(query, params=()):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return cursor

def fetch_all(query, params=()):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def fetch_one(query, params=()):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return fetch_all(query)

def save_data(table_name, data):
    # Verificar si la estructura de los datos coincide con el esquema de la tabla
    if not data:
        print(f"Error: No hay datos para insertar en la tabla '{table_name}'.")
        return

    placeholders = ', '.join(['?'] * len(data[0]))
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.executemany(query, data)
        connection.commit()
