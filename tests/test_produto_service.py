"""
Testes unitários para ProdutoService
"""
import pytest
import tempfile
import os
from datetime import datetime

from src.models.produto import Produto
from src.services.produto_service import ProdutoService
from src.database.connection import DatabaseConnection
from src.database.migrations import create_tables, drop_tables
from src.exceptions.estoque_exceptions import ProdutoNaoEncontradoException


class TestProdutoService:
    """Testes para o serviço de produtos"""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup executado antes de cada teste"""
        # Cria banco temporário para cada teste
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, "test.db")
        
        self.db_connection = DatabaseConnection(self.test_db_path)
        create_tables()
        
        self.produto_service = ProdutoService(self.db_connection)
        
        yield
        
        # Cleanup
        self.db_connection.close()
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_criar_produto_sucesso(self):
        """Testa criação de produto com sucesso"""
        produto = Produto(
            nome="Notebook Dell",
            descricao="Notebook para desenvolvimento",
            preco_unitario=2500.00,
            estoque_atual=5
        )
        
        produto_criado = self.produto_service.criar_produto(produto)
        
        assert produto_criado.id is not None
        assert produto_criado.nome == "Notebook Dell"
        assert produto_criado.preco_unitario == 2500.00
        assert produto_criado.estoque_atual == 5
        assert produto_criado.created_at is not None
    
    def test_criar_produto_nome_duplicado(self):
        """Testa erro ao criar produto com nome duplicado"""
        produto1 = Produto(nome="Mouse Logitech")
        produto2 = Produto(nome="Mouse Logitech")
        
        self.produto_service.criar_produto(produto1)
        
        with pytest.raises(ValueError, match="Já existe um produto"):
            self.produto_service.criar_produto(produto2)
    
    def test_buscar_produto_por_id_sucesso(self):
        """Testa busca de produto por ID com sucesso"""
        produto = Produto(nome="Teclado Mecânico", preco_unitario=350.00)
        produto_criado = self.produto_service.criar_produto(produto)
        
        produto_encontrado = self.produto_service.buscar_produto_por_id(produto_criado.id)
        
        assert produto_encontrado.id == produto_criado.id
        assert produto_encontrado.nome == "Teclado Mecânico"
        assert produto_encontrado.preco_unitario == 350.00
    
    def test_buscar_produto_por_id_nao_encontrado(self):
        """Testa erro ao buscar produto inexistente por ID"""
        with pytest.raises(ProdutoNaoEncontradoException):
            self.produto_service.buscar_produto_por_id(999)
    
    def test_buscar_produto_por_nome_sucesso(self):
        """Testa busca de produto por nome com sucesso"""
        produto = Produto(nome="Monitor 24 polegadas")
        self.produto_service.criar_produto(produto)
        
        produto_encontrado = self.produto_service.buscar_produto_por_nome("Monitor 24 polegadas")
        
        assert produto_encontrado.nome == "Monitor 24 polegadas"
    
    def test_buscar_produto_por_nome_nao_encontrado(self):
        """Testa erro ao buscar produto inexistente por nome"""
        with pytest.raises(ProdutoNaoEncontradoException):
            self.produto_service.buscar_produto_por_nome("Produto Inexistente")
    
    def test_listar_produtos_vazio(self):
        """Testa listagem quando não há produtos"""
        produtos = self.produto_service.listar_produtos()
        assert len(produtos) == 0
    
    def test_listar_produtos_com_dados(self):
        """Testa listagem de produtos"""
        produto1 = Produto(nome="Produto A")
        produto2 = Produto(nome="Produto B")
        produto3 = Produto(nome="Produto C")
        
        self.produto_service.criar_produto(produto1)
        self.produto_service.criar_produto(produto2)
        self.produto_service.criar_produto(produto3)
        
        produtos = self.produto_service.listar_produtos()
        
        assert len(produtos) == 3
        nomes = [p.nome for p in produtos]
        assert "Produto A" in nomes
        assert "Produto B" in nomes
        assert "Produto C" in nomes
    
    def test_atualizar_produto_sucesso(self):
        """Testa atualização de produto com sucesso"""
        produto = Produto(nome="Produto Original", preco_unitario=100.00)
        produto_criado = self.produto_service.criar_produto(produto)
        
        # Atualiza dados
        produto_criado.nome = "Produto Atualizado"
        produto_criado.preco_unitario = 150.00
        produto_criado.descricao = "Nova descrição"
        
        produto_atualizado = self.produto_service.atualizar_produto(produto_criado)
        
        assert produto_atualizado.nome == "Produto Atualizado"
        assert produto_atualizado.preco_unitario == 150.00
        assert produto_atualizado.descricao == "Nova descrição"
        assert produto_atualizado.updated_at > produto_atualizado.created_at
    
    def test_atualizar_produto_sem_id(self):
        """Testa erro ao tentar atualizar produto sem ID"""
        produto = Produto(nome="Produto Sem ID")
        
        with pytest.raises(ValueError, match="Produto deve ter ID"):
            self.produto_service.atualizar_produto(produto)
    
    def test_atualizar_produto_inexistente(self):
        """Testa erro ao atualizar produto inexistente"""
        produto = Produto(nome="Produto Inexistente")
        produto.id = 999
        
        with pytest.raises(ProdutoNaoEncontradoException):
            self.produto_service.atualizar_produto(produto)
    
    def test_excluir_produto_sucesso(self):
        """Testa exclusão de produto com sucesso"""
        produto = Produto(nome="Produto Para Excluir")
        produto_criado = self.produto_service.criar_produto(produto)
        
        self.produto_service.excluir_produto(produto_criado.id)
        
        with pytest.raises(ProdutoNaoEncontradoException):
            self.produto_service.buscar_produto_por_id(produto_criado.id)
    
    def test_excluir_produto_inexistente(self):
        """Testa erro ao excluir produto inexistente"""
        with pytest.raises(ProdutoNaoEncontradoException):
            self.produto_service.excluir_produto(999)
    
    def test_atualizar_estoque_sucesso(self):
        """Testa atualização de estoque com sucesso"""
        produto = Produto(nome="Produto Estoque", estoque_atual=10)
        produto_criado = self.produto_service.criar_produto(produto)
        
        produto_atualizado = self.produto_service.atualizar_estoque(produto_criado.id, 25)
        
        assert produto_atualizado.estoque_atual == 25
    
    def test_atualizar_estoque_negativo(self):
        """Testa erro ao tentar definir estoque negativo"""
        produto = Produto(nome="Produto Estoque")
        produto_criado = self.produto_service.criar_produto(produto)
        
        with pytest.raises(ValueError, match="Estoque não pode ser negativo"):
            self.produto_service.atualizar_estoque(produto_criado.id, -5)
    
    def test_produto_tem_estoque_suficiente(self):
        """Testa verificação de estoque suficiente"""
        produto = Produto(nome="Produto Teste", estoque_atual=10)
        
        assert produto.tem_estoque_suficiente(5) == True
        assert produto.tem_estoque_suficiente(10) == True
        assert produto.tem_estoque_suficiente(15) == False
