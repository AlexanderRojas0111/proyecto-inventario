import unittest
from gestion_inventario import app  # Asegúrate de que la importación sea correcta

class TestGestionInventarioApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_show_register_sale(self):
        # ... código existente ...
        entries = self.app.get_all_entry_widgets()
        self.assertGreater(len(entries), 0, "No se encontraron widgets de entrada")
        if len(entries) > 0:
            client_entry = entries[0]
            # ... resto del código ...
        else:
            self.fail("No se encontraron widgets de entrada necesarios para la prueba")

    # Otras pruebas...

if __name__ == '__main__':
    unittest.main()
