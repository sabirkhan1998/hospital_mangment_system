from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.laboratory import Laboratory

router=APIRouter(prefix="/laboratories",tags=["laboratories"])

@router.post("/")
def create_laboratory(laboratory:Laboratory):
    with Session(engine)as session:
        session.add(laboratory)
        session.commit()
        session.refresh(laboratory)
        return laboratory

@router.get("/")
def get_laboratories():
    with Session(engine)as session:
        laboratories=session.exec(select(Laboratory)).all()
        return laboratories

@router.get("/{id}")
def get_laboratory(id:int):
    with Session(engine)as session:
        laboratory=session.get(Laboratory,id)
        if not laboratory:
            raise HTTPException(status_code=404,detail="laboratory not found")
        return laboratory

@router.put("/{id}")
def update_laboratory(id:int,laboratory:Laboratory):
    with Session(engine)as session:
        db_laboratory=session.get(Laboratory,id)
        if not db_laboratory:
            raise HTTPException(status_code=404,detail="laboratory not found")
        db_laboratory.patient_id=laboratory.patient_id
        db_laboratory.test_name=laboratory.test_name
        db_laboratory.result=laboratory.result
        db_laboratory.price=laboratory.price
        session.add(db_laboratory)
        session.commit()
        session.refresh(db_laboratory)
        return db_laboratory

@router.delete("/{id}")
def delete_laboratory(id:int):
    with Session(engine)as session:
        laboratory=session.get(Laboratory,id)
        if not laboratory:
            raise HTTPException(status_code=404,detail="laboratory not found")
        session.delete(laboratory)
        session.commit()
        return {"message": "laboratory deleted"}