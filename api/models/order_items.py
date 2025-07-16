from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from api.database.base import Base

class OrderItem(Base):
    __tablename__ = 'itens_pedido'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    amount = Column('amount', Integer)
    flavor = Column('flavor', String)
    size = Column('size', String)
    unit_price = Column('unit_price', Float)
    order = Column('order', ForeignKey('pedidos.id'))
    active = Column('active', Boolean)

    def __init__(self, amount, flavor, size, unit_price, order, active=True):
        self.amount = amount
        self.flavor = flavor
        self.size = size
        self.unit_price =unit_price
        self.order = order
        self.active = active
    