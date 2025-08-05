Feature: Controle de Estoque
  Como um usuário do sistema de estoque
  Eu quero controlar movimentações de entrada e saída
  Para manter o inventário atualizado e evitar rupturas

  Background:
    Given que o sistema está limpo

  Scenario: Registrar entrada de estoque
    Given que existe um produto "Smartphone Samsung"
    When eu registro uma entrada de 20 unidades do produto "Smartphone Samsung"
    Then o estoque do produto "Smartphone Samsung" deve ser 20 unidades
    And deve ser criada uma movimentação de entrada

  Scenario: Registrar saída de estoque com quantidade suficiente
    Given o produto "Tablet Apple" tem 15 unidades no estoque
    When eu registro uma saída de 5 unidades do produto "Tablet Apple"
    Then o estoque do produto "Tablet Apple" deve ser 10 unidades
    And deve ser criada uma movimentação de saída

  Scenario: Impedir saída de produto com estoque insuficiente
    Given o produto "Cabo HDMI" tem 5 unidades no estoque
    When tento registrar uma saída de 6 unidades
    Then o sistema deve exibir "Estoque insuficiente"
    And não deve alterar o estoque
    And o estoque deve permanecer 5

  Scenario: Impedir saída quando produto não tem estoque
    Given o produto "Headset Gamer" tem 0 unidades no estoque
    When tento registrar uma saída de 1 unidades
    Then deve retornar erro de estoque insuficiente
    And o estoque deve permanecer 0

  Scenario: Registrar múltiplas entradas e saídas
    Given o produto "Pen Drive 32GB" tem 0 unidades no estoque
    When eu registro uma entrada de 50 unidades do produto "Pen Drive 32GB"
    And eu registro uma saída de 15 unidades do produto "Pen Drive 32GB"
    And eu registro uma entrada de 10 unidades do produto "Pen Drive 32GB"
    And eu registro uma saída de 20 unidades do produto "Pen Drive 32GB"
    Then o estoque do produto "Pen Drive 32GB" deve ser 25 unidades

  Scenario: Tentar registrar entrada com quantidade zero
    Given que existe um produto "Mouse Wireless"
    When tento registrar uma entrada de 0 unidades do produto "Mouse Wireless"
    Then deve retornar erro de movimentação inválida

  Scenario: Tentar registrar saída com quantidade zero
    Given o produto "Carregador USB-C" tem 10 unidades no estoque
    When tento registrar uma saída de 0 unidades do produto "Carregador USB-C"
    Then deve retornar erro de movimentação inválida

  Scenario: Estoque exato - retirar toda quantidade disponível
    Given o produto "Adaptador HDMI" tem 3 unidades no estoque
    When eu registro uma saída de 3 unidades do produto "Adaptador HDMI"
    Then o estoque do produto "Adaptador HDMI" deve ser 0 unidades
    And deve ser criada uma movimentação de saída

  Scenario: Verificar estoque após várias operações
    Given o produto "SSD 500GB" tem 8 unidades no estoque
    When eu registro uma entrada de 12 unidades do produto "SSD 500GB"
    And eu registro uma saída de 7 unidades do produto "SSD 500GB"
    And eu registro uma entrada de 5 unidades do produto "SSD 500GB"
    And eu registro uma saída de 3 unidades do produto "SSD 500GB"
    Then o estoque do produto "SSD 500GB" deve ser 15 unidades
