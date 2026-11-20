from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.patient import Patient

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/")
def create_patient(patient: Patient):
    with Session(engine) as session:
        session.add(patient)
        session.commit()
        session.refresh(patient)
        return patient

@router.get("/")
def get_patients():
    with Session(engine) as session:
        patients = session.exec(select(Patient)).all()
        return patients

@router.get("/{id}")
def get_patient(id: int):
    with Session(engine) as session:
        patient = session.get(Patient, id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
@router.put("/{id}")
def update_patient(id:int,patient:Patient):
    with Session(engine)as session:
        db_patient=session.get(Patient,id)
        if not db_patient:
            raise HTTPException(status_code=404, detail="patient not found")
        db_patient.name = patient.name
        db_patient.age = patient.age
        db_patient.phone = patient.phone
        db_patient.gender = patient.gender
        db_patient.address = patient.address
        session.add(db_patient)
        session.commit()
        session.refresh(db_patient)
        return db_patient

@router.delete("/{id}")
def delete_patient(id:int):
    with Session(engine) as session:
        patient=session.get(Patient,id)
        if not patient:
            raise HTTPException(status_code=404, detail="patient not found")
        
        session.delete(patient)
        session.commit()
        return {"message": "Patient deleted"}
        
