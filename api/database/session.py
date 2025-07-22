from sqlalchemy.orm import Session
from api.database.engine import SessionLocal

def get_session():
    """
    Dependência do FastAPI que fornece uma sessão de banco de dados.

    Esta função cria uma nova sessão de banco de dados e a fecha quando sai do escopo. 
    Ela deve ser usada como dependência em rotas do FastAPI.

    Yields: Session: Uma sessão de banco de dados.
    """
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()