import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import csv
import os
from migrar_db import main

class TestMigrarDB(unittest.TestCase):

    @patch('migrar_db.sqlite3.connect')
    @patch('migrar_db.open', new_callable=unittest.mock.mock_open, read_data="Correo,Contraseña,Nombre\nadmin@example.com,password,Admin\nuser@example.com,1234,User")
    def test_insert_users(self, mock_open, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value

        main()

        mock_cursor.execute.assert_any_call('''
            INSERT INTO users (Correo, Contraseña, Nombre)
            VALUES (?, ?, ?)
        ''', ('admin@example.com', 'password', 'Admin'))
        mock_cursor.execute.assert_any_call('''
            INSERT INTO users (Correo, Contraseña, Nombre)
            VALUES (?, ?, ?)
        ''', ('user@example.com', '1234', 'User'))
        mock_conn.commit.assert_called_once()

    @patch('migrar_db.sqlite3.connect')
    @patch('migrar_db.open', new_callable=unittest.mock.mock_open, read_data="ID_Producto,Nombre,Stock_Actual,Stock_Minimo,Precio_Unitario\nP001,Producto 1,50,10,100.0\nP002,Producto 2,20,5,200.0")
    def test_insert_products(self, mock_open, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value

        main()

        mock_cursor.execute.assert_any_call('''
            INSERT INTO products (ID_Producto, Nombre, Stock_Actual, Stock_Minimo, Precio_Unitario)
            VALUES (?, ?, ?, ?, ?)
        ''', ('P001', 'Producto 1', 50, 10, 100.0))
        mock_cursor.execute.assert_any_call('''
            INSERT INTO products (ID_Producto, Nombre, Stock_Actual, Stock_Minimo, Precio_Unitario)
            VALUES (?, ?, ?, ?, ?)
        ''', ('P002', 'Producto 2', 20, 5, 200.0))
        mock_conn.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()