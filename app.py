from flask import Flask
from Backend.controllers.database import db
from Backend.controllers.config import config
from flask_jwt_extended import JWTManager
from flask_restful import Api
from werkzeug.security import generate_password_hash
from Backend.controllers.models import User, TokenBlocklist, Department
from flask_cors import CORS
from Backend.controllers.cleanup_tokens import delete_expired_tokens

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
        print('Default departments created successfully!')

    return app, api

app, api = create_app()
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"], supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

#==================================================
#auth.py
#==================================================

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
    PaymentAPI,
    UpdateDoctorAPI,
    UpdatePatientAPI,
    BlockUserAPI,
    UnblockUserAPI,
    HomeStatsAPI,
    PublicDepartmentsAPI
)

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
api.add_resource(PaymentAPI, '/patient/payments/<int:treatment_id>')
api.add_resource(UpdateDoctorAPI, '/admin/doctors/<int:user_id>')
api.add_resource(UpdatePatientAPI, '/admin/patients/<int:user_id>')
api.add_resource(BlockUserAPI, '/admin/users/<int:user_id>/block')
api.add_resource(UnblockUserAPI, '/admin/users/<int:user_id>/unblock')
api.add_resource(HomeStatsAPI, '/home/stats')
api.add_resource(PublicDepartmentsAPI, '/departments')

if __name__ == "__main__":
    app.run(host="localhost", debug = True)