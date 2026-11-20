from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.billing import Billing

router=APIRouter(prefix="/billings",tags=["billings"])

@router.post("/")
def create_billing(billing:Billing):
    with Session(engine)as session:
        session.add(billing)
        session.commit()
        session.refresh(billing)
        return billing

@router.get("/")
def get_billings():
    with Session(engine)as session:
        billings=session.exec(select(Billing)).all()
        return billings

@router.get("/{id}")
def get_billing(id:int):
    with Session(engine)as session:
        billing=session.get(Billing,id)
        if not billing:
            raise HTTPException(status_code=404,detail="billing not found")
        return billing

@router.put("/{id}")
def update_billing(id:int,billing:Billing):
    with Session(engine)as session:
        db_billing=session.get(Billing,id)
        if not db_billing:
            raise HTTPException(status_code=404,detail="billing not found")
        db_billing.patient_id=billing.patient_id
        db_billing.appointment_id=billing.appointment_id
        db_billing.amount=billing.amount
        db_billing.status=billing.status
        session.add(db_billing)
        session.commit()
        session.refresh(db_billing)
        return db_billing

@router.delete("/{id}")
def delete_billing(id:int):
    with Session(engine)as session:
        billing=session.get(Billing,id)
        if not billing:
            raise HTTPException(status_code=404,detail="billing not found")
        session.delete(billing)
        session.commit()
        return {"message": "billing deleted"}