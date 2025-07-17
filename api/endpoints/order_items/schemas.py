from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

# T é um tipo genérico que será substituído por outro schema (ex: OrderPublicSchema)
T = TypeVar("T")

class ResponseOrderItemsSchema(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None # Pode ser um objeto, uma lista, ou None


class CreateOrderItemsSchema(BaseModel):
    amount: int
    flavor: str
    size: str
    unit_price: float
    order: int

    class Config:
        from_attributes = True

class OrderItemsPublicSchema(BaseModel):
    id: int
    amount: int
    flavor: str
    size: str
    unit_price: float
    order: int
    active: bool

    class Config:
        from_attributes = True
