from typing import Dict, Any, Literal
from pydantic import BaseModel
from datetime import date


class Id(BaseModel):
    id: int


class CustomerId(BaseModel):
    customer_id: int


class StatusDetails(BaseModel):
    status: int
    detail: str | Dict[str, Any]


class AddressDetails(BaseModel):
    address: str | None = None
    city: str
    province: str | None = None
    zip: str | None = None


class CustomerInfo(AddressDetails):
    first_name: str
    last_name: str
    email: str
    phone: str

    class Config:
        orm_mode = True


class CustomerAllInfo(CustomerInfo, Id):
    pass


class Customers(StatusDetails):
    customers: list[CustomerAllInfo]


class Task(BaseModel):
    description: str
    date: date


class TaskInfo(Task, Id):
    is_done: bool


class Tasks(StatusDetails):
    tasks: list[TaskInfo]


class Deal(AddressDetails, CustomerId, Id):
    area: int
    people: int
    date: date
    instructions: str
    roomAccess: str
    price: int
    progress: Literal["in progress", "done", "closed"]

    class Config:
        orm_mode = True


class DealInfo(StatusDetails):
    deal: Deal


class Deals(StatusDetails):
    deals: list[Deal]
