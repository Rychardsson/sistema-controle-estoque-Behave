"""
Modelo de dados para Produto
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Produto:
    """
    Classe que representa um produto no sistema de estoque
    """
    nome: str
    descricao: Optional[str] = None
    preco_unitario: float = 0.0
    estoque_atual: int = 0
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Inicializa campos de data se não fornecidos"""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def atualizar_estoque(self, nova_quantidade: int) -> None:
        """
        Atualiza a quantidade em estoque
        
        Args:
            nova_quantidade: Nova quantidade em estoque
            
        Raises:
            ValueError: Se a quantidade for negativa
        """
        if nova_quantidade < 0:
            raise ValueError("Estoque não pode ser negativo")
        
        self.estoque_atual = nova_quantidade
        self.updated_at = datetime.now()
    
    def tem_estoque_suficiente(self, quantidade: int) -> bool:
        """
        Verifica se há estoque suficiente para uma operação
        
        Args:
            quantidade: Quantidade desejada
            
        Returns:
            True se há estoque suficiente, False caso contrário
        """
        return self.estoque_atual >= quantidade
    
    def __str__(self) -> str:
        return f"Produto(id={self.id}, nome='{self.nome}', estoque={self.estoque_atual})"
    
    def __repr__(self) -> str:
        return self.__str__()
