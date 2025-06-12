import pytest
from app.user_management import UserManager
from app.data_manager import execute_query


@pytest.fixture
def setup_database():
    # Configuración de la base de datos para pruebas
    execute_query("DELETE FROM users")
    yield
    execute_query("DELETE FROM users")


def test_register_user(setup_database):
    um = UserManager()
    um.create_user("test@example.com", "password123", "Test User")
    user = um.authenticate_user("test@example.com", "password123")
    assert user is not None
    assert user["Correo"] == "test@example.com"
    assert user["Nombre"] == "Test User"


def test_authenticate_user_invalid_password(setup_database):
    um = UserManager()
    um.create_user("test@example.com", "password123", "Test User")
    user = um.authenticate_user("test@example.com", "wrongpassword")
    assert user is None
