"""
Script principal para demonstrar o sistema de controle de estoque
"""
import os
from datetime import datetime

from src.database.connection import get_database_connection
from src.database.migrations import create_tables, reset_database
from src.models.produto import Produto
from src.services.produto_service import ProdutoService
from src.services.estoque_service import EstoqueService
from src.exceptions.estoque_exceptions import EstoqueInsuficienteException


def demonstrar_sistema():
    """Demonstra as funcionalidades do sistema"""
    
    print("🚀 Sistema de Controle de Estoque com Behave")
    print("=" * 50)
    
    # Inicializa banco de dados
    print("\n📊 Inicializando banco de dados...")
    create_tables()
    
    # Inicializa serviços
    produto_service = ProdutoService()
    estoque_service = EstoqueService()
    
    print("✅ Sistema inicializado com sucesso!\n")
    
    # 1. Cadastro de Produtos
    print("📦 1. CADASTRANDO PRODUTOS")
    print("-" * 30)
    
    produtos = [
        Produto(nome="Notebook Dell Inspiron", descricao="Notebook para desenvolvimento", preco_unitario=2500.00),
        Produto(nome="Mouse Logitech MX", descricao="Mouse sem fio", preco_unitario=350.00),
        Produto(nome="Cabo HDMI 2m", descricao="Cabo HDMI 4K", preco_unitario=45.00),
        Produto(nome="SSD Samsung 500GB", descricao="SSD NVMe", preco_unitario=380.00),
        Produto(nome="Teclado Mecânico", descricao="Teclado mecânico RGB", preco_unitario=450.00)
    ]
    
    produtos_criados = []
    for produto in produtos:
        produto_criado = produto_service.criar_produto(produto)
        produtos_criados.append(produto_criado)
        print(f"   ✅ {produto_criado.nome} - R$ {produto_criado.preco_unitario:.2f}")
    
    # 2. Movimentações de Entrada
    print(f"\n📈 2. REGISTRANDO ENTRADAS DE ESTOQUE")
    print("-" * 40)
    
    entradas = [
        (produtos_criados[0].id, 10, "Compra inicial"),
        (produtos_criados[1].id, 25, "Estoque de reposição"),
        (produtos_criados[2].id, 50, "Lote grande"),
        (produtos_criados[3].id, 15, "Compra mensal"),
        (produtos_criados[4].id, 8, "Estoque mínimo")
    ]
    
    for produto_id, quantidade, observacao in entradas:
        movimentacao = estoque_service.registrar_entrada(produto_id, quantidade, observacao)
        produto = produto_service.buscar_produto_por_id(produto_id)
        print(f"   📥 {produto.nome}: +{quantidade} unidades (Total: {produto.estoque_atual})")
    
    # 3. Movimentações de Saída
    print(f"\n📉 3. REGISTRANDO SAÍDAS DE ESTOQUE")
    print("-" * 40)
    
    saidas = [
        (produtos_criados[0].id, 3, "Venda cliente A"),
        (produtos_criados[1].id, 10, "Venda loja física"),
        (produtos_criados[2].id, 20, "Venda online"),
        (produtos_criados[3].id, 5, "Instalação cliente")
    ]
    
    for produto_id, quantidade, observacao in saidas:
        movimentacao = estoque_service.registrar_saida(produto_id, quantidade, observacao)
        produto = produto_service.buscar_produto_por_id(produto_id)
        print(f"   📤 {produto.nome}: -{quantidade} unidades (Total: {produto.estoque_atual})")
    
    # 4. Tentativa de Saída com Estoque Insuficiente
    print(f"\n🚫 4. TESTANDO REGRA DE NEGÓCIO - ESTOQUE INSUFICIENTE")
    print("-" * 60)
    
    try:
        cabo_hdmi = produtos_criados[2]  # Cabo HDMI
        produto_atual = produto_service.buscar_produto_por_id(cabo_hdmi.id)
        print(f"   📦 {produto_atual.nome} - Estoque atual: {produto_atual.estoque_atual} unidades")
        print(f"   🔄 Tentando retirar 35 unidades...")
        
        estoque_service.registrar_saida(cabo_hdmi.id, 35, "Tentativa de venda grande")
        
    except EstoqueInsuficienteException as e:
        print(f"   ❌ ERRO: {e}")
        print(f"   ✅ Sistema protegeu contra estoque negativo!")
    
    # 5. Relatório de Estoque
    print(f"\n📊 5. RELATÓRIO DE ESTOQUE ATUAL")
    print("-" * 35)
    
    produtos_atuais = produto_service.listar_produtos()
    total_valor = 0
    
    for produto in produtos_atuais:
        valor_estoque = produto.estoque_atual * produto.preco_unitario
        total_valor += valor_estoque
        print(f"   📦 {produto.nome:<25} | Estoque: {produto.estoque_atual:>3} | Valor: R$ {valor_estoque:>8.2f}")
    
    print(f"   {'-' * 70}")
    print(f"   💰 VALOR TOTAL DO ESTOQUE: R$ {total_valor:.2f}")
    
    # 6. Produtos com Estoque Baixo
    print(f"\n⚠️  6. PRODUTOS COM ESTOQUE BAIXO (≤ 10 unidades)")
    print("-" * 55)
    
    produtos_baixo = estoque_service.obter_produtos_com_estoque_baixo(limite=10)
    
    if produtos_baixo:
        for produto in produtos_baixo:
            print(f"   ⚠️  {produto.nome:<25} | Estoque: {produto.estoque_atual:>3} unidades")
    else:
        print("   ✅ Nenhum produto com estoque baixo!")
    
    # 7. Histórico de Movimentações
    print(f"\n📋 7. ÚLTIMAS MOVIMENTAÇÕES")
    print("-" * 30)
    
    movimentacoes = estoque_service.listar_movimentacoes()
    
    for i, mov in enumerate(movimentacoes[:8]):  # Mostra apenas as 8 mais recentes
        produto = produto_service.buscar_produto_por_id(mov.produto_id)
        icone = "📥" if mov.is_entrada() else "📤"
        sinal = "+" if mov.is_entrada() else "-"
        print(f"   {icone} {produto.nome:<20} | {sinal}{mov.quantidade:>3} | {mov.created_at.strftime('%d/%m %H:%M')}")
    
    print(f"\n🎉 Demonstração concluída com sucesso!")
    print("💡 Execute 'behave' para rodar os testes BDD")
    print("💡 Execute 'pytest tests/' para rodar os testes unitários")


def resetar_banco():
    """Reseta o banco de dados"""
    print("🔄 Resetando banco de dados...")
    reset_database()
    print("✅ Banco resetado com sucesso!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        resetar_banco()
    else:
        demonstrar_sistema()
