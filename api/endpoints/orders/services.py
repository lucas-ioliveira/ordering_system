from passlib.context import CryptContext

from api.endpoints.orders.repository import OrderRepository
from api.endpoints.orders.schemas import CreateOrderSchema
from api.models.users import User
from api.models.orders import Order

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def get_all_orders(self, offset: int = 0, limit: int = 10):
        return self.repository.get_all_orders(offset, limit)

    def get_order(self, id_order: int, user: User):
        order = self.repository.get_order_by_id(id_order)
        if not order:
            return None
        if order.user != user.id and not user.admin:
            return 'unauthorized'
        return order

    def create_order(self, data: CreateOrderSchema):
        order = Order(user=data.user)
        return self.repository.create_order(order)
    
    def cancel_order(self, id_order: int, user: User):
        order = self.repository.get_order_by_id(id_order)
        if not order:
            return None
        if order.user != user.id and not user.admin:
            return 'unauthorized'
        return self.repository.cancel_order(id_order)


