import sqlite3
from data_manager import execute_query, fetch_all, fetch_one
from inventory import update_inventory

def register_sale(client, payment_method, user, observations=""):
    """Registra una nueva venta."""
    query = '''
    INSERT INTO sales (Fecha, Cliente, Total, Estado, Usuario, Método_Pago, Observaciones)
    VALUES (datetime('now'), ?, 0, 'Pendiente', ?, ?, ?)
    '''
    cursor = execute_query(query, (client, user, payment_method, observations))
    return cursor.lastrowid

def add_sale_detail(sale_id, product_id, quantity, price_unit, discount=0):
    """Añade detalles de productos a una venta."""
    query = '''
    INSERT INTO sale_details (ID_Venta, ID_Producto, Cantidad, Precio_Unitario, Subtotal, Descuento)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    subtotal = (quantity * price_unit) - discount
    execute_query(query, (sale_id, product_id, quantity, price_unit, subtotal, discount))
    update_inventory(product_id, -quantity, "Salida", "Sistema", f"Venta {sale_id}", sale_id)
    update_sale_total(sale_id)

def update_sale_total(sale_id):
    """Calcula y actualiza el total de una venta."""
    query = '''
    SELECT SUM(Subtotal) FROM sale_details WHERE ID_Venta = ?
    '''
    total = fetch_one(query, (sale_id,))[0]
    query = '''
    UPDATE sales SET Total = ? WHERE ID_Venta = ?
    '''
    execute_query(query, (total, sale_id))

def cancel_sale(sale_id, cancellation_reason, user):
    """Cancela una venta y actualiza el inventario."""
    query = '''
    SELECT Estado FROM sales WHERE ID_Venta = ?
    '''
    current_status = fetch_one(query, (sale_id,))
    if not current_status or current_status[0] == "Cancelada":
        return False

    query = '''
    UPDATE sales SET Estado = 'Cancelada', Observaciones = Observaciones || ' | CANCELACIÓN: ' || ? || ' por ' || ? || ' en ' || datetime('now')
    WHERE ID_Venta = ?
    '''
    execute_query(query, (cancellation_reason, user, sale_id))

    query = '''
    SELECT ID_Producto, Cantidad FROM sale_details WHERE ID_Venta = ?
    '''
    details = fetch_all(query, (sale_id,))
    for detail in details:
        update_inventory(detail[0], detail[1], "Entrada", user, f"Cancelación de venta {sale_id}", f"CANCEL-{sale_id}")

    return True

def complete_sale(sale_id, payment_confirmation=None):
    """Marca una venta como completada."""
    query = '''
    SELECT Estado FROM sales WHERE ID_Venta = ?
    '''
    current_status = fetch_one(query, (sale_id,))
    if not current_status or current_status[0] != "Pendiente":
        return False

    query = '''
    UPDATE sales SET Estado = 'Completada', Observaciones = Observaciones || ' | Confirmación de pago: ' || ?
    WHERE ID_Venta = ?
    '''
    execute_query(query, (payment_confirmation, sale_id))

    return True

def create_return(sale_id, product_id, quantity, reason, user):
    """Registra una devolución parcial o total de una venta."""
    query = '''
    SELECT Estado FROM sales WHERE ID_Venta = ?
    '''
    sale_status = fetch_one(query, (sale_id,))
    if not sale_status or sale_status[0] != "Completada":
        return False

    query = '''
    SELECT Cantidad FROM sale_details WHERE ID_Venta = ? AND ID_Producto = ?
    '''
    original_detail = fetch_one(query, (sale_id, product_id))
    if not original_detail or quantity > original_detail[0]:
        return False

    query = '''
    INSERT INTO returns (ID_Venta_Original, ID_Producto, Cantidad, Fecha, Motivo, Usuario)
    VALUES (?, ?, ?, datetime('now'), ?, ?)
    '''
    cursor = execute_query(query, (sale_id, product_id, quantity, reason, user))
    return_id = cursor.lastrowid

    update_inventory(product_id, quantity, "Entrada", user, f"Devolución de venta {sale_id}", return_id)

    return True

def get_sale_history(client=None, start_date=None, end_date=None, status=None, payment_method=None):
    """Obtiene el historial de ventas con filtros opcionales."""
    query = '''
    SELECT * FROM sales WHERE 1=1
    '''
    params = []
    if client:
        query += ' AND Cliente = ?'
        params.append(client)
    if start_date:
        query += ' AND Fecha >= ?'
        params.append(start_date)
    if end_date:
        query += ' AND Fecha <= ?'
        params.append(end_date)
    if status:
        query += ' AND Estado = ?'
        params.append(status)
    if payment_method:
        query += ' AND Método_Pago = ?'
        params.append(payment_method)

    query += ' ORDER BY Fecha DESC'
    return fetch_all(query, params)

def get_sale_details(sale_id):
    """Obtiene los detalles de una venta específica."""
    query = '''
    SELECT * FROM sales WHERE ID_Venta = ?
    '''
    sale_info = fetch_one(query, (sale_id,))
    if not sale_info:
        return None, None

    query = '''
    SELECT * FROM sale_details WHERE ID_Venta = ?
    '''
    details = fetch_all(query, (sale_id,))
    return sale_info, details

def generate_sale_report(start_date, end_date):
    """Genera un informe de ventas para un período específico."""
    query = '''
    SELECT * FROM sales WHERE Fecha BETWEEN ? AND ? AND Estado = 'Completada'
    '''
    period_sales = fetch_all(query, (start_date, end_date))
    if not period_sales:
        return {
            "total_ventas": 0,
            "num_ventas": 0,
            "productos_vendidos": 0,
            "venta_promedio": 0,
            "metodos_pago": {},
            "productos_populares": [],
            "ventas_por_dia": {}
        }

    query = '''
    SELECT * FROM sale_details WHERE ID_Venta IN (SELECT ID_Venta FROM sales WHERE Fecha BETWEEN ? AND ? AND Estado = 'Completada')
    '''
    period_details = fetch_all(query, (start_date, end_date))

    total_sales = sum(sale[3] for sale in period_sales)
    num_sales = len(period_sales)
    avg_sale = total_sales / num_sales if num_sales > 0 else 0

    payment_methods = {}
    for sale in period_sales:
        payment_methods[sale[6]] = payment_methods.get(sale[6], 0) + 1

    product_sales = {}
    for detail in period_details:
        product_sales[detail[1]] = product_sales.get(detail[1], 0) + detail[3]

    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:10]

    sales_by_day = {}
    for sale in period_sales:
        day = sale[1].split(' ')[0]
        sales_by_day[day] = sales_by_day.get(day, 0) + sale[3]

    report = {
        "total_ventas": total_sales,
        "num_ventas": num_sales,
        "productos_vendidos": sum(detail[3] for detail in period_details),
        "venta_promedio": avg_sale,
        "metodos_pago": payment_methods,
        "productos_populares": top_products,
        "ventas_por_dia": sales_by_day
    }

    return report