import unittest
<<<<<<< HEAD
from unittest.mock import patch, MagicMock, call
import sqlite3
from migrar_db import main
=======
from unittest.mock import patch, MagicMock
from migrar_db import connect_db, load_products, load_users, load_purchases, load_sales
import pandas as pd
from io import StringIO
>>>>>>> c78e6b52bc7d26d1ed819ed8ad0afc2dd8268633

class TestMigrarDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_cursor = MagicMock()
        cls.mock_connection = MagicMock()
        cls.mock_connection.cursor.return_value = cls.mock_cursor

<<<<<<< HEAD
    @patch('migrar_db.sqlite3.connect')
    @patch('migrar_db.open', new_callable=unittest.mock.mock_open, read_data="Correo,Contraseña,Nombre\nadmin@example.com,password,Admin\nuser@example.com,1234,User")



    def test_insert_users(self, mock_open, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Sobreescribir la función que verifica si existen columnas
        # para que siempre devuelva True
        with patch('migrar_db.column_exists', return_value=True):
            main()

        # Busca una llamada similar en lugar de exigir formato exacto
        found = False
        for call_args in mock_cursor.execute.call_args_list:
            query = call_args[0][0].strip().replace('\n', ' ').replace('    ', ' ')
            if ('INSERT INTO users' in query and 
                'Correo' in query and 
                'Contraseña' in query and 
                'Nombre' in query):
                params = call_args[0][1]
                if params == ('admin@example.com', 'password', 'Admin'):
                    found = True
                    break
        
        self.assertTrue(found, "No se encontró la inserción del usuario admin con los parámetros correctos")

    @patch('migrar_db.sqlite3.connect')
    @patch('migrar_db.open', new_callable=unittest.mock.mock_open, read_data="ID_Producto,Nombre,Stock_Actual,Stock_Minimo,Precio_Unitario\nP001,Producto 1,50,10,100.0\nP002,Producto 2,20,5,200.0")




    def test_insert_products(self, mock_open, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Sobreescribir la función que verifica si existen columnas
        # para que siempre devuelva True
        with patch('migrar_db.column_exists', return_value=True):
            main()

        # Busca una llamada similar en lugar de exigir formato exacto
        found = False
        for call_args in mock_cursor.execute.call_args_list:
            if len(call_args[0]) < 2:
                continue  # Saltamos llamadas sin parámetros
                
            query = call_args[0][0].strip().replace('\n', ' ').replace('    ', ' ')
            if ('INSERT INTO products' in query and 
                'ID_Producto' in query and 
                'Nombre' in query and 
                'Stock_Actual' in query and 
                'Stock_Minimo' in query and 
                'Precio_Unitario' in query):
                params = call_args[0][1]
                if params == ('P001', 'Producto 1', 50, 10, 100.0):
                    found = True
                    break
        
        self.assertTrue(found, "No se encontró la inserción del producto P001 con los parámetros correctos")

if __name__ == "__main__":
    unittest.main()
=======
    def test_load_products(self):
        """Prueba la carga de productos desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            # Simular la existencia de un archivo
            with patch('builtins.open', unittest.mock.mock_open(read_data="ID_Producto,Nombre,Stock_Actual,Stock_Minimo,Precio_Unitario\nP001,Producto 1,50,10,100.0")):
                load_products(self.mock_cursor)
                self.mock_cursor.execute.assert_called_with('INSERT INTO products (ID_Producto, Nombre, Stock_Actual, Stock_Minimo, Precio_Unitario) VALUES (?, ?, ?, ?, ?)', ('P001', 'Producto 1', 50, 10, 100.0))

                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)
                self.mock_cursor.execute.assert_called_with('INSERT INTO products (ID_Producto, Nombre, Stock_Actual, Stock_Minimo, Precio_Unitario) VALUES (?, ?, ?, ?, ?)', ('P001', 'Producto 1', 50, 10, 100.0))


    def test_load_users(self):
        """Prueba la carga de usuarios desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            with patch('builtins.open', unittest.mock.mock_open(read_data="Correo,Contraseña,Nombre\nadmin@example.com,password,Admin")):
                load_users(self.mock_cursor)
                self.mock_cursor.execute.assert_called_with('INSERT INTO users (Correo, Contraseña, Nombre) VALUES (?, ?, ?)', ('admin@example.com', 'password', 'Admin'))

                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)
                self.mock_cursor.execute.assert_called_with('INSERT INTO users (Correo, Contraseña, Nombre) VALUES (?, ?, ?)', ('admin@example.com', 'password', 'Admin'))


    def test_load_purchases(self):
        """Prueba la carga de compras desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            data = "ID_Compra,Fecha,Proveedor,Total,Estado,Usuario,Observaciones\nC001,2023-01-01,Supplier 1,100.0,Completed,User1,First purchase"
            with patch('pandas.read_csv', return_value=pd.read_csv(StringIO(data))):
                load_purchases(self.mock_cursor)
                self.mock_cursor.execute.assert_called_with('INSERT INTO purchases (ID_Compra, Fecha, Proveedor, Total, Estado, Usuario, Observaciones) VALUES (?, ?, ?, ?, ?, ?, ?)', ('C001', '2023-01-01', 'Supplier 1', 100.0, 'Completed', 'User1', 'First purchase'))

                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)
                self.mock_cursor.execute.assert_called_with('INSERT INTO purchases (ID_Compra, Fecha, Proveedor, Total, Estado, Usuario, Observaciones) VALUES (?, ?, ?, ?, ?, ?, ?)', ('C001', '2023-01-01', 'Supplier 1', 100.0, 'Completed', 'User1', 'First purchase'))


    def test_load_sales(self):
        """Prueba la carga de ventas desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            data = "ID_Venta,Fecha,Cliente,Total,Estado,Usuario,Método_Pago,Observaciones\nV001,2023-01-01,Client 1,150.0,Completed,User1,Credit Card,First sale"
            with patch('pandas.read_csv', return_value=pd.read_csv(StringIO(data))):
                load_sales(self.mock_cursor)
                self.mock_cursor.execute.assert_called_with('INSERT INTO sales (ID_Venta, Fecha, Cliente, Total, Estado, Usuario, Método_Pago, Observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', ('V001', '2023-01-01', 'Client 1', 150.0, 'Completed', 'User1', 'Credit Card', 'First sale'))

                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)
                self.mock_cursor.execute.assert_called_with('INSERT INTO sales (ID_Venta, Fecha, Cliente, Total, Estado, Usuario, Método_Pago, Observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', ('V001', '2023-01-01', 'Client 1', 150.0, 'Completed', 'User1', 'Credit Card', 'First sale'))
>>>>>>> c78e6b52bc7d26d1ed819ed8ad0afc2dd8268633
