from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
from models import Base, Patient, Appointment

from twilio.rest import Client
from dotenv import load_dotenv

from transformers import pipeline

from datetime import datetime
import os

# ===================================
# LOAD ENV
# ===================================

load_dotenv()

# ===================================
# DATABASE SETUP
# ===================================

Base.metadata.create_all(bind=engine)

# ===================================
# FASTAPI APP
# ===================================

app = FastAPI()

# ===================================
# CORS
# ===================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================================
# HOME
# ===================================

@app.get("/")
def home():

    return {
        "message": "MediCall AI Running Successfully"
    }

# ===================================
# ADD PATIENT
# ===================================

@app.post("/add-patient")
def add_patient(
    name: str,
    phone: str,
    language: str
):

    db = SessionLocal()

    try:

        patient = Patient(
            name=name,
            phone=phone,
            language=language
        )

        db.add(patient)

        db.commit()

        return {
            "message": "Patient Added Successfully"
        }

    except Exception as e:

        return {
            "message": str(e)
        }

# ===================================
# GET PATIENTS
# ===================================

@app.get("/patients")
def get_patients():

    db = SessionLocal()

    patients = db.query(Patient).all()

    return patients

# ===================================
# DELETE PATIENT
# ===================================

@app.delete("/delete-patient/{patient_id}")
def delete_patient(patient_id: int):

    db = SessionLocal()

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:

        return {
            "message": "Patient Not Found"
        }

    db.delete(patient)

    db.commit()

    return {
        "message": "Patient Deleted Successfully"
    }

# ===================================
# ADD APPOINTMENT
# ===================================

@app.post("/add-appointment")
def add_appointment(
    patient_id: int,
    doctor_name: str,
    appointment_date: str
):

    db = SessionLocal()

    try:

        appointment_datetime = datetime.strptime(
            appointment_date,
            "%Y-%m-%d %H:%M"
        )

    except:

        return {
            "message": "Use format: YYYY-MM-DD HH:MM"
        }

    appointment = Appointment(
        patient_id=patient_id,
        doctor_name=doctor_name,
        appointment_date=appointment_datetime,
        status="Scheduled"
    )

    db.add(appointment)

    db.commit()

    return {
        "message": "Appointment Added Successfully"
    }

# ===================================
# GET APPOINTMENTS
# ===================================

@app.get("/appointments")
def get_appointments():

    db = SessionLocal()

    appointments = db.query(
        Appointment
    ).all()

    return appointments

# ===================================
# DELETE APPOINTMENT
# ===================================

@app.delete("/delete-appointment/{appointment_id}")
def delete_appointment(appointment_id: int):

    db = SessionLocal()

    appointment = db.query(
        Appointment
    ).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:

        return {
            "message": "Appointment Not Found"
        }

    db.delete(appointment)

    db.commit()

    return {
        "message": "Appointment Deleted Successfully"
    }

# ===================================
# FREE AI MODEL
# ===================================

chatbot = pipeline(
    "text-generation",
    model="distilgpt2"
)
# ===================================
# AI CHAT
# ===================================

@app.post("/ai-chat")
def ai_chat(message: str):

    msg = message.lower()

    # Fever
    if "fever" in msg:
        reply = """
Possible fever detected.

• Drink plenty of water
• Take proper rest
• Use paracetamol if needed
• Consult a doctor if fever is high
"""

    # Cold
    elif "cold" in msg or "cough" in msg:
        reply = """
Cold/Cough symptoms detected.

• Drink warm water
• Avoid cold drinks
• Take steam regularly
• Consult doctor if symptoms increase
"""

    # Headache
    elif "headache" in msg:
        reply = """
Headache detected.

• Rest properly
• Drink enough water
• Avoid stress
• Consult doctor if pain continues
"""

    # Stomach Pain
    elif "stomach" in msg:
        reply = """
Stomach issue detected.

• Eat light food
• Stay hydrated
• Avoid spicy food
• Visit doctor if pain becomes severe
"""

    # Default
    else:
        reply = """
Please describe symptoms clearly.

Example:
• Fever
• Headache
• Cold
• Cough
• Weakness
"""

    return {
        "response": reply
    }
        
# ===================================
# TWILIO SETUP
# ===================================

client_twilio = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

# ===================================
# CALL PATIENT
# ===================================

@app.post("/call-patient")
def call_patient(phone: str):

    try:

        call = client_twilio.calls.create(
            to=phone,

            from_=os.getenv(
                "TWILIO_PHONE"
            ),

            url="http://demo.twilio.com/docs/voice.xml"
        )

        return {
            "message": "Calling Patient",
            "call_sid": call.sid
        }

    except Exception as e:

        return {
            "message": str(e)
        }

# ===================================
# VOICE RESPONSE
# ===================================

@app.post("/voice")
def voice():

    xml = '''
    <Response>
        <Say>
        Namaste! Your appointment is tomorrow.
        Please visit clinic on time.
        Thank you.
        </Say>
    </Response>
    '''

    return Response(
        content=xml,
        media_type="application/xml"
    )