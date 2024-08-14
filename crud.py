from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
from schemas import CustomerInfo, Task, Deal


def get_all_customers(db: Session):
    return db.query(models.Customers).all() or []


def get_customer(db: Session, user_id: int):
    customer = db.query(models.Customers).filter(models.Customers.id == user_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found!")
    return customer


def create_customer(db: Session, customer: CustomerInfo):
    existing_customer = db.query(models.Customers).filter(models.Customers.email == customer.email).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Email already exists!")

    try:
        db_customer = models.Customers(**customer.dict())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to create customer: {str(error)}")


def delete_customer(db: Session, id: int):
    customer = db.query(models.Customers).filter(models.Customers.id == id).first()

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found!")

    try:
        db.delete(customer)
        db.commit()
        return True
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to delete customer: {str(error)}")


def create_task(db: Session, task: Task):
    try:
        date_obj = datetime.strptime(str(task.date), '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format! Expected format: YYYY-MM-DD.")

    try:
        db_task = models.Tasks(description=task.description, date=date_obj)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to create task: {str(error)}")


def get_task(db: Session, task_id: int):
    task = db.query(models.Customers).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    return task


def get_all_tasks(db: Session):
    return db.query(models.Tasks).all() or []


def create_deal(db: Session, deal: Deal):
    customer_id = deal.customer_id
    customer = db.query(models.Customers).filter(models.Customers.id == customer_id).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found!")

    try:
        # Create and commit the deal
        db_deal = models.Deals(**deal.dict())
        db.add(db_deal)
        db.commit()
        db.refresh(db_deal)
        return db_deal
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to create deal: {str(error)}")


def get_deal(db: Session, id: int):
    deal = db.query(models.Deals).filter(models.Deals.id == id).first()

    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found!")

    return deal


def get_deals(db: Session):
    return db.query(models.Deals).all() or []
