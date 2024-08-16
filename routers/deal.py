from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
import crud.deal_crud as crud
from schemas import Deal, StatusDetails, DealDetails, Deals

router = APIRouter(
    prefix="/api",
    tags=["deals"]
)


@router.post("/deal", response_model=StatusDetails)
def create_deal(data: Deal, db: Session = Depends(get_db)):
    crud.create_deal(db, data)
    return {"status": 200, "detail": "Success!"}


@router.get("/deal/customer/{customer_id}", response_model=Deals)
def get_deal_by_customer_id(customer_id: int, db: Session = Depends(get_db)):
    user_deals = crud.get_deal_by_customer_id(db, customer_id)
    return {"status": 200, "detail": "Success!", "deals": user_deals}


@router.put("/deal/{id}", response_model=DealDetails)
def change_deal(id: int, data: Deal, db: Session = Depends(get_db)):
    updated_deal = crud.change_deal(db, data, id)
    return {"status": 200, "detail": "Deal updated successfully!", "deal": updated_deal}


@router.delete("/deal/{id}", response_model=Deals)
def delete_deal(id: int, db: Session = Depends(get_db)):
    deals = crud.delete_deal(db, id)
    return {"status": 200, "detail": "Deal deleted successfully!", "deals": deals}


@router.get("/deal/{id}", response_model=DealDetails)
def get_deal(id: int, db: Session = Depends(get_db)):
    deal = crud.get_deal(db, id)
    return {"status": 200, "detail": "Success!", "deal": deal}


@router.get("/deals", response_model=Deals)
def get_all_deals(db: Session = Depends(get_db)):
    deals = crud.get_deals(db)
    return {"status": 200, "detail": "Success!", "deals": deals}
