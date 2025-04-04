import unittest
from unittest.mock import MagicMock, patch
from gestion_inventario import InventoryMediatorImpl

class TestInventoryMediator(unittest.TestCase):
    def setUp(self):
        self.mediator = InventoryMediatorImpl()
        
        # Mockear todas las dependencias
        self.mediator.update_inventory_fn = MagicMock()
        self.mediator.register_sale_fn = MagicMock(return_value=1)
        self.mediator.add_sale_detail_fn = MagicMock()
        self.mediator.register_purchase_fn = MagicMock(return_value=1)
        self.mediator.add_purchase_detail_fn = MagicMock()
        self.mediator.report_generator.generate = MagicMock(return_value="Reporte de prueba")

    def test_update_inventory(self):
        result = self.mediator.update_inventory(
            "P001", 10, "Entrada", "user", "test", "doc123"
        )
        self.assertTrue(result)
        self.mediator.update_inventory_fn.assert_called_once_with(
            "P001", 10, "Entrada", "user", "test", "doc123"
        )

    def test_register_sale(self):
        sale_details = [{
            "product_id": "P001",
            "quantity": 2,
            "price_unit": 10.5,
            "discount": 0
        }]
        
        result = self.mediator.register_sale("Cliente1", "Efectivo", sale_details)
        self.assertTrue(result)
        
        # Verificar que se registró la venta
        self.mediator.register_sale_fn.assert_called_once_with("Cliente1", "Efectivo", "Sistema")
        
        # Verificar que se añadieron los detalles
        self.mediator.add_sale_detail_fn.assert_called_once_with(1, "P001", 2, 10.5, 0)
        
        # Verificar que se actualizó el inventario
        self.mediator.update_inventory_fn.assert_called_once_with(
            "P001", 2, "Salida", "Sistema", "Venta #1", "Venta-1"
        )

    def test_register_purchase(self):
        purchase_details = [{
            "product_id": "P002",
            "quantity": 5,
            "price_unit": 8.0
        }]
        
        result = self.mediator.register_purchase("Proveedor1", purchase_details)
        self.assertTrue(result)
        
        # Verificar que se registró la compra
        self.mediator.register_purchase_fn.assert_called_once_with("Proveedor1", "Sistema")
        
        # Verificar que se añadieron los detalles
        self.mediator.add_purchase_detail_fn.assert_called_once_with(1, "P002", 5, 8.0)
        
        # Verificar que se actualizó el inventario
        self.mediator.update_inventory_fn.assert_called_once_with(
            "P002", 5, "Entrada", "Sistema", "Compra #1", "Compra-1"
        )

    def test_generate_report(self):
        result = self.mediator.generate_report("2023-01-01", "2023-01-31")
        self.assertEqual(result, "Reporte de prueba")
        self.mediator.report_generator.generate.assert_called_once_with(
            "2023-01-01", "2023-01-31"
        )

    def test_update_inventory_failure(self):
        self.mediator.update_inventory_fn.side_effect = Exception("Error de prueba")
        result = self.mediator.update_inventory(
            "P001", 10, "Entrada", "user", "test", "doc123"
        )
        self.assertFalse(result)

    def test_register_sale_failure(self):
        self.mediator.register_sale_fn.side_effect = Exception("Error de prueba")
        sale_details = [{
            "product_id": "P001",
            "quantity": 2,
            "price_unit": 10.5,
            "discount": 0
        }]
        
        result = self.mediator.register_sale("Cliente1", "Efectivo", sale_details)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
