"""
Modelo de dados para Movimentação de Estoque
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class TipoMovimentacao(Enum):
    """Tipos de movimentação de estoque"""
    ENTRADA = "entrada"
    SAIDA = "saida"


@dataclass
class Movimentacao:
    """
    Classe que representa uma movimentação de estoque
    """
    produto_id: int
    tipo: TipoMovimentacao
    quantidade: int
    observacao: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Inicializa campos de data e validações"""
        if self.created_at is None:
            self.created_at = datetime.now()
        
        # Validações
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        if not isinstance(self.tipo, TipoMovimentacao):
            if isinstance(self.tipo, str):
                try:
                    self.tipo = TipoMovimentacao(self.tipo.lower())
                except ValueError:
                    raise ValueError(f"Tipo de movimentação inválido: {self.tipo}")
            else:
                raise ValueError(f"Tipo de movimentação deve ser TipoMovimentacao ou string válida")
    
    def is_entrada(self) -> bool:
        """Verifica se é uma movimentação de entrada"""
        return self.tipo == TipoMovimentacao.ENTRADA
    
    def is_saida(self) -> bool:
        """Verifica se é uma movimentação de saída"""
        return self.tipo == TipoMovimentacao.SAIDA
    
    def get_impacto_estoque(self) -> int:
        """
        Retorna o impacto da movimentação no estoque
        
        Returns:
            Valor positivo para entrada, negativo para saída
        """
        if self.is_entrada():
            return self.quantidade
        else:
            return -self.quantidade
    
    def __str__(self) -> str:
        return f"Movimentacao(id={self.id}, produto_id={self.produto_id}, tipo='{self.tipo.value}', quantidade={self.quantidade})"
    
    def __repr__(self) -> str:
        return self.__str__()
