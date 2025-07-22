from fastapi import Depends
from sqlalchemy.orm import Session
from api.database.session import get_session
from api.endpoints.order_items.repository import OrderItemsRepository
from api.endpoints.order_items.services import OrderItemsService

def get_order_items_service(session: Session = Depends(get_session)) -> OrderItemsService:
    """
    Fornecer uma instância de OrderItemsService.

    Esta função é uma dependência do FastAPI que fornece uma instância de OrderItemsService usando a sessão de banco de dados fornecida. Ela inicializa um OrderRepository com a sessão e retorna um OrderItemsService com esse repositório.

    Parâmetros
    session : Session Uma sessão de banco de dados, fornecida pela injeção de dependência do FastAPI.

    Retornos
    OrderItemsService Uma instância de OrderItemsService.
    """

    repository = OrderItemsRepository(session)
    return OrderItemsService(repository)
