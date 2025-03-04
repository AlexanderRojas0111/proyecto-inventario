import sqlite3

DATABASE = 'inventario.db'

def execute_query(query, params=()):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

def fetch_all(query, params=()):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def fetch_one(query, params=()):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

def load_data(table_name):
    query = f"SELECT * FROM {table_name}"
    return fetch_all(query)

def save_data(table_name, data):
    placeholders = ', '.join(['?'] * len(data[0]))
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executemany(query, data)
        conn.commit()