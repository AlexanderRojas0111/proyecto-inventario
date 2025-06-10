import unittest
from unittest.mock import patch, MagicMock, call
import sqlite3
from migrar_db import main

class TestMigrarDB(unittest.TestCase):

    @patch('migrar_db.sqlite3.connect')
    @patch('migrar_db.open', new_callable=unittest.mock.mock_open, read_data="Correo,Contraseña,Nombre\nadmin@example.com,password,Admin\nuser@example.com,1234,User")



    def test_insert_users(self, mock_open, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Sobreescribir la función que verifica si existen columnas
        # para que siempre devuelva True
        with patch('migrar_db.column_exists', return_value=True):
            main()

        # Busca una llamada similar en lugar de exigir formato exacto
        found = False
        for call_args in mock_cursor.execute.call_args_list:
            query = call_args[0][0].strip().replace('\n', ' ').replace('    ', ' ')
            if ('INSERT INTO users' in query and 
                'Correo' in query and 
                'Contraseña' in query and 
                'Nombre' in query):
                params = call_args[0][1]
                if params == ('admin@example.com', 'password', 'Admin'):
                    found = True
                    break
        
        self.assertTrue(found, "No se encontró la inserción del usuario admin con los parámetros correctos")

    @patch('migrar_db.sqlite3.connect')
    @patch('migrar_db.open', new_callable=unittest.mock.mock_open, read_data="ID_Producto,Nombre,Stock_Actual,Stock_Minimo,Precio_Unitario\nP001,Producto 1,50,10,100.0\nP002,Producto 2,20,5,200.0")




    def test_insert_products(self, mock_open, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Sobreescribir la función que verifica si existen columnas
        # para que siempre devuelva True
        with patch('migrar_db.column_exists', return_value=True):
            main()

        # Busca una llamada similar en lugar de exigir formato exacto
        found = False
        for call_args in mock_cursor.execute.call_args_list:
            if len(call_args[0]) < 2:
                continue  # Saltamos llamadas sin parámetros
                
            query = call_args[0][0].strip().replace('\n', ' ').replace('    ', ' ')
            if ('INSERT INTO products' in query and 
                'ID_Producto' in query and 
                'Nombre' in query and 
                'Stock_Actual' in query and 
                'Stock_Minimo' in query and 
                'Precio_Unitario' in query):
                params = call_args[0][1]
                if params == ('P001', 'Producto 1', 50, 10, 100.0):
                    found = True
                    break
        
        self.assertTrue(found, "No se encontró la inserción del producto P001 con los parámetros correctos")

if __name__ == "__main__":
    unittest.main()
