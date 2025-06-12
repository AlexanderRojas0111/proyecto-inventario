from app.data_manager import execute_query, fetch_all, fetch_one


class InventoryManagement:
    def __init__(self, db):
        self.db = db

    def get_current_stock(self, product_id):
        query = "SELECT Stock_Actual FROM products WHERE ID_Producto = ?"
        result = fetch_one(query, (product_id,))
        if result:
            return result["Stock_Actual"]
        return None

    def adjust_inventory(self, product_id, quantity, movement_type):
        current_stock = self.get_current_stock(product_id)
        if current_stock is None:
            return False

        new_stock = (
            current_stock + quantity
            if movement_type == "add"
            else current_stock - quantity
        )
        if new_stock < 0:
            return False

        query = "UPDATE products SET Stock_Actual = ? WHERE ID_Producto = ?"
        execute_query(query, (new_stock, product_id))
        return True


from app.data_manager import get_db_connection


def update_inventory(product_id, quantity, movement_type, user, description, reference):
    db = get_db_connection()
    inventory_manager = InventoryManagement(db)
    success = inventory_manager.adjust_inventory(product_id, quantity, movement_type)
    if success:
        query = """
        INSERT INTO inventory (ID_Producto, Cantidad, Tipo_Movimiento, Usuario, Descripción, Documento_Referencia, Fecha)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """
        execute_query(
            query, (product_id, quantity, movement_type, user, description, reference)
        )
    return success


def get_current_stock(product_id=None):
    """Obtiene el stock actual de un producto específico o de todos los productos."""
    try:
        if product_id:
            query = "SELECT Stock_Actual FROM products WHERE ID_Producto = ?"
            result = fetch_one(query, (product_id,))
            return result["Stock_Actual"] if result else None
        else:
            query = (
                "SELECT ID_Producto, Nombre, Stock_Actual, Stock_Minimo FROM products"
            )
            return fetch_all(query)
    except Exception as e:
        print(f"Error al obtener el stock actual: {e}")
        return None


def get_low_stock_products():
    """Obtiene los productos cuyo stock está por debajo del mínimo requerido."""
    try:
        query = "SELECT * FROM products WHERE Stock_Actual < Stock_Minimo"
        return fetch_all(query)
    except Exception as e:
        print(f"Error al obtener productos con stock bajo: {e}")
        return []


def get_product_movements(product_id, start_date=None, end_date=None):
    """Obtiene los movimientos de un producto en un período de tiempo."""
    try:
        query = "SELECT * FROM inventory WHERE ID_Producto = ?"
        params = [product_id]
        if start_date:
            query += " AND Fecha >= ?"
            params.append(start_date)
        if end_date:
            query += " AND Fecha <= ?"
            params.append(end_date)
        query += " ORDER BY Fecha DESC"
        return fetch_all(query, params)
    except Exception as e:
        print(f"Error al obtener movimientos del producto: {e}")
        return []


def calculate_inventory_value():
    """Calcula el valor total del inventario."""
    try:
        query = "SELECT SUM(Stock_Actual * Precio_Unitario) AS Total FROM products"
        result = fetch_one(query)
        return result["Total"] if result else 0.0
    except Exception as e:
        print(f"Error al calcular el valor del inventario: {e}")
        return 0.0


def adjust_inventory(product_id, new_quantity, user, reason):
    """Realiza un ajuste de inventario cuando hay discrepancias."""
    try:
        query = "SELECT Stock_Actual FROM products WHERE ID_Producto = ?"
        result = fetch_one(query, (product_id,))
        if not result:
            return False
        current_stock = result["Stock_Actual"]
        difference = new_quantity - current_stock
        movement_type = "Entrada" if difference > 0 else "Salida"
        update_inventory(
            product_id,
            abs(difference),
            movement_type,
            user,
            f"Ajuste de inventario: {reason}",
            "Ajuste manual",
        )
        query = "UPDATE products SET Stock_Actual = ? WHERE ID_Producto = ?"
        execute_query(query, (new_quantity, product_id))
        return True
    except Exception as e:
        print(f"Error al ajustar el inventario: {e}")
        return False
