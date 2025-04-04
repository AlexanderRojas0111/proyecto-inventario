import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch, MagicMock
from gestion_inventario import GestionInventarioApp

class TestInventarioCorregido(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        # Configurar mocks
        cls.mediator_patch = patch('gestion_inventario.InventoryMediatorImpl')
        cls.mock_mediator = cls.mediator_patch.start()
        cls.mock_mediator.return_value.register_sale.return_value = True
        
        # Crear instancia de la aplicación
        cls.app = GestionInventarioApp(cls.root)
        cls.root.update()

    @classmethod
    def tearDownClass(cls):
        cls.mediator_patch.stop()
        cls.root.destroy()

    def test_ui_inicializacion(self):
        """Verifica que los componentes principales de la UI se creen correctamente"""
        # Verificar frame de contenido
        self.assertIsNotNone(self.app.content_frame)
        
        # Verificar botones del menú
        menu_frames = [w for w in self.root.winfo_children() 
                      if isinstance(w, ttk.Frame)]
        self.assertTrue(len(menu_frames) > 0, "No se encontró el frame del menú")
        
        if menu_frames:
            menu_buttons = [w for w in menu_frames[0].winfo_children()
                          if isinstance(w, ttk.Button)]
            self.assertTrue(len(menu_buttons) >= 4, "No se encontraron los 4 botones del menú")

    @patch('gestion_inventario.messagebox')
    def test_formulario_venta(self, mock_msg):
        """Prueba el formulario de registro de ventas"""
        self.app.show_register_sale()
        
        # Verificar campos del formulario
        entries = [w for w in self.app.content_frame.winfo_children()
                 if isinstance(w, ttk.Entry)]
        self.assertTrue(len(entries) >= 2, "No se encontraron los campos de entrada")

    @patch('gestion_inventario.messagebox')
    def test_envio_valido(self, mock_msg):
        """Prueba el envío válido del formulario"""
        self.app.show_register_sale()
        
        # Simular entrada de datos
        for child in self.app.content_frame.winfo_children():
            if isinstance(child, ttk.Entry):
                child.insert(0, "Test")
        
        # Encontrar y hacer clic en botón Registrar
        submit_buttons = [w for w in self.app.content_frame.winfo_children()
                        if isinstance(w, ttk.Button) and "Registrar" in str(w.cget("text"))]
        
        if submit_buttons:
            submit_buttons[0].invoke()
            self.mock_mediator.return_value.register_sale.assert_called_once()
        else:
            self.fail("No se encontró el botón Registrar")

    @patch('gestion_inventario.messagebox')
    def test_envio_invalido(self, mock_msg):
        """Prueba el envío inválido del formulario"""
        self.app.show_register_sale()
        
        # Encontrar y hacer clic en botón Registrar sin completar campos
        submit_buttons = [w for w in self.app.content_frame.winfo_children()
                        if isinstance(w, ttk.Button) and "Registrar" in str(w.cget("text"))]
        
        if submit_buttons:
            submit_buttons[0].invoke()
            mock_msg.showerror.assert_called_once()
        else:
            self.fail("No se encontró el botón Registrar")

if __name__ == '__main__':
    unittest.main()
