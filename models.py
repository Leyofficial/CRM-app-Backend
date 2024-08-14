from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    province = Column(String, nullable=True)
    zip = Column(String, nullable=True)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    is_done = Column(Boolean, default=False)
    description = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)


class Deals(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    province = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    area = Column(Integer, nullable=False)
    people = Column(Integer, nullable=False)
    date = Column(Integer, nullable=False)
    instructions = Column(String, nullable=True)
    roomAccess = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    progress = Column(String, nullable=False)
