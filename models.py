from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


# conexão
db = create_engine("sqlite:///banco.db")

# base do banco de dados
Base = declarative_base()

# classes

# Usuario
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean)
    #admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = (senha)
        self.ativo = ativo
        self.admin = admin

# Pedido
class Pedido(Base):
    __tablename__ = "pedido"

    # ChoiceType requer uma "lista de tuplas" ou uma "tupla de tuplas"
    # Usando o ChoiceType garante o uso estrito e correto das opções definidas
    SATATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_usuario = Column("id_usuario", ForeignKey("usuario.id"))
    status = Column("status", ChoiceType(SATATUS_PEDIDOS), nullable=False)
    preco = Column("preco", Float)
    #itens =

    def __init__(self, id_usuario, status="PENDENTE", preco=0):
        self.id_usuario = id_usuario
        self.status = status
        self.preco = preco

# ItensPedido
class ItensPedidos(Base):
    __tablename__ = "itens_pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_pedido = Column("id_pedido", ForeignKey("pedido.id"))
    quantidade = Column("quantidade", Integer) 
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
        
# execução da criação dos metadados