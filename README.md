# proyecto-inventario

Creación de un software para generar inventarios.

## Requisitos

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/tu_usuario/proyecto-inventario.git
    cd proyecto-inventario
    ```

2. Crea un entorno virtual y actívalo:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instala las dependencias:
    ```sh
    pip install --upgrade pip setuptools wheel
    pip install numpy==1.21.0
    pip install -r requirements.txt --no-deps
    ```

## Ejecución

1. Ejecuta el script `migrar_db.py` para crear la base de datos:
    ```sh
    python migrar_db.py
    ```

2. Inicia la aplicación Flask:
    ```sh
    python run.py
    ```

3. Abre tu navegador web y navega a `http://127.0.0.1:5000/`.

## Uso de la API

### Registrar un usuario

- **URL:** `/register`
- **Método:** `POST`
- **Cuerpo JSON:**
    ```json
    {
        "email": "newuser@example.com",
        "password": "newpassword",
        "name": "New User"
    }
    ```

### Iniciar sesión

- **URL:** `/login`
- **Método:** `POST`
- **Cuerpo JSON:**
    ```json
    {
        "email": "newuser@example.com",
        "password": "newpassword"
    }
    ```

### Actualizar inventario

- **URL:** `/inventory/update`
- **Método:** `POST`
- **Cuerpo JSON:**
    ```json
    {
        "product_id": "P001",
        "quantity": 10,
        "movement_type": "Entrada",
        "user": "Admin",
        "description": "Stock inicial",
        "reference_document": "DOC123"
    }
    ```

### Registrar una venta

- **URL:** `/sales/register`
- **Método:** `POST`
- **Cuerpo JSON:**
    ```json
    {
        "client": "Cliente 1",
        "payment_method": "Efectivo",
        "user": "Admin",
        "details": [
            {
                "product_id": "P001",
                "quantity": 2,
                "price_unit": 100.0,
                "discount": 0.0
            }
        ]
    }
    ```

### Registrar una compra

- **URL:** `/purchases/register`
- **Método:** `POST`
- **Cuerpo JSON:**
    ```json
    {
        "supplier": "Proveedor 1",
        "user": "Admin",
        "details": [
            {
                "product_id": "P001",
                "quantity": 10,
                "price_unit": 50.0
            }
        ]
    }
    ```

### Generar un informe de ventas

- **URL:** `/reports/sales`
- **Método:** `GET`
- **Parámetros de consulta:**
    - `start_date`: Fecha inicial (formato 'YYYY-MM-DD')
    - `end_date`: Fecha final (formato 'YYYY-MM-DD')

## Pruebas

Para ejecutar las pruebas unitarias y de integración, utiliza el siguiente comando:

```sh
pytest