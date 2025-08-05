# Sistema de Controle de Estoque com Behave

Este projeto implementa um sistema de controle de estoque com regras de negócio robustas, testado com BDD usando Behave.

## Funcionalidades

- ✅ Cadastro de produtos
- ✅ Movimentações de estoque (entrada/saída)
- ✅ Prevenção de estoque negativo
- ✅ Recálculo automático do total de estoque
- ✅ Validação de limites (retirada maior que disponível)

## Tecnologias

- Python 3.x
- SQLite (banco de dados)
- Behave (BDD - Behavior Driven Development)
- Pytest (testes unitários)

## Estrutura do Projeto

```
sistema-controle-estoque-Behave/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── produto.py
│   │   └── movimentacao.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── produto_service.py
│   │   └── estoque_service.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── migrations.py
│   └── exceptions/
│       ├── __init__.py
│       └── estoque_exceptions.py
├── features/
│   ├── environment.py
│   ├── steps/
│   │   ├── __init__.py
│   │   ├── produto_steps.py
│   │   └── estoque_steps.py
│   ├── produto.feature
│   └── estoque.feature
├── tests/
│   ├── __init__.py
│   ├── test_produto_service.py
│   └── test_estoque_service.py
├── requirements.txt
└── README.md
```

## Instalação

1. Clone o repositório
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando os Testes BDD

```bash
# Executar todos os testes Behave
behave

# Executar testes de uma feature específica
behave features/estoque.feature

# Executar com saída detalhada
behave -v
```

## Executando Testes Unitários

```bash
pytest tests/
```

## Banco de Dados

O sistema utiliza SQLite com as seguintes tabelas:

### Tabela: produtos

- id (INTEGER PRIMARY KEY)
- nome (TEXT NOT NULL)
- descricao (TEXT)
- preco_unitario (REAL)
- estoque_atual (INTEGER DEFAULT 0)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Tabela: movimentacoes

- id (INTEGER PRIMARY KEY)
- produto_id (INTEGER FOREIGN KEY)
- tipo (TEXT) -- 'entrada' ou 'saida'
- quantidade (INTEGER)
- observacao (TEXT)
- created_at (TIMESTAMP)

## Exemplos de Uso

### Cenários de Teste (Gherkin)

```gherkin
Scenario: Impedir saída de produto com estoque insuficiente
  Given o produto "Cabo HDMI" tem 5 unidades no estoque
  When tento registrar uma saída de 6 unidades
  Then o sistema deve exibir "Estoque insuficiente"
  And não deve alterar o estoque
```
