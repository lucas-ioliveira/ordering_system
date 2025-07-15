from passlib.context import CryptContext

from api.endpoints.orders.repository import OrderRepository
from api.endpoints.orders.schemas import CreateOrderSchema
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

    def get_all_orders(self, offset: int = 0, limit: int = 10):
        """
        Recupera todos os pedidos do banco de dados com paginação.

        Parâmetros
        ----------
        offset : int, opcional O número de pedidos a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0.
        limit : int, opcional O número máximo de pedidos a serem retornados. Padrão é 10.

        Retornos
        -------
        list[Order] A lista de pedidos se encontrado, caso contr rio uma lista vazia.
        """
        return self.repository.get_all_orders(offset, limit)

    def get_order(self, id_order: int, user: User):
        """
        Recupera um pedido pelo seu ID do banco de dados.

        Verifica se o pedido existe e se o usuário tem permiss o para acess -lo.

        Se o pedido existir e o usuário tiver permiss o, retorna o pedido.
        Se o pedido não existir, retorna None.
        Se o usuário não tiver permiss o, retorna 'unauthorized'.

        Parâmetros
        ----------
        id_order : int
            O ID do pedido a ser recuperado.
        user : User
            O usuário que está fazendo a requisição.

        Retornos
        -------
        Order | None | str
            O pedido se encontrado e o usuário tiver permiss o, None se o pedido n o existir, ou 'unauthorized' se o usuário não tiver permissão.
        """
        order = self.repository.get_order_by_id(id_order)
        if not order:
            return None
        if order.user != user.id and not user.admin:
            return 'unauthorized'
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
        return self.repository.create_order(order)
    
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
        Order | None | str
            O pedido atualizado se encontrado e o usuário tiver permiss o, None se o pedido n o existir, ou 'unauthorized' se o usuário não tiver permiss o.
        """
        order = self.repository.get_order_by_id(id_order)
        if not order:
            return None
        if order.user != user.id and not user.admin:
            return 'unauthorized'
        return self.repository.cancel_order(id_order)


