from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import models
from schemas import CustomerInfo, Task, Deal, Customer


def get_all_customers(db: Session):
    return db.query(models.Customers).all() or []


def get_customer(db: Session, user_id: int):
    customer = db.query(models.Customers).filter(models.Customers.id == user_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found!")
    return customer


def get_deal_customer(db: Session, customer_id: int):
    customer = db.query(models.Customers).filter(models.Customers.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found!")
    return customer

def change_customer(db: Session, user_id: int, customer_data: Customer):
    customer = get_customer(db, user_id)

    customer.id = user_id
    customer.first_name = customer_data.first_name
    customer.last_name = customer_data.last_name
    customer.email = customer_data.email
    customer.phone = customer_data.phone
    customer.address = customer_data.address
    customer.city = customer_data.city
    customer.province = customer_data.province
    customer.zip = customer_data.zip

    db.commit()
    db.refresh(customer)

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
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    return task


def change_task(db: Session, data: Task, task_id: int):
    task = get_task(db, task_id)
    task.description = data.description
    task.date = data.date
    task.is_done = data.is_done

    db.commit()
    db.refresh(task)

    return task


def get_all_tasks(db: Session):
    return db.query(models.Tasks).all() or []


def create_deal(db: Session, deal: Deal):
    customer_id = deal.customer_id
    customer = get_deal_customer(db, customer_id)

    try:
        if customer:
            db_deal = models.Deals(**deal.dict())
            db.add(db_deal)
            db.commit()
            db.refresh(db_deal)
            return db_deal

    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to create deal: {str(error)}")


def get_deal_by_customer_id(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    if customer:
        deals = db.query(models.Deals).filter(models.Deals.customer_id == customer_id).all()
        if not deals:
            raise HTTPException(status_code=404, detail="No deals found for this customer!")

        return deals


def get_deal(db: Session, id: int):
    deal = db.query(models.Deals).filter(models.Deals.id == id).first()

    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found!")

    return deal


def change_deal(db: Session, data: Deal, deal_id: int):
    try:
        deal = get_deal(db, deal_id)
        if deal:
            deal.address = data.address
            deal.city = data.city
            deal.province = data.province
            deal.zip = data.zip
            deal.area = data.area
            deal.people = data.people
            deal.date = data.date
            deal.instructions = data.instructions
            deal.roomAccess = data.roomAccess
            deal.price = data.price
            deal.progress = data.progress

            db.commit()
            db.refresh(deal)

            return deal
    except SQLAlchemyError as error:
        raise HTTPException(status_code=400, detail=f"Failed to update deal: {str(error)}")


def get_deals(db: Session):
    return db.query(models.Deals).all() or []
