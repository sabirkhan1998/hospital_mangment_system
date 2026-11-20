from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.pharmacy import Pharmacy

router=APIRouter(prefix="/pharmacies",tags=["pharmacies"])

@router.post("/")
def create_pharmacy(pharmacy:Pharmacy):
    with Session(engine)as session:
        session.add(pharmacy)
        session.commit()
        session.refresh(pharmacy)
        return pharmacy

@router.get("/")
def get_pharmacies():
    with Session(engine)as session:
        pharmacies=session.exec(select(Pharmacy)).all()
        return pharmacies

@router.get("/{id}")
def get_pharmacy(id:int):
    with Session(engine)as session:
        pharmacy=session.get(Pharmacy,id)
        if not pharmacy:
            raise HTTPException(status_code=404,detail="pharmacy not found")
        return pharmacy

@router.put("/{id}")
def update_pharmacy(id:int,pharmacy:Pharmacy):
    with Session(engine)as session:
        db_pharmacy=session.get(Pharmacy,id)
        if not db_pharmacy:
            raise HTTPException(status_code=404,detail="pharmacy not found")
        db_pharmacy.patient_id=pharmacy.patient_id
        db_pharmacy.medicine_name=pharmacy.medicine_name
        db_pharmacy.quantity=pharmacy.quantity
        db_pharmacy.price=pharmacy.price
        session.add(db_pharmacy)
        session.commit()
        session.refresh(db_pharmacy)
        return db_pharmacy

@router.delete("/{id}")
def delete_pharmacy(id:int):
    with Session(engine)as session:
        pharmacy=session.get(Pharmacy,id)
        if not pharmacy:
            raise HTTPException(status_code=404,detail="pharmacy not found")
        session.delete(pharmacy)
        session.commit()
        return {"message": "pharmacy deleted"}