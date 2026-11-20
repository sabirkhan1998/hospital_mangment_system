from sqlmodel import SQLModel ,Field

class Billing(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    patient_id:int=Field(foreign_key="patient.id")
    appointment_id:int | None=Field(default=None,foreign_key="appointment.id")
    amount:int
    status:str
