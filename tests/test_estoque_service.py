"""
Testes unitários para EstoqueService
"""
import pytest
import tempfile
import os

from src.models.produto import Produto
from src.models.movimentacao import Movimentacao, TipoMovimentacao
from src.services.produto_service import ProdutoService
from src.services.estoque_service import EstoqueService
from src.database.connection import DatabaseConnection
from src.database.migrations import create_tables
from src.exceptions.estoque_exceptions import (
    EstoqueInsuficienteException,
    MovimentacaoInvalidaException,
    ProdutoNaoEncontradoException
)


class TestEstoqueService:
    """Testes para o serviço de estoque"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup executado antes de cada teste"""
        # Cria banco temporário para cada teste
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test.db")
        
        self.db_connection = DatabaseConnection(self.test_db_path)
        create_tables()
        
        self.produto_service = ProdutoService(self.db_connection)
        self.estoque_service = EstoqueService(self.db_connection)
        
        # Cria produto padrão para testes
        self.produto_teste = Produto(nome="Produto Teste", estoque_atual=10)
        self.produto_teste = self.produto_service.criar_produto(self.produto_teste)
        
        yield
        
        # Cleanup
        self.db_connection.close()
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_registrar_entrada_sucesso(self):
        """Testa registro de entrada com sucesso"""
        estoque_inicial = self.produto_teste.estoque_atual
        quantidade_entrada = 15
        
        movimentacao = self.estoque_service.registrar_entrada(
            produto_id=self.produto_teste.id,
            quantidade=quantidade_entrada,
            observacao="Entrada teste"
        )
        
        # Verifica movimentação
        assert movimentacao.id is not None
        assert movimentacao.produto_id == self.produto_teste.id
        assert movimentacao.quantidade == quantidade_entrada
        assert movimentacao.is_entrada()
        assert movimentacao.observacao == "Entrada teste"
        
        # Verifica atualização do estoque
        produto_atualizado = self.produto_service.buscar_produto_por_id(self.produto_teste.id)
        assert produto_atualizado.estoque_atual == estoque_inicial + quantidade_entrada
    
    def test_registrar_entrada_quantidade_zero(self):
        """Testa erro ao registrar entrada com quantidade zero"""
        with pytest.raises(MovimentacaoInvalidaException, match="Quantidade deve ser maior que zero"):
            self.estoque_service.registrar_entrada(
                produto_id=self.produto_teste.id,
                quantidade=0
            )
    
    def test_registrar_entrada_quantidade_negativa(self):
        """Testa erro ao registrar entrada com quantidade negativa"""
        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            self.estoque_service.registrar_entrada(
                produto_id=self.produto_teste.id,
                quantidade=-5
            )
    
    def test_registrar_entrada_produto_inexistente(self):
        """Testa erro ao registrar entrada para produto inexistente"""
        with pytest.raises(ProdutoNaoEncontradoException):
            self.estoque_service.registrar_entrada(
                produto_id=999,
                quantidade=10
            )
    
    def test_registrar_saida_sucesso(self):
        """Testa registro de saída com sucesso"""
        estoque_inicial = self.produto_teste.estoque_atual
        quantidade_saida = 5
        
        movimentacao = self.estoque_service.registrar_saida(
            produto_id=self.produto_teste.id,
            quantidade=quantidade_saida,
            observacao="Saída teste"
        )
        
        # Verifica movimentação
        assert movimentacao.id is not None
        assert movimentacao.produto_id == self.produto_teste.id
        assert movimentacao.quantidade == quantidade_saida
        assert movimentacao.is_saida()
        assert movimentacao.observacao == "Saída teste"
        
        # Verifica atualização do estoque
        produto_atualizado = self.produto_service.buscar_produto_por_id(self.produto_teste.id)
        assert produto_atualizado.estoque_atual == estoque_inicial - quantidade_saida
    
    def test_registrar_saida_estoque_insuficiente(self):
        """Testa erro ao registrar saída com estoque insuficiente"""
        quantidade_saida = self.produto_teste.estoque_atual + 5
        
        with pytest.raises(EstoqueInsuficienteException) as exc_info:
            self.estoque_service.registrar_saida(
                produto_id=self.produto_teste.id,
                quantidade=quantidade_saida
            )
        
        # Verifica detalhes da exceção
        exception = exc_info.value
        assert exception.produto_nome == self.produto_teste.nome
        assert exception.estoque_atual == self.produto_teste.estoque_atual
        assert exception.quantidade_solicitada == quantidade_saida
        
        # Verifica que estoque não foi alterado
        produto_atual = self.produto_service.buscar_produto_por_id(self.produto_teste.id)
        assert produto_atual.estoque_atual == self.produto_teste.estoque_atual
    
    def test_registrar_saida_estoque_exato(self):
        """Testa registro de saída com quantidade exata do estoque"""
        quantidade_saida = self.produto_teste.estoque_atual
        
        movimentacao = self.estoque_service.registrar_saida(
            produto_id=self.produto_teste.id,
            quantidade=quantidade_saida
        )
        
        assert movimentacao.id is not None
        
        # Verifica que estoque ficou zerado
        produto_atualizado = self.produto_service.buscar_produto_por_id(self.produto_teste.id)
        assert produto_atualizado.estoque_atual == 0
    
    def test_registrar_saida_quantidade_zero(self):
        """Testa erro ao registrar saída com quantidade zero"""
        with pytest.raises(MovimentacaoInvalidaException, match="Quantidade deve ser maior que zero"):
            self.estoque_service.registrar_saida(
                produto_id=self.produto_teste.id,
                quantidade=0
            )
    
    def test_listar_movimentacoes_todas(self):
        """Testa listagem de todas as movimentações"""
        # Registra algumas movimentações
        self.estoque_service.registrar_entrada(self.produto_teste.id, 20)
        self.estoque_service.registrar_saida(self.produto_teste.id, 5)
        self.estoque_service.registrar_entrada(self.produto_teste.id, 10)
        
        movimentacoes = self.estoque_service.listar_movimentacoes()
        
        assert len(movimentacoes) == 3
        # Verifica que estão ordenadas por data (mais recente primeiro)
        assert movimentacoes[0].created_at >= movimentacoes[1].created_at
        assert movimentacoes[1].created_at >= movimentacoes[2].created_at
    
    def test_listar_movimentacoes_por_produto(self):
        """Testa listagem de movimentações filtrada por produto"""
        # Cria outro produto
        produto2 = Produto(nome="Produto 2", estoque_atual=5)
        produto2 = self.produto_service.criar_produto(produto2)
        
        # Registra movimentações para ambos os produtos
        self.estoque_service.registrar_entrada(self.produto_teste.id, 20)
        self.estoque_service.registrar_entrada(produto2.id, 15)
        self.estoque_service.registrar_saida(self.produto_teste.id, 5)
        
        # Lista movimentações apenas do produto_teste
        movimentacoes = self.estoque_service.listar_movimentacoes(produto_id=self.produto_teste.id)
        
        assert len(movimentacoes) == 2
        for mov in movimentacoes:
            assert mov.produto_id == self.produto_teste.id
    
    def test_listar_movimentacoes_por_tipo(self):
        """Testa listagem de movimentações filtrada por tipo"""
        # Registra movimentações de tipos diferentes
        self.estoque_service.registrar_entrada(self.produto_teste.id, 20)
        self.estoque_service.registrar_entrada(self.produto_teste.id, 10)
        self.estoque_service.registrar_saida(self.produto_teste.id, 5)
        
        # Lista apenas entradas
        entradas = self.estoque_service.listar_movimentacoes(tipo=TipoMovimentacao.ENTRADA)
        assert len(entradas) == 2
        for mov in entradas:
            assert mov.is_entrada()
        
        # Lista apenas saídas
        saidas = self.estoque_service.listar_movimentacoes(tipo=TipoMovimentacao.SAIDA)
        assert len(saidas) == 1
        assert saidas[0].is_saida()
    
    def test_obter_saldo_produto(self):
        """Testa cálculo do saldo de produto baseado nas movimentações"""
        # Registra algumas movimentações
        self.estoque_service.registrar_entrada(self.produto_teste.id, 25)  # +25
        self.estoque_service.registrar_saida(self.produto_teste.id, 8)     # -8
        self.estoque_service.registrar_entrada(self.produto_teste.id, 5)   # +5
        self.estoque_service.registrar_saida(self.produto_teste.id, 3)     # -3
        
        saldo = self.estoque_service.obter_saldo_produto(self.produto_teste.id)
        
        # Saldo inicial (10) + movimentações (25 - 8 + 5 - 3) = 29
        assert saldo == 29
    
    def test_recalcular_estoque_produto(self):
        """Testa recálculo do estoque baseado nas movimentações"""
        # Altera manualmente o estoque do produto para valor incorreto
        self.produto_service.atualizar_estoque(self.produto_teste.id, 999)
        
        # Registra movimentações
        self.estoque_service.registrar_entrada(self.produto_teste.id, 15)
        self.estoque_service.registrar_saida(self.produto_teste.id, 5)
        
        # Recalcula o estoque
        produto_recalculado = self.estoque_service.recalcular_estoque_produto(self.produto_teste.id)
        
        # Deve ser: estoque inicial (10) + entrada (15) - saída (5) = 20
        assert produto_recalculado.estoque_atual == 20
    
    def test_verificar_estoque_disponivel(self):
        """Testa verificação de estoque disponível"""
        assert self.estoque_service.verificar_estoque_disponivel(self.produto_teste.id, 5) == True
        assert self.estoque_service.verificar_estoque_disponivel(self.produto_teste.id, 10) == True
        assert self.estoque_service.verificar_estoque_disponivel(self.produto_teste.id, 15) == False
    
    def test_obter_produtos_com_estoque_baixo(self):
        """Testa listagem de produtos com estoque baixo"""
        # Cria produtos com diferentes níveis de estoque
        produto_baixo1 = Produto(nome="Produto Baixo 1", estoque_atual=2)
        produto_baixo2 = Produto(nome="Produto Baixo 2", estoque_atual=5)
        produto_normal = Produto(nome="Produto Normal", estoque_atual=20)
        
        self.produto_service.criar_produto(produto_baixo1)
        self.produto_service.criar_produto(produto_baixo2)
        self.produto_service.criar_produto(produto_normal)
        
        # Lista produtos com estoque <= 5
        produtos_baixo = self.estoque_service.obter_produtos_com_estoque_baixo(limite=5)
        
        # Deve incluir produto_baixo1, produto_baixo2 e produto_teste (estoque=10)
        # mas não produto_normal
        nomes_baixo = [p.nome for p in produtos_baixo]
        assert "Produto Baixo 1" in nomes_baixo
        assert "Produto Baixo 2" in nomes_baixo
        assert "Produto Normal" not in nomes_baixo
        
        # Verifica ordenação (menor estoque primeiro)
        assert produtos_baixo[0].estoque_atual <= produtos_baixo[-1].estoque_atual
    
    def test_multiplas_operacoes_estoque(self):
        """Testa múltiplas operações de estoque em sequência"""
        produto_id = self.produto_teste.id
        estoque_inicial = self.produto_teste.estoque_atual  # 10
        
        # Série de operações
        self.estoque_service.registrar_entrada(produto_id, 30)   # 10 + 30 = 40
        self.estoque_service.registrar_saida(produto_id, 15)     # 40 - 15 = 25
        self.estoque_service.registrar_entrada(produto_id, 5)    # 25 + 5 = 30
        self.estoque_service.registrar_saida(produto_id, 8)      # 30 - 8 = 22
        self.estoque_service.registrar_saida(produto_id, 12)     # 22 - 12 = 10
        
        # Verifica estoque final
        produto_final = self.produto_service.buscar_produto_por_id(produto_id)
        assert produto_final.estoque_atual == 10
        
        # Verifica que foram criadas 5 movimentações
        movimentacoes = self.estoque_service.listar_movimentacoes(produto_id=produto_id)
        assert len(movimentacoes) == 5
