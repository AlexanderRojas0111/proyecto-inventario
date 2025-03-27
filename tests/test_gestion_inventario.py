import unittest
from gestion_inventario import app  # Asegúrate de que la importación sea correcta

class TestGestionInventarioApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_show_register_sale(self):
        """Prueba que verifica la visualización del registro de ventas."""
        entries = self.app.get_all_entry_widgets()
        self.assertGreater(len(entries), 0, "No se encontraron widgets de entrada")
        
        client_entry = entries[0] if entries else None
        self.assertIsNotNone(client_entry, "No se encontraron widgets de entrada necesarios para la prueba")
        # ... resto del código ...


    # Otras pruebas...

if __name__ == '__main__':
    unittest.main()
