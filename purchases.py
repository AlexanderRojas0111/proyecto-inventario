import sqlite3
import logging

from data_manager import execute_query, fetch_all, fetch_one
from inventory import update_inventory

def register_purchase(supplier: str, user: str, observations: str = "") -> int:
    """Registra una nueva compra y registra errores en caso de fallo."""
    logging.basicConfig(level=logging.INFO)

    query = '''
    INSERT INTO purchases (Fecha, Proveedor, Total, Estado, Usuario, Observaciones)
    VALUES (datetime('now'), ?, 0, 'Pendiente', ?, ?)
    '''
    try:
        cursor = execute_query(query, (supplier, user, observations))
    except Exception as e:
        logging.error(f"Error al registrar la compra: {e}")
        return 0

    return cursor.lastrowid

def add_purchase_detail(purchase_id: int, product_id: int, quantity: int, price_unit: float):
    """Añade detalles de productos a una compra y registra errores en caso de fallo."""

    query = '''
    INSERT INTO purchase_details (ID_Compra, ID_Producto, Cantidad, Precio_Unitario, Subtotal)
    VALUES (?, ?, ?, ?, ?)
    '''
    try:
        subtotal = quantity * price_unit
        execute_query(query, (purchase_id, product_id, quantity, price_unit, subtotal))

        update_inventory(product_id, quantity, "Entrada", "Sistema", f"Compra {purchase_id}", purchase_id)
        update_purchase_total(purchase_id)
    except Exception as e:
        logging.error(f"Error al añadir detalle de compra: {e}")

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

def cancel_purchase(purchase_id: int, cancellation_reason: str, user: str) -> bool:
    """Cancela una compra y actualiza el inventario, registrando errores en caso de fallo."""

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

def receive_purchase(purchase_id: int, user: str, observations: str = "") -> bool:
    """Marca una compra como recibida y actualiza precios de productos si es necesario, registrando errores en caso de fallo."""

    query = '''
    SELECT Estado FROM purchases WHERE ID_Compra = ?
    '''
    try:
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
    except Exception as e:
        logging.error(f"Error al recibir compra: {e}")
        return False

def get_purchase_history(supplier: str = None, start_date: str = None, end_date: str = None, status: str = None) -> list:
    """Obtiene el historial de compras con filtros opcionales y registra errores en caso de fallo."""

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
    try:
        return fetch_all(query, params)
    except Exception as e:
        logging.error(f"Error al obtener el historial de compras: {e}")
        return []

def get_purchase_details(purchase_id: int) -> tuple:
    """Obtiene los detalles de una compra específica y registra errores en caso de fallo."""

    query = '''
    SELECT * FROM purchases WHERE ID_Compra = ?
    '''
    try:
        purchase_info = fetch_one(query, (purchase_id,))

        if not purchase_info:
            return None, None

        query = '''
        SELECT * FROM purchase_details WHERE ID_Compra = ?
        '''
        details = fetch_all(query, (purchase_id,))
        return purchase_info, details
    except Exception as e:
        logging.error(f"Error al obtener detalles de la compra: {e}")
        return None, None

def modify_purchase_detail(detail_id: int, new_quantity: int = None, new_price: float = None) -> bool:
    """Modifica los detalles de un ítem en una compra pendiente y registra errores en caso de fallo."""

    query = '''
    SELECT ID_Compra FROM purchase_details WHERE ID_Detalle = ?
    '''
    try:
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

    except Exception as e:
        logging.error(f"Error al modificar detalle de compra: {e}")
        return False

    return True
