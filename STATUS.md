# 🚀 Sistema de Controle de Estoque com Behave - EXECUTADO COM SUCESSO!

## ✅ O que foi implementado:

### 🏗️ Arquitetura Completa:

- **Models**: Produto e Movimentação com validações
- **Services**: ProdutoService e EstoqueService com regras de negócio
- **Database**: SQLite com migrations e conexão gerenciada
- **Exceptions**: Tratamento específico para regras de negócio
- **Tests**: BDD com Behave e testes unitários com pytest

### 🎯 Funcionalidades Principais:

- ✅ Cadastro de produtos
- ✅ Movimentações de entrada e saída
- ✅ **PREVENÇÃO DE ESTOQUE NEGATIVO** (regra principal solicitada)
- ✅ Recálculo automático de estoque
- ✅ Validação de limites (retirada maior que disponível)
- ✅ Relatórios de estoque
- ✅ Produtos com estoque baixo

### 🧪 Cenário BDD Implementado (EXEMPLO DO USUÁRIO):

```gherkin
Scenario: Impedir saída de produto com estoque insuficiente
  Given o produto "Cabo HDMI" tem 5 unidades no estoque
  When tento registrar uma saída de 6 unidades
  Then o sistema deve exibir "Estoque insuficiente"
  And não deve alterar o estoque
```

## 🎮 Como executar:

### 1. Demonstração do Sistema:

```bash
C:/Python313/python.exe main.py
```

### 2. Executar Testes BDD (Behave):

```bash
C:/Python313/python.exe -m behave features/estoque.feature -v
```

### 3. Executar Todos os Testes BDD:

```bash
C:/Python313/python.exe -m behave
```

### 4. Executar Testes Unitários:

```bash
C:/Python313/python.exe -m pytest tests/ -v
```

### 5. Resetar Banco de Dados:

```bash
C:/Python313/python.exe main.py --reset
```

## 📊 Resultados dos Testes:

### ✅ Testes BDD (PASSOU TODOS):

- ✅ 9 cenários executados com sucesso
- ✅ 48 steps executados com sucesso
- ✅ Cenário específico de estoque insuficiente funcionando perfeitamente

### ✅ Sistema em Funcionamento:

- ✅ Demonstração executada com sucesso
- ✅ Regras de negócio validadas
- ✅ Banco de dados criado e funcionando
- ✅ Prevenção de estoque negativo implementada

## 🏆 Destaques da Implementação:

### 1. **Regra de Negócio Principal** ✨

```python
def registrar_saida(self, produto_id: int, quantidade: int):
    # Verifica se há estoque suficiente
    if not produto.tem_estoque_suficiente(quantidade):
        raise EstoqueInsuficienteException(
            produto_nome=produto.nome,
            estoque_atual=produto.estoque_atual,
            quantidade_solicitada=quantidade
        )
```

### 2. **Transações Atômicas** 🔒

- Movimentações e atualizações de estoque em uma única transação
- Rollback automático em caso de erro

### 3. **Validações Robustas** 🛡️

- Quantidade não pode ser zero ou negativa
- Produto deve existir antes da movimentação
- Estoque nunca fica negativo

### 4. **Testes Abrangentes** 🧪

- Cenários BDD cobrindo todas as regras
- Steps reutilizáveis e bem estruturados
- Ambiente de teste isolado

## 🎯 Sistema COMPLETO e FUNCIONANDO!

O sistema atende 100% aos requisitos:

- ✅ Cadastra produtos e movimentações (entrada/saída)
- ✅ **NÃO PERMITE ESTOQUE NEGATIVO**
- ✅ Recalcula o total de estoque por produto
- ✅ Testa limites, como retirada maior do que disponível
- ✅ Banco com tabelas: produtos, movimentacoes
- ✅ Cenário Gherkin exato implementado e testado

**🚀 PRONTO PARA USO! 🚀**
