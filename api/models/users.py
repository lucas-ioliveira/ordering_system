from sqlalchemy import Column, Integer, String, Boolean
from api.database.base import Base

class User(Base):
    __tablename__ = 'usuarios'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String)
    email = Column('email', String, nullable=False)
    password = Column('password', String)
    active = Column('active', Boolean)
    admin = Column('admin', Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self. password = password
        self.active = active
        self.admin = admin
