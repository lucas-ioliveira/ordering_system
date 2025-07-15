from fastapi import Depends
from sqlalchemy.orm import Session
from api.database.session import get_session
from api.endpoints.auth.repository import AuthRepository
from api.endpoints.auth.services import AuthService
from api.config.security import oauth2_scheme

def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    """
    Argumentos:
    - session (Session): A sessão do banco de dados.

    Retornos:
    - AuthService: Uma instância de AuthService.
    """
    repository = AuthRepository(session)
    return AuthService(repository)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service)
):
    """
    Retorna o usuário autenticado a partir do token de acesso informado.

    O token de acesso obtido por meio do endpoint /api/v1/auth/login-form e informado
    automaticamente pelo FastAPI por meio do parâmetro token.

    A função utilizada como decorator em rotas que necessitam de autenticação.

    Retornos:
    - User: O usuário autenticado.
    """
    return service.verify_token(token)