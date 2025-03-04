import unittest
from inventory import update_inventory, get_current_stock, get_low_stock_products, get_product_movements, calculate_inventory_value, adjust_inventory

class TestInventoryManagement(unittest.TestCase):
    def setUp(self):
        # Configurar la base de datos para pruebas
        self.database = 'inventario_test.db'
        self.setup_database()

    def setup_database(self):
        import sqlite3
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            ID_Producto TEXT PRIMARY KEY,
            Nombre TEXT,
            Stock_Actual INTEGER,
            Stock_Minimo INTEGER,
            Precio_Unitario REAL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ID_Producto TEXT,
            Cantidad INTEGER,
            Tipo_Movimiento TEXT,
            Usuario TEXT,
            Descripción TEXT,
            Documento_Referencia TEXT,
            Fecha TIMESTAMP
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            Correo TEXT PRIMARY KEY,
            Contraseña TEXT,
            Nombre TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            ID_Compra TEXT PRIMARY KEY,
            Fecha TIMESTAMP,
            Proveedor TEXT,
            Total REAL,
            Estado TEXT,
            Usuario TEXT,
            Observaciones TEXT
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            ID_Venta TEXT PRIMARY KEY,
            Fecha TIMESTAMP,
            Cliente TEXT,
            Total REAL,
            Estado TEXT,
            Usuario TEXT,
            Método_Pago TEXT,
            Observaciones TEXT
        )
        ''')
        conn.commit()
        conn.close()

    def test_update_inventory(self):
        try:
            update_inventory("P001", 10, "Entrada", "Admin", "Stock inicial", "DOC123")
            print("Prueba de actualización de inventario exitosa.")
        except Exception as e:
            self.fail(f"Prueba de actualización de inventario fallida: {e}")

    def test_get_current_stock(self):
        try:
            stock = get_current_stock("P001")
            self.assertIsNotNone(stock, "El stock no debería ser None")
            print("Prueba de obtención de stock actual exitosa.")
        except Exception as e:
            self.fail(f"Prueba de obtención de stock actual fallida: {e}")

    def test_get_low_stock_products(self):
        try:
            low_stock_products = get_low_stock_products()
            self.assertIsInstance(low_stock_products, list, "El resultado debería ser una lista")
            print("Prueba de obtención de productos con bajo stock exitosa.")
        except Exception as e:
            self.fail(f"Prueba de obtención de productos con bajo stock fallida: {e}")

    def test_get_product_movements(self):
        try:
            movements = get_product_movements("P001")
            self.assertIsInstance(movements, list, "El resultado debería ser una lista")
            print("Prueba de obtención de movimientos de producto exitosa.")
        except Exception as e:
            self.fail(f"Prueba de obtención de movimientos de producto fallida: {e}")

    def test_calculate_inventory_value(self):
        try:
            value = calculate_inventory_value()
            self.assertIsInstance(value, float, "El resultado debería ser un float")
            print("Prueba de cálculo del valor del inventario exitosa.")
        except Exception as e:
            self.fail(f"Prueba de cálculo del valor del inventario fallida: {e}")

    def test_adjust_inventory(self):
        try:
            result = adjust_inventory("P001", 60, "Admin", "Ajuste de prueba")
            self.assertTrue(result, "El ajuste de inventario debería ser exitoso")
            print("Prueba de ajuste de inventario exitosa.")
        except Exception as e:
            self.fail(f"Prueba de ajuste de inventario fallida: {e}")

if __name__ == "__main__":
    unittest.main()