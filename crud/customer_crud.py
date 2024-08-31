from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
from schemas import CustomerInfo, Customer


# GET
def get_all_customers(db: Session):
    return db.query(models.Customers).all() or []


# GET
def get_customer(db: Session, user_id: int):
    customer = db.query(models.Customers).filter(models.Customers.id == user_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found!")
    return customer


# POST
def create_customer(db: Session, customer: Customer):
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


# PUT
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


# DELETE
def delete_customer(db: Session, id: int):
    customer = get_customer(db, id)
    try:
        db.delete(customer)
        db.commit()
        return get_all_customers(db)
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to delete customer: {str(error)}")
