from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import create_db_tables
from models.patient import Patient
from models.department import Department
from models.doctor import Doctor
from models.appointment import Appointment
from models.billing import Billing
from models.pharmacy import Pharmacy
from models.laboratory import Laboratory
from routers import patient,department,doctor,appointment,billing,pharmacy,laboratory


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(patient.router)
app.include_router(department.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(billing.router)
app.include_router(pharmacy.router)
app.include_router(laboratory.router)
app.mount("/app", StaticFiles(directory="static", html=True), name="static")
@app.on_event("startup")
def on_startup():
    create_db_tables()