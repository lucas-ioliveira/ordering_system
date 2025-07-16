from fastapi import HTTPException

from api.endpoints.orders.repository import OrderRepository
from api.endpoints.orders.schemas import CreateOrderSchema
from api.config.emuns import UserErrorMessages, OrderErrorMessages
from api.models.users import User
from api.models.orders import Order

class OrderService:
    def __init__(self, repository: OrderRepository):
        """
        Inicializa o serviço de pedidos.

        Parâmetros
        ----------
        repository : OrderRepository
            O repositório de pedidos.
        """
        self.repository = repository

    def get_all_orders(self, user: User, offset: int = 0, limit: int = 10):
        """
        Recupera todos os pedidos do banco de dados com paginação.

        Parâmetros
        ----------
        user : User
            O usuário autenticado atual.
        offset : int, opcional O número de pedidos a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0.
        limit : int, opcional O número máximo de pedidos a serem retornados. Padrão é 10.

        Retornos
        -------
        list[Order] A lista de pedidos se encontrado, caso contrário uma lista vazia.
        """
        if user.admin:
            return self.repository.get_all_orders(offset, limit)

        return self.repository.get_orders_by_user(user.id, offset, limit)

    def get_order(self, id_order: int, user: User):
        """
        Recupera um pedido pelo seu ID do banco de dados.

        Verifica se o pedido existe e se o usuário tem permiss o para acess -lo.

        Se o pedido existir e o usuário tiver permissão, retorna o pedido.
        Se o pedido não existir, retorna um erro HTTP 404 com a mensagem 'Order not found'.
        Se o usuário não tiver permissão, retorna um erro HTTP 401 com a mensagem 'Unauthorized'.

        Parâmetros
        ----------
        id_order : int
            O ID do pedido a ser recuperado.
        user : User
            O usuário que está fazendo a requisição.

        Retornos
        -------
        Order
            O pedido se encontrado e o usuário tiver permissão.
        HTTPException
            Um erro HTTP 404 com a mensagem 'Order not found' se o pedido não existir.
            Um erro HTTP 401 com a mensagem 'Unauthorized' se o usuário não tiver permissão.
        
        """
        order = self.repository.get_order_by_id(id_order, user.id)
        if not order:
            raise HTTPException(status_code=404, detail=OrderErrorMessages.ORDER_NOT_FOUND)
        if order.user != user.id and not user.admin:
            raise HTTPException(status_code=401, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        return order

    def create_order(self, data: CreateOrderSchema):
        """
        Cria um novo pedido no banco de dados.

        Parâmetros
        ----------
        data : CreateOrderSchema
            O esquema com os dados do pedido a ser criado.

        Retornos
        -------
        Order
            O pedido criado com o ID atualizado.
        """
        order = Order(user=data.user)
        order_created = self.repository.create_order(order)
        if not order_created:
            raise HTTPException(status_code=500, detail=OrderErrorMessages.ORDER_NOT_CREATED)
        return order_created
    
    def cancel_order(self, id_order: int, user: User):
        """
        Cancela um pedido no banco de dados.

        Verifica se o pedido existe e se o usuário tem permiss o para cancelá-lo.

        Se o pedido existir e o usuário tiver permissão, altera o status do pedido para 'CANCELADO' e retorna o pedido atualizado.
        Se o pedido não existir, retorna None.
        Se o usuário não tiver permiss o, retorna 'unauthorized'.

        Parâmetros
        ----------
        id_order : int
            O ID do pedido a ser cancelado.
        user : User
            O usuário que está fazendo a requisição.

        Retornos
        -------
        Order
            O pedido atualizado se encontrado e o usuário tiver permissão.
        HTTPException
            Um erro HTTP 404 com a mensagem 'Order not found' se o pedido não existir.
            Um erro HTTP 401 com a mensagem 'Unauthorized' se o usuário não tiver permissão. 
        """
        order = self.repository.get_order_by_id(id_order)
        if not order:
            raise HTTPException(status_code=404, detail=OrderErrorMessages.ORDER_NOT_FOUND)

        if order.user != user.id and not user.admin:
            raise HTTPException(status_code=401, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        order_created = self.repository.cancel_order(id_order)
        if not order_created:
            raise HTTPException(status_code=500, detail=OrderErrorMessages.ORDER_NOT_CANCELLED)
        
        return order_created
    
    def finish_order(self, id_order: int, user: User):
        """
        Finaliza um pedido no banco de dados.

        Verifica se o pedido existe e se o usuário tem permiss o para cancelá-lo.

        Se o pedido existir e o usuário tiver permissão, altera o status do pedido para 'FINALIZADO' e retorna o pedido atualizado.
        Se o pedido não existir, retorna None.
        Se o usuário não tiver permiss o, retorna 'unauthorized'.

        Parâmetros
        ----------
        id_order : int
            O ID do pedido a ser finalizado.
        user : User
            O usuário que está fazendo a requisição.

        Retornos
        -------
        Order
            O pedido atualizado se encontrado e o usuário tiver permissão.
        HTTPException
            Um erro HTTP 404 com a mensagem 'Order not found' se o pedido não existir.
            Um erro HTTP 401 com a mensagem 'Unauthorized' se o usuário não tiver permissão. 
        """
        order = self.repository.get_order_by_id(id_order)
        if not order:
            raise HTTPException(status_code=404, detail=OrderErrorMessages.ORDER_NOT_FOUND)

        if not user.admin:
            raise HTTPException(status_code=401, detail=UserErrorMessages.USER_NOT_AUTHORIZED)
        
        order_created = self.repository.finish_order(id_order)
        if not order_created:
            raise HTTPException(status_code=500, detail=OrderErrorMessages.ORDER_NOT_CANCELLED)
        
        return order_created
