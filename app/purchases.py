import sqlite3
from app.data_manager import execute_query, fetch_all, fetch_one
from app.inventory import update_inventory, InventoryManagement  # Asegúrate de que InventoryManagement esté en el módulo inventory
from datetime import datetime

# Definir la conexión a la base de datos
DATABASE = 'inventario.db'

def get_db_connection():
    return sqlite3.connect(DATABASE)

db = get_db_connection()

def register_purchase(product_id, quantity, supplier_id, cost, db):
    """
    Registra una compra de producto.
    
    Args:
        product_id (int): ID del producto comprado
        quantity (int): Cantidad comprada
        supplier_id (int): ID del proveedor
        cost (float): Costo total de la compra
        
    Returns:
        dict: Información de la compra en caso de éxito
        None: En caso de error
    """
    # Fetch available products for display
    available_products = fetch_all("SELECT ID_Producto, Nombre FROM products;")
    print("Productos disponibles:")
    for product in available_products:
        print(f"ID: {product['ID_Producto']}, Nombre: {product['Nombre']}")
    
    # Ajustar el inventario (aumentar stock)
    inventory_manager = InventoryManagement(db)

    """
    Registra una compra de producto.
    
    Args:
        product_id (int): ID del producto comprado
        quantity (int): Cantidad comprada
        supplier_id (int): ID del proveedor
        cost (float): Costo total de la compra
        
    Returns:
        dict: Información de la compra en caso de éxito
        None: En caso de error
    """
    # Ajustar el inventario (aumentar stock)
    inventory_manager = InventoryManagement(db)
    success = inventory_manager.adjust_inventory(product_id, quantity, 'add')
    
    if not success:
        return None
    
    # Registrar la compra en la base de datos
    purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        result = db.execute(
            """
            INSERT INTO purchases (ID_Producto, Cantidad, ID_Proveedor, Costo, Fecha)
            VALUES (?, ?, ?, ?, ?)
            RETURNING ID_Compra
            """,
            (product_id, quantity, supplier_id, cost, purchase_date)
        )
        
        # Verificar el resultado y obtener el ID de compra
        if result:
            # Si result es una tupla, el ID de compra estará en la primera posición
            if isinstance(result, tuple) or isinstance(result, list):
                purchase_id = result[0]
            # Si result es un diccionario, obtenemos el ID_Compra
            elif isinstance(result, dict):
                purchase_id = result.get('ID_Compra')
            # Si result es un valor escalar (como un entero), lo usamos directamente
            else:
                purchase_id = result
            
            # Crear y devolver un diccionario con la información de la compra
            purchase_info = {
                'id': purchase_id,
                'product_id': product_id,
                'quantity': quantity,
                'supplier_id': supplier_id,
                'cost': cost,
                'date': purchase_date
            }
            
            return purchase_info
        
    except Exception as e:
        print(f"Error al registrar la compra: {e}")
    
    return None

def add_purchase_detail(purchase_id, product_id, quantity, price_unit):
    subtotal = quantity * price_unit
    query = '''
    INSERT INTO purchase_details (ID_Compra, ID_Producto, Cantidad, Precio_Unitario, Subtotal)
    VALUES (?, ?, ?, ?, ?)
    '''
    execute_query(query, (purchase_id, product_id, quantity, price_unit, subtotal))
    update_inventory(product_id, quantity, "Entrada", "Sistema", f"Compra {purchase_id}", purchase_id)
    update_purchase_total(purchase_id)

def update_purchase_total(purchase_id):
    """Calcula y actualiza el total de una compra."""
    query = '''
    SELECT SUM(Subtotal) FROM purchase_details WHERE ID_Compra = ?
    '''
    result = fetch_one(query, (purchase_id,))
    
    # Verificar si result es None o si result[0] es None
    if result is None or result[0] is None:
        total = 0
    else:
        total = result[0]
    
    update_query = '''
    UPDATE purchases SET Total = ? WHERE ID_Compra = ?
    '''
    execute_query(update_query, (total, purchase_id))
    return total

def cancel_purchase(purchase_id, cancellation_reason, user):
    """Cancela una compra y actualiza el inventario."""
    query = '''
    SELECT Estado FROM purchases WHERE ID_Compra = ?
    '''
    current_status = fetch_one(query, (purchase_id,))
    if not current_status or current_status[0] == "Cancelada":
        return False

    query = '''
    UPDATE purchases SET Estado = 'Cancelada', Observaciones = Observaciones || ' | CANCELACIÓN: ' || ? || ' por ' || ? || ' en ' || datetime('now')
    WHERE ID_Compra = ?
    '''
    execute_query(query, (cancellation_reason, user, purchase_id))

    if current_status[0] == "Recibida":
        query = '''
        SELECT ID_Producto, Cantidad FROM purchase_details WHERE ID_Compra = ?
        '''
        details = fetch_all(query, (purchase_id,))
        for detail in details:
            update_inventory(detail[0], -detail[1], "Salida", user, f"Cancelación de compra {purchase_id}", f"CANCEL-{purchase_id}")

    return True

def receive_purchase(purchase_id, user, observations=""):
    """Marca una compra como recibida y actualiza precios de productos si es necesario."""
    query = '''
    SELECT Estado FROM purchases WHERE ID_Compra = ?
    '''
    current_status = fetch_one(query, (purchase_id,))
    if not current_status or current_status[0] != "Pendiente":
        return False

    query = '''
    UPDATE purchases SET Estado = 'Recibida', Observaciones = Observaciones || ' | ' || ?
    WHERE ID_Compra = ?
    '''
    execute_query(query, (observations, purchase_id))

    query = '''
    SELECT ID_Producto, Precio_Unitario FROM purchase_details WHERE ID_Compra = ?
    '''
    details = fetch_all(query, (purchase_id,))
    for detail in details:
        product_id = detail[0]
        new_price = detail[1]
        query = '''
        UPDATE products SET Último_Precio_Compra = ?, Última_Actualización = datetime('now')
        WHERE ID_Producto = ?
        '''
        execute_query(query, (new_price, product_id))

    return True

def get_purchase_history(supplier=None, start_date=None, end_date=None, status=None):
    """Obtiene el historial de compras con filtros opcionales."""
    query = '''
    SELECT * FROM purchases WHERE 1=1
    '''
    params = []
    if supplier:
        query += ' AND Proveedor = ?'
        params.append(supplier)
    if start_date:
        query += ' AND Fecha >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND Fecha <= ?'
        params.append(end_date)
    if status:
        query += ' AND Estado = ?'
        params.append(status)

    query += ' ORDER BY Fecha DESC'
    return fetch_all(query, params)

def get_purchase_details(purchase_id):
    """Obtiene los detalles de una compra específica."""
    query = '''
    SELECT * FROM purchases WHERE ID_Compra = ?
    '''
    purchase_info = fetch_one(query, (purchase_id,))
    if not purchase_info:
        return None, None

    query = '''
    SELECT * FROM purchase_details WHERE ID_Compra = ?
    '''
    details = fetch_all(query, (purchase_id,))
    return purchase_info, details

def modify_purchase_detail(detail_id, new_quantity=None, new_price=None):
    """Modifica los detalles de un ítem en una compra pendiente."""
    query = '''
    SELECT ID_Compra FROM purchase_details WHERE ID_Detalle = ?
    '''
    purchase_id = fetch_one(query, (detail_id,))
    if not purchase_id:
        return False

    query = '''
    SELECT Estado FROM purchases WHERE ID_Compra = ?
    '''
    purchase_status = fetch_one(query, (purchase_id[0],))
    if purchase_status[0] != "Pendiente":
        return False

    if new_quantity is not None:
        query = '''
        UPDATE purchase_details SET Cantidad = ? WHERE ID_Detalle = ?
        '''
        execute_query(query, (new_quantity, detail_id))

    if new_price is not None:
        query = '''
        UPDATE purchase_details SET Precio_Unitario = ? WHERE ID_Detalle = ?
        '''
        execute_query(query, (new_price, detail_id))

    query = '''
    UPDATE purchase_details SET Subtotal = Cantidad * Precio_Unitario WHERE ID_Detalle = ?
    '''
    execute_query(query, (detail_id,))
    update_purchase_total(purchase_id[0])

    return True
