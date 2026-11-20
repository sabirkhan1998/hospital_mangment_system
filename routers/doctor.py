from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.doctor import Doctor

router=APIRouter(prefix="/doctors",tags=["doctors"])

@router.post("/")
def create_doctor(doctor:Doctor):
    with Session(engine)as session:
        session.add(doctor)
        session.commit()
        session.refresh(doctor)
        return doctor
@router.get("/")
def get_doctors():
    with Session(engine)as session:
        doctors=session.exec(select(Doctor)).all()
        return doctors
@router.get("/{id}")
def get_doctor(id:int):
    with Session(engine) as session:
        doctor=session.get(Doctor,id)
        if not doctor:
            raise HTTPException(status_code=404,detail="doctor not found")
        return doctor

@router.put("/{id}")
def update_doctor(id:int,doctor:Doctor):
    with Session(engine)as session:
        db_doctor=session.get(Doctor,id)
        if not db_doctor:
            raise HTTPException(status_code=404,detail="doctor not found")
        db_doctor.department_id=doctor.department_id
        db_doctor.name=doctor.name
        db_doctor.phone=doctor.phone
        db_doctor.specialization=doctor.specialization
        session.add(db_doctor)
        session.commit()
        session.refresh(db_doctor)
        return db_doctor
@router.delete("/{id}")
def delete_doctor(id:int):
    with Session(engine)as session:
        doctor=session.get(Doctor,id)
        if not doctor:
            raise HTTPException(status_code=404,detail="doctor not found")
        session.delete(doctor)
        session.commit()
        return {"message": "doctor deleted"}