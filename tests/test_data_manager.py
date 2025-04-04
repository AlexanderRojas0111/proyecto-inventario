import unittest
from unittest.mock import patch, MagicMock, call
import sqlite3
from data_manager import (
    execute_query, fetch_all, fetch_one, load_data, save_data,
    SQLiteRepository, DatabaseException, ConnectionError, QueryExecutionError
)

class TestSQLiteRepository(unittest.TestCase):
    def setUp(self):
        self.repo = SQLiteRepository()
        self.repo.connection = MagicMock()
        self.repo.logger = MagicMock()

    def test_singleton_pattern(self):
        repo1 = SQLiteRepository()
        repo2 = SQLiteRepository()
        self.assertIs(repo1, repo2)

    def test_execute_success(self):
        mock_cursor = MagicMock()
        self.repo.connection.cursor.return_value = mock_cursor
        
        query = "INSERT INTO test VALUES (?, ?)"
        params = (1, "test")
        result = self.repo.execute(query, params)
        
        mock_cursor.execute.assert_called_once_with(query, params)
        self.repo.connection.commit.assert_called_once()
        self.assertEqual(result, mock_cursor)
        self.repo.logger.debug.assert_called()

    def test_execute_failure(self):
        self.repo.connection.cursor.side_effect = sqlite3.Error("Test error")
        
        with self.assertRaises(QueryExecutionError):
            self.repo.execute("BAD QUERY")
        
        self.repo.logger.error.assert_called()

    def test_fetch_all_success(self):
        expected = [("row1",), ("row2",)]
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = expected
        self.repo.connection.cursor.return_value = mock_cursor
        
        result = self.repo.fetch_all("SELECT * FROM test")
        
        self.assertEqual(result, expected)
        self.repo.logger.debug.assert_called()

    def test_save_bulk_empty_data(self):
        self.repo.save_bulk("test", [])
        self.repo.logger.warning.assert_called()

class TestLegacyFunctions(unittest.TestCase):
    @patch('data_manager.SQLiteRepository')
    def test_execute_query(self, mock_repo):
        mock_instance = mock_repo.return_value
        execute_query("test", (1,))
        mock_instance.execute.assert_called_once_with("test", (1,))

    @patch('data_manager.SQLiteRepository')
    def test_fetch_all(self, mock_repo):
        mock_instance = mock_repo.return_value
        fetch_all("test", (1,))
        mock_instance.fetch_all.assert_called_once_with("test", (1,))

    @patch('data_manager.SQLiteRepository')
    def test_save_data(self, mock_repo):
        mock_instance = mock_repo.return_value
        data = [("test",)]
        save_data("table", data)
        mock_instance.save_bulk.assert_called_once_with("table", data)

class TestExceptionHandling(unittest.TestCase):
    def test_connection_error(self):
        with patch('data_manager.sqlite3.connect', side_effect=sqlite3.Error("Connection failed")):
            with self.assertRaises(ConnectionError):
                repo = SQLiteRepository()

    def test_query_execution_error(self):
        repo = SQLiteRepository()
        repo.connection = MagicMock()
        repo.connection.cursor.side_effect = sqlite3.Error("Query failed")
        
        with self.assertRaises(QueryExecutionError):
            repo.execute("BAD QUERY")

if __name__ == "__main__":
    unittest.main()
