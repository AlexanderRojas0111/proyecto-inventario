import sqlite3
from flask_bcrypt import Bcrypt
from app.data_manager import execute_query, fetch_one

bcrypt = Bcrypt()

DATABASE = 'inventario.db'

def hash_password(password):
    # Generar una sal y hashear la contraseña
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(hashed_password, user_password):
    # Verificar la contraseña ingresada con la contraseña hasheada
    return bcrypt.check_password_hash(hashed_password, user_password)

def authenticate_user(email, password):
    query = '''
    SELECT * FROM users WHERE Correo = ?
    '''
    user = fetch_one(query, (email,))
    if user and check_password(user['Contraseña'], password):
        return {'email': user['Correo'], 'name': user['Nombre']}
    return None

def register_user(email, password, name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (Correo, Contraseña, Nombre) VALUES (?, ?, ?)", (email, hashed_password, name))
        conn.commit()
        print(f"Usuario registrado: {email}")
    except sqlite3.IntegrityError:
        print(f"Error: El usuario con correo {email} ya existe.")
    conn.close()