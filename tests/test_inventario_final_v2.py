import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch, MagicMock
from gestion_inventario import GestionInventarioApp

class TestInventarioFinal(unittest.TestCase):
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
        cls.root.after(100, lambda: None)  # Pequeña pausa para inicialización

    @classmethod
    def tearDownClass(cls):
        cls.mediator_patch.stop()
        cls.root.destroy()

    def buscar_widget(self, padre, tipo=None, texto=None):
        """Busca widgets recursivamente según tipo y/o texto"""
        widgets = []
        for child in padre.winfo_children():
            if tipo and isinstance(child, tipo):
                if texto and hasattr(child, 'cget') and texto in str(child.cget('text')):
                    widgets.append(child)
                elif not texto:
                    widgets.append(child)
            widgets.extend(self.buscar_widget(child, tipo, texto))
        return widgets

    def test_ui_inicializacion(self):
        """Verifica creación de componentes principales"""
        self.assertIsNotNone(self.app.content_frame)
        menu_buttons = self.buscar_widget(self.root, ttk.Button)
        self.assertGreaterEqual(len(menu_buttons), 4)

    @patch('gestion_inventario.messagebox')
    def test_envio_valido(self, mock_msg):
        """Prueba envío válido del formulario"""
        self.app.show_register_sale()
        self.root.update()
        
        # Llenar formulario
        entries = self.buscar_widget(self.app.content_frame, ttk.Entry)
        for entry in entries:
            entry.insert(0, "123")  # Valor numérico para campos de cantidad/precio
        
        # Encontrar y presionar botón
        submit_btn = self.buscar_widget(self.app.content_frame, ttk.Button, "Registrar")[0]
        submit_btn.invoke()
        self.root.update()
        
        # Verificar llamada al mediador
        self.mock_mediator.return_value.register_sale.assert_called_once()

    @patch('gestion_inventario.messagebox')
    def test_envio_invalido(self, mock_msg):
        """Prueba envío inválido del formulario"""
        self.app.show_register_sale()
        self.root.update()
        
        submit_btn = self.buscar_widget(self.app.content_frame, ttk.Button, "Registrar")[0]
        submit_btn.invoke()
        self.root.update()
        
        mock_msg.showerror.assert_called_once()

if __name__ == '__main__':
    unittest.main()
