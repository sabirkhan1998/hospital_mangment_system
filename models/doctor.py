from sqlmodel import SQLModel,Field

class Doctor(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    department_id:int=Field(foreign_key="department.id")
    name:str
    phone:str
    specialization:str