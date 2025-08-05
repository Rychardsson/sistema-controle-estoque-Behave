"""
Steps para testes de produtos
"""
from behave import given, when, then
from src.models.produto import Produto
from src.services.produto_service import ProdutoService
from src.exceptions.estoque_exceptions import ProdutoNaoEncontradoException


@given('que existe um produto "{nome}" com preço {preco:f}')
def step_existe_produto_com_preco(context, nome, preco):
    """Cria um produto com nome e preço especificados"""
    produto_service = ProdutoService(context.db_connection)
    
    produto = Produto(
        nome=nome,
        preco_unitario=preco,
        estoque_atual=0
    )
    
    produto_criado = produto_service.criar_produto(produto)
    context.produtos[nome] = produto_criado


@given('que existe um produto "{nome}"')
def step_existe_produto(context, nome):
    """Cria um produto básico com nome especificado"""
    step_existe_produto_com_preco(context, nome, 0.0)


@given('que existe um produto "{nome}" com estoque de {quantidade:d} unidades')
def step_existe_produto_com_estoque(context, nome, quantidade):
    """Cria um produto com estoque inicial"""
    produto_service = ProdutoService(context.db_connection)
    
    produto = Produto(
        nome=nome,
        estoque_atual=quantidade
    )
    
    produto_criado = produto_service.criar_produto(produto)
    context.produtos[nome] = produto_criado


@when('eu cadastro um produto "{nome}" com preço {preco:f}')
def step_cadastro_produto_com_preco(context, nome, preco):
    """Cadastra um novo produto"""
    produto_service = ProdutoService(context.db_connection)
    
    try:
        produto = Produto(
            nome=nome,
            preco_unitario=preco
        )
        
        produto_criado = produto_service.criar_produto(produto)
        context.produtos[nome] = produto_criado
        context.ultimo_erro = None
        
    except Exception as e:
        context.ultimo_erro = e


@when('eu cadastro um produto "{nome}"')
def step_cadastro_produto(context, nome):
    """Cadastra um produto básico"""
    step_cadastro_produto_com_preco(context, nome, 0.0)


@when('eu busco o produto "{nome}"')
def step_busco_produto(context, nome):
    """Busca um produto pelo nome"""
    produto_service = ProdutoService(context.db_connection)
    
    try:
        produto = produto_service.buscar_produto_por_nome(nome)
        context.produto_encontrado = produto
        context.ultimo_erro = None
        
    except Exception as e:
        context.ultimo_erro = e
        context.produto_encontrado = None


@when('eu atualizo o preço do produto "{nome}" para {novo_preco:f}')
def step_atualizo_preco_produto(context, nome, novo_preco):
    """Atualiza o preço de um produto"""
    produto_service = ProdutoService(context.db_connection)
    
    try:
        produto = context.produtos[nome]
        produto.preco_unitario = novo_preco
        
        produto_atualizado = produto_service.atualizar_produto(produto)
        context.produtos[nome] = produto_atualizado
        context.ultimo_erro = None
        
    except Exception as e:
        context.ultimo_erro = e


@then('o produto "{nome}" deve estar cadastrado')
def step_produto_deve_estar_cadastrado(context, nome):
    """Verifica se o produto foi cadastrado"""
    assert nome in context.produtos
    assert context.produtos[nome].id is not None


@then('o produto "{nome}" deve ter preço {preco_esperado:f}')
def step_produto_deve_ter_preco(context, nome, preco_esperado):
    """Verifica o preço do produto"""
    produto = context.produtos[nome]
    assert produto.preco_unitario == preco_esperado


@then('o produto "{nome}" deve ter estoque de {estoque_esperado:d} unidades')
def step_produto_deve_ter_estoque(context, nome, estoque_esperado):
    """Verifica o estoque do produto"""
    produto = context.produtos[nome]
    assert produto.estoque_atual == estoque_esperado


@then('deve retornar erro "{mensagem_erro}"')
def step_deve_retornar_erro(context, mensagem_erro):
    """Verifica se ocorreu o erro esperado"""
    assert context.ultimo_erro is not None
    assert mensagem_erro.lower() in str(context.ultimo_erro).lower()


@then('o produto deve ser encontrado')
def step_produto_deve_ser_encontrado(context):
    """Verifica se o produto foi encontrado"""
    assert context.produto_encontrado is not None
    assert context.ultimo_erro is None


@then('deve retornar erro de produto não encontrado')
def step_deve_retornar_produto_nao_encontrado(context):
    """Verifica se ocorreu erro de produto não encontrado"""
    assert context.ultimo_erro is not None
    assert isinstance(context.ultimo_erro, ProdutoNaoEncontradoException)
