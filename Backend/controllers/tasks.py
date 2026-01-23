from Backend.controllers.celery_app import celery_app
from Backend.controllers.database import db
from Backend.controllers.models import Appointment, User, Treatment, DoctorProfile
from datetime import date, datetime, timedelta
import csv
import os

# ============================================================================
# Celery Tasks
# ============================================================================

@celery_app.task
def export_patient_treatments_csv(patient_id):
    """
    User-triggered async job that exports all treatment details for a patient.
    Creates a CSV file with treatment history.
    """
    patient = User.query.get(patient_id)
    if not patient or patient.role != "patient":
        return {"status": "error", "message": "Patient not found"}
    
    # Get all completed appointments with treatments
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        status="COMPLETED"
    ).order_by(Appointment.appointment_date.desc()).all()
    
    # Create exports directory if it doesn't exist
    export_dir = os.path.join(os.getcwd(), "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"treatment_history_{patient.username}_{timestamp}.csv"
    csv_path = os.path.join(export_dir, csv_filename)
    
    # Write CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header row
        writer.writerow([
            "User ID",
            "Username", 
            "Consulting Doctor",
            "Doctor Specialization",
            "Appointment Date",
            "Appointment Time",
            "Diagnosis",
            "Treatment/Prescription",
            "Notes"
        ])
        
        # Data rows
        for appointment in appointments:
            doctor = User.query.get(appointment.doctor_id)
            doctor_profile = DoctorProfile.query.filter_by(user_id=appointment.doctor_id).first() if doctor else None
            treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
            
            writer.writerow([
                patient.id,
                patient.username,
                doctor.username if doctor else "Unknown",
                doctor_profile.specialization if doctor_profile else "N/A",
                str(appointment.appointment_date),
                str(appointment.appointment_time) if appointment.appointment_time else "N/A",
                treatment.diagnosis if treatment else "N/A",
                treatment.prescription if treatment else "N/A",
                treatment.notes if treatment else "N/A"
            ])
    
    return {
        "status": "completed",
        "file_path": csv_path,
        "filename": csv_filename,
        "total_records": len(appointments)
    }
