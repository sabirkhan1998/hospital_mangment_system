from sqlmodel import SQLModel,Field

class Appointment(SQLModel,table=True):
    id:int=Field(default=None,primary_key=True)
    patient_id:int=Field(foreign_key="patient.id")
    doctor_id:int=Field(foreign_key="doctor.id")
    date_time:str