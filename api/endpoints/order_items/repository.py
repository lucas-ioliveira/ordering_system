from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from api.models.order_items import OrderItem

class OrderItemsRepository:
    def __init__(self, session: Session):
        """
        Inicializa o repositório de pedidos.

        Parâmetros
        ----------
        session : Session
            A sessão do banco de dados.
        """
        self.session = session

    def get_all_order_items(self, offset: int = 0, limit: int = 10) -> list[OrderItem]:
        """
            Recupera todos os pedidos do banco de dados.

            Parâmetros
            offset : int, opcional O número de pedidos a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0.
            limit : int, opcional O número máximo de pedidos a serem retornados. Padrão é 10.

            Retornos
            list[OrderItem] A lista de pedidos se encontrado, caso contrário uma lista vazia.
        """
        try:
            return self.session.query(OrderItem).filter(OrderItem.active == True).offset(offset).limit(limit).all()
        except SQLAlchemyError:
            return []

    def get_order_items_by_id(self, id) -> Optional[OrderItem]:
        """
            Recupera um pedido pelo seu ID do banco de dados.

            Parâmetros
            id : int O ID do pedido a ser recuperado.

            Retornos
            Optional[OrderItem] O objeto do pedido se encontrado, caso contrário None.
        """
        try:
            return self.session.query(OrderItem).filter(OrderItem.id == id, OrderItem.active == True).first()
        except SQLAlchemyError:
            return None

    def create_order_item(self, order_item: OrderItem) -> OrderItem:
        """
        Cria um novo pedido no banco de dados.

        Parameters
        ----------
        OrderItem : OrderItem
            O pedido a ser criado.

        Returns
        -------
        OrderItem
            O pedido criado com o ID atualizado.
        """
        try:

            self.session.add(order_item)
            self.session.commit()
            self.session.refresh(order_item)
            return order_item
        except SQLAlchemyError:
            return None
