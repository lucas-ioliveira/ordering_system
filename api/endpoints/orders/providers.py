from fastapi import Depends
from sqlalchemy.orm import Session
from api.database.session import get_session
from api.endpoints.orders.repository import OrderRepository
from api.endpoints.orders.services import OrderService

def get_order_service(session: Session = Depends(get_session)) -> OrderService:
    """
    Fornecer uma instância de OrderService.

    Esta função é uma dependência do FastAPI que fornece uma instância de OrderService usando a sessão de banco de dados fornecida. Ela inicializa um OrderRepository com a sessão e retorna um OrderService com esse repositório.

    Parâmetros
    session : Session Uma sessão de banco de dados, fornecida pela injeção de dependência do FastAPI.

    Retornos
    OrderService Uma instância de OrderService.
    """

    repository = OrderRepository(session)
    return OrderService(repository)
