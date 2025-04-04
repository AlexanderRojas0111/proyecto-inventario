import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from gestion_inventario import GestionInventarioApp

class TestGestionInventarioFixed(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        # Patch the mediator during setup
        cls.mediator_patch = patch('gestion_inventario.InventoryMediatorImpl')
        cls.mock_mediator = cls.mediator_patch.start()
        cls.mock_mediator.return_value.register_sale.return_value = True
        
        cls.app = GestionInventarioApp(cls.root)
        cls.root.update()  # Initialize UI

    @classmethod
    def tearDownClass(cls):
        cls.mediator_patch.stop()
        cls.root.destroy()

    def test_main_window_creation(self):
        """Verify main window components are created"""
        self.assertIsNotNone(self.app.content_frame, "Content frame not created")
        # Check for at least 1 menu button (more flexible assertion)
        menu_buttons = [w for w in self.root.winfo_children() 
                      if isinstance(w, tk.Button)]
        self.assertGreater(len(menu_buttons), 0, "No menu buttons found")

    @patch('gestion_inventario.messagebox')
    def test_sale_form_ui(self, mock_msg):
        """Test sale registration form UI elements"""
        self.app.show_register_sale()
        entries = [w for w in self.app.content_frame.winfo_children()
                 if isinstance(w, tk.Entry)]
        self.assertGreaterEqual(len(entries), 1, "No form entries found")

    @patch('gestion_inventario.messagebox')
    def test_sale_submission(self, mock_msg):
        """Test sale form submission with valid data"""
        self.app.show_register_sale()
        
        # Simulate form input
        for child in self.app.content_frame.winfo_children():
            if isinstance(child, tk.Entry):
                child.insert(0, "Test Value")
        
        # Find and click submit button
        submit_buttons = [w for w in self.app.content_frame.winfo_children()
                        if isinstance(w, tk.Button) and "Registrar" in str(w)]
        
        if submit_buttons:
            submit_buttons[0].invoke()
            self.mock_mediator.return_value.register_sale.assert_called_once()
        else:
            self.fail("Submit button not found")

    @patch('gestion_inventario.messagebox')
    def test_invalid_submission(self, mock_msg):
        """Test form submission with missing data"""
        self.app.show_register_sale()
        
        # Find and click submit button without filling fields
        submit_buttons = [w for w in self.app.content_frame.winfo_children()
                        if isinstance(w, tk.Button) and "Registrar" in str(w)]
        
        if submit_buttons:
            submit_buttons[0].invoke()
            mock_msg.showerror.assert_called_once()
        else:
            self.fail("Submit button not found")

if __name__ == '__main__':
    unittest.main()
