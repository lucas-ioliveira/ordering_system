from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from api.models.orders import Order

class OrderRepository:
    def __init__(self, session: Session):
        """
        Inicializa o repositório de pedidos.

        Parâmetros
        ----------
        session : Session
            A sessão do banco de dados.
        """
        self.session = session

    def get_all_orders(self, offset: int = 0, limit: int = 10) -> list[Order]:
        """
            Recupera todos os pedidos do banco de dados.

            Parâmetros
            offset : int, opcional O número de pedidos a serem pulados antes de iniciar a coleta do conjunto de resultados. Padrão é 0.
            limit : int, opcional O número máximo de pedidos a serem retornados. Padrão é 10.

            Retornos
            list[Order] A lista de pedidos se encontrado, caso contrário uma lista vazia.
        """
        try:
            return self.session.query(Order).filter(Order.active == True).offset(offset).limit(limit).all()
        except SQLAlchemyError:
            return []
    
    def get_orders_by_user(self, user_id: int, offset: int = 0, limit: int = 10):
        try:
            return self.session.query(Order).filter(Order.user == user_id, Order.active == True).offset(offset).limit(limit).all()
        except SQLAlchemyError:
            return []

    def get_order_by_id(self, id_order: int) -> Optional[Order]:
        """
            Recupera um pedido pelo seu ID do banco de dados.

            Parâmetros
            id : int O ID do pedido a ser recuperado.

            Retornos
            Optional[Order] O objeto do pedido se encontrado, caso contrário None.
        """
        try:
            return self.session.query(Order).filter(Order.id == id_order, Order.active == True).first()
        except SQLAlchemyError:
            return None

    def create_order(self, order: Order) -> Order:
        """
        Cria um novo pedido no banco de dados.

        Parameters
        ----------
        order : Order
            O pedido a ser criado.

        Returns
        -------
        Order
            O pedido criado com o ID atualizado.
        """
        try:

            self.session.add(order)
            self.session.commit()
            self.session.refresh(order)
            return order
        except SQLAlchemyError:
            return None

    def cancel_order(self, id_order: int) -> Optional[Order]:
        """
        Cancela um pedido no banco de dados.

        Parameters
        ----------
        id_order : int
            O ID do pedido a ser cancelado.

        Returns
        -------
        Order | None
            O pedido atualizado se encontrado e cancelado, ou None se não encontrado.
        """
        try:
            order = self.get_order_by_id(id_order)
            if not order:
                return None

            order.status = 'CANCELADO'
            self.session.commit()
            self.session.refresh(order)
            return order
        except SQLAlchemyError:
            self.session.rollback()
            return None

    def finish_order(self, id_order: int) -> Optional[Order]:
        """
        Finaliza um pedido no banco de dados.

        Parameters
        ----------
        id_order : int
            O ID do pedido a ser finalizado.

        Returns
        -------
        Order | None
            O pedido atualizado se encontrado e finalizado, ou None se não encontrado.
        """
        try:
            order = self.get_order_by_id(id_order)
            if not order:
                return None

            order.status = 'FINALIZADO'
            self.session.commit()
            self.session.refresh(order)
            return order
        except SQLAlchemyError:
            self.session.rollback()
            return None