import sqlite3
from data_manager import fetch_all

def generate_sales_report(start_date, end_date):
    """
    Genera un informe de ventas para un período específico.
    
    Args:
        start_date (str): Fecha inicial (formato 'YYYY-MM-DD')
        end_date (str): Fecha final (formato 'YYYY-MM-DD')
        
    Returns:
        dict: Informe de ventas con estadísticas
    """
    # Obtener ventas en el período
    query = '''
    SELECT * FROM sales WHERE Fecha BETWEEN ? AND ? AND Estado = 'Completada'
    '''
    period_sales = fetch_all(query, (start_date, end_date))
    
    # Si no hay ventas, retornar informe vacío
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
    
    # Obtener detalles de las ventas
    query = '''
    SELECT * FROM sale_details WHERE ID_Venta IN (SELECT ID_Venta FROM sales WHERE Fecha BETWEEN ? AND ? AND Estado = 'Completada')
    '''
    period_details = fetch_all(query, (start_date, end_date))
    
    # Calcular estadísticas
    total_sales = sum(sale[3] for sale in period_sales)
    num_sales = len(period_sales)
    avg_sale = total_sales / num_sales if num_sales > 0 else 0
    
    # Métodos de pago
    payment_methods = {}
    for sale in period_sales:
        payment_methods[sale[6]] = payment_methods.get(sale[6], 0) + 1
    
    # Productos más vendidos
    product_sales = {}
    for detail in period_details:
        product_sales[detail[1]] = product_sales.get(detail[1], 0) + detail[3]
    
    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Ventas por día
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