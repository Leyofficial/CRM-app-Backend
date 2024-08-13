from sqlalchemy.orm import Session
import models
from schemas import CustomerInfo


def get_all_customers(db: Session):
    return db.query(models.Customers).all() or []


def get_customer(db: Session, user_id: int):
    return db.query(models.Customers).filter(models.Customers.id == user_id).first()


def create_customer(db: Session, customer: CustomerInfo):
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

