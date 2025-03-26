import time
import unittest
from user_management import UserManager
from unittest.mock import patch  # Importar patch para simular funciones


class TestUserManagement(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManager()

    def test_create_user(self):
        # Genera un correo único para cada prueba
        import time
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
