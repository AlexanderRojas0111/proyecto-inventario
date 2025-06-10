import sqlite3

DATABASE = 'inventario.db'

def get_db_connection():
    return sqlite3.connect(DATABASE)

def execute_query(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None
    finally:
        conn.close()

def fetch_one(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result:
            columns = [column[0] for column in cursor.description]
            result_dict = dict(zip(columns, result))
            print(f"Resultado de fetch_one: {result_dict}")
            return result_dict
        return None
    except sqlite3.Error as e:
        print(f"Error en fetch_one: {e}")
        return None
    finally:
        conn.close()

def fetch_all(query, params=()):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        if results:
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in results]
        return []
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
    finally:
        conn.close()