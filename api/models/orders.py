from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from api.database.base import Base

class Order(Base):
    __tablename__ = 'pedidos'

    # ORDER_STATUS = (
    #     ('PENDENTE', 'PENDENTE'),
    #     ('CANCELADO', 'CANCELADO'),
    #     ('FINALIZADO', 'FINALIZADO')
    # )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    user = Column('user', ForeignKey('usuarios.id'))
    status = Column('status', String)
    price = Column('price', Float)
    active = Column('active', Boolean)
    items = relationship('OrderItem', cascade='all, delete')
    
    def __init__(self, user, status='PENDENTE', price=0, active=True):
        self.user = user
        self.status = status
        self.price = price
        self.active = active

    def update_order_price(self):
        self.price = sum(item.unit_price * item.amount for item in self.items if item.active)