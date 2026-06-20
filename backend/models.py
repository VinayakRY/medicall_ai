from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from database import Base

# Patient Table
class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100)
    )

    phone = Column(
        String(20)
    )

    language = Column(
        String(20)
    )

# Appointment Table
class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )

    doctor_name = Column(
        String(100)
    )

    appointment_date = Column(
        DateTime
    )

    status = Column(
        String(50)
    )