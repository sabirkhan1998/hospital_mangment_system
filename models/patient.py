from sqlmodel import SQLModel,Field

class Patient(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    name:str
    age:int=Field(gt=0)
    phone:str
    gender:str
    address:str |None = None
    