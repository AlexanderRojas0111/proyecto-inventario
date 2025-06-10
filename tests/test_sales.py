import unittest
from unittest.mock import patch, MagicMock
from app.sales import register_sale  # Ajusta la ruta de importación según sea necesario

class TestSales(unittest.TestCase):

    @patch('app.sales.sqlite3.connect')  # Parchear sqlite3.connect en lugar de db.execute
    @patch('app.sales.InventoryManagement')  # Ajusta la ruta de importación según sea necesario
    def test_register_sale(self, mock_inventory_management, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        mock_inventory_manager = mock_inventory_management.return_value
        mock_inventory_manager.get_current_stock.return_value = 10
        mock_inventory_manager.adjust_inventory.return_value = True

        sale_info = register_sale(1, 5, 1)
        
        self.assertIsNotNone(sale_info)
        self.assertEqual(sale_info['id'], 1)
        self.assertEqual(sale_info['product_id'], 1)
        self.assertEqual(sale_info['quantity'], 5)
        self.assertEqual(sale_info['client_id'], 1)

        # Verificar que se llamó a la consulta correcta
        mock_cursor.execute.assert_any_call('''
            INSERT INTO sales (ID_Producto, Cantidad, ID_Cliente, Fecha)
            VALUES (?, ?, ?, ?)
            RETURNING ID_Venta
        ''', (1, 5, 1, unittest.mock.ANY))

if __name__ == "__main__":
    unittest.main()