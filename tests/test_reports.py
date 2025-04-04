import unittest
from unittest.mock import patch, MagicMock
from reports import (
    PDFReportStrategy,
    ExcelReportStrategy,
    HTMLReportStrategy,
    ReportGenerator
)

class TestReportStrategies(unittest.TestCase):
    def test_pdf_report_generation(self):
        strategy = PDFReportStrategy()
        test_data = {
            "total_ventas": 1000,
            "num_ventas": 10,
            "productos_vendidos": 50,
            "venta_promedio": 100
        }
        result = strategy.generate(test_data)
        self.assertIn("PDF Report", result)
        self.assertIn("Total Ventas: $1,000.00", result)

    def test_excel_report_generation(self):
        strategy = ExcelReportStrategy()
        test_data = {
            "total_ventas": 2000,
            "num_ventas": 20,
            "productos_vendidos": 100,
            "venta_promedio": 100
        }
        result = strategy.generate(test_data)
        self.assertIn("Excel Report", result)
        self.assertIn("Total Ventas\t2000", result)

    def test_html_report_generation(self):
        strategy = HTMLReportStrategy()
        test_data = {
            "total_ventas": 3000,
            "num_ventas": 30,
            "productos_vendidos": 150,
            "venta_promedio": 100
        }
        result = strategy.generate(test_data)
        self.assertIn("<html>", result)
        self.assertIn("<h1>Reporte de Ventas</h1>", result)

class TestReportGenerator(unittest.TestCase):
    @patch('reports.ReportGenerator._get_report_data')
    def test_report_generation_with_strategy(self, mock_get_data):
        mock_get_data.return_value = {
            "total_ventas": 1000,
            "num_ventas": 10,
            "productos_vendidos": 50,
            "venta_promedio": 100
        }

        # Test PDF strategy (default)
        generator = ReportGenerator()
        result = generator.generate_report("2023-01-01", "2023-01-31")
        self.assertIn("PDF Report", result)

        # Test Excel strategy
        generator.strategy = ExcelReportStrategy()
        result = generator.generate_report("2023-01-01", "2023-01-31")
        self.assertIn("Excel Report", result)

        # Test HTML strategy
        generator.strategy = HTMLReportStrategy()
        result = generator.generate_report("2023-01-01", "2023-01-31")
        self.assertIn("<html>", result)

    @patch('reports.fetch_all')
    def test_get_report_data(self, mock_fetch):
        mock_fetch.side_effect = [
            [('2023-01-01', 1, 100, 'Completada', 'Cliente1', 'Efectivo')],
            [('1', 'P001', 2, 50, 0)]
        ]

        generator = ReportGenerator()
        data = generator._get_report_data("2023-01-01", "2023-01-31")
        
        self.assertEqual(data["total_ventas"], 100)
        self.assertEqual(data["num_ventas"], 1)
        self.assertEqual(data["productos_vendidos"], 2)

if __name__ == "__main__":
    unittest.main()
