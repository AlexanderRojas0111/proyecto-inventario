import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from data_manager import execute_query, fetch_all, fetch_one, load_data, save_data

class TestDataManager(unittest.TestCase):

    @patch('data_manager.sqlite3.connect')
    def test_execute_query(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value

        query = "INSERT INTO test_table (col1, col2) VALUES (?, ?)"
        params = ("value1", "value2")
        execute_query(query, params)

        mock_cursor.execute.assert_called_once_with(query, params)
        mock_conn.commit.assert_called_once()

    @patch('data_manager.sqlite3.connect')
    def test_fetch_all(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [("row1_col1", "row1_col2"), ("row2_col1", "row2_col2")]

        query = "SELECT * FROM test_table"
        result = fetch_all(query)

        mock_cursor.execute.assert_called_once_with(query, ())
        self.assertEqual(result, [("row1_col1", "row1_col2"), ("row2_col1", "row2_col2")])

    @patch('data_manager.sqlite3.connect')
    def test_fetch_one(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ("row1_col1", "row1_col2")

        query = "SELECT * FROM test_table WHERE col1 = ?"
        params = ("value1",)
        result = fetch_one(query, params)

        mock_cursor.execute.assert_called_once_with(query, params)
        self.assertEqual(result, ("row1_col1", "row1_col2"))

    @patch('data_manager.fetch_all')
    def test_load_data(self, mock_fetch_all):
        mock_fetch_all.return_value = [("row1_col1", "row1_col2"), ("row2_col1", "row2_col2")]

        table_name = "test_table"
        result = load_data(table_name)

        mock_fetch_all.assert_called_once_with(f"SELECT * FROM {table_name}")
        self.assertEqual(result, [("row1_col1", "row1_col2"), ("row2_col1", "row2_col2")])

    @patch('data_manager.sqlite3.connect')
    def test_save_data(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value

        table_name = "test_table"
        data = [("value1", "value2"), ("value3", "value4")]
        save_data(table_name, data)

        placeholders = ', '.join(['?'] * len(data[0]))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        mock_cursor.executemany.assert_called_once_with(query, data)
        mock_conn.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()