"""
Exceções customizadas para o sistema de estoque
"""


class EstoqueException(Exception):
    """Exceção base para problemas relacionados ao estoque"""
    pass


class EstoqueInsuficienteException(EstoqueException):
    """Exceção lançada quando não há estoque suficiente para uma operação"""
    
    def __init__(self, produto_nome: str, estoque_atual: int, quantidade_solicitada: int):
        self.produto_nome = produto_nome
        self.estoque_atual = estoque_atual
        self.quantidade_solicitada = quantidade_solicitada
        
        mensagem = (
            f"Estoque insuficiente para o produto '{produto_nome}'. "
            f"Estoque atual: {estoque_atual}, "
            f"Quantidade solicitada: {quantidade_solicitada}"
        )
        super().__init__(mensagem)


class ProdutoNaoEncontradoException(EstoqueException):
    """Exceção lançada quando um produto não é encontrado"""
    
    def __init__(self, identificador):
        self.identificador = identificador
        mensagem = f"Produto não encontrado: {identificador}"
        super().__init__(mensagem)


class MovimentacaoInvalidaException(EstoqueException):
    """Exceção lançada para movimentações inválidas"""
    
    def __init__(self, motivo: str):
        self.motivo = motivo
        mensagem = f"Movimentação inválida: {motivo}"
        super().__init__(mensagem)


class EstoqueNegativoException(EstoqueException):
    """Exceção lançada quando se tenta definir estoque negativo"""
    
    def __init__(self, produto_nome: str, quantidade: int):
        self.produto_nome = produto_nome
        self.quantidade = quantidade
        mensagem = f"Não é possível definir estoque negativo ({quantidade}) para o produto '{produto_nome}'"
        super().__init__(mensagem)
