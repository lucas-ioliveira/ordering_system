from fastapi import APIRouter, Depends, status
from typing import List

from api.endpoints.auth.providers import get_current_user
from api.endpoints.orders.schemas import (CreateOrderSchema, OrderPublicSchema, ResponseOrderSchema)
from api.endpoints.orders.services import OrderService
from api.endpoints.orders.providers import get_order_service
from api.models.users import User


router = APIRouter(
    prefix='/api/v1/orders', 
    tags=['orders'],
    dependencies=[Depends(get_current_user)]
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=ResponseOrderSchema[List[OrderPublicSchema]])
async def get_all_orders(offset: int = 0, limit: int = 10, service: OrderService = Depends(get_order_service)):
    """
    Recupera todos os pedidos do banco de dados com paginação.

    Este endpoint permite que os usuários busquem uma lista de pedidos, com paginação opcional usando parâmetros de offset e limite.

    Parâmetros
    ----------
    offset : int, opcional O número de pedidos a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0. limit : int, opcional O número máximo de pedidos a serem retornados. Padrão é 10. service : OrderService A instância do serviço de pedidos usada para recuperar pedidos. user : User O usuário autenticado atual.

    Retornos
    ----------
    ResponseOrderSchema[List[OrderPublicSchema]] Um esquema de resposta contendo uma mensagem e a lista de pedidos.
    """

    orders = service.get_all_orders(offset, limit)
    return ResponseOrderSchema(message='Orders found', data=orders)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseOrderSchema[OrderPublicSchema])
async def create_order(create_order_schema: CreateOrderSchema, 
                       service: OrderService = Depends(get_order_service)):

    """
    Cria um novo pedido no banco de dados.

    Recebe os dados do pedido e o criador do pedido e verifica se o usuário tem permiss o para criar um novo pedido.

    Se o pedido for criado com sucesso, retorna o pedido criado com o status HTTP 201.
    Se o pedido n o for criado, retorna um erro HTTP 400 com a mensagem 'Erro ao criar o pedido.'.
    """
    order = service.create_order(create_order_schema)
    return ResponseOrderSchema(message='Pedido criado com sucesso.', data=order)

@router.get('/{id_order}', status_code=status.HTTP_200_OK, response_model=ResponseOrderSchema[OrderPublicSchema])
async def get_order(id_order : int, service: OrderService = Depends(get_order_service),
                       user: User = Depends(get_current_user)):

    """
    Recupera um pedido do banco de dados.

    Recebe o ID do pedido e verifica se o pedido existe e se o usuário tem permiss o para acessá-lo.

    Se o pedido existir e o usuário tiver permiss o, retorna o pedido.
    Se o pedido n o existir, retorna um erro HTTP 404 com a mensagem 'Order not found'.
    Se o usuário n o tiver permiss o, retorna um erro HTTP 401 com a mensagem 'Unauthorized'.
    """
    order = service.get_order(id_order, user)
    return ResponseOrderSchema(message='Order found', data=order)

@router.post('/{id_order}/cancel', status_code=status.HTTP_200_OK, response_model=ResponseOrderSchema[OrderPublicSchema])
async def cancel_order(id_order : int, service: OrderService = Depends(get_order_service),
                       user: User = Depends(get_current_user)):
    """
    Cancela um pedido no banco de dados.

    Recebe o ID do pedido a ser cancelado e verifica se o pedido existe e se o usuário tem permiss o para cancelá-lo.

    Se o pedido existir e o usuário tiver permissão, altera o status do pedido para 'CANCELADO' e retorna o pedido atualizado.

    Caso contrário, lança um erro HTTP 404 com a mensagem 'Order not found' ou um erro HTTP 401 com a mensagem 'Unauthorized'.

    Parameters
    ----------
    id_order : int
        O ID do pedido a ser cancelado.

    Returns
    -------
    dict[str, Any] Um dicionário com uma mensagem de confirmação de cancelamento do pedido e o pedido atualizado.

    Raises
    ------
    HTTPException
        Se o pedido não existir ou o usuário não tiver permissão para cancelá-lo.
    """
    order = service.cancel_order(id_order, user)
    return ResponseOrderSchema(message='Order canceled', data=order)