"""
Configuração do ambiente para testes BDD
"""
import os
import tempfile
from pathlib import Path

from src.database.connection import DatabaseConnection, set_database_connection
from src.database.migrations import create_tables, drop_tables


def before_all(context):
    """Executado uma vez antes de todos os testes"""
    # Cria um banco de dados temporário para os testes
    context.temp_dir = tempfile.mkdtemp()
    context.test_db_path = os.path.join(context.temp_dir, "test_estoque.db")
    
    # Configura conexão com banco de teste
    context.db_connection = DatabaseConnection(context.test_db_path)
    set_database_connection(context.db_connection)
    
    # Cria as tabelas
    create_tables()


def before_scenario(context, scenario):
    """Executado antes de cada cenário"""
    # Limpa as tabelas para cada cenário
    drop_tables()
    create_tables()
    
    # Reinicia variáveis de contexto
    context.produtos = {}
    context.movimentacoes = []
    context.ultimo_erro = None
    context.ultima_mensagem = None


def after_all(context):
    """Executado uma vez após todos os testes"""
    # Fecha conexão e limpa arquivos temporários
    if hasattr(context, 'db_connection'):
        context.db_connection.close()
    
    if hasattr(context, 'temp_dir'):
        import shutil
        shutil.rmtree(context.temp_dir, ignore_errors=True)
