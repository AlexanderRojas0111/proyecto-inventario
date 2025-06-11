<<<<<<< HEAD
import pytest
from app.user_management import register_user, authenticate_user
from app.data_manager import execute_query

@pytest.fixture
def setup_database():
    # Configuración de la base de datos para pruebas
    execute_query('DELETE FROM users')
    yield
    execute_query('DELETE FROM users')

def test_register_user(setup_database):
    register_user('test@example.com', 'password123', 'Test User')
    user = authenticate_user('test@example.com', 'password123')
    assert user is not None
    assert user['email'] == 'test@example.com'
    assert user['name'] == 'Test User'

def test_authenticate_user_invalid_password(setup_database):
    register_user('test@example.com', 'password123', 'Test User')
    user = authenticate_user('test@example.com', 'wrongpassword')
    assert user is None
=======
import time
import unittest
from user_management import UserManager
from unittest.mock import patch  # Importar patch para simular funciones


class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager()

    def test_create_user(self):
        # Genera un correo único para cada prueba
        unique_email = f"test{int(time.time())}@example.com"
        
        with patch('data_manager.execute_query') as mock_execute_query:  # Simular execute_query
            result = self.user_manager.create_user(unique_email, "password123", "Test User")

        self.assertTrue(result)

    def test_update_user(self):
        """Prueba la actualización de un usuario existente.""" 
        unique_email = f"test_update{int(time.time())}@example.com"
        self.user_manager.create_user(unique_email, "password123", "Test User")
        with patch('data_manager.execute_query') as mock_execute_query:  # Simular execute_query
            result = self.user_manager.update_user(unique_email, "newpassword123")

        self.assertTrue(result)

    def test_delete_user(self):
        """Prueba la eliminación de un usuario existente.""" 
        unique_email = f"test_delete{int(time.time())}@example.com"
        self.user_manager.create_user(unique_email, "password123", "Test User")
        with patch('data_manager.execute_query') as mock_execute_query:  # Simular execute_query
            result = self.user_manager.delete_user(unique_email)

        self.assertTrue(result)

    def test_authenticate_user(self):
        """Prueba la autenticación de un usuario existente.""" 
        unique_email = f"test_authenticate{int(time.time())}@example.com"
        self.user_manager.create_user(unique_email, "password123", "Test User")
        with patch('data_manager.fetch_one') as mock_fetch_one:  # Simular fetch_one
            mock_fetch_one.return_value = (unique_email, "Test User")  # Simular el retorno de un usuario
            user_info = self.user_manager.authenticate_user(unique_email, "password123")

        self.assertIsNotNone(user_info)
        self.assertEqual(user_info["Correo"], unique_email)


if __name__ == '__main__':
    unittest.main()

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
        """Prueba la carga de productos desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            # Simular la existencia de un archivo
            with patch('builtins.open', unittest.mock.mock_open(read_data="ID_Producto,Nombre,Stock_Actual,Stock_Minimo,Precio_Unitario\nP001,Producto 1,50,10,100.0")):
                load_products(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

    def test_load_users(self):
        """Prueba la carga de usuarios desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            with patch('builtins.open', unittest.mock.mock_open(read_data="Correo,Contraseña,Nombre\nadmin@example.com,password,Admin")):
                load_users(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

    def test_load_purchases(self):
        """Prueba la carga de compras desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            data = "ID_Compra,Fecha,Proveedor,Total,Estado,Usuario,Observaciones\nC001,2023-01-01,Supplier 1,100.0,Completed,User1,First purchase"
            with patch('pandas.read_csv', return_value=pd.read_csv(StringIO(data))):
                load_purchases(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

    def test_load_sales(self):
        """Prueba la carga de ventas desde un archivo CSV."""
        with patch('migrar_db.connect_db', return_value=(self.mock_connection, self.mock_cursor)):
            data = "ID_Venta,Fecha,Cliente,Total,Estado,Usuario,Método_Pago,Observaciones\nV001,2023-01-01,Client 1,150.0,Completed,User1,Credit Card,First sale"
            with patch('pandas.read_csv', return_value=pd.read_csv(StringIO(data))):
                load_sales(self.mock_cursor)
                self.assertTrue(self.mock_cursor.execute.called)
                self.assertGreaterEqual(self.mock_cursor.execute.call_count, 1)

if __name__ == '__main__':
    unittest.main()

>>>>>>> c78e6b52bc7d26d1ed819ed8ad0afc2dd8268633
