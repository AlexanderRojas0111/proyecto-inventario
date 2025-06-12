import sqlite3


def agregar_usuario(correo, contraseña, nombre):

    # Conectar a la base de datos
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    # Ejecutar la consulta SQL para insertar o reemplazar un nuevo usuario
    cursor.execute(
        "INSERT OR REPLACE INTO users (Correo, Contraseña, Nombre) VALUES (?, ?, ?);",
        (correo, contraseña, nombre),
    )

    # Guardar los cambios
    conn.commit()
    print("Usuario agregado exitosamente.")

    # Cerrar la conexión
    conn.close()


if __name__ == "__main__":
    agregar_usuario("admin@example.com", "password", "Admin User")  # Ejemplo de usuario
