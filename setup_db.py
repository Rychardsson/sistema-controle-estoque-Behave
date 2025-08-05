"""
Script para inicializar o banco de dados
"""
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.database.migrations import create_tables

if __name__ == "__main__":
    print("Criando tabelas do banco de dados...")
    create_tables()
    print("Tabelas criadas com sucesso!")
