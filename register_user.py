import sqlite3
from app.user_management import hash_password

DATABASE = "inventario.db"


def register_user(email, password, name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (Correo, Contraseña, Nombre) VALUES (?, ?, ?)",
            (email, hashed_password, name),
        )
        conn.commit()
        print(f"Usuario registrado: {email}")
    except sqlite3.IntegrityError:
        print(f"Error: El usuario con correo {email} ya existe.")
    conn.close()


if __name__ == "__main__":
    register_user("admin@example.com", "password", "Admin")
