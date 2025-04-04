from abc import ABC, abstractmethod
from data_manager import fetch_all
from typing import Dict, Any

class ReportStrategy(ABC):
    """Interfaz para el patrón Strategy de generación de reportes"""
    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> Any:
        pass

class PDFReportStrategy(ReportStrategy):
    """Estrategia para generar reportes en formato PDF"""
    def generate(self, data: Dict[str, Any]) -> str:
        # Implementación básica - en producción usaría una librería como ReportLab
        pdf_content = f"PDF Report\n{'='*40}\n"
        pdf_content += f"Total Ventas: ${data['total_ventas']:,.2f}\n"
        pdf_content += f"Número de Ventas: {data['num_ventas']}\n"
        pdf_content += f"Productos Vendidos: {data['productos_vendidos']}\n"
        pdf_content += f"Venta Promedio: ${data['venta_promedio']:,.2f}\n"
        return pdf_content

class ExcelReportStrategy(ReportStrategy):
    """Estrategia para generar reportes en formato Excel"""
    def generate(self, data: Dict[str, Any]) -> str:
        # Implementación básica - en producción usaría openpyxl
        excel_content = "Excel Report\n"
        excel_content += f"Total Ventas\t{data['total_ventas']}\n"
        excel_content += f"Número de Ventas\t{data['num_ventas']}\n"
        excel_content += f"Productos Vendidos\t{data['productos_vendidos']}\n"
        excel_content += f"Venta Promedio\t{data['venta_promedio']}\n"
        return excel_content

class HTMLReportStrategy(ReportStrategy):
    """Estrategia para generar reportes en formato HTML"""
    def generate(self, data: Dict[str, Any]) -> str:
        html_content = f"""
        <html>
        <head><title>Reporte de Ventas</title></head>
        <body>
            <h1>Reporte de Ventas</h1>
            <table border="1">
                <tr><th>Total Ventas</th><td>${data['total_ventas']:,.2f}</td></tr>
                <tr><th>Número de Ventas</th><td>{data['num_ventas']}</td></tr>
                <tr><th>Productos Vendidos</th><td>{data['productos_vendidos']}</td></tr>
                <tr><th>Venta Promedio</th><td>${data['venta_promedio']:,.2f}</td></tr>
            </table>
        </body>
        </html>
        """
        return html_content

class ReportGenerator:
    """Contexto que utiliza una estrategia de generación de reportes"""
    def __init__(self, strategy: ReportStrategy = None):
        self._strategy = strategy or PDFReportStrategy()

    @property
    def strategy(self) -> ReportStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ReportStrategy) -> None:
        self._strategy = strategy

    def generate_report(self, start_date: str, end_date: str) -> Any:
        """Genera el reporte usando la estrategia configurada"""
        report_data = self._get_report_data(start_date, end_date)
        return self._strategy.generate(report_data)

    def _get_report_data(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Obtiene los datos del reporte desde la base de datos"""
        # Obtener ventas en el período
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
        
        return {
            "total_ventas": total_sales,
            "num_ventas": num_sales,
            "productos_vendidos": sum(detail[3] for detail in period_details),
            "venta_promedio": avg_sale,
            "metodos_pago": payment_methods,
            "productos_populares": top_products,
            "ventas_por_dia": sales_by_day
        }

# Función legacy para mantener compatibilidad
def generate_sales_report(start_date: str, end_date: str) -> dict:
    """Función legacy que usa PDF como formato por defecto"""
    generator = ReportGenerator(PDFReportStrategy())
    return generator.generate_report(start_date, end_date)
