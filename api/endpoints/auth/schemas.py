from pydantic import BaseModel, EmailStr
from pydantic.generics import GenericModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ResponseUserSchema(GenericModel, Generic[T]):
    message: str
    data: Optional[T] = None

class ResponseUser(BaseModel):
    id: int
    name: str
    email: EmailStr
    active: bool
    admin: bool

    class Config:
        from_attributes = True

class CreateUserSchemas(BaseModel):
    name: str
    email: str
    password: str
    active: bool
    # admin: Optional[bool]

    class Config:
        from_attibutes = True

class CreateUserAdminSchemas(BaseModel):
    name: str
    email: str
    password: str
    active: bool
    admin: bool

    class Config:
        from_attibutes = True

class LoginUserSchemas(BaseModel):
    email: str
    password: str

    class Config:
        from_attibutes = True