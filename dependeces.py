from fastapi import Depends, HTTPException
from models import Usuario, db
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


def pegar_sessao():
    Session = sessionmaker(bind=db) # Criar a classe de sessão
    session = Session() # Isntancia o objeto da classe
    try:
        yield session
    
    except:
        session.rollback()
        raise

    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    # O tipo de token "Bearer" usa o padrão de autenticação OAuth2
    # Devido a isso, o refresh-token deve ser enviado no header da requisição como um parametro como uma "dependência"
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token")

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")

    return usuario