import unittest
from user_management import create_user, update_user, delete_user

class TestUserManagement(unittest.TestCase):

    def test_create_user(self):
        result = create_user("test_user@example.com", "password123", ["user"])

        self.assertTrue(result)

    def test_update_user(self):
        # Primero, creamos un usuario para actualizar
        create_user("update_user@example.com", "password123", ["user"])

        result = update_user("update_user@example.com", "newpassword123")


        self.assertTrue(result)

    def test_delete_user(self):
        # Primero, creamos un usuario para eliminar
        create_user("delete_user@example.com", "password123", ["user"])

        result = delete_user("delete_user@example.com")


        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
