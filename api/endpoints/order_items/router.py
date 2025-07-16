from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from api.endpoints.auth.providers import get_current_user
from api.endpoints.order_items.schemas import (CreateOrderItemsSchema, OrderItemsPublicSchema, ResponseOrderItemsSchema)
from api.endpoints.order_items.services import OrderItemsService
from api.endpoints.order_items.providers import get_order_items_service
from api.models.users import User


router = APIRouter(
    prefix='/api/v1/order-items', 
    tags=['order-items'],
    dependencies=[Depends(get_current_user)])

@router.get('/', status_code=status.HTTP_200_OK, response_model=ResponseOrderItemsSchema[List[OrderItemsPublicSchema]])
async def get_all_order_items(offset: int = 0, limit: int = 10, service: OrderItemsService = Depends(get_order_items_service)):
    """
    Recupera todos os itens do pedido do banco de dados com paginação.

    Este endpoint permite que os usuários busquem uma lista de pedidos, com paginação opcional usando parâmetros de offset e limite.

    Parâmetros
    ----------
    offset : int, opcional O número de pedidos a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0. limit : int, opcional O número máximo de pedidos a serem retornados. Padrão é 10. service : OrderItemsService A instância do serviço de pedidos usada para recuperar pedidos. user : User O usuário autenticado atual.

    Retornos
    ----------
    ResponseOrderItemsSchema[List[OrderItemsPublicSchema]] Um esquema de resposta contendo uma mensagem e a lista de pedidos.
    """

    order_items = service.get_all_order_items(offset, limit)
    return ResponseOrderItemsSchema(message='Order items found', data=order_items)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseOrderItemsSchema[OrderItemsPublicSchema])
async def create_order_items(create_order_items_schema: CreateOrderItemsSchema, 
                            service: OrderItemsService = Depends(get_order_items_service),
                            user: User = Depends(get_current_user)):
    
    """
    Cria um novo item do pedido no banco de dados.

    Recebe os dados do item do pedido e o criador do pedido e verifica se o usuário tem permiss o para criar um novo item do pedido.

    Se o item do pedido for criado com sucesso, retorna o item do pedido criado com o status HTTP 201.
    Se o item do pedido n o for criado, retorna um erro HTTP 400 com a mensagem 'Erro ao criar o item do pedido.'.
    Se o usuário não tiver permissão, retorna um erro HTTP 401 com a mensagem 'Unauthorized'.
    """
    order_items = service.create_order_items(create_order_items_schema, user)
    return ResponseOrderItemsSchema(message='Item do do pedido criado com sucesso.', data=order_items)

@router.get('/{id_order_items}', status_code=status.HTTP_200_OK, response_model=ResponseOrderItemsSchema[OrderItemsPublicSchema])
async def get_order_items(id_order_items : int, service: OrderItemsService = Depends(get_order_items_service),
                       user: User = Depends(get_current_user)):

    """
    Recupera um pedido do banco de dados.

    Recebe o ID do pedido e verifica se o pedido existe e se o usuário tem permiss o para acessá-lo.

    Se o pedido existir e o usuário tiver permiss o, retorna o pedido.
    Se o pedido não existir, retorna um erro HTTP 404 com a mensagem 'Order not found'.
    Se o usuário não tiver permissão, retorna um erro HTTP 401 com a mensagem 'Unauthorized'.
    """
    order = service.get_order_items(id_order_items, user)
    return ResponseOrderItemsSchema(message='Order found', data=order)
