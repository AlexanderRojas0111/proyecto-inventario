import sqlite3


def verificar_usuario(correo, contraseña):

    # Conectar a la base de datos
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    # Ejecutar la consulta SQL
    query = "SELECT * FROM users WHERE Correo = ? AND Contraseña = ?;"
    cursor.execute(query, (correo, contraseña))

    # Obtener los resultados
    resultados = cursor.fetchall()
    if not resultados:
        print("No se encontró ningún usuario con las credenciales proporcionadas.")
        return

    # Verificar si se encontraron resultados
    print("Usuario encontrado:")
    for row in resultados:
        print(", ".join(map(str, row)))

    # Cerrar la conexión
    conn.close()


if __name__ == "__main__":
    verificar_usuario("admin@example.com", "password")  # Ejemplo de uso
