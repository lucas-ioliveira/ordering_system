from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ResponseUserSchema(GenericModel, Generic[T]):
    message: str
    data: Optional[T] = None

class CreateUserSchemas(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        # Tranformar os campos em atributos da classe
        from_attibutes = True

class LoginUserSchemas(BaseModel):
    email: str
    password: str

    class Config:
        from_attibutes = True