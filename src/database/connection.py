"""
Gerenciamento de conexão com o banco de dados SQLite
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional


class DatabaseConnection:
    """Classe para gerenciar conexões com o banco SQLite"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa a conexão com o banco
        
        Args:
            db_path: Caminho para o arquivo do banco. Se None, usa 'estoque.db'
        """
        if db_path is None:
            db_path = "estoque.db"
        
        self.db_path = db_path
        self._connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> sqlite3.Connection:
        """
        Cria e retorna uma conexão com o banco
        
        Returns:
            Conexão SQLite
        """
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row  # Para acessar colunas por nome
        
        return self._connection
    
    def close(self) -> None:
        """Fecha a conexão com o banco"""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    @contextmanager
    def get_cursor(self):
        """
        Context manager para obter um cursor
        
        Yields:
            Cursor SQLite
        """
        conn = self.connect()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
    
    def execute_script(self, script: str) -> None:
        """
        Executa um script SQL
        
        Args:
            script: Script SQL para executar
        """
        with self.get_cursor() as cursor:
            cursor.executescript(script)
    
    def reset_database(self) -> None:
        """Remove o arquivo do banco se existir"""
        self.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


# Instância singleton para uso global
_db_connection: Optional[DatabaseConnection] = None


def get_database_connection(db_path: Optional[str] = None) -> DatabaseConnection:
    """
    Retorna a instância singleton da conexão com banco
    
    Args:
        db_path: Caminho para o banco (usado apenas na primeira chamada)
        
    Returns:
        Instância de DatabaseConnection
    """
    global _db_connection
    
    if _db_connection is None:
        _db_connection = DatabaseConnection(db_path)
    
    return _db_connection


def set_database_connection(db_connection: DatabaseConnection) -> None:
    """
    Define a instância da conexão com banco (usado para testes)
    
    Args:
        db_connection: Nova instância de DatabaseConnection
    """
    global _db_connection
    _db_connection = db_connection
