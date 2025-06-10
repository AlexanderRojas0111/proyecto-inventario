import sqlite3
from app.user_management import register_user, authenticate_user

def view_records():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('inventario.db')
        cursor = conn.cursor()
        
        # Obtener una lista de todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Mostrar los registros de cada tabla
        for table in tables:
            print(f"Registros de la tabla {table[0]}:")
            cursor.execute(f"SELECT * FROM {table[0]}")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print("\n")
        
        # Cerrar la conexión
        conn.close()
    except sqlite3.Error as e:
        print(f"Error al ver los registros: {e}")

def register_and_authenticate():
    # Registrar un nuevo usuario
    register_user("newuser@example.com", "newpassword", "New User")
    
    # Autenticar al nuevo usuario
    user = authenticate_user("newuser@example.com", "newpassword")
    if user:
        print(f"Usuario autenticado: {user}")
    else:
        print("Autenticación fallida")
    
    # Verificar los registros de la tabla users
    view_records()

if __name__ == "__main__":
    register_and_authenticate()