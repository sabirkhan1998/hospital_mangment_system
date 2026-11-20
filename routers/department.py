from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import engine
from models.department import Department

router=APIRouter(prefix="/departments",tags=["departments"])

@router.post("/")
def create_department(department:Department):
    with Session(engine)as session:
        session.add(department)
        session.commit()
        session.refresh(department)
        return department

@router.get("/")
def get_departments():
    with Session(engine)as session:
        department = session.exec(select(Department)).all()
        return department

@router.get("/{id}")
def get_department(id:int):
    with Session(engine) as session:
        department=session.get(Department,id)
        if not department:
            raise HTTPException(status_code=404,detail="department not found")
        return department

@router.put("/{id}")
def update_department(id:int,department:Department):
    with Session(engine)as session:
        db_department=session.get(Department,id)
        if not db_department:
            raise HTTPException(status_code=404,detail="department not found")
        db_department.name=department.name
        session.add(db_department)
        session.commit()
        session.refresh(db_department)
        return db_department

@router.delete("/{id}")
def delete_department(id:int):
    with Session(engine)as session:
        department=session.get(Department,id)
        if  not department:
            raise HTTPException(status_code=404,detail="department not found")
        session.delete(department)
        session.commit()
        return {"message": "department deleted"}