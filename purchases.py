import sqlite3
from data_manager import execute_query, fetch_all, fetch_one
from inventory import update_inventory

def register_purchase(supplier, user, observations=""):
    """Registra una nueva compra."""
    query = '''
    INSERT INTO purchases (Fecha, Proveedor, Total, Estado, Usuario, Observaciones)
    VALUES (datetime('now'), ?, 0, 'Pendiente', ?, ?)
    '''
    cursor = execute_query(query, (supplier, user, observations))
    return cursor.lastrowid

def add_purchase_detail(purchase_id, product_id, quantity, price_unit):
    """Añade detalles de productos a una compra."""
    query = '''
    INSERT INTO purchase_details (ID_Compra, ID_Producto, Cantidad, Precio_Unitario, Subtotal)
    VALUES (?, ?, ?, ?, ?)
    '''
    subtotal = quantity * price_unit
    execute_query(query, (purchase_id, product_id, quantity, price_unit, subtotal))
    update_inventory(product_id, quantity, "Entrada", "Sistema", f"Compra {purchase_id}", purchase_id)
    update_purchase_total(purchase_id)

def update_purchase_total(purchase_id):
    """Calcula y actualiza el total de una compra."""
    query = '''
    SELECT SUM(Subtotal) FROM purchase_details WHERE ID_Compra = ?
    '''
    total = fetch_one(query, (purchase_id,))[0]
    query = '''
    UPDATE purchases SET Total = ? WHERE ID_Compra = ?
    '''
    execute_query(query, (total, purchase_id))

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