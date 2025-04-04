import sqlite3
import logging
from typing import List, Tuple, Optional, Any
from abc import ABC, abstractmethod

class DatabaseException(Exception):
    """Excepción base para errores de base de datos"""
    pass

class ConnectionError(DatabaseException):
    """Error al conectar a la base de datos"""
    pass

class QueryExecutionError(DatabaseException):
    """Error al ejecutar una consulta"""
    pass

class DatabaseRepository(ABC):
    """Interfaz abstracta para el patrón Repository"""
    @abstractmethod
    def execute(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Cursor]:
        pass
    
    @abstractmethod
    def fetch_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        pass
    
    @abstractmethod
    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Tuple]:
        pass
    
    @abstractmethod
    def save_bulk(self, table: str, data: List[Tuple]) -> None:
        pass

class SQLiteRepository(DatabaseRepository):
    """Implementación concreta para SQLite usando Singleton"""
    _instance = None
    DATABASE = 'inventario.db'
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Configuración inicial del repositorio"""
        self._setup_logging()
        self.connection = self._connect()
    
    def _setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            filename='error.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SQLiteRepository')
    
    def _connect(self) -> sqlite3.Connection:
        """Establece la conexión con la base de datos"""
        try:
            conn = sqlite3.connect(self.DATABASE)
            conn.row_factory = sqlite3.Row
            self.logger.info("Conexión a la base de datos establecida")
            return conn
        except sqlite3.Error as e:
            self.logger.critical(f"Error de conexión: {e}")
            raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")
    
    def execute(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Cursor]:
        """Ejecuta una consulta de escritura"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            self.logger.debug(f"Consulta ejecutada: {query[:50]}...")
            return cursor
        except sqlite3.Error as e:
            self.logger.error(f"Error en execute: {e} - Query: {query[:100]}...")
            raise QueryExecutionError(f"Error al ejecutar consulta: {e}")
    
    def fetch_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Recupera múltiples registros"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            self.logger.debug(f"FetchAll: {len(results)} resultados")
            return results
        except sqlite3.Error as e:
            self.logger.error(f"Error en fetch_all: {e} - Query: {query[:100]}...")
            raise QueryExecutionError(f"Error al recuperar datos: {e}")
    
    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Tuple]:
        """Recupera un único registro"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            self.logger.debug(f"FetchOne: {result}")
            return result
        except sqlite3.Error as e:
            self.logger.error(f"Error en fetch_one: {e} - Query: {query[:100]}...")
            raise QueryExecutionError(f"Error al recuperar dato: {e}")
    
    def save_bulk(self, table: str, data: List[Tuple]) -> None:
        """Inserta múltiples registros"""
        if not data:
            self.logger.warning(f"Intento de insertar datos vacíos en {table}")
            return
            
        try:
            placeholders = ', '.join(['?'] * len(data[0]))
            query = f"INSERT INTO {table} VALUES ({placeholders})"
            self.connection.executemany(query, data)
            self.connection.commit()
            self.logger.info(f"Insertados {len(data)} registros en {table}")
        except sqlite3.Error as e:
            self.logger.error(f"Error en save_bulk: {e} - Tabla: {table}")
            raise QueryExecutionError(f"Error al guardar datos: {e}")

# Funciones legacy para mantener compatibilidad
def connect_db():
    return SQLiteRepository().connection

def execute_query(query, params=()):
    return SQLiteRepository().execute(query, params)

def fetch_all(query, params=()):
    return SQLiteRepository().fetch_all(query, params)

def fetch_one(query, params=()):
    return SQLiteRepository().fetch_one(query, params)

def load_data(table_name):
    return SQLiteRepository().fetch_all(f"SELECT * FROM {table_name}")

def save_data(table_name, data):
    SQLiteRepository().save_bulk(table_name, data)

if __name__ == "__main__":
    # Ejemplo de uso con el nuevo repositorio
    repo = SQLiteRepository()
    try:
        # Insertar datos de prueba
        sample_data = [
            ('P001', 'Producto 1', 50, 10, 100.0),
            ('P002', 'Producto 2', 30, 5, 200.0)
        ]
        repo.save_bulk('products', sample_data)
        
        # Consultar datos
        products = repo.fetch_all("SELECT * FROM products")
        print("Productos:", products)
        
    except DatabaseException as e:
        print(f"Error en la operación: {e}")
