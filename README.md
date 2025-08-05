# 🚀 Sistema de Controle de Estoque com Behave

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Behave](https://img.shields.io/badge/BDD-Behave-green.svg)](https://behave.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue.svg)](https://sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-15%20scenarios%20✅-brightgreen.svg)](#testes)

Um sistema completo de controle de estoque desenvolvido com **arquitetura limpa** e **regras de negócio robustas**, validado através de **testes automatizados BDD (Behavior Driven Development)** usando Behave.

## 🎯 Funcionalidades Principais

- ✅ **Cadastro completo de produtos** (nome, descrição, preço, estoque)
- ✅ **Movimentações de estoque** (entradas e saídas com rastreabilidade)
- ✅ **🚫 Prevenção rigorosa de estoque negativo** (regra de negócio crítica)
- ✅ **Recálculo automático** do total de estoque por produto
- ✅ **Validação de limites** (impede retiradas maiores que o disponível)
- ✅ **Relatórios de estoque** em tempo real
- ✅ **Alertas de estoque baixo** configuráveis
- ✅ **Histórico completo** de todas as movimentações
- ✅ **Transações atômicas** (consistência de dados garantida)

## 🛠️ Tecnologias e Ferramentas

- **Python 3.13+** - Linguagem principal
- **SQLite** - Banco de dados relacional
- **Behave** - Framework BDD para testes comportamentais
- **Pytest** - Framework para testes unitários
- **Dataclasses** - Modelagem de dados moderna
- **Context Managers** - Gerenciamento seguro de recursos

## 🏗️ Arquitetura do Sistema

O projeto segue os princípios de **Clean Architecture** com separação clara de responsabilidades:

```
sistema-controle-estoque-Behave/
├── 📁 src/                          # Código fonte principal
│   ├── 📁 models/                   # Entidades de domínio
│   │   ├── __init__.py
│   │   ├── produto.py               # Modelo Produto
│   │   └── movimentacao.py          # Modelo Movimentação
│   ├── 📁 services/                 # Regras de negócio
│   │   ├── __init__.py
│   │   ├── produto_service.py       # CRUD de produtos
│   │   └── estoque_service.py       # Lógica de estoque
│   ├── 📁 database/                 # Camada de dados
│   │   ├── __init__.py
│   │   ├── connection.py            # Gerenciamento de conexões
│   │   └── migrations.py            # Scripts de criação de tabelas
│   └── 📁 exceptions/               # Exceções customizadas
│       ├── __init__.py
│       └── estoque_exceptions.py    # Exceções de regras de negócio
├── 📁 features/                     # Testes BDD (Behave)
│   ├── environment.py               # Configuração do ambiente de teste
│   ├── 📁 steps/                    # Implementação dos steps
│   │   ├── __init__.py
│   │   ├── produto_steps.py         # Steps para produtos
│   │   └── estoque_steps.py         # Steps para estoque
│   ├── produto.feature              # Cenários de produtos
│   └── estoque.feature              # Cenários de estoque
├── 📁 tests/                        # Testes unitários
│   ├── __init__.py
│   ├── test_produto_service.py      # Testes do ProdutoService
│   └── test_estoque_service.py      # Testes do EstoqueService
├── 📄 main.py                       # Demonstração do sistema
├── 📄 setup_db.py                   # Script de inicialização do banco
├── 📄 behave.ini                    # Configuração do Behave
├── 📄 requirements.txt              # Dependências Python
└── 📄 README.md                     # Documentação
```

### 🎨 Padrões Arquiteturais Utilizados

- **Repository Pattern** - Abstração da camada de dados
- **Service Layer** - Encapsulamento das regras de negócio
- **Dependency Injection** - Inversão de dependências para testabilidade
- **Exception Handling** - Tratamento específico de erros de domínio
- **Transactional Pattern** - Garantia de consistência em operações complexas

## 🚀 Instalação e Configuração

### Pré-requisitos

- **Python 3.13+** instalado
- **Git** para clonagem do repositório

### Passos para instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Rychardsson/sistema-controle-estoque-Behave.git
   cd sistema-controle-estoque-Behave
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o banco de dados:**

   ```bash
   python setup_db.py
   ```

4. **Execute a demonstração:**
   ```bash
   python main.py
   ```

## 🧪 Executando os Testes

### Testes BDD (Behave) - Comportamentais

```bash
# Executar todos os testes BDD
behave

# Executar feature específica
behave features/estoque.feature

# Executar com saída detalhada
behave -v

# Executar cenário específico
behave -n "Impedir saída de produto com estoque insuficiente"
```

### Testes Unitários (Pytest)

```bash
# Executar todos os testes unitários
pytest tests/

# Executar com relatório de cobertura
pytest tests/ --cov=src

# Executar com saída detalhada
pytest tests/ -v
```

### 📊 Resultados dos Testes (Última Execução)

- ✅ **2 features** executadas com sucesso
- ✅ **15 cenários** BDD aprovados (100% de sucesso)
- ✅ **71 steps** implementados e funcionando
- ✅ **Tempo de execução:** 0.3 segundos
- ✅ **Cobertura:** Todas as regras de negócio validadas

## 🗄️ Modelagem do Banco de Dados

O sistema utiliza **SQLite** com estrutura otimizada para controle de estoque:

### 📋 Tabela: `produtos`

| Campo            | Tipo                 | Descrição                           |
| ---------------- | -------------------- | ----------------------------------- |
| `id`             | INTEGER PRIMARY KEY  | Identificador único auto-incremento |
| `nome`           | TEXT NOT NULL UNIQUE | Nome do produto (único)             |
| `descricao`      | TEXT                 | Descrição detalhada do produto      |
| `preco_unitario` | REAL DEFAULT 0.0     | Preço unitário do produto           |
| `estoque_atual`  | INTEGER DEFAULT 0    | Quantidade atual em estoque         |
| `created_at`     | TIMESTAMP            | Data/hora de criação                |
| `updated_at`     | TIMESTAMP            | Data/hora da última atualização     |

### 📋 Tabela: `movimentacoes`

| Campo        | Tipo                | Descrição                                   |
| ------------ | ------------------- | ------------------------------------------- |
| `id`         | INTEGER PRIMARY KEY | Identificador único auto-incremento         |
| `produto_id` | INTEGER FOREIGN KEY | Referência ao produto                       |
| `tipo`       | TEXT CHECK          | Tipo da movimentação ('entrada' ou 'saida') |
| `quantidade` | INTEGER CHECK > 0   | Quantidade movimentada                      |
| `observacao` | TEXT                | Observações sobre a movimentação            |
| `created_at` | TIMESTAMP           | Data/hora da movimentação                   |

### 🔗 Relacionamentos

- **produtos** 1:N **movimentacoes** (Um produto pode ter várias movimentações)
- **Integridade referencial** garantida com Foreign Keys
- **Triggers automáticos** para atualização de timestamps

## 💡 Exemplos de Uso e Cenários BDD

### 🎯 Cenário Principal: Prevenção de Estoque Negativo

```gherkin
Feature: Controle de Estoque
  Como um usuário do sistema de estoque
  Eu quero controlar movimentações de entrada e saída
  Para manter o inventário atualizado e evitar rupturas

  Scenario: Impedir saída de produto com estoque insuficiente
    Given o produto "Cabo HDMI" tem 5 unidades no estoque
    When tento registrar uma saída de 6 unidades
    Then o sistema deve exibir "Estoque insuficiente"
    And não deve alterar o estoque
    And o estoque deve permanecer 5
```

### 📝 Outros Cenários Implementados

<details>
<summary><b>🔍 Clique para ver todos os cenários testados</b></summary>

#### Gestão de Produtos

```gherkin
Scenario: Cadastrar um novo produto
  When eu cadastro um produto "Notebook Dell" com preço 2500.00
  Then o produto "Notebook Dell" deve estar cadastrado
  And o produto "Notebook Dell" deve ter preço 2500.00

Scenario: Cadastrar produto com nome duplicado
  Given que existe um produto "Mouse Logitech"
  When eu cadastro um produto "Mouse Logitech"
  Then deve retornar erro "Já existe um produto com o nome"
```

#### Movimentações de Estoque

```gherkin
Scenario: Registrar entrada de estoque
  Given que existe um produto "Smartphone Samsung"
  When eu registro uma entrada de 20 unidades do produto "Smartphone Samsung"
  Then o estoque do produto "Smartphone Samsung" deve ser 20 unidades
  And deve ser criada uma movimentação de entrada

Scenario: Registrar múltiplas entradas e saídas
  Given o produto "Pen Drive 32GB" tem 0 unidades no estoque
  When eu registro uma entrada de 50 unidades do produto "Pen Drive 32GB"
  And eu registro uma saída de 15 unidades do produto "Pen Drive 32GB"
  And eu registro uma entrada de 10 unidades do produto "Pen Drive 32GB"
  And eu registro uma saída de 20 unidades do produto "Pen Drive 32GB"
  Then o estoque do produto "Pen Drive 32GB" deve ser 25 unidades
```

#### Validações de Regras de Negócio

```gherkin
Scenario: Tentar registrar entrada com quantidade zero
  Given que existe um produto "Mouse Wireless"
  When tento registrar uma entrada de 0 unidades do produto "Mouse Wireless"
  Then deve retornar erro de movimentação inválida

Scenario: Estoque exato - retirar toda quantidade disponível
  Given o produto "Adaptador HDMI" tem 3 unidades no estoque
  When eu registro uma saída de 3 unidades do produto "Adaptador HDMI"
  Then o estoque do produto "Adaptador HDMI" deve ser 0 unidades
```

</details>

### 🖥️ Demonstração em Terminal

```bash
# Execute a demonstração completa
python main.py
```

**Saída esperada:**

```
🚀 Sistema de Controle de Estoque com Behave
==================================================
📦 1. CADASTRANDO PRODUTOS
   ✅ Notebook Dell Inspiron - R$ 2500.00
   ✅ Mouse Logitech MX - R$ 350.00
   ✅ Cabo HDMI 2m - R$ 45.00

📈 2. REGISTRANDO ENTRADAS DE ESTOQUE
   📥 Notebook Dell Inspiron: +10 unidades (Total: 10)
   📥 Mouse Logitech MX: +25 unidades (Total: 25)

🚫 4. TESTANDO REGRA DE NEGÓCIO - ESTOQUE INSUFICIENTE
   ❌ ERRO: Estoque insuficiente para o produto 'Cabo HDMI 2m'
   ✅ Sistema protegeu contra estoque negativo!
```

## 🛡️ Regras de Negócio Implementadas

### ✅ Validações Críticas

1. **🚫 Estoque Nunca Negativo**

   - Sistema bloqueia qualquer operação que resulte em estoque < 0
   - Validação em tempo real antes de executar movimentações
   - Rollback automático em caso de tentativa inválida

2. **📊 Consistência de Dados**

   - Transações atômicas para operações complexas
   - Atualização automática de estoque após movimentações
   - Timestamps automáticos para auditoria

3. **🔍 Validações de Entrada**

   - Quantidade deve ser sempre > 0
   - Produtos devem existir antes de movimentações
   - Nomes de produtos devem ser únicos

4. **📈 Recálculos Automáticos**
   - Estoque recalculado baseado no histórico de movimentações
   - Relatórios em tempo real
   - Alertas de estoque baixo configuráveis

### ⚡ Performance e Confiabilidade

- **Índices otimizados** no banco de dados
- **Connection pooling** para operações eficientes
- **Tratamento de exceções** específico por domínio
- **Logs detalhados** para troubleshooting

## 🤝 Contribuindo

### Como contribuir:

1. **Fork** este repositório
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Implemente** sua funcionalidade com testes
4. **Execute** todos os testes: `behave && pytest`
5. **Commit** suas mudanças (`git commit -m 'Add: Amazing Feature'`)
6. **Push** para a branch (`git push origin feature/AmazingFeature`)
7. Abra um **Pull Request**

### Padrões de código:

- Siga **PEP 8** para formatação Python
- Escreva **testes BDD** para novas funcionalidades
- Documente **regras de negócio** complexas
- Use **type hints** sempre que possível

## 📚 Recursos Adicionais

### 📖 Documentação Relacionada

- [Behave Documentation](https://behave.readthedocs.io/) - Framework BDD
- [Python SQLite3](https://docs.python.org/3/library/sqlite3.html) - Banco de dados
- [Pytest Documentation](https://pytest.org/) - Framework de testes

### 🎓 Conceitos Aplicados

- **Behavior Driven Development (BDD)**
- **Test Driven Development (TDD)**
- **Clean Architecture**
- **Domain Driven Design (DDD)**
- **SOLID Principles**

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Rychardsson** - [GitHub](https://github.com/Rychardsson)

---

<div align="center">

### ⭐ Se este projeto foi útil, considere dar uma estrela!

**Sistema de Controle de Estoque com Behave** - Desenvolvido com ❤️ e Python

</div>
