from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependeces import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrão de autenticação do sistema
    """
    return {"mensagem": "você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(id_usuario = pedido_schema.id_usuario)

    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido {novo_pedido.id }"}
