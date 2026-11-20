from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from dependeces import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone



def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": str(id_usuario), 
        "exp": data_expiracao.timestamp()
        }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()

    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False 

    return usuario


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def index():
    """
    Essa é a rota padrão de autenticação do sistema
    """
    return {"mensagem": "você acessou a rota de autenticação", "autenticado": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first() # Gera uma query no banco de dados que verifica se há registro do mesmo email
    
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit() # Salva todas as alterações no banco de dados
        return {"mensagem": f"usuário cadastrado com sucesso {usuario_schema.email}"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema,session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
            }

# Rota de verificação via Authorize
@auth_router.post("/login-form")
async def login_form(dados_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_form.username, dados_form.password, session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
            }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    
    return {
                "access_token": access_token,
                "token_type": "Bearer"
                }