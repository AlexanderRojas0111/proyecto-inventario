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