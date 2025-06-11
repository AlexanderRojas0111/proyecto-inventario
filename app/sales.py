import sqlite3
from app.data_manager import execute_query, fetch_all, fetch_one
from app.inventory import update_inventory, InventoryManagement
from datetime import datetime

# Definir la conexión a la base de datos
DATABASE = 'inventario.db'

def get_db_connection():
    return sqlite3.connect(DATABASE)

db = get_db_connection()

def register_sale(product_id, quantity, client_id, db):
    """
    Registra una venta de producto.
    
    Args:
        product_id (int): ID del producto vendido
        quantity (int): Cantidad vendida
        client_id (int): ID del cliente
        
    Returns:
        dict: Información de la venta en caso de éxito
        None: En caso de error
    """
    # Fetch available products for display
    available_products = fetch_all("SELECT ID_Producto, Nombre FROM products;")
    print("Productos disponibles:")
    for product in available_products:
        print(f"ID: {product['ID_Producto']}, Nombre: {product['Nombre']}")
    
    # Verificar si hay suficiente stock
    inventory_manager = InventoryManagement(db)

    """
    Registra una venta de producto.
    
    Args:
        product_id (int): ID del producto vendido
        quantity (int): Cantidad vendida
        client_id (int): ID del cliente
        
    Returns:
        dict: Información de la venta en caso de éxito
        None: En caso de error
    """
    # Verificar si hay suficiente stock
    inventory_manager = InventoryManagement(db)
    current_stock = inventory_manager.get_current_stock(product_id)
    
    if current_stock is None or current_stock < quantity:
        return None  # No hay suficiente stock
    
    # Ajustar el inventario
    success = inventory_manager.adjust_inventory(product_id, quantity, 'remove')
    if not success:
        return None
    
    # Registrar la venta en la base de datos
    sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        result = db.execute(
            """
            INSERT INTO sales (ID_Producto, Cantidad, ID_Cliente, Fecha)
            VALUES (?, ?, ?, ?)
            RETURNING ID_Venta
            """,
            (product_id, quantity, client_id, sale_date)
        )
        
        # Verificar el resultado y obtener el ID de venta
        if result:
            # Si result es una tupla, el ID de venta estará en la primera posición
            if isinstance(result, tuple) or isinstance(result, list):
                sale_id = result[0]
            # Si result es un diccionario, obtenemos el ID_Venta
            elif isinstance(result, dict):
                sale_id = result.get('ID_Venta')
            # Si result es un valor escalar (como un entero), lo usamos directamente
            else:
                sale_id = result
            
            # Crear y devolver un diccionario con la información de la venta
            sale_info = {
                'id': sale_id,
                'product_id': product_id,
                'quantity': quantity,
                'client_id': client_id,
                'date': sale_date
            }
            
            return sale_info
        
    except Exception as e:
        print(f"Error al registrar la venta: {e}")
    
    return None

def add_sale_detail(sale_id, product_id, quantity, price_unit, discount):
    subtotal = quantity * price_unit - discount
    query = '''
    INSERT INTO sale_details (ID_Venta, ID_Producto, Cantidad, Precio_Unitario, Subtotal, Descuento)
    VALUES (?, ?, ?, ?, ?, ?)
    '''
    execute_query(query, (sale_id, product_id, quantity, price_unit, subtotal, discount))
    update_inventory(product_id, -quantity, "Salida", "Sistema", f"Venta {sale_id}", sale_id)
    update_sale_total(sale_id)

def update_sale_total(sale_id):
    """Calcula y actualiza el total de una venta."""
    query = '''
    SELECT SUM(Subtotal) FROM sale_details WHERE ID_Venta = ?
    '''
    result = fetch_one(query, (sale_id,))

    # Verificar si result es None o si result['SUM(Subtotal)'] es None
    if result is None or result.get('SUM(Subtotal)') is None:
        total = 0
    else:
        total = result['SUM(Subtotal)']

    update_query = '''
    UPDATE sales SET Total = ? WHERE ID_Venta = ?
    '''
    execute_query(update_query, (total, sale_id))
    return total

def cancel_sale(sale_id, cancellation_reason, user):
    """Cancela una venta y actualiza el inventario.
    
    Args:
        sale_id (int): ID de la venta a cancelar.
        cancellation_reason (str): Motivo de la cancelación.
        user (str): Usuario que cancela la venta.
        
    Returns:
        bool: True si la cancelación fue exitosa, False en caso contrario.
    """

    query = '''
    SELECT Estado FROM sales WHERE ID_Venta = ?
    '''
    current_status = fetch_one(query, (sale_id,))
    if not current_status or current_status[0] == "Cancelada":
        print("La venta ya está cancelada o no existe.")

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
    """Marca una venta como completada.
    
    Args:
        sale_id (int): ID de la venta a completar.
        payment_confirmation (str): Confirmación del pago, si está disponible.
        
    Returns:
        bool: True si la venta fue completada, False en caso contrario.
    """

    query = '''
    SELECT Estado FROM sales WHERE ID_Venta = ?
    '''
    current_status = fetch_one(query, (sale_id,))
    if not current_status or current_status[0] != "Pendiente":
        print("La venta no está en estado pendiente o no existe.")

        return False

    query = '''
    UPDATE sales SET Estado = 'Completada', Observaciones = Observaciones || ' | Confirmación de pago: ' || ?
    WHERE ID_Venta = ?
    '''
    execute_query(query, (payment_confirmation, sale_id))

    return True

def create_return(sale_id, product_id, quantity, reason, user):
    """Registra una devolución parcial o total de una venta.
    
    Args:
        sale_id (int): ID de la venta original.
        product_id (int): ID del producto a devolver.
        quantity (int): Cantidad a devolver.
        reason (str): Motivo de la devolución.
        user (str): Usuario que registra la devolución.
        
    Returns:
        bool: True si la devolución fue exitosa, False en caso contrario.
    """

    query = '''
    SELECT Estado FROM sales WHERE ID_Venta = ?
    '''
    sale_status = fetch_one(query, (sale_id,))
    if not sale_status or sale_status[0] != "Completada":
        print("La venta no está completada o no existe.")

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
    """Obtiene el historial de ventas con filtros opcionales.
    
    Args:
        client (str): Filtro por cliente.
        start_date (str): Fecha de inicio para el historial.
        end_date (str): Fecha de fin para el historial.
        status (str): Estado de la venta.
        payment_method (str): Método de pago utilizado.
        
    Returns:
        list: Lista de ventas que cumplen con los filtros.
    """
    
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
    
    try:
        return fetch_all(query, params)
    except sqlite3.Error as e:
        print(f"Error al obtener el historial de ventas: {e}")
        return []



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
    for detail in details:
        product_id = detail['product_id']
        quantity = detail['quantity']
        price_unit = detail['price_unit']
        discount = detail.get('discount', 0.0)
        subtotal = (quantity * price_unit) - discount
        # Usa estas variables en tu consulta SQL
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
