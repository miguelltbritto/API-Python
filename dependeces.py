from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    Session = sessionmaker(bind=db) # Criar a classe de sessão
    session = Session() # Isntancia o objeto da classe
    try:
        yield session
    
    except:
        pass
    
    finally:
        session.close()