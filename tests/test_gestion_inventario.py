import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from gestion_inventario import GestionInventarioApp

class TestGestionInventarioApp(unittest.TestCase):
    @patch('tkinter.Tk')
    def setUp(self, mock_tk):
        self.root = mock_tk()
        self.app = GestionInventarioApp(self.root)

    @patch('gestion_inventario.update_inventory')
    @patch('gestion_inventario.messagebox.showinfo')
    @patch('gestion_inventario.messagebox.showerror')
    def test_show_update_inventory(self, mock_showerror, mock_showinfo, mock_update_inventory):
        self.app.show_update_inventory()
        
        # Simulate user input
        entries = [widget for widget in self.app.content_frame.winfo_children() if isinstance(widget, tk.Entry)]
        product_id_entry = entries[0]
        quantity_entry = entries[1]
        movement_type_entry = entries[2]
        description_entry = entries[3]
        reference_document_entry = entries[4]

        product_id_entry.insert(0, "P001")
        quantity_entry.insert(0, "10")
        movement_type_entry.insert(0, "Entrada")
        description_entry.insert(0, "Stock inicial")
        reference_document_entry.insert(0, "DOC123")
        
        # Simulate button click
        self.app.content_frame.winfo_children()[-1].invoke()
        
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
        entries = [widget for widget in self.app.content_frame.winfo_children() if isinstance(widget, tk.Entry)]
        client_entry = entries[0]
        payment_method_entry = entries[1]
        
        client_entry.insert(0, "Cliente1")
        payment_method_entry.insert(0, "Efectivo")
        
        # Simulate adding sale details
        sale_details_frame = self.app.content_frame.winfo_children()[5]
        sale_details_entries = [widget for widget in sale_details_frame.winfo_children() if isinstance(widget, tk.Entry)]
        product_id_entry = sale_details_entries[0]
        quantity_entry = sale_details_entries[1]
        price_unit_entry = sale_details_entries[2]
        discount_entry = sale_details_entries[3]

        product_id_entry.insert(0, "P001")
        quantity_entry.insert(0, "2")
        price_unit_entry.insert(0, "50.0")
        discount_entry.insert(0, "5.0")
        sale_details_frame.winfo_children()[-1].invoke()  # Add detail button
        
        # Simulate button click
        self.app.content_frame.winfo_children()[-1].invoke()
        
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
        entries = [widget for widget in self.app.content_frame.winfo_children() if isinstance(widget, tk.Entry)]
        supplier_entry = entries[0]
        
        supplier_entry.insert(0, "Proveedor1")
        
        # Simulate adding purchase details
        purchase_details_frame = self.app.content_frame.winfo_children()[3]
        purchase_details_entries = [widget for widget in purchase_details_frame.winfo_children() if isinstance(widget, tk.Entry)]
        product_id_entry = purchase_details_entries[0]
        quantity_entry = purchase_details_entries[1]
        price_unit_entry = purchase_details_entries[2]

        product_id_entry.insert(0, "P001")
        quantity_entry.insert(0, "5")
        price_unit_entry.insert(0, "20.0")
        purchase_details_frame.winfo_children()[-1].invoke()  # Add detail button
        
        # Simulate button click
        self.app.content_frame.winfo_children()[-1].invoke()
        
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
        entries = [widget for widget in self.app.content_frame.winfo_children() if isinstance(widget, tk.Entry)]
        start_date_entry = entries[0]
        end_date_entry = entries[1]

        start_date_entry.insert(0, "2023-01-01")
        end_date_entry.insert(0, "2023-12-31")
        
        # Simulate button click
        self.app.content_frame.winfo_children()[-1].invoke()
        
        mock_generate_sales_report.assert_called_once_with("2023-01-01", "2023-12-31")
        mock_showinfo.assert_called_once()
        mock_showerror.assert_not_called()

if __name__ == "__main__":
    unittest.main()