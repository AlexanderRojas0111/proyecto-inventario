import unittest
from unittest.mock import MagicMock, patch
from inventory import (
    InventoryObserver,
    InventorySubject,
    update_inventory,
    adjust_inventory,
    get_current_stock,
    get_low_stock_products,
    get_product_movements,
    calculate_inventory_value
)

class MockObserver(InventoryObserver):
    """Observador mock para pruebas"""
    def __init__(self):
        self.updates = []
    
    def on_inventory_update(self, product_id, movement_type, quantity):
        self.updates.append((product_id, movement_type, quantity))

class TestInventoryObserver(unittest.TestCase):
    def setUp(self):
        self.observer = MockObserver()
        InventorySubject.attach(self.observer)
    
    def tearDown(self):
        InventorySubject.detach(self.observer)
    
    @patch('inventory.execute_query')
    def test_update_inventory_notifies(self, mock_execute):
        update_inventory("P001", 10, "Entrada", "user", "test", "doc123")
        self.assertEqual(len(self.observer.updates), 1)
        self.assertEqual(self.observer.updates[0], ("P001", "Entrada", 10))
    
    @patch('inventory.execute_query')
    @patch('inventory.fetch_one')
    def test_adjust_inventory_notifies(self, mock_fetch, mock_execute):
        mock_fetch.return_value = (5,)  # Stock actual
        adjust_inventory("P001", 15, "user", "test")
        self.assertEqual(len(self.observer.updates), 1)
        self.assertEqual(self.observer.updates[0], ("P001", "Entrada", 10))
    
    @patch('inventory.execute_query')
    def test_multiple_observers(self, mock_execute):
        observer2 = MockObserver()
        InventorySubject.attach(observer2)
        
        update_inventory("P002", 5, "Salida", "user", "test", "doc123")
        
        self.assertEqual(len(self.observer.updates), 1)
        self.assertEqual(len(observer2.updates), 1)
        InventorySubject.detach(observer2)
    
    @patch('inventory.execute_query')
    def test_detached_observer(self, mock_execute):
        observer2 = MockObserver()
        InventorySubject.attach(observer2)
        InventorySubject.detach(observer2)
        
        update_inventory("P003", 8, "Entrada", "user", "test", "doc123")
        
        self.assertEqual(len(self.observer.updates), 1)
        self.assertEqual(len(observer2.updates), 0)

class TestInventoryFunctions(unittest.TestCase):
    @patch('inventory.fetch_one')
    def test_get_current_stock(self, mock_fetch):
        mock_fetch.return_value = (10,)
        result = get_current_stock("P001")
        self.assertEqual(result, 10)
    
    @patch('inventory.fetch_all')
    def test_get_low_stock_products(self, mock_fetch):
        mock_fetch.return_value = [("P001", "Producto 1", 5, 10)]
        result = get_low_stock_products()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "P001")

if __name__ == "__main__":
    unittest.main()
