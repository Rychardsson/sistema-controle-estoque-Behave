"""
Migrations para criação das tabelas do banco de dados
"""
from .connection import get_database_connection


def create_tables() -> None:
    """Cria todas as tabelas necessárias no banco"""
    
    db = get_database_connection()
    
    # Script SQL para criar as tabelas
    script = """
    -- Tabela de produtos
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT,
        preco_unitario REAL DEFAULT 0.0,
        estoque_atual INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabela de movimentações
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saida')),
        quantidade INTEGER NOT NULL CHECK (quantidade > 0),
        observacao TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (produto_id) REFERENCES produtos (id) ON DELETE CASCADE
    );
    
    -- Índices para melhorar performance
    CREATE INDEX IF NOT EXISTS idx_produtos_nome ON produtos(nome);
    CREATE INDEX IF NOT EXISTS idx_movimentacoes_produto_id ON movimentacoes(produto_id);
    CREATE INDEX IF NOT EXISTS idx_movimentacoes_tipo ON movimentacoes(tipo);
    CREATE INDEX IF NOT EXISTS idx_movimentacoes_created_at ON movimentacoes(created_at);
    
    -- Trigger para atualizar updated_at automaticamente
    CREATE TRIGGER IF NOT EXISTS update_produtos_updated_at
        AFTER UPDATE ON produtos
        FOR EACH ROW
    BEGIN
        UPDATE produtos SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;
    """
    
    db.execute_script(script)


def drop_tables() -> None:
    """Remove todas as tabelas (usado para testes)"""
    
    db = get_database_connection()
    
    script = """
    DROP TABLE IF EXISTS movimentacoes;
    DROP TABLE IF EXISTS produtos;
    DROP TRIGGER IF EXISTS update_produtos_updated_at;
    """
    
    db.execute_script(script)


def reset_database() -> None:
    """Reseta o banco de dados - remove e recria as tabelas"""
    drop_tables()
    create_tables()


if __name__ == "__main__":
    # Executar migrations quando o script for executado diretamente
    print("Criando tabelas do banco de dados...")
    create_tables()
    print("Tabelas criadas com sucesso!")
