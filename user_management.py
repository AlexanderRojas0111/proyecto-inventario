import sqlite3
from data_manager import fetch_all, fetch_one

def authenticate_user(email, password):
    """Autentica un usuario."""
    try:
        query = '''
        SELECT * FROM users WHERE Correo = ? AND Contraseña = ?
        '''
        user = fetch_one(query, (email, password))
        if user:
            return user
        return None
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
        return None

def get_user_roles(user_id):
    """Obtiene los roles de un usuario."""
    try:
        query = '''
        SELECT roles.* FROM roles
        JOIN user_roles ON roles.ID_Rol = user_roles.ID_Rol
        WHERE user_roles.ID_Usuario = ?
        '''
        user_roles_data = fetch_all(query, (user_id,))
        return user_roles_data
    except Exception as e:
        print(f"Error al obtener roles del usuario: {e}")
        return []

def get_role_permissions(role_id):
    """Obtiene los permisos de un rol."""
    try:
        query = '''
        SELECT permissions.* FROM permissions
        JOIN role_permissions ON permissions.ID_Permiso = role_permissions.ID_Permiso
        WHERE role_permissions.ID_Rol = ?
        '''
        role_permissions_data = fetch_all(query, (role_id,))
        return role_permissions_data
    except Exception as e:
        print(f"Error al obtener permisos del rol: {e}")
        return []

def user_has_permission(user_id, permission_name):
    """Verifica si un usuario tiene un permiso específico por nombre."""
    try:
        query = '''
        SELECT permissions.* FROM permissions
        JOIN role_permissions ON permissions.ID_Permiso = role_permissions.ID_Permiso
        JOIN user_roles ON role_permissions.ID_Rol = user_roles.ID_Rol
        WHERE user_roles.ID_Usuario = ? AND permissions.Nombre = ?
        '''
        permission_data = fetch_all(query, (user_id, permission_name))
        if permission_data:
            return True
        return False
    except Exception as e:
        print(f"Error al verificar permisos del usuario: {e}")
        return False

# Ejemplo de uso (asumiendo que tienes datos en la base de datos):
if __name__ == "__main__":
    # Suponiendo que tienes un usuario con ID 1, un rol con ID 1, y un permiso con nombre "editar_productos"
    user_id = 1
    permission_name = "editar_productos"

    if user_has_permission(user_id, permission_name):
        print(f"El usuario {user_id} tiene el permiso {permission_name}.")
    else:
        print(f"El usuario {user_id} no tiene el permiso {permission_name}.")

    user_roles = get_user_roles(user_id)
    print(f"Roles del usuario {user_id}: {user_roles}")

    if user_roles:
        role_id = user_roles[0]["ID_Rol"]
        role_permissions = get_role_permissions(role_id)
        print(f"Permisos del rol {role_id}: {role_permissions}")