import unittest
from unittest.mock import patch, MagicMock
from migrar_db import connect_db, load_products, load_users, load_purchases, load_sales
import pandas as pd
from io import StringIO

class TestMigrarDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_cursor = MagicMock()
        cls.mock_connection = MagicMock()
        cls.mock_connection.cursor.return_value = cls.mock_cursor

    def test_load_products(self):
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            # Simulate the existence of a file
            with patch('builtins.open', unittest.mock.mock_open(read_data="ID_Producto,Nombre,Stock_Actual,Stock_Minimo,Precio_Unitario\nP001,Producto 1,50,10,100.0")):
                load_products(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

    def test_load_users(self):
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            with patch('builtins.open', unittest.mock.mock_open(read_data="Correo,Contraseña,Nombre\nadmin@example.com,password,Admin")):
                load_users(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

    def test_load_purchases(self):
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            data = "ID_Compra,Fecha,Proveedor,Total,Estado,Usuario,Observaciones\nC001,2023-01-01,Supplier 1,100.0,Completed,User1,First purchase"
            with patch('pandas.read_csv', return_value=pd.read_csv(StringIO(data))):
                load_purchases(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

    def test_load_sales(self):
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            data = "ID_Venta,Fecha,Cliente,Total,Estado,Usuario,Método_Pago,Observaciones\nV001,2023-01-01,Client 1,150.0,Completed,User1,Credit Card,First sale"
            with patch('pandas.read_csv', return_value=pd.read_csv(StringIO(data))):
                load_sales(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

if __name__ == '__main__':
    unittest.main()
