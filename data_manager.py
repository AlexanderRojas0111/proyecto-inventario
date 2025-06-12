import sqlite3
import logging

DATABASE = "inventario.db"

# Configuración del registro
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def connect_db():
    """Establece una conexión con la base de datos SQLite."""
    try:
        connection = sqlite3.connect(DATABASE)
        logging.info("Conexión a la base de datos establecida.")
        return connection
    except sqlite3.Error as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        print(
            "No se pudo establecer la conexión con la base de datos. Verifique los detalles en el registro."
        )
        return None


def execute_query(query, params=()):
    """Ejecuta una consulta en la base de datos."""
    with connect_db() as connection:
        if connection is None:
            return  # Salir si no hay conexión
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            connection.commit()
            logging.info(
                f"Consulta ejecutada correctamente: {query}, parámetros: {params}"
            )
            return cursor
        except sqlite3.Error as e:
            logging.error(
                f"Error al ejecutar la consulta: {e}. Consulta: {query}, Parámetros: {params}"
            )
            print(
                "No se pudo ejecutar la consulta. Verifique los detalles en el registro."
            )


def fetch_all(query, params=()):
    """Recupera todos los resultados de una consulta."""
    with connect_db() as connection:
        if connection is None:
            return []
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            logging.info(
                f"Datos recuperados correctamente para la consulta: {query}, parámetros: {params}"
            )
            return results
        except sqlite3.Error as e:
            logging.error(
                f"Error al recuperar datos: {e}. Consulta: {query}, Parámetros: {params}"
            )
            print(
                "No se pudo recuperar los datos. Verifique los detalles en el registro."
            )
            return []


def fetch_one(query, params=()):
    """Recupera un único resultado de una consulta."""
    with connect_db() as connection:
        if connection is None:
            return None
        cursor = connection.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
            logging.info(
                f"Dato recuperado correctamente: {result} para la consulta: {query}, parámetros: {params}"
            )
            return result
        except sqlite3.Error as e:
            logging.error(
                f"Error al recuperar el dato: {e}. Consulta: {query}, Parámetros: {params}"
            )
            print(
                "No se pudo recuperar el dato. Verifique los detalles en el registro."
            )
            return None


def load_data(table_name):
    """Cargar todos los datos de la tabla especificada."""
    query = f"SELECT * FROM {table_name}"
    return fetch_all(query)


def save_data(table_name, data):
    """Guardar datos en la tabla especificada."""
    if not data:
        logging.error(f"Error: No hay datos para insertar en la tabla '{table_name}'.")
        print(f"Error: No hay datos para insertar en la tabla '{table_name}'.")
        return

    placeholders = ", ".join(["?"] * len(data[0]))
    query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    with connect_db() as connection:
        if connection is None:
            return
        cursor = connection.cursor()
        try:
            cursor.executemany(query, data)
            connection.commit()
            logging.info(
                f"Datos guardados correctamente en '{table_name}'. Datos: {data}"
            )
        except sqlite3.Error as e:
            logging.error(
                f"Error al guardar datos: {e}. Consulta: {query}, Parámetros: {data}"
            )
            print(
                "No se pudo guardar los datos. Verifique los detalles en el registro."
            )


if __name__ == "__main__":
    # Ejemplo de uso
    sample_data = [
        ("P001", "Producto 1", 50, 10, 100.0),
        ("P002", "Producto 2", 30, 5, 200.0),
    ]
    save_data(
        "products", sample_data
    )  # Asegúrate de que la tabla products exista en tu base de datos
    all_products = load_data("products")
    print("Todos los productos:", all_products)
