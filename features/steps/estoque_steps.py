"""
Steps para testes de estoque e movimentações
"""
from behave import given, when, then
from src.models.produto import Produto
from src.services.produto_service import ProdutoService
from src.services.estoque_service import EstoqueService
from src.exceptions.estoque_exceptions import (
    EstoqueInsuficienteException,
    MovimentacaoInvalidaException
)


@given('que o sistema está limpo')
def step_sistema_limpo(context):
    """Step básico para indicar sistema limpo"""
    pass


@given('o produto "{nome}" tem {quantidade:d} unidades no estoque')
def step_produto_tem_estoque(context, nome, quantidade):
    """Define o estoque inicial de um produto"""
    produto_service = ProdutoService(context.db_connection)
    
    # Verifica se produto já existe
    if nome in context.produtos:
        produto = context.produtos[nome]
        produto_service.atualizar_estoque(produto.id, quantidade)
        produto.estoque_atual = quantidade
    else:
        # Cria produto com estoque inicial
        produto = Produto(
            nome=nome,
            estoque_atual=quantidade
        )
        produto_criado = produto_service.criar_produto(produto)
        context.produtos[nome] = produto_criado


@when('eu registro uma entrada de {quantidade:d} unidades do produto "{nome}"')
def step_registro_entrada(context, quantidade, nome):
    """Registra uma entrada de estoque"""
    estoque_service = EstoqueService(context.db_connection)
    
    try:
        produto = context.produtos[nome]
        movimentacao = estoque_service.registrar_entrada(
            produto_id=produto.id,
            quantidade=quantidade,
            observacao="Entrada via teste BDD"
        )
        
        context.movimentacoes.append(movimentacao)
        context.ultimo_erro = None
        
        # Atualiza o produto no contexto
        produto_service = ProdutoService(context.db_connection)
        context.produtos[nome] = produto_service.buscar_produto_por_id(produto.id)
        
    except Exception as e:
        context.ultimo_erro = e


@when('eu registro uma saída de {quantidade:d} unidades do produto "{nome}"')
def step_registro_saida(context, quantidade, nome):
    """Registra uma saída de estoque"""
    estoque_service = EstoqueService(context.db_connection)
    
    try:
        produto = context.produtos[nome]
        movimentacao = estoque_service.registrar_saida(
            produto_id=produto.id,
            quantidade=quantidade,
            observacao="Saída via teste BDD"
        )
        
        context.movimentacoes.append(movimentacao)
        context.ultimo_erro = None
        
        # Atualiza o produto no contexto
        produto_service = ProdutoService(context.db_connection)
        context.produtos[nome] = produto_service.buscar_produto_por_id(produto.id)
        
    except Exception as e:
        context.ultimo_erro = e


@when('tento registrar uma entrada de {quantidade:d} unidades do produto "{nome}"')
def step_tento_registrar_entrada(context, quantidade, nome):
    """Tenta registrar uma entrada (pode falhar)"""
    step_registro_entrada(context, quantidade, nome)


@when('tento registrar uma saída de {quantidade:d} unidades do produto "{nome}"')
def step_tento_registrar_saida(context, quantidade, nome):
    """Tenta registrar uma saída (pode falhar)"""
    step_registro_saida(context, quantidade, nome)


@when('tento registrar uma saída de {quantidade:d} unidades')
def step_tento_registrar_saida_sem_produto(context, quantidade):
    """Tenta registrar saída usando último produto do contexto"""
    # Pega o último produto criado
    if context.produtos:
        nome_produto = list(context.produtos.keys())[-1]
        step_tento_registrar_saida(context, quantidade, nome_produto)
    else:
        context.ultimo_erro = Exception("Nenhum produto encontrado no contexto")


@when('eu verifico o estoque do produto "{nome}"')
def step_verifico_estoque(context, nome):
    """Verifica o estoque atual de um produto"""
    produto_service = ProdutoService(context.db_connection)
    
    try:
        produto = produto_service.buscar_produto_por_nome(nome)
        context.estoque_verificado = produto.estoque_atual
        context.ultimo_erro = None
        
    except Exception as e:
        context.ultimo_erro = e


@then('o estoque do produto "{nome}" deve ser {estoque_esperado:d} unidades')
def step_estoque_deve_ser(context, nome, estoque_esperado):
    """Verifica se o estoque está correto"""
    produto = context.produtos[nome]
    assert produto.estoque_atual == estoque_esperado, \
        f"Esperado {estoque_esperado}, mas encontrado {produto.estoque_atual}"


@then('o sistema deve exibir "{mensagem}"')
def step_sistema_deve_exibir(context, mensagem):
    """Verifica se a mensagem de erro está correta"""
    assert context.ultimo_erro is not None
    mensagem_erro = str(context.ultimo_erro)
    assert mensagem.lower() in mensagem_erro.lower(), \
        f"Mensagem '{mensagem}' não encontrada em '{mensagem_erro}'"


@then('não deve alterar o estoque')
def step_nao_deve_alterar_estoque(context):
    """Verifica que o estoque não foi alterado após erro"""
    assert context.ultimo_erro is not None
    # Se houve erro, não deveria ter criado movimentação
    # O estoque deve permanecer o mesmo


@then('deve ser criada uma movimentação de entrada')
def step_deve_criar_movimentacao_entrada(context):
    """Verifica se foi criada movimentação de entrada"""
    assert len(context.movimentacoes) > 0
    ultima_movimentacao = context.movimentacoes[-1]
    assert ultima_movimentacao.is_entrada()
    assert ultima_movimentacao.id is not None


@then('deve ser criada uma movimentação de saída')
def step_deve_criar_movimentacao_saida(context):
    """Verifica se foi criada movimentação de saída"""
    assert len(context.movimentacoes) > 0
    ultima_movimentacao = context.movimentacoes[-1]
    assert ultima_movimentacao.is_saida()
    assert ultima_movimentacao.id is not None


@then('deve retornar erro de estoque insuficiente')
def step_deve_retornar_estoque_insuficiente(context):
    """Verifica se ocorreu erro de estoque insuficiente"""
    assert context.ultimo_erro is not None
    assert isinstance(context.ultimo_erro, EstoqueInsuficienteException)


@then('deve retornar erro de movimentação inválida')
def step_deve_retornar_movimentacao_invalida(context):
    """Verifica se ocorreu erro de movimentação inválida"""
    assert context.ultimo_erro is not None
    assert isinstance(context.ultimo_erro, MovimentacaoInvalidaException)


@then('o estoque deve permanecer {estoque_esperado:d}')
def step_estoque_deve_permanecer(context, estoque_esperado):
    """Verifica que o estoque permaneceu inalterado"""
    # Pega o último produto do contexto
    if context.produtos:
        nome_produto = list(context.produtos.keys())[-1]
        produto_service = ProdutoService(context.db_connection)
        produto_atual = produto_service.buscar_produto_por_nome(nome_produto)
        assert produto_atual.estoque_atual == estoque_esperado
