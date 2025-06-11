import logging
from data_manager import execute_query, fetch_one  

class UserManager:
    def __init__(self):
        pass
    
    def create_user(self, email: str, password: str, roles: list) -> bool:
        """Crea un nuevo usuario en la base de datos. 
        Args:
            email (str): El correo electrónico del usuario.
            password (str): La contraseña del usuario.
            roles (list): Lista de roles asignados al usuario.
        Returns:
            bool: True si el usuario fue creado exitosamente, False en caso contrario.
        """ 

        try:
            query = "INSERT INTO users (Correo, Contraseña) VALUES (?, ?)" 
            # Verificar si el usuario ya existe
            existing_user = fetch_one("SELECT * FROM users WHERE Correo = ?", (email,))
            if existing_user:
                print(f"Error: El usuario con correo {email} ya existe.")
                return False

            execute_query(query, (email, password))
            # Aquí se pueden agregar roles si es necesario
            return True
        except Exception as e:
            logging.error(f"Error al crear usuario: {e}")
            return False

    def update_user(self, email: str, password: str) -> bool:
        """Actualiza la información de un usuario existente.
        Args:
            email (str): El correo electrónico del usuario.
            password (str): La nueva contraseña del usuario.
        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """ 

        try:
            query = "UPDATE users SET Contraseña = ? WHERE Correo = ?"
            execute_query(query, (password, email))
            return True
        except Exception as e:
            logging.error(f"Error al actualizar usuario: {e}")
            return False

    def delete_user(self, email: str) -> bool:
        """Elimina un usuario de la base de datos.
        Args:
            email (str): El correo electrónico del usuario a eliminar.
        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """ 

        try:
            query = "DELETE FROM users WHERE Correo = ?"
            execute_query(query, (email,))
            return True
        except Exception as e:
            logging.error(f"Error al eliminar usuario: {e}")
            return False

    def authenticate_user(self, email: str, password: str):
        """Autentica a un usuario y devuelve su información si es exitoso.
        Args:
            email (str): El correo electrónico del usuario.
            password (str): La contraseña del usuario.
        Returns:
            dict or None: Información del usuario si la autenticación es exitosa, None en caso contrario.
        """ 

        try:
            query = "SELECT * FROM users WHERE Correo = ? AND Contraseña = ?"
            user = fetch_one(query, (email, password))
            if user:
                return {"Correo": user[0], "Nombre": user[1]}  # Ajustar según la estructura de la tabla
            return None
        except Exception as e:
            logging.error(f"Error al autenticar usuario: {e}")
            return None
