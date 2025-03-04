import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gestion_inventario import GestionInventarioApp

class TestGestionInventarioApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = GestionInventarioApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('gestion_inventario.update_inventory')
    @patch('gestion_inventario.messagebox.showinfo')
    @patch('gestion_inventario.messagebox.showerror')
    def test_show_update_inventory(self, mock_showerror, mock_showinfo, mock_update_inventory):
        self.app.show_update_inventory()
        
        # Simulate user input
        entries = self.app.content_frame.winfo_children()
        entries[1].insert(0, "P001")  # product_id_entry
        entries[3].insert(0, "10")    # quantity_entry
        entries[5].insert(0, "Entrada")  # movement_type_entry
        entries[7].insert(0, "Stock inicial")  # description_entry
        entries[9].insert(0, "DOC123")  # reference_document_entry
        
        # Simulate button click
        entries[10].invoke()
        
        mock_update_inventory.assert_called_once_with("P001", 10, "Entrada", "Sistema", "Stock inicial", "DOC123")
        mock_showinfo.assert_called_once_with("Info", "Inventario actualizado.")
        mock_showerror.assert_not_called()

    @patch('gestion_inventario.register_sale')
    @patch('gestion_inventario.add_sale_detail')
    @patch('gestion_inventario.messagebox.showinfo')
    @patch('gestion_inventario.messagebox.showerror')
    def test_show_register_sale(self, mock_showerror, mock_showinfo, mock_add_sale_detail, mock_register_sale):
        self.app.show_register_sale()
        
        # Simulate user input
        entries = self.app.content_frame.winfo_children()
        entries[1].insert(0, "Cliente1")  # client_entry
        entries[3].insert(0, "Efectivo")  # payment_method_entry
        
        # Simulate adding sale details
        sale_details_frame = entries[5]
        sale_details_entries = sale_details_frame.winfo_children()
        sale_details_entries[1].insert(0, "P001")  # product_id_entry
        sale_details_entries[3].insert(0, "2")     # quantity_entry
        sale_details_entries[5].insert(0, "50.0")  # price_unit_entry
        sale_details_entries[7].insert(0, "5.0")   # discount_entry
        sale_details_entries[8].invoke()  # Add detail button
        
        # Simulate button click
        entries[6].invoke()
        
        mock_register_sale.assert_called_once_with("Cliente1", "Efectivo", "Sistema")
        mock_add_sale_detail.assert_called_once()
        mock_showinfo.assert_called_once_with("Info", "Venta registrada.")
        mock_showerror.assert_not_called()

    @patch('gestion_inventario.register_purchase')
    @patch('gestion_inventario.add_purchase_detail')
    @patch('gestion_inventario.messagebox.showinfo')
    @patch('gestion_inventario.messagebox.showerror')
    def test_show_register_purchase(self, mock_showerror, mock_showinfo, mock_add_purchase_detail, mock_register_purchase):
        self.app.show_register_purchase()
        
        # Simulate user input
        entries = self.app.content_frame.winfo_children()
        entries[1].insert(0, "Proveedor1")  # supplier_entry
        
        # Simulate adding purchase details
        purchase_details_frame = entries[3]
        purchase_details_entries = purchase_details_frame.winfo_children()
        purchase_details_entries[1].insert(0, "P001")  # product_id_entry
        purchase_details_entries[3].insert(0, "5")     # quantity_entry
        purchase_details_entries[5].insert(0, "20.0")  # price_unit_entry
        purchase_details_entries[6].invoke()  # Add detail button
        
        # Simulate button click
        entries[4].invoke()
        
        mock_register_purchase.assert_called_once_with("Proveedor1", "Sistema")
        mock_add_purchase_detail.assert_called_once()
        mock_showinfo.assert_called_once_with("Info", "Compra registrada.")
        mock_showerror.assert_not_called()

    @patch('gestion_inventario.generate_sales_report')
    @patch('gestion_inventario.messagebox.showinfo')
    @patch('gestion_inventario.messagebox.showerror')
    def test_show_generate_report(self, mock_showerror, mock_showinfo, mock_generate_sales_report):
        self.app.show_generate_report()
        
        # Simulate user input
        entries = self.app.content_frame.winfo_children()
        entries[1].insert(0, "2023-01-01")  # start_date_entry
        entries[3].insert(0, "2023-12-31")  # end_date_entry
        
        # Simulate button click
        entries[4].invoke()
        
        mock_generate_sales_report.assert_called_once_with("2023-01-01", "2023-12-31")
        mock_showinfo.assert_called_once()
        mock_showerror.assert_not_called()

if __name__ == "__main__":
    unittest.main()