import sqlite3
from app.user_management import hash_password

DATABASE = 'inventario.db'

def update_user_password(email, new_password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    hashed_password = hash_password(new_password)
    cursor.execute("UPDATE users SET Contraseña = ? WHERE Correo = ?", (hashed_password, email))
    conn.commit()
    conn.close()
    print(f"Contraseña actualizada para el usuario: {email}")

if __name__ == "__main__":
    update_user_password('admin@example.com', 'password')
