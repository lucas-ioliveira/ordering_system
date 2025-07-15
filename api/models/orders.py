from sqlalchemy import Column, Integer, String, Float, ForeignKey
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
    #items = 
    
    def __init__(self, user, status='PENDENTE', price=0):
        self.user = user
        self.status = status
        self.price = price