import logging
from data_manager import execute_query, fetch_one  # Agregada la importación de fetch_one

def create_user(email: str, password: str, roles: list) -> bool:
    """Crea un nuevo usuario en la base de datos."""
    try:
        query = "INSERT INTO users (Correo, Contraseña) VALUES (?, ?)"
        execute_query(query, (email, password))
        # Aquí se pueden agregar roles si es necesario
        return True
    except Exception as e:
        logging.error(f"Error al crear usuario: {e}")
        return False

def update_user(email: str, password: str) -> bool:
    """Actualiza la información de un usuario existente."""
    try:
        query = "UPDATE users SET Contraseña = ? WHERE Correo = ?"
        execute_query(query, (password, email))
        return True
    except Exception as e:
        logging.error(f"Error al actualizar usuario: {e}")
        return False

def delete_user(email: str) -> bool:
    """Elimina un usuario de la base de datos."""
    try:
        query = "DELETE FROM users WHERE Correo = ?"
        execute_query(query, (email,))
        return True
    except Exception as e:
        logging.error(f"Error al eliminar usuario: {e}")
        return False

def authenticate_user(email: str, password: str):
    """Autentica a un usuario y devuelve su información si es exitoso."""
    try:
        query = "SELECT * FROM users WHERE Correo = ? AND Contraseña = ?"
        user = fetch_one(query, (email, password))
        if user:
            return {"Correo": user[0], "Nombre": user[1]}  # Ajustar según la estructura de la tabla
        return None
    except Exception as e:
        logging.error(f"Error al autenticar usuario: {e}")
        return None
