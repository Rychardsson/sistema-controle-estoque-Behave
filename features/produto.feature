Feature: Gerenciamento de Produtos
  Como um usuário do sistema de estoque
  Eu quero gerenciar produtos
  Para controlar o inventário da empresa

  Background:
    Given que o sistema está limpo

  Scenario: Cadastrar um novo produto
    When eu cadastro um produto "Notebook Dell" com preço 2500.00
    Then o produto "Notebook Dell" deve estar cadastrado
    And o produto "Notebook Dell" deve ter preço 2500.00
    And o produto "Notebook Dell" deve ter estoque de 0 unidades

  Scenario: Cadastrar produto com nome duplicado
    Given que existe um produto "Mouse Logitech"
    When eu cadastro um produto "Mouse Logitech"
    Then deve retornar erro "Já existe um produto com o nome"

  Scenario: Buscar produto existente
    Given que existe um produto "Teclado Mecânico" com preço 350.00
    When eu busco o produto "Teclado Mecânico"
    Then o produto deve ser encontrado

  Scenario: Buscar produto inexistente
    When eu busco o produto "Produto Inexistente"
    Then deve retornar erro de produto não encontrado

  Scenario: Atualizar preço do produto
    Given que existe um produto "Monitor 24" com preço 800.00
    When eu atualizo o preço do produto "Monitor 24" para 750.00
    Then o produto "Monitor 24" deve ter preço 750.00

  Scenario: Cadastrar produto com estoque inicial
    Given que existe um produto "Cabo HDMI" com estoque de 10 unidades
    Then o produto "Cabo HDMI" deve ter estoque de 10 unidades
