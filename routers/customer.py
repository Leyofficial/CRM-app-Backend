from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
from dependencies import get_db
from schemas import StatusDetails, CustomerInfo, Customers

router = APIRouter(
    prefix="/api"
)


@router.post("/customer", response_model=StatusDetails)
def create_customer(data: CustomerInfo, db: Session = Depends(get_db)):
    customer = crud.create_customer(db, data)
    if customer is None:
        raise HTTPException(status_code=400, detail="Failed to create customer")
    return {'status': 200, 'detail': 'Success!'}


@router.get("/customers", response_model=Customers)
def get_customer(db: Session = Depends(get_db)):
    customers = crud.get_all_customers(db)
    return {'status': 200, 'detail': 'Success!', 'customers': customers}


@router.delete("/customer", response_model=StatusDetails, status_code=201)
def delete_customer(id: int, db: Session = Depends(get_db)):
    success = crud.delete_customer(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"status": 200, "detail": "Customer deleted successfully"}