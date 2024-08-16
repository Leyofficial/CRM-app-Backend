from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import models
from crud.customer_crud import get_customer
from schemas import Deal


# GET
def get_deal(db: Session, id: int):
    deal = db.query(models.Deals).filter(models.Deals.id == id).first()

    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found!")

    return deal


# GET
def get_deals(db: Session):
    return db.query(models.Deals).all() or []


# GET
def get_deal_by_customer_id(db: Session, customer_id: int):
    customer = get_customer(db, customer_id)
    if customer:
        deals = db.query(models.Deals).filter(models.Deals.customer_id == customer_id).all()
        if not deals:
            raise HTTPException(status_code=404, detail="No deals found for this customer!")

        return deals


# POST
def create_deal(db: Session, deal: Deal):
    customer_id = deal.customer_id
    customer = get_customer(db, customer_id)

    try:
        if customer:
            db_deal = models.Deals(**deal.dict())
            db.add(db_deal)
            db.commit()
            db.refresh(db_deal)
            return db_deal

    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to create deal: {str(error)}")


# PUT
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


# DELETE
def delete_deal(db: Session, id: int):
    deal = get_deal(db, id)
    try:
        db.delete(deal)
        db.commit()
        return get_deals(db)
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Failed to delete deal: {str(error)}")


