"""
Serviço para gerenciamento de produtos
"""
import sqlite3
from typing import List, Optional
from datetime import datetime

from ..models.produto import Produto
from ..database.connection import get_database_connection
from ..exceptions.estoque_exceptions import ProdutoNaoEncontradoException


class ProdutoService:
    """Serviço para operações CRUD de produtos"""
    
    def __init__(self, db_connection=None):
        """
        Inicializa o serviço
        
        Args:
            db_connection: Conexão com banco (usado para testes)
        """
        self.db = db_connection or get_database_connection()
    
    def criar_produto(self, produto: Produto) -> Produto:
        """
        Cria um novo produto no banco
        
        Args:
            produto: Instância do produto a ser criado
            
        Returns:
            Produto criado com ID preenchido
            
        Raises:
            ValueError: Se já existe produto com o mesmo nome
        """
        with self.db.get_cursor() as cursor:
            try:
                cursor.execute("""
                    INSERT INTO produtos (nome, descricao, preco_unitario, estoque_atual, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    produto.nome,
                    produto.descricao,
                    produto.preco_unitario,
                    produto.estoque_atual,
                    produto.created_at,
                    produto.updated_at
                ))
                
                produto.id = cursor.lastrowid
                return produto
                
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    raise ValueError(f"Já existe um produto com o nome '{produto.nome}'")
                raise
    
    def buscar_produto_por_id(self, produto_id: int) -> Produto:
        """
        Busca um produto pelo ID
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Produto encontrado
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não for encontrado
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
            row = cursor.fetchone()
            
            if not row:
                raise ProdutoNaoEncontradoException(produto_id)
            
            return self._row_to_produto(row)
    
    def buscar_produto_por_nome(self, nome: str) -> Produto:
        """
        Busca um produto pelo nome
        
        Args:
            nome: Nome do produto
            
        Returns:
            Produto encontrado
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não for encontrado
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
            row = cursor.fetchone()
            
            if not row:
                raise ProdutoNaoEncontradoException(nome)
            
            return self._row_to_produto(row)
    
    def listar_produtos(self) -> List[Produto]:
        """
        Lista todos os produtos
        
        Returns:
            Lista de produtos
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM produtos ORDER BY nome")
            rows = cursor.fetchall()
            
            return [self._row_to_produto(row) for row in rows]
    
    def atualizar_produto(self, produto: Produto) -> Produto:
        """
        Atualiza um produto existente
        
        Args:
            produto: Produto com dados atualizados
            
        Returns:
            Produto atualizado
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não for encontrado
        """
        if produto.id is None:
            raise ValueError("Produto deve ter ID para ser atualizado")
        
        # Verifica se produto existe
        self.buscar_produto_por_id(produto.id)
        
        produto.updated_at = datetime.now()
        
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE produtos 
                SET nome = ?, descricao = ?, preco_unitario = ?, estoque_atual = ?, updated_at = ?
                WHERE id = ?
            """, (
                produto.nome,
                produto.descricao,
                produto.preco_unitario,
                produto.estoque_atual,
                produto.updated_at,
                produto.id
            ))
            
            return produto
    
    def excluir_produto(self, produto_id: int) -> None:
        """
        Exclui um produto
        
        Args:
            produto_id: ID do produto a ser excluído
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não for encontrado
        """
        # Verifica se produto existe
        self.buscar_produto_por_id(produto_id)
        
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    
    def atualizar_estoque(self, produto_id: int, nova_quantidade: int) -> Produto:
        """
        Atualiza apenas o estoque de um produto
        
        Args:
            produto_id: ID do produto
            nova_quantidade: Nova quantidade em estoque
            
        Returns:
            Produto atualizado
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não for encontrado
            ValueError: Se quantidade for negativa
        """
        if nova_quantidade < 0:
            raise ValueError("Estoque não pode ser negativo")
        
        produto = self.buscar_produto_por_id(produto_id)
        produto.atualizar_estoque(nova_quantidade)
        
        return self.atualizar_produto(produto)
    
    def _row_to_produto(self, row) -> Produto:
        """
        Converte uma linha do banco em objeto Produto
        
        Args:
            row: Linha do banco de dados
            
        Returns:
            Instância de Produto
        """
        return Produto(
            id=row['id'],
            nome=row['nome'],
            descricao=row['descricao'],
            preco_unitario=row['preco_unitario'],
            estoque_atual=row['estoque_atual'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None
        )
