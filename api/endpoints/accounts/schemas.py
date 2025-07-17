from pydantic import BaseModel, EmailStr
from typing import Optional, Generic, TypeVar

T = TypeVar("T")


class ResponseAccountsSchema(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None

class ResponseAccountsPublicSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    active: bool

    class Config:
        from_attributes = True

class ResponseAccountsAdminSchema(ResponseAccountsPublicSchema):
    admin: bool