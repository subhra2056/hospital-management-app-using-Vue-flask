from flask_restful import Resource
from flask import jsonify, make_response, request
from .models import User, PatientProfile, TokenBlocklist, DoctorProfile, Appointment, Treatment, Payment, Department, DoctorAvailability
from flask_jwt_extended import jwt_required, get_jwt, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from .database import db
from datetime import datetime, date, time, timedelta
from sqlalchemy import and_, or_

#==============================================================================
#Login 
#==============================================================================

class LoginAPI(Resource):

    def post(self):

        login_credentials = request.get_json()

        if not login_credentials:
            return make_response(
                jsonify({"message" : "Login details are required"}),
                400
            )
        
        email = login_credentials.get("email", None)
        password = login_credentials.get("password", None)

        if not email or not password:
            return make_response(
                jsonify({"message" : "Invalid email or password"}),
                400
            )
        
        user = User.query.filter_by(email = email).first()

        if not user or not check_password_hash(user.password, password):
            return make_response(
                jsonify({"message" : "Invalid email or password"}),
                401
            )

        if not user.active:
            return make_response(
                jsonify({"message": "Account is blocked. Contact admin.", "blocked": True}),
                403
            )

        access_token = create_access_token(identity=str(user.id))

        return make_response(
            jsonify({
                "message" : "Login successful",
                "user_details" : {
                    "email" : user.email,
                    "role" : user.role,
                    "active": user.active
                },
                "access_token" : access_token
            }),
            200
        )

#==============================================================================
#Patient Create Account
#==============================================================================
    

class PatientRegisterAPI(Resource):

    def post(self):

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({"message": "Registration details are required"}),
                400
            )

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        age = data.get("age")
        gender = data.get("gender")
        phone = data.get("phone")
        address = data.get("address")

        if not email or not password:
            return make_response(
                jsonify({"message": "Email and password are required"}),
                400
            )

        if not age or not gender or not phone:
            return make_response(
                jsonify({"message": "Age, gender and phone are required"}),
                400
            )

        if User.query.filter_by(email=email).first():
            return make_response(
                jsonify({"message": "User already exists"}),
                409
            )

        if (len(phone) > 15 or len(phone) < 10):
            return make_response(
                jsonify({"message": "Invalid phone number"}),
                400
            )

        try:
            user = User(
                username=username,   
                email=email,
                password=generate_password_hash(password),
                role="patient",
                active=True
            )

            db.session.add(user)
            db.session.flush() 

            patient_profile = PatientProfile(
                user_id=user.id,
                age=age,
                gender=gender,
                phone=phone,
                address=address
            )

            db.session.add(patient_profile)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": "Registration failed"}),
                500
            )

        return make_response(
            jsonify({
                "message": "Patient registered successfully",
                "user": {
                    "name": user.username,
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                },
                "patient_profile": {
                    "age": patient_profile.age,
                    "gender": patient_profile.gender,
                    "phone": patient_profile.phone,
                    "address": patient_profile.address
                }
            }),
            201
        )
    
#==============================================================================
#Logout
#==============================================================================

class LogoutAPI(Resource):

    @jwt_required()
    def post(self):

        jwt_payload = get_jwt()
        jti = jwt_payload["jti"]


        blocked_token = TokenBlocklist(jti=jti)
        db.session.add(blocked_token)
        db.session.commit()

        return make_response(
            jsonify({"message": "Logged out successfully"}),
            200
        )
    

#==============================================================================
#Doctor registration
#==============================================================================

class DoctorRegistration(Resource):

    @jwt_required()
    def post(self):

        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)

        data = request.get_json()

        if not data:
            return make_response(
                jsonify({"message": "Registration details are required"}),
                400
            )

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        department_id = data.get("department_id")
        specialization = data.get("specialization")
        experience_years = data.get("experience_years")
        gender = data.get("gender")

        if not email or not password or not username or not department_id:
            return make_response(
                jsonify({"message": "Username, email, password and department_id are required"}),
                400
            )

        # Validate department exists
        department = Department.query.get(department_id)
        if not department:
            return make_response(
                jsonify({"message": "Invalid department_id"}),
                400
            )

        try:
            experience_years = int(experience_years)
        except (ValueError, TypeError):
            return make_response(
                jsonify({"message": "experience_years must be a valid number"}),
                400
            )

        if experience_years < 0:
            return make_response(
                jsonify({"message": "experience_years cannot be negative"}),
                400
            )

        if User.query.filter_by(email=email).first():
            return make_response(
                jsonify({"message": "User already exists"}),
                409
            )

        try:
            user = User(
                username=username,   
                email=email,
                password=generate_password_hash(password),
                role="doctor",
                active=True
            )

            db.session.add(user)
            db.session.flush() 

            doctor_profile = DoctorProfile(
                user_id=user.id,
                department_id = department_id,
                specialization = specialization,
                experience_years = experience_years,
                gender = gender
            )

            db.session.add(doctor_profile)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": "Registration failed"}),
                500
            )

        return make_response(
            jsonify({
                "message": "Doctor registered successfully",
                "user": {
                    "name": user.username,
                    "id": user.id,
                    "email": user.email,
                    "role": user.role
                },
                "doctor_profile": {
                    "department_id": doctor_profile.department_id,
                    "department_name": department.name,
                    "specialization": doctor_profile.specialization,
                    "experience_years": doctor_profile.experience_years,
                    "gender": doctor_profile.gender,
                }
            }),
            201
        )

#==============================================================================
#Doctor Count
#==============================================================================
    
class DoctorCount(Resource):

    @jwt_required()
    def get(self):
        count = User.query.filter_by(role="doctor").count()
        return {"total_doctors": count}, 200
    
#==============================================================================
#Patient Count
#==============================================================================
    
class PatientCount(Resource):

    @jwt_required()
    def get(self):
        count = User.query.filter_by(role="patient").count()
        return {"total_patients": count}, 200

#==============================================================================
#Doctor List
#==============================================================================

class DoctorList(Resource):
    def get(self):
        doctors = (
            db.session.query(User)
            .join(DoctorProfile)
            .join(Department, DoctorProfile.department_id == Department.id)
            .filter(User.role == "doctor")
            .all()
        )

        result = []

        for user in doctors:
            profile = user.doctor_profile

            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "department_id": profile.department_id,
                "department_name": profile.department_ref.name,
                "specialization": profile.specialization,
                "experience_years": profile.experience_years,
                "gender": profile.gender,
                "active": user.active
            })

        return {"doctors": result}, 200
    
#==============================================================================
#Patient List
#==============================================================================
    
class PatientList(Resource):
    def get(self):
        patients = (
            db.session.query(User)
            .join(PatientProfile)
            .filter(User.role == "patient")
            .all()
        )

        result = []

        for user in patients:
            profile = user.patient_profile

            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "age": profile.age,
                "gender": profile.gender,
                "phone": profile.phone,
                "address": profile.address,
                "active": user.active
            })

        return {"patients": result}, 200

#==============================================================================
#Appointment Booking
#==============================================================================

class BookAppointmentAPI(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        patient_id = int(get_jwt_identity())
        
        doctor_id = data.get("doctor_id")
        appointment_date = data.get("appointment_date")
        appointment_time = data.get("appointment_time")
        
        if not all([doctor_id, appointment_date, appointment_time]):
            return make_response(jsonify({"message": "All fields are required"}), 400)
        
        try:
            appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            appointment_time = datetime.strptime(appointment_time, "%H:%M").time()
        except ValueError:
            return make_response(jsonify({"message": "Invalid date or time format"}), 400)
        
        # Check if this slot is already booked by anyone
        existing_slot = Appointment.query.filter_by(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status="BOOKED"
        ).first()
        
        if existing_slot:
            return make_response(jsonify({"message": "This time slot is already booked"}), 409)
        
        # Check if this patient already has a booking with this doctor on the same date
        patient_existing = Appointment.query.filter_by(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            status="BOOKED"
        ).first()
        
        if patient_existing:
            return make_response(jsonify({"message": "You already have an appointment with this doctor on this date"}), 409)
        
        # Find and mark the availability slot as booked
        doctor_profile = DoctorProfile.query.filter_by(user_id=doctor_id).first()
        if doctor_profile:
            availability_slot = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id,
                date=appointment_date,
                start_time=appointment_time,
                is_booked=False
            ).first()
            if availability_slot:
                availability_slot.is_booked = True
        
        appointment = Appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status="BOOKED"
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        return make_response(jsonify({
            "message": "Appointment booked successfully",
            "appointment_id": appointment.id
        }), 201)

#==============================================================================
#Cancel Appointment
#==============================================================================

class CancelAppointmentAPI(Resource):
    @jwt_required()
    def post(self, appointment_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return make_response(jsonify({"message": "Appointment not found"}), 404)
        
        if user.role == "patient" and appointment.patient_id != user_id:
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        if user.role == "doctor" and appointment.doctor_id != user_id:
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        appointment.status = "CANCELLED"
        db.session.commit()
        
        return make_response(jsonify({"message": "Appointment cancelled successfully"}), 200)

#==============================================================================
#Doctor Availability
#==============================================================================

class DoctorAvailabilityAPI(Resource):
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "doctor":
            return make_response(jsonify({"message": "Only doctors can set availability"}), 403)
        
        doctor_profile = DoctorProfile.query.filter_by(user_id=user_id).first()
        if not doctor_profile:
            return make_response(jsonify({"message": "Doctor profile not found"}), 404)
        
        data = request.get_json()
        date_str = data.get("date")
        start_time_str = data.get("start_time")
        end_time_str = data.get("end_time")
        
        if not all([date_str, start_time_str, end_time_str]):
            return make_response(jsonify({"message": "All fields required"}), 400)
        
        try:
            avail_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return make_response(jsonify({"message": "Invalid date or time format"}), 400)
        
        if avail_date < date.today():
            return make_response(jsonify({"message": "Cannot set availability for past dates"}), 400)
        
        availability = DoctorAvailability(
            doctor_profile_id=doctor_profile.id,
            date=avail_date,
            start_time=start_time,
            end_time=end_time,
            is_booked=False
        )
        
        db.session.add(availability)
        db.session.commit()
        
        return make_response(jsonify({"message": "Availability added successfully"}), 201)
    
    @jwt_required()
    def get(self, doctor_id=None):
        if doctor_id:
            doctor_profile = DoctorProfile.query.filter_by(user_id=doctor_id).first()
            if not doctor_profile:
                return make_response(jsonify({"message": "Doctor not found"}), 404)
            
            availabilities = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id,
                is_booked=False
            ).filter(DoctorAvailability.date >= date.today()).all()
        else:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            
            if user.role != "doctor":
                return make_response(jsonify({"message": "Unauthorized"}), 403)
            
            doctor_profile = DoctorProfile.query.filter_by(user_id=user_id).first()
            if not doctor_profile:
                return make_response(jsonify({"message": "Doctor profile not found"}), 404)
            
            availabilities = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id
            ).filter(DoctorAvailability.date >= date.today()).all()
        
        result = []
        for avail in availabilities:
            result.append({
                "id": avail.id,
                "date": str(avail.date),
                "start_time": str(avail.start_time),
                "end_time": str(avail.end_time),
                "is_booked": avail.is_booked
            })
        
        return make_response(jsonify({"availabilities": result}), 200)
    
    @jwt_required()
    def put(self, availability_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "doctor":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        doctor_profile = DoctorProfile.query.filter_by(user_id=user_id).first()
        if not doctor_profile:
            return make_response(jsonify({"message": "Doctor profile not found"}), 404)
        
        availability = DoctorAvailability.query.filter_by(
            id=availability_id,
            doctor_profile_id=doctor_profile.id
        ).first()
        
        if not availability:
            return make_response(jsonify({"message": "Availability not found"}), 404)
        
        if availability.is_booked:
            return make_response(jsonify({"message": "Cannot edit booked availability"}), 400)
        
        data = request.get_json()
        date_str = data.get("date")
        start_time_str = data.get("start_time")
        end_time_str = data.get("end_time")
        
        if not all([date_str, start_time_str, end_time_str]):
            return make_response(jsonify({"message": "All fields required"}), 400)
        
        try:
            avail_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return make_response(jsonify({"message": "Invalid date or time format"}), 400)
        
        if avail_date < date.today():
            return make_response(jsonify({"message": "Cannot set availability for past dates"}), 400)
        
        availability.date = avail_date
        availability.start_time = start_time
        availability.end_time = end_time
        
        db.session.commit()
        
        return make_response(jsonify({"message": "Availability updated successfully"}), 200)
    
    @jwt_required()
    def delete(self, availability_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "doctor":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        doctor_profile = DoctorProfile.query.filter_by(user_id=user_id).first()
        if not doctor_profile:
            return make_response(jsonify({"message": "Doctor profile not found"}), 404)
        
        availability = DoctorAvailability.query.filter_by(
            id=availability_id,
            doctor_profile_id=doctor_profile.id
        ).first()
        
        if not availability:
            return make_response(jsonify({"message": "Availability not found"}), 404)
        
        if availability.is_booked:
            return make_response(jsonify({"message": "Cannot delete booked availability"}), 400)
        
        db.session.delete(availability)
        db.session.commit()
        
        return make_response(jsonify({"message": "Availability deleted successfully"}), 200)

#==============================================================================
#Patient Appointments
#==============================================================================

class PatientAppointmentsAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "patient":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        appointments = Appointment.query.filter_by(patient_id=user_id).order_by(
            Appointment.appointment_date.desc(),
            Appointment.appointment_time.desc()
        ).all()
        
        result = []
        for apt in appointments:
            doctor = User.query.get(apt.doctor_id)
            doctor_profile = doctor.doctor_profile if doctor else None
            
            appointment_data = {
                "id": apt.id,
                "doctor_name": doctor.username if doctor else "Unknown",
                "doctor_specialization": doctor_profile.specialization if doctor_profile else "N/A",
                "appointment_date": str(apt.appointment_date),
                "appointment_time": str(apt.appointment_time),
                "status": apt.status,
                "created_at": str(apt.created_at)
            }
            
            if apt.treatment:
                appointment_data["treatment"] = {
                    "diagnosis": apt.treatment.diagnosis,
                    "prescription": apt.treatment.prescription,
                    "notes": apt.treatment.notes,
                    "next_visit": str(apt.treatment.next_visit) if apt.treatment.next_visit else None
                }
            
            result.append(appointment_data)
        
        return make_response(jsonify({"appointments": result}), 200)

#==============================================================================
#Doctor Appointments
#==============================================================================

class DoctorAppointmentsAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "doctor":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        appointments = Appointment.query.filter_by(doctor_id=user_id).order_by(
            Appointment.appointment_date.asc(),
            Appointment.appointment_time.asc()
        ).all()
        
        result = []
        for apt in appointments:
            patient = User.query.get(apt.patient_id)
            patient_profile = patient.patient_profile if patient else None
            
            appointment_data = {
                "id": apt.id,
                "patient_name": patient.username if patient else "Unknown",
                "patient_email": patient.email if patient else "N/A",
                "patient_phone": patient_profile.phone if patient_profile else "N/A",
                "appointment_date": str(apt.appointment_date),
                "appointment_time": str(apt.appointment_time),
                "status": apt.status,
                "created_at": str(apt.created_at)
            }
            
            if apt.treatment:
                appointment_data["treatment"] = {
                    "diagnosis": apt.treatment.diagnosis,
                    "prescription": apt.treatment.prescription,
                    "notes": apt.treatment.notes,
                    "next_visit": str(apt.treatment.next_visit) if apt.treatment.next_visit else None
                }
            
            result.append(appointment_data)
        
        return make_response(jsonify({"appointments": result}), 200)

#==============================================================================
#Add Treatment
#==============================================================================

class AddTreatmentAPI(Resource):
    @jwt_required()
    def post(self, appointment_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "doctor":
            return make_response(jsonify({"message": "Only doctors can add treatments"}), 403)
        
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return make_response(jsonify({"message": "Appointment not found"}), 404)
        
        if appointment.doctor_id != user_id:
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        data = request.get_json()
        diagnosis = data.get("diagnosis")
        prescription = data.get("prescription")
        notes = data.get("notes")
        next_visit_str = data.get("next_visit")
        
        if not diagnosis:
            return make_response(jsonify({"message": "Diagnosis is required"}), 400)
        
        next_visit = None
        if next_visit_str:
            try:
                next_visit = datetime.strptime(next_visit_str, "%Y-%m-%d").date()
            except ValueError:
                return make_response(jsonify({"message": "Invalid date format"}), 400)
        
        treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
        
        if treatment:
            treatment.diagnosis = diagnosis
            treatment.prescription = prescription
            treatment.notes = notes
            treatment.next_visit = next_visit
        else:
            treatment = Treatment(
                appointment_id=appointment_id,
                diagnosis=diagnosis,
                prescription=prescription,
                notes=notes,
                next_visit=next_visit
            )
            db.session.add(treatment)
        
        appointment.status = "COMPLETED"
        
        # Delete the availability slot that was used for this appointment
        doctor_profile = DoctorProfile.query.filter_by(user_id=user_id).first()
        if doctor_profile:
            availability_slot = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id,
                date=appointment.appointment_date,
                start_time=appointment.appointment_time,
                is_booked=True
            ).first()
            if availability_slot:
                db.session.delete(availability_slot)
        
        db.session.commit()
        
        return make_response(jsonify({"message": "Treatment added successfully"}), 201)

#==============================================================================
#Search Doctors
#==============================================================================

class SearchDoctorsAPI(Resource):
    def get(self):
        specialization = request.args.get("specialization")
        name = request.args.get("name")
        
        query = db.session.query(User).join(DoctorProfile).join(Department, DoctorProfile.department_id == Department.id).filter(User.role == "doctor")
        
        if specialization:
            query = query.filter(DoctorProfile.specialization.ilike(f"%{specialization}%"))
        
        if name:
            query = query.filter(User.username.ilike(f"%{name}%"))
        
        doctors = query.all()
        
        result = []
        for user in doctors:
            profile = user.doctor_profile
            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "department_id": profile.department_id,
                "department_name": profile.department_ref.name,
                "specialization": profile.specialization,
                "experience_years": profile.experience_years,
                "gender": profile.gender
            })
        
        return make_response(jsonify({"doctors": result}), 200)

#==============================================================================
#Search Patients
#==============================================================================

class SearchPatientsAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        name = request.args.get("name")
        patient_id = request.args.get("id")
        phone = request.args.get("phone")
        
        query = db.session.query(User).join(PatientProfile).filter(User.role == "patient")
        
        if name:
            query = query.filter(User.username.ilike(f"%{name}%"))
        
        if patient_id:
            query = query.filter(User.id == int(patient_id))
        
        if phone:
            query = query.filter(PatientProfile.phone.ilike(f"%{phone}%"))
        
        patients = query.all()
        
        result = []
        for user in patients:
            profile = user.patient_profile
            result.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "age": profile.age,
                "gender": profile.gender,
                "phone": profile.phone,
                "address": profile.address
            })
        
        return make_response(jsonify({"patients": result}), 200)

#==============================================================================
#All Appointments (Admin)
#==============================================================================

class AllAppointmentsAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        status = request.args.get("status")
        query = Appointment.query
        
        if status:
            query = query.filter_by(status=status.upper())
        
        appointments = query.order_by(
            Appointment.appointment_date.desc(),
            Appointment.appointment_time.desc()
        ).all()
        
        result = []
        for apt in appointments:
            patient = User.query.get(apt.patient_id)
            doctor = User.query.get(apt.doctor_id)
            doctor_profile = doctor.doctor_profile if doctor else None
            
            result.append({
                "id": apt.id,
                "patient_name": patient.username if patient else "Unknown",
                "patient_email": patient.email if patient else "N/A",
                "doctor_name": doctor.username if doctor else "Unknown",
                "doctor_specialization": doctor_profile.specialization if doctor_profile else "N/A",
                "appointment_date": str(apt.appointment_date),
                "appointment_time": str(apt.appointment_time),
                "status": apt.status,
                "created_at": str(apt.created_at)
            })
        
        return make_response(jsonify({"appointments": result}), 200)

#==============================================================================
#Appointment Count (Admin)
#==============================================================================

class AppointmentCountAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        total = Appointment.query.count()
        booked = Appointment.query.filter_by(status="BOOKED").count()
        completed = Appointment.query.filter_by(status="COMPLETED").count()
        cancelled = Appointment.query.filter_by(status="CANCELLED").count()
        
        return make_response(jsonify({
            "total_appointments": total,
            "booked": booked,
            "completed": completed,
            "cancelled": cancelled
        }), 200)

#==============================================================================
#Update Patient Profile
#==============================================================================

class UpdatePatientProfileAPI(Resource):
    @jwt_required()
    def put(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "patient":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        data = request.get_json()
        profile = user.patient_profile
        
        if not profile:
            return make_response(jsonify({"message": "Profile not found"}), 404)
        
        if "age" in data:
            profile.age = data["age"]
        if "gender" in data:
            profile.gender = data["gender"]
        if "phone" in data:
            profile.phone = data["phone"]
        if "address" in data:
            profile.address = data["address"]
        if "username" in data:
            user.username = data["username"]
        
        db.session.commit()
        
        return make_response(jsonify({"message": "Profile updated successfully"}), 200)

#==============================================================================
#Delete Doctor/Patient (Admin)
#==============================================================================

class DeleteUserAPI(Resource):
    @jwt_required()
    def delete(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return make_response(jsonify({"message": "Invalid token"}), 401)
        
        if current_user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        if user.role == "admin":
            return make_response(jsonify({"message": "Cannot delete admin"}), 400)
        
        user.active = False
        db.session.commit()
        
        return make_response(jsonify({"message": "User deactivated successfully"}), 200)

#==============================================================================
#Get User Profile
#==============================================================================

class GetUserProfileAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        profile_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "active": user.active,
            "created_at": str(user.created_at)
        }
        
        if user.role == "patient" and user.patient_profile:
            profile = user.patient_profile
            profile_data["profile"] = {
                "age": profile.age,
                "gender": profile.gender,
                "phone": profile.phone,
                "address": profile.address
            }
        
        if user.role == "doctor" and user.doctor_profile:
            profile = user.doctor_profile
            profile_data["profile"] = {
                "department": profile.department_ref.name if profile.department_ref else None,
                "specialization": profile.specialization,
                "experience_years": profile.experience_years,
                "gender": profile.gender
            }
        
        return make_response(jsonify(profile_data), 200)

    @jwt_required()
    def put(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        data = request.get_json()
        
        if user.role == "patient":
            if not user.patient_profile:
                # Create patient profile if it doesn't exist
                from Backend.controllers.models import PatientProfile
                user.patient_profile = PatientProfile(user_id=user.id)
                db.session.add(user.patient_profile)
            
            profile = user.patient_profile
            if "age" in data:
                profile.age = data["age"] if data["age"] else None
            if "gender" in data:
                profile.gender = data["gender"] if data["gender"] else None
            if "phone" in data:
                profile.phone = data["phone"] if data["phone"] else None
            if "address" in data:
                profile.address = data["address"] if data["address"] else None
                
        elif user.role == "doctor":
            if not user.doctor_profile:
                return make_response(jsonify({"message": "Doctor profile not found"}), 404)
            
            profile = user.doctor_profile
            if "specialization" in data:
                profile.specialization = data["specialization"] if data["specialization"] else None
            if "experience_years" in data:
                profile.experience_years = data["experience_years"] if data["experience_years"] else None
            if "gender" in data:
                profile.gender = data["gender"] if data["gender"] else None
        else:
            return make_response(jsonify({"message": "Profile update not supported for this role"}), 400)
        
        try:
            db.session.commit()
            return make_response(jsonify({"message": "Profile updated successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Failed to update profile"}), 500)

#==============================================================================
#Export Patient Treatments CSV
#==============================================================================

class ExportPatientTreatmentsAPI(Resource):
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "patient":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        from Backend.controllers.tasks import export_patient_treatments_csv
        
        task = export_patient_treatments_csv.delay(user_id)
        
        return make_response(jsonify({
            "message": "Export job started",
            "task_id": task.id
        }), 202)

#==============================================================================
# Department Management (Admin)
#==============================================================================

class DepartmentAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        departments = Department.query.all()
        result = []
        
        for dept in departments:
            result.append({
                "id": dept.id,
                "name": dept.name,
                "description": dept.description,
                "doctors_registered": dept.doctors_registered
            })
        
        return make_response(jsonify({"departments": result}), 200)
    
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        
        if not name:
            return make_response(jsonify({"message": "Department name is required"}), 400)
        
        if Department.query.filter_by(name=name).first():
            return make_response(jsonify({"message": "Department already exists"}), 409)
        
        department = Department(
            name=name,
            description=description,
            doctors_registered=0
        )
        
        db.session.add(department)
        db.session.commit()
        
        return make_response(jsonify({
            "message": "Department created successfully",
            "department": {
                "id": department.id,
                "name": department.name,
                "description": department.description
            }
        }), 201)
    
    @jwt_required()
    def delete(self, department_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        department = Department.query.get(department_id)
        if not department:
            return make_response(jsonify({"message": "Department not found"}), 404)
        
        # Check if department has doctors registered
        if department.doctors_registered > 0:
            return make_response(jsonify({"message": "Cannot delete department with registered doctors"}), 400)
        
        db.session.delete(department)
        db.session.commit()
        
        return make_response(jsonify({"message": "Department deleted successfully"}), 200)

#==============================================================================
# Payment API
#==============================================================================

class PaymentAPI(Resource):
    @jwt_required()
    def post(self, treatment_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if user.role != "patient":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        treatment = Treatment.query.filter_by(id=treatment_id, appointment__patient_id=user_id).first()
        if not treatment:
            return make_response(jsonify({"message": "Treatment not found"}), 404)
        
        data = request.get_json()
        amount = data.get("amount")
        payment_method = data.get("payment_method")
        card_number = data.get("card_number")
        expiry_date = data.get("expiry_date")
        cvv = data.get("cvv")
        
        if not all([amount, payment_method]):
            return make_response(jsonify({"message": "Amount and payment method are required"}), 400)
        
        # Generate a dummy transaction ID
        import uuid
        transaction_id = str(uuid.uuid4())[:8].upper()
        
        payment = Payment(
            treatment_id=treatment_id,
            patient_id=user_id,
            amount=float(amount),
            payment_method=payment_method,
            transaction_id=transaction_id,
            status="COMPLETED"  # Dummy payment always succeeds
        )
        
        db.session.add(payment)
        db.session.commit()
        
        return make_response(jsonify({
            "message": "Payment processed successfully",
            "payment": {
                "id": payment.id,
                "transaction_id": payment.transaction_id,
                "amount": payment.amount,
                "status": payment.status
            }
        }), 201)

#==============================================================================
#Update Doctor Profile
#==============================================================================

class UpdateDoctorAPI(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return make_response(jsonify({"message": "Invalid token"}), 401)
        
        if current_user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        user = User.query.get(user_id)
        if not user or user.role != "doctor":
            return make_response(jsonify({"message": "Doctor not found"}), 404)
        
        data = request.get_json()
        doctor_profile = user.doctor_profile
        if not doctor_profile:
            return make_response(jsonify({"message": "Doctor profile not found"}), 404)
        
        # Update user fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            if User.query.filter_by(email=data['email']).filter(User.id != user_id).first():
                return make_response(jsonify({"message": "Email already exists"}), 409)
            user.email = data['email']
        
        # Update doctor profile fields
        if 'department_id' in data:
            department = Department.query.get(data['department_id'])
            if not department:
                return make_response(jsonify({"message": "Invalid department_id"}), 400)
            doctor_profile.department_id = data['department_id']
        if 'specialization' in data:
            doctor_profile.specialization = data['specialization']
        if 'experience_years' in data:
            try:
                doctor_profile.experience_years = int(data['experience_years'])
            except (ValueError, TypeError):
                return make_response(jsonify({"message": "experience_years must be a number"}), 400)
        if 'gender' in data:
            doctor_profile.gender = data['gender']
        
        db.session.commit()
        
        return make_response(jsonify({"message": "Doctor updated successfully"}), 200)
    
    @jwt_required()
    def delete(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return make_response(jsonify({"message": "Invalid token"}), 401)
        
        if current_user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        user = User.query.get(user_id)
        if not user or user.role != "doctor":
            return make_response(jsonify({"message": "Doctor not found"}), 404)
        
        try:
            # Delete related payments, treatments, and appointments
            appointments = Appointment.query.filter_by(doctor_id=user_id).all()
            for appointment in appointments:
                # Delete payments for this appointment's treatment
                if appointment.treatment:
                    payments = Payment.query.filter_by(treatment_id=appointment.treatment.id).all()
                    for payment in payments:
                        db.session.delete(payment)
                db.session.delete(appointment)
            
            doctor_profile = user.doctor_profile
            if doctor_profile:
                # Delete availabilities (cascaded)
                db.session.delete(doctor_profile)
            
            db.session.delete(user)
            db.session.commit()
            
            return make_response(jsonify({"message": "Doctor deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Failed to delete doctor", "error": str(e)}), 500)

#==============================================================================
#Update Patient Profile
#==============================================================================

class UpdatePatientAPI(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return make_response(jsonify({"message": "Invalid token"}), 401)
        
        if current_user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        user = User.query.get(user_id)
        if not user or user.role != "patient":
            return make_response(jsonify({"message": "Patient not found"}), 404)
        
        data = request.get_json()
        patient_profile = user.patient_profile
        if not patient_profile:
            return make_response(jsonify({"message": "Patient profile not found"}), 404)
        
        # Update user fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            if User.query.filter_by(email=data['email']).filter(User.id != user_id).first():
                return make_response(jsonify({"message": "Email already exists"}), 409)
            user.email = data['email']
        
        # Update patient profile fields
        if 'age' in data:
            try:
                patient_profile.age = int(data['age'])
            except (ValueError, TypeError):
                return make_response(jsonify({"message": "age must be a number"}), 400)
        if 'gender' in data:
            patient_profile.gender = data['gender']
        if 'phone' in data:
            patient_profile.phone = data['phone']
        if 'address' in data:
            patient_profile.address = data['address']
        
        db.session.commit()
        
        return make_response(jsonify({"message": "Patient updated successfully"}), 200)
    
    @jwt_required()
    def delete(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return make_response(jsonify({"message": "Invalid token"}), 401)
        
        if current_user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        user = User.query.get(user_id)
        if not user or user.role != "patient":
            return make_response(jsonify({"message": "Patient not found"}), 404)
        
        try:
            # Delete related payments, treatments, and appointments
            appointments = Appointment.query.filter_by(patient_id=user_id).all()
            for appointment in appointments:
                # Delete payments for this appointment's treatment
                if appointment.treatment:
                    payments = Payment.query.filter_by(treatment_id=appointment.treatment.id).all()
                    for payment in payments:
                        db.session.delete(payment)
                db.session.delete(appointment)
            
            patient_profile = user.patient_profile
            if patient_profile:
                db.session.delete(patient_profile)
            
            db.session.delete(user)
            db.session.commit()
            
            return make_response(jsonify({"message": "Patient deleted successfully"}), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"message": "Failed to delete patient", "error": str(e)}), 500)

#==============================================================================
#Block User
#==============================================================================

class BlockUserAPI(Resource):
    @jwt_required()
    def post(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return make_response(jsonify({"message": "Invalid token"}), 401)
        
        if current_user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        if user.role == "admin":
            return make_response(jsonify({"message": "Cannot block admin"}), 400)
        
        user.active = False
        db.session.commit()
        
        return make_response(jsonify({"message": "User blocked successfully"}), 200)

#==============================================================================
#Unblock User
#==============================================================================

class UnblockUserAPI(Resource):
    @jwt_required()
    def post(self, user_id):
        current_user_id = int(get_jwt_identity())
        current_user = User.query.get(current_user_id)
        
        if not current_user:
            return make_response(jsonify({"message": "Invalid token"}), 401)
        
        if current_user.role != "admin":
            return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
        
        user.active = True
        db.session.commit()
        
        return make_response(jsonify({"message": "User unblocked successfully"}), 200)

#==============================================================================
#Home Stats (Public)
#==============================================================================

class HomeStatsAPI(Resource):
    def get(self):
        total_patients = User.query.filter_by(role="patient").count()
        total_doctors = User.query.filter_by(role="doctor").count()
        total_appointments = Appointment.query.count()
        
        return make_response(jsonify({
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments
        }), 200)

#==============================================================================
#Public Departments List (For all authenticated users)
#==============================================================================

class PublicDepartmentsAPI(Resource):
    @jwt_required()
    def get(self):
        departments = Department.query.all()
        result = []
        
        for dept in departments:
            result.append({
                "id": dept.id,
                "name": dept.name,
                "description": dept.description,
                "doctors_registered": dept.doctors_registered
            })
        
        return make_response(jsonify({"departments": result}), 200)

