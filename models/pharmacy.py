from sqlmodel import SQLModel,Field

class Pharmacy(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    patient_id:int=Field(foreign_key="patient.id")
    medicine_name:str
    quantity:int
    price:int