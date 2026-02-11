from datetime import datetime
from Backend.controllers.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor_profile = db.relationship("DoctorProfile", back_populates="user", uselist=False)
    patient_profile = db.relationship("PatientProfile", back_populates="user", uselist=False)


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DoctorProfile(db.Model):
    __tablename__ = "doctor_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    experience_years = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    user = db.relationship("User", back_populates="doctor_profile")
    department_ref = db.relationship("Department", back_populates="doctors")
    availabilities = db.relationship("DoctorAvailability", back_populates="doctor", cascade="all, delete")


class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availability"
    __table_args__ = (
        db.UniqueConstraint('doctor_profile_id', 'date', 'start_time', 'end_time', name='unique_availability_slot'),
    )

    id = db.Column(db.Integer, primary_key=True)
    doctor_profile_id = db.Column(db.Integer, db.ForeignKey("doctor_profiles.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)

    doctor = db.relationship("DoctorProfile", back_populates="availabilities")


class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    user = db.relationship("User", back_populates="patient_profile")


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default="BOOKED")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("User", foreign_keys=[patient_id])
    doctor = db.relationship("User", foreign_keys=[doctor_id])
    treatment = db.relationship("Treatment", back_populates="appointment", uselist=False, cascade="all, delete")


class Treatment(db.Model):
    __tablename__ = "treatments"

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), unique=True, nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    next_visit = db.Column(db.Date)
    treatment_cost = db.Column(db.Float, default=0.0)

    appointment = db.relationship("Appointment", back_populates="treatment")

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    doctors_registered = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with doctors
    doctors = db.relationship("DoctorProfile", back_populates="department_ref", cascade="all, delete")
