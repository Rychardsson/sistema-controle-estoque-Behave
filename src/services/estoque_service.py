"""
Serviço para gerenciamento de estoque e movimentações
"""
import sqlite3
from typing import List, Optional
from datetime import datetime

from ..models.produto import Produto
from ..models.movimentacao import Movimentacao, TipoMovimentacao
from ..database.connection import get_database_connection
from ..exceptions.estoque_exceptions import (
    EstoqueInsuficienteException,
    ProdutoNaoEncontradoException,
    MovimentacaoInvalidaException,
    EstoqueNegativoException
)
from .produto_service import ProdutoService


class EstoqueService:
    """Serviço para gerenciamento de movimentações de estoque"""
    
    def __init__(self, db_connection=None):
        """
        Inicializa o serviço
        
        Args:
            db_connection: Conexão com banco (usado para testes)
        """
        self.db = db_connection or get_database_connection()
        self.produto_service = ProdutoService(db_connection)
    
    def registrar_entrada(self, produto_id: int, quantidade: int, observacao: Optional[str] = None) -> Movimentacao:
        """
        Registra uma entrada de estoque
        
        Args:
            produto_id: ID do produto
            quantidade: Quantidade a ser adicionada
            observacao: Observação opcional
            
        Returns:
            Movimentação criada
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não existir
            MovimentacaoInvalidaException: Se dados inválidos
        """
        if quantidade <= 0:
            raise MovimentacaoInvalidaException("Quantidade deve ser maior que zero")
        
        # Verifica se produto existe
        produto = self.produto_service.buscar_produto_por_id(produto_id)
        
        # Cria a movimentação
        movimentacao = Movimentacao(
            produto_id=produto_id,
            tipo=TipoMovimentacao.ENTRADA,
            quantidade=quantidade,
            observacao=observacao
        )
        
        # Salva movimentação e atualiza estoque em transação
        with self.db.get_cursor() as cursor:
            # Insere movimentação
            cursor.execute("""
                INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                movimentacao.produto_id,
                movimentacao.tipo.value,
                movimentacao.quantidade,
                movimentacao.observacao,
                movimentacao.created_at
            ))
            
            movimentacao.id = cursor.lastrowid
            
            # Atualiza estoque do produto
            novo_estoque = produto.estoque_atual + quantidade
            cursor.execute("""
                UPDATE produtos SET estoque_atual = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (novo_estoque, produto_id))
        
        return movimentacao
    
    def registrar_saida(self, produto_id: int, quantidade: int, observacao: Optional[str] = None) -> Movimentacao:
        """
        Registra uma saída de estoque
        
        Args:
            produto_id: ID do produto
            quantidade: Quantidade a ser retirada
            observacao: Observação opcional
            
        Returns:
            Movimentação criada
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não existir
            EstoqueInsuficienteException: Se não há estoque suficiente
            MovimentacaoInvalidaException: Se dados inválidos
        """
        if quantidade <= 0:
            raise MovimentacaoInvalidaException("Quantidade deve ser maior que zero")
        
        # Verifica se produto existe
        produto = self.produto_service.buscar_produto_por_id(produto_id)
        
        # Verifica se há estoque suficiente
        if not produto.tem_estoque_suficiente(quantidade):
            raise EstoqueInsuficienteException(
                produto_nome=produto.nome,
                estoque_atual=produto.estoque_atual,
                quantidade_solicitada=quantidade
            )
        
        # Cria a movimentação
        movimentacao = Movimentacao(
            produto_id=produto_id,
            tipo=TipoMovimentacao.SAIDA,
            quantidade=quantidade,
            observacao=observacao
        )
        
        # Salva movimentação e atualiza estoque em transação
        with self.db.get_cursor() as cursor:
            # Insere movimentação
            cursor.execute("""
                INSERT INTO movimentacoes (produto_id, tipo, quantidade, observacao, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (
                movimentacao.produto_id,
                movimentacao.tipo.value,
                movimentacao.quantidade,
                movimentacao.observacao,
                movimentacao.created_at
            ))
            
            movimentacao.id = cursor.lastrowid
            
            # Atualiza estoque do produto
            novo_estoque = produto.estoque_atual - quantidade
            cursor.execute("""
                UPDATE produtos SET estoque_atual = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (novo_estoque, produto_id))
        
        return movimentacao
    
    def listar_movimentacoes(self, produto_id: Optional[int] = None, 
                           tipo: Optional[TipoMovimentacao] = None) -> List[Movimentacao]:
        """
        Lista movimentações com filtros opcionais
        
        Args:
            produto_id: ID do produto (opcional)
            tipo: Tipo de movimentação (opcional)
            
        Returns:
            Lista de movimentações
        """
        query = "SELECT * FROM movimentacoes WHERE 1=1"
        params = []
        
        if produto_id is not None:
            query += " AND produto_id = ?"
            params.append(produto_id)
        
        if tipo is not None:
            query += " AND tipo = ?"
            params.append(tipo.value)
        
        query += " ORDER BY created_at DESC"
        
        with self.db.get_cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [self._row_to_movimentacao(row) for row in rows]
    
    def obter_saldo_produto(self, produto_id: int) -> int:
        """
        Calcula o saldo atual de um produto baseado nas movimentações
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Saldo atual do produto
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não existir
        """
        # Verifica se produto existe
        self.produto_service.buscar_produto_por_id(produto_id)
        
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN tipo = 'entrada' THEN quantidade ELSE 0 END), 0) as entradas,
                    COALESCE(SUM(CASE WHEN tipo = 'saida' THEN quantidade ELSE 0 END), 0) as saidas
                FROM movimentacoes 
                WHERE produto_id = ?
            """, (produto_id,))
            
            row = cursor.fetchone()
            entradas = row['entradas'] or 0
            saidas = row['saidas'] or 0
            
            return entradas - saidas
    
    def recalcular_estoque_produto(self, produto_id: int) -> Produto:
        """
        Recalcula o estoque de um produto baseado nas movimentações
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Produto com estoque atualizado
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não existir
        """
        saldo_calculado = self.obter_saldo_produto(produto_id)
        return self.produto_service.atualizar_estoque(produto_id, saldo_calculado)
    
    def verificar_estoque_disponivel(self, produto_id: int, quantidade: int) -> bool:
        """
        Verifica se há estoque suficiente para uma operação
        
        Args:
            produto_id: ID do produto
            quantidade: Quantidade desejada
            
        Returns:
            True se há estoque suficiente
            
        Raises:
            ProdutoNaoEncontradoException: Se produto não existir
        """
        produto = self.produto_service.buscar_produto_por_id(produto_id)
        return produto.tem_estoque_suficiente(quantidade)
    
    def obter_produtos_com_estoque_baixo(self, limite: int = 5) -> List[Produto]:
        """
        Retorna produtos com estoque abaixo do limite
        
        Args:
            limite: Limite mínimo de estoque
            
        Returns:
            Lista de produtos com estoque baixo
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM produtos 
                WHERE estoque_atual <= ? 
                ORDER BY estoque_atual ASC, nome ASC
            """, (limite,))
            
            rows = cursor.fetchall()
            return [self.produto_service._row_to_produto(row) for row in rows]
    
    def _row_to_movimentacao(self, row) -> Movimentacao:
        """
        Converte uma linha do banco em objeto Movimentacao
        
        Args:
            row: Linha do banco de dados
            
        Returns:
            Instância de Movimentacao
        """
        return Movimentacao(
            id=row['id'],
            produto_id=row['produto_id'],
            tipo=TipoMovimentacao(row['tipo']),
            quantidade=row['quantidade'],
            observacao=row['observacao'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )
