from sqlmodel import SQLModel,Field

class Laboratory(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    patient_id:int=Field(foreign_key="patient.id")
    test_name:str
    result:str | None=None
    price:int