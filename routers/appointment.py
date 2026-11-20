from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.appointment import Appointment

router=APIRouter(prefix="/appointments",tags=["appointments"])

@router.post("/")
def create_appointment(appointment:Appointment):
    with Session(engine)as session:
        session.add(appointment)
        session.commit()
        session.refresh(appointment)
        return appointment

@router.get("/")
def get_appointments():
    with Session(engine)as session:
        appointments=session.exec(select(Appointment)).all()
        return appointments

@router.get("/{id}")
def get_appointment(id:int):
    with Session(engine)as session:
        appointment=session.get(Appointment,id)
        if not appointment:
            raise HTTPException(status_code=404,detail="appointment not found")
        return appointment

@router.put("/{id}")
def update_appointment(id:int,appointment:Appointment):
    with Session(engine)as session:
        db_appointment=session.get(Appointment,id)
        if not db_appointment:
            raise HTTPException(status_code=404,detail="appointment not found")
        db_appointment.patient_id=appointment.patient_id
        db_appointment.doctor_id=appointment.doctor_id
        db_appointment.date_time=appointment.date_time
        db_appointment.status=appointment.status
        session.add(db_appointment)
        session.commit()
        session.refresh(db_appointment)
        return db_appointment

@router.delete("/{id}")
def delete_appointment(id:int):
    with Session(engine)as session:
        appointment=session.get(Appointment,id)
        if not appointment:
            raise HTTPException(status_code=404,detail="appointment not found")
        session.delete(appointment)
        session.commit()
        return {"message": "appointment deleted"}