from pydantic import BaseModel
from typing import Optional
from enum import Enum

#Schema usuario
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True

# Schema Pedido
class StatusPedido(str, Enum):
    # O sqlalchemy_utils aceita nativamente classes como parametro de escolhas
    # Dessa forma, não é preciso usar uma constante de tupla de tuplas 
    PENDENTE = "PENDENTE"
    CANCELADO = "CANCELADO"
    FINALIZADO = "FINALIZADO"

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
            from_attributes = True

# Schema login
class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
            from_attributes = True