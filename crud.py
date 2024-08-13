from datetime import datetime

from sqlalchemy.orm import Session
import models
from schemas import CustomerInfo, Task

def get_all_customers(db: Session):
    return db.query(models.Customers).all() or []


def get_customer(db: Session, user_id: int):
    return db.query(models.Customers).filter(models.Customers.id == user_id).first()


def create_customer(db: Session, customer: CustomerInfo):
    # Проверка на существующего пользователя по email
    existing_customer = db.query(models.Customers).filter(models.Customers.email == customer.email).first()
    if existing_customer:
        return None

    db_customer = models.Customers(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, id: int):
    customer = db.query(models.Customers).filter(models.Customers.id == id).first()

    if customer is None:
        return False

    db.delete(customer)
    db.commit()
    return True


def create_task(db: Session, task: Task):
    try:
        date_obj = datetime.strptime(task.date, '%Y-%m-%d').date()
    except ValueError:
        return {"error": "Invalid type"}

    db_task = models.Tasks(description=task.description, date=date_obj)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_all_tasks(db: Session):
    return db.query(models.Tasks).all() or []
