import unittest
from unittest.mock import patch, MagicMock
from app.purchases import register_purchase  # Ajusta la ruta de importación según sea necesario

class TestPurchases(unittest.TestCase):

    @patch('app.purchases.sqlite3.connect')  # Parchear sqlite3.connect en lugar de db.execute
    @patch('app.purchases.InventoryManagement')  # Ajusta la ruta de importación según sea necesario
    def test_register_purchase(self, mock_inventory_management, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        mock_inventory_manager = mock_inventory_management.return_value
        mock_inventory_manager.adjust_inventory.return_value = True

        purchase_info = register_purchase(1, 10, 1, 100.0)
        
        self.assertIsNotNone(purchase_info)
        self.assertEqual(purchase_info['id'], 1)
        self.assertEqual(purchase_info['product_id'], 1)
        self.assertEqual(purchase_info['quantity'], 10)
        self.assertEqual(purchase_info['supplier_id'], 1)
        self.assertEqual(purchase_info['cost'], 100.0)

        # Verificar que se llamó a la consulta correcta
        mock_cursor.execute.assert_any_call('''
            INSERT INTO purchases (ID_Producto, Cantidad, ID_Proveedor, Costo)
            VALUES (?, ?, ?, ?)
            RETURNING ID_Compra
        ''', (1, 10, 1, 100.0))

if __name__ == "__main__":
    unittest.main()