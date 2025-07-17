from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Optional, Generic, TypeVar, List

from api.endpoints.order_items.schemas import OrderItemsPublicSchema

# T é um tipo genérico que será substituído por outro schema (ex: OrderPublicSchema)
T = TypeVar("T")

class ResponseOrderSchema(GenericModel, Generic[T]):
    message: str
    data: Optional[T] = None # Pode ser um objeto, uma lista, ou None


class CreateOrderSchema(BaseModel):
    user: int

    class Config:
        from_attributes = True

class OrderPublicSchema(BaseModel):
    id: int
    user: int
    status: str
    price: float
    active: bool
    items: List[OrderItemsPublicSchema]

    class Config:
        from_attributes = True
