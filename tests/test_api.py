import pytest
from app import app
from app.user_management import UserManager


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register_user():
    UserManager.register_user("test@example.com", "password123", "Test User")
    user = UserManager.authenticate_user("test@example.com", "password123")
    assert user is not None
    assert user["Correo"] == "test@example.com"
    assert user["Nombre"] == "Test User"


def test_login(client):
    # Primero, registramos un usuario
    UserManager.register_user("testuser@example.com", "testpassword", "Test User")

    # Luego, intentamos iniciar sesión con el usuario registrado
    response = client.post(
        "/login", json={"email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_update_inventory(client):
    response = client.post(
        "/inventory/update",
        json={
            "product_id": "P001",
            "quantity": 10,
            "movement_type": "Entrada",
            "user": "Admin",
            "description": "Stock inicial",
            "reference_document": "DOC123",
        },
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory updated successfully"


def test_register_sale(client):
    response = client.post(
        "/sales/register",
        json={
            "client": "Cliente 1",
            "payment_method": "Efectivo",
            "user": "Admin",
            "details": [
                {
                    "product_id": "P001",
                    "quantity": 2,
                    "price_unit": 100.0,
                    "discount": 0.0,
                }
            ],
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Sale registered successfully"


def test_register_purchase(client):
    response = client.post(
        "/purchases/register",
        json={
            "supplier": "Proveedor 1",
            "user": "Admin",
            "details": [{"product_id": "P001", "quantity": 10, "price_unit": 50.0}],
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Purchase registered successfully"


def test_generate_sales_report(client):
    response = client.get(
        "/reports/sales",
        query_string={"start_date": "2022-01-01", "end_date": "2022-12-31"},
    )
    assert response.status_code == 200
    assert "report" in response.get_json()
