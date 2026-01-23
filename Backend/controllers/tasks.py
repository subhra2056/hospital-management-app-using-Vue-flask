from Backend.controllers.celery_app import celery_app
from Backend.controllers.database import db
from Backend.controllers.models import Appointment, User, Treatment
from datetime import date, datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import os

@celery_app.task
def send_daily_reminders():
    today = date.today()
    appointments = Appointment.query.filter_by(
        appointment_date=today,
        status="BOOKED"
    ).all()
    
    for appointment in appointments:
        patient = User.query.get(appointment.patient_id)
        doctor = User.query.get(appointment.doctor_id)
        
        if patient and patient.email:
            message = f"Reminder: You have an appointment with Dr. {doctor.username if doctor else 'Unknown'} today at {appointment.appointment_time}. Please arrive on time."
            
            try:
                send_email(patient.email, "Appointment Reminder", message)
            except Exception as e:
                print(f"Failed to send reminder to {patient.email}: {e}")
    
    return f"Sent {len(appointments)} reminders"

@celery_app.task
def send_monthly_reports():
    today = date.today()
    if today.day != 1:
        return "Not the first day of the month"
    
    last_month = today.replace(day=1) - timedelta(days=1)
    month_start = last_month.replace(day=1)
    
    doctors = User.query.filter_by(role="doctor").all()
    
    for doctor in doctors:
        appointments = Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_date >= month_start,
            Appointment.appointment_date <= last_month,
            Appointment.status == "COMPLETED"
        ).all()
        
        if appointments:
            report_html = generate_monthly_report(doctor, appointments, last_month)
            
            if doctor.email:
                try:
                    send_email(doctor.email, f"Monthly Activity Report - {last_month.strftime('%B %Y')}", report_html, html=True)
                except Exception as e:
                    print(f"Failed to send report to {doctor.email}: {e}")
    
    return "Monthly reports sent"

@celery_app.task
def export_patient_treatments_csv(patient_id):
    patient = User.query.get(patient_id)
    if not patient or patient.role != "patient":
        return "Patient not found"
    
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        status="COMPLETED"
    ).order_by(Appointment.appointment_date.desc()).all()
    
    csv_filename = f"patient_{patient_id}_treatments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_path = os.path.join("exports", csv_filename)
    
    os.makedirs("exports", exist_ok=True)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "User ID", "Username", "Consulting Doctor", "Appointment Date",
            "Diagnosis", "Treatment", "Next Visit"
        ])
        
        for appointment in appointments:
            doctor = User.query.get(appointment.doctor_id)
            treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
            
            writer.writerow([
                patient.id,
                patient.username,
                doctor.username if doctor else "Unknown",
                str(appointment.appointment_date),
                treatment.diagnosis if treatment else "N/A",
                treatment.prescription if treatment else "N/A",
                str(treatment.next_visit) if treatment and treatment.next_visit else "N/A"
            ])
    
    if patient.email:
        try:
            send_email_with_attachment(patient.email, "Your Treatment History Export", 
                                     "Please find your treatment history attached.", csv_path)
        except Exception as e:
            print(f"Failed to send CSV to {patient.email}: {e}")
    
    return csv_path

def send_email(to_email, subject, body, html=False):
    from_email = os.getenv("SMTP_EMAIL", "hospital@example.com")
    password = os.getenv("SMTP_PASSWORD", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    if not password:
        print("SMTP credentials not configured. Skipping email.")
        return
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    if html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Email sending failed: {e}")

def send_email_with_attachment(to_email, subject, body, attachment_path):
    from_email = os.getenv("SMTP_EMAIL", "hospital@example.com")
    password = os.getenv("SMTP_PASSWORD", "")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    if not password:
        print("SMTP credentials not configured. Skipping email.")
        return
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        msg.attach(part)
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(f"Email sending failed: {e}")

def generate_monthly_report(doctor, appointments, month_date):
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            h1 {{ color: #5e63b6; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #5e63b6; color: white; }}
        </style>
    </head>
    <body>
        <h1>Monthly Activity Report - {month_date.strftime('%B %Y')}</h1>
        <p>Dear Dr. {doctor.username},</p>
        <p>Here is your activity report for {month_date.strftime('%B %Y')}:</p>
        
        <h2>Summary</h2>
        <ul>
            <li>Total Appointments: {len(appointments)}</li>
        </ul>
        
        <h2>Appointment Details</h2>
        <table>
            <tr>
                <th>Date</th>
                <th>Patient</th>
                <th>Diagnosis</th>
                <th>Treatment</th>
            </tr>
    """
    
    for appointment in appointments:
        patient = User.query.get(appointment.patient_id)
        treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
        
        html += f"""
            <tr>
                <td>{appointment.appointment_date}</td>
                <td>{patient.username if patient else 'Unknown'}</td>
                <td>{treatment.diagnosis if treatment else 'N/A'}</td>
                <td>{treatment.prescription if treatment else 'N/A'}</td>
            </tr>
        """
    
    html += """
        </table>
        <p>Thank you for your dedication to patient care.</p>
    </body>
    </html>
    """
    
    return html
