from typing import Dict, Any
from pydantic import BaseModel


class StatusDetails(BaseModel):
    status: int
    detail: str | Dict[str, Any]


class Customer(BaseModel):
    id: int


class CustomerInfo(Customer):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str | None = None
    city: str
    province: str | None = None
    zip: str | None = None

    class Config:
        orm_mode = True


class Customers(StatusDetails):
    customers: list[CustomerInfo]
