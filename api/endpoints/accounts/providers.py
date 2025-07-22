from fastapi import Depends
from sqlalchemy.orm import Session

from api.database.session import get_session
from api.endpoints.accounts.repository import AccountRepository
from api.endpoints.accounts.services import AccountService

def get_account_service(session: Session = Depends(get_session)) -> AccountService:
    """
    Argumentos:
    - session (Session): A sessão do banco de dados.

    Retornos:
    - AccountService: Uma instância de AccountService.
    """
    repository = AccountRepository(session)
    return AccountService(repository)