from typing import Dict, Any
from pydantic import BaseModel
from datetime import date

class StatusDetails(BaseModel):
    status: int
    detail: str | Dict[str, Any]


class Id(BaseModel):
    id: int


class CustomerInfo(BaseModel):
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


class CustomerAllInfo(CustomerInfo, Id):
    pass


class Customers(StatusDetails):
    customers: list[CustomerAllInfo]


class Task(BaseModel):
    description: str
    date: date


class TaskInfo(Task, Id):
    pass


class Tasks(StatusDetails):
    tasks: list[TaskInfo]
