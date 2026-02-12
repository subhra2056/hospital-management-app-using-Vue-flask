from flask import Flask
from Backend.controllers.database import db
from Backend.controllers.config import config
from flask_jwt_extended import JWTManager
from flask_restful import Api
from werkzeug.security import generate_password_hash
from Backend.controllers.models import User, TokenBlocklist, Department
from flask_cors import CORS
from Backend.controllers.cleanup_tokens import delete_expired_tokens
import subprocess
import requests
import time
import sys

def start_ollama():
    """
    Start Ollama service if it's not already running
    """
    try:
        # Check if Ollama is already running
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            print("✓ Ollama is already running")
            return True
    except requests.exceptions.RequestException:
        pass
    
    # Try to start Ollama
    print("Starting Ollama service...")
    try:
        # Start Ollama in background
        if sys.platform == "win32":
            subprocess.Popen(
                ["ollama", "serve"],
                creationflags=subprocess.CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        # Wait for Ollama to start
        for i in range(10):
            time.sleep(1)
            try:
                response = requests.get("http://localhost:11434/api/version", timeout=2)
                if response.status_code == 200:
                    print("✓ Ollama started successfully")
                    return True
            except requests.exceptions.RequestException:
                continue
        
        print("⚠ Warning: Ollama may not have started properly")
        return False
    except FileNotFoundError:
        print("⚠ Warning: Ollama is not installed. Chatbot AI features will not work.")
        print("   Download from: https://ollama.com/download")
        return False
    except Exception as e:
        print(f"⚠ Warning: Failed to start Ollama: {e}")
        return False

def create_app():

    app = Flask(__name__)
    app.config.from_object(config) #Takes all the configuration values from config.py and loads them into Flask App

    api = Api(app, prefix="/api")

    db.init_app(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return TokenBlocklist.query.filter_by(
            jti=jwt_payload["jti"]
        ).first() is not None

    with app.app_context():
        db.create_all()
        delete_expired_tokens()

        admin = User.query.filter_by(role="admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@gmail.com",
                password=generate_password_hash("password123"),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()

            print('Admin profile created successfully!')

        # Create default departments if they don't exist
        departments = [
            {"name": "Cardiology", "description": "Heart and cardiovascular system"},
            {"name": "Neurology", "description": "Brain and nervous system"},
            {"name": "Orthopedics", "description": "Bones, joints, and muscles"},
            {"name": "Pediatrics", "description": "Children's health"},
            {"name": "Dermatology", "description": "Skin conditions"},
        ]

        for dept_data in departments:
            dept = Department.query.filter_by(name=dept_data["name"]).first()
            if not dept:
                dept = Department(
                    name=dept_data["name"],
                    description=dept_data["description"]
                )
                db.session.add(dept)

        db.session.commit()

    return app, api

app, api = create_app()
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"], supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

from Backend.controllers.routes import (
    LoginAPI,
    LogoutAPI,
    PatientRegisterAPI,
    DoctorRegistration,
    DoctorCount,
    PatientCount,
    DoctorList,
    PatientList,
    BookAppointmentAPI,
    CancelAppointmentAPI,
    DoctorAvailabilityAPI,
    PatientAppointmentsAPI,
    DoctorAppointmentsAPI,
    AddTreatmentAPI,
    SearchDoctorsAPI,
    SearchPatientsAPI,
    AllAppointmentsAPI,
    AppointmentCountAPI,
    UpdatePatientProfileAPI,
    DeleteUserAPI,
    ExportPatientTreatmentsAPI,
    GetUserProfileAPI,
    DepartmentAPI,
    UpdateDoctorAPI,
    UpdatePatientAPI,
    BlockUserAPI,
    UnblockUserAPI,
    HomeStatsAPI,
    PublicDepartmentsAPI
)

# Import new modular chatbot routes
from Backend.controllers.chatbot_routes.patient_chatbot import PatientChatbotAPI as ChatbotAPI
from Backend.controllers.chatbot_routes.doctor_chatbot import DoctorChatbotAPI

api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(PatientRegisterAPI, '/patient/register')
api.add_resource(DoctorRegistration, '/doctor/register')
api.add_resource(DoctorCount, "/admin/doctors/count")
api.add_resource(PatientCount, "/admin/patients/count")
api.add_resource(DoctorList, "/admin/doctor-list")
api.add_resource(PatientList, "/admin/patient-list")
api.add_resource(BookAppointmentAPI, '/patient/appointments/book')
api.add_resource(CancelAppointmentAPI, '/appointments/<int:appointment_id>/cancel')
api.add_resource(DoctorAvailabilityAPI, '/doctor/availability', '/doctor/availability/edit/<int:availability_id>', '/public/doctor/<int:doctor_id>/availability')
api.add_resource(PatientAppointmentsAPI, '/patient/appointments')
api.add_resource(DoctorAppointmentsAPI, '/doctor/appointments')
api.add_resource(AddTreatmentAPI, '/doctor/appointments/<int:appointment_id>/treatment')
api.add_resource(SearchDoctorsAPI, '/search/doctors')
api.add_resource(SearchPatientsAPI, '/admin/search/patients')
api.add_resource(AllAppointmentsAPI, '/admin/appointments')
api.add_resource(AppointmentCountAPI, '/admin/appointments/count')
api.add_resource(UpdatePatientProfileAPI, '/patient/profile')
api.add_resource(DeleteUserAPI, '/admin/users/<int:user_id>')
api.add_resource(ExportPatientTreatmentsAPI, '/patient/export-treatments')
api.add_resource(GetUserProfileAPI, '/user/profile')
api.add_resource(DepartmentAPI, '/admin/departments', '/admin/departments/<int:department_id>')
api.add_resource(UpdateDoctorAPI, '/admin/doctors/<int:user_id>')
api.add_resource(UpdatePatientAPI, '/admin/patients/<int:user_id>')
api.add_resource(BlockUserAPI, '/admin/users/<int:user_id>/block')
api.add_resource(UnblockUserAPI, '/admin/users/<int:user_id>/unblock')
api.add_resource(HomeStatsAPI, '/home/stats')
api.add_resource(PublicDepartmentsAPI, '/departments')
api.add_resource(ChatbotAPI, '/chatbot/query')
api.add_resource(DoctorChatbotAPI, '/doctor/chatbot')

if __name__ == "__main__":
    # Start Ollama before running Flask
    start_ollama()
    app.run(host="localhost", debug = True)
