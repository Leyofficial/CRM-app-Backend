from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud.customer_crud as crud
from dependencies import get_db
from schemas import StatusDetails, CustomerInfo, Customers, Customer

router = APIRouter(
    prefix="/api",
    tags=["customers"]
)


@router.post("/customer", response_model=StatusDetails)
def create_customer(data: CustomerInfo, db: Session = Depends(get_db)):
    crud.create_customer(db, data)
    return {'status': 200, 'detail': 'Success!'}


@router.get("/customer/{id}", response_model=CustomerInfo)
def get_customer(id: int, db: Session = Depends(get_db)):
    customer = crud.get_customer(db, id)
    return {'status': 200, 'detail': 'Success!', 'customer': customer}


@router.get("/customers", response_model=Customers)
def get_customers(db: Session = Depends(get_db)):
    customers = crud.get_all_customers(db)
    return {'status': 200, 'detail': 'Success!', 'customers': customers}


@router.put("/customer/{id}", response_model=CustomerInfo)
def change_customer(id: int, customer_data: Customer, db: Session = Depends(get_db)):
    updated_customer = crud.change_customer(db, id, customer_data)
    return {"status": 200, "detail": "Customer updated successfully!", "customer": updated_customer}


@router.delete("/customer/{id}", response_model=Customers, status_code=201)
def delete_customer(id: int, db: Session = Depends(get_db)):
    customers = crud.delete_customer(db, id)
    return {"status": 200, "detail": "Customer deleted successfully!", "customers": customers}
