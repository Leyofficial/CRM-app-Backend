from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud
from dependencies import get_db
from schemas import StatusDetails, CustomerInfo, Customers

router = APIRouter(
    prefix="/api"
)


@router.post("/customer", response_model=StatusDetails)
def create_customer(data: CustomerInfo, db: Session = Depends(get_db)):
    crud.create_customer(db, data)
    return {'status': 200, 'detail': 'Success!'}


@router.get("/customers", response_model=Customers)
def get_customer(db: Session = Depends(get_db)):
    customers = crud.get_all_customers(db)
    return {'status': 200, 'detail': 'Success!', 'customers': customers}


@router.delete("/customer/{id}", response_model=StatusDetails, status_code=201)
def delete_customer(id: int, db: Session = Depends(get_db)):
    crud.delete_customer(db, id)
    return {"status": 200, "detail": "Customer deleted successfully"}
