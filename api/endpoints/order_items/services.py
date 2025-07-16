from fastapi import HTTPException

from api.config.emuns import UserErrorMessages, OrderErrorMessages
from api.database.session import get_session
from api.endpoints.orders.repository import OrderRepository
from api.endpoints.order_items.repository import OrderItemsRepository
from api.endpoints.order_items.schemas import CreateOrderItemsSchema
from api.models.users import User
from api.models.order_items import OrderItem


class OrderItemsService:
    def __init__(self, repository: OrderItemsRepository):
        """
        Inicializa o serviço de itens de pedidos.

        Parâmetros
        ----------
        repository : OrderItemsRepository
            O repositório de pedidos.
        """
        self.repository = repository

    def get_all_order_items(self, offset: int = 0, limit: int = 10):
        """
        Recupera todos os pedidos do banco de dados com paginação.

        Parâmetros
        ----------
        offset : int, opcional O número de pedidos a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0.
        limit : int, opcional O número máximo de pedidos a serem retornados. Padrão é 10.

        Retornos
        -------
        list[OrderItems] A lista de itens de pedidos se encontrado, caso contrário uma lista vazia.
        """
        return self.repository.get_all_order_items(offset, limit)

    def get_order_items(self, id_order_items: int, user: User):
        """
        Recupera um imtem pedido pelo seu ID do banco de dados.

        Verifica se o pedido existe e se o usuário tem permiss o para acess -lo.

        Se o pedido existir e o usuário tiver permiss o, retorna o pedido.
        Se o pedido não existir, retorna None.
        Se o usuário não tiver permiss o, retorna 'unauthorized'.

        Parâmetros
        ----------
        id_order_items : int
            O ID do pedido a ser recuperado.
        user : User
            O usuário que está fazendo a requisição.

        Retornos
        -------
        Order | HTTPException
            O pedido se encontrado e o usuário tiver permissão.
            Um erro HTTP 404 com a mensagem 'Order not found' se o pedido não existir.
            Um erro HTTP 401 com a mensagem 'Unauthorized' se o usuário não tiver permissão.
            
        """
        order = self.repository.get_order_by_id(id_order_items)
        if not order:
            raise HTTPException(status_code=404, detail=OrderErrorMessages.ORDER_NOT_FOUND)
        if order.user != user.id and not user.admin:
            raise HTTPException(status_code=401, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        return order

    def create_order_items(self, data: CreateOrderItemsSchema, user: User):
        """
        Cria um novo item de pedido no banco de dados.

        Parâmetros
        ----------
        data : CreateOrderItemsSchema
            O esquema com os dados do item de pedido a ser criado.

        Retornos
        -------
        Order itemms
            O item de pedido criado com o ID atualizado.
        """
        session = next(get_session())
        order_repo = OrderRepository(session)
        order = order_repo.get_order_by_id(data.order)

        if not order:
            raise HTTPException(status_code=404, detail=OrderErrorMessages.ORDER_NOT_FOUND)

        if order.user != user.id and not user.admin:
            raise HTTPException(status_code=401, detail=UserErrorMessages.USER_NOT_AUTHORIZED)

        if order.status == 'CANCELADO':
            raise HTTPException(status_code=400, detail=OrderErrorMessages.ORDER_ALREADY_CANCELLED)

        order_item = OrderItem(
            amount=data.amount,
            flavor=data.flavor,
            size=data.size,
            unit_price=data.unit_price,
            order=order.id)

        order_item_created = self.repository.create_order_item(order_item)
        order.update_order_price()
        session.commit()
        session.refresh(order)
        return order_item_created



