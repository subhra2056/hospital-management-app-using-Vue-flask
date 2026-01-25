"""
Patient Chatbot API - Clean modular implementation
"""
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime

from Backend.controllers.models import User, PatientProfile, DoctorProfile, Department, Appointment, DoctorAvailability
from Backend.controllers.database import db

# Import chatbot modules
from Backend.controllers.chatbot.intent_detector import get_patient_intent_prompt
from Backend.controllers.chatbot.entity_extractor import extract_json_from_llm
from Backend.controllers.chatbot.ai_client import generate_ai_response


class PatientChatbotAPI(Resource):
    """
    Patient chatbot endpoint - handles all patient chat interactions
    Supports: appointment booking, symptom checking, appointment management
    """
    
    @jwt_required()
    def post(self):
        # Authenticate user
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != "patient":
            return make_response(jsonify({"message": "Only patients can use this feature"}), 403)
        
        patient_profile = PatientProfile.query.filter_by(user_id=user_id).first()
        if not patient_profile:
            return make_response(jsonify({"message": "Patient profile not found"}), 404)
        
        # Get message from request
        data = request.get_json()
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return make_response(jsonify({"response": "Please send a message!", "doctors": []}), 400)
        
        today = date.today()
        
        # Get available departments
        departments = Department.query.all()
        dept_list = [d.name for d in departments]
        
        # Step 1: Detect intent using AI
        intent_prompt = get_patient_intent_prompt(user_message, dept_list)
        ai_response = generate_ai_response(intent_prompt, temperature=0.1)
        
        # Debug logging
        print(f"[PATIENT CHATBOT] User message: {user_message}")
        print(f"[RAW AI RESPONSE] {ai_response}")
        
        # Step 2: Extract entities from AI response
        raw_data = extract_json_from_llm(ai_response)
        intent = raw_data.get("intent", "general_query")
        entities = raw_data.get("entities", {})
        
        print(f"[INTENT DETECTED] {intent}")
        print(f"[RAW DATA] {raw_data}")
        print(f"[ENTITIES] {entities}")
        
        # ===== HANDLE BOOK APPOINTMENT =====
        if intent == "book_appointment":
            department = entities.get("department", "")
            doctor_name = entities.get("doctor_name", "")
            symptoms = entities.get("symptoms", [])
            
            # Find doctors with available slots
            doctors_query = db.session.query(User).join(DoctorProfile).join(
                Department, DoctorProfile.department_id == Department.id
            ).filter(User.role == "doctor", User.active == True)
            
            if department:
                doctors_query = doctors_query.filter(Department.name.ilike(f"%{department}%"))
            
            if doctor_name:
                doctors_query = doctors_query.filter(User.username.ilike(f"%{doctor_name}%"))
            
            doctors = doctors_query.limit(10).all()
            
            # Get available slots for these doctors
            doctor_list = []
            for doc in doctors:
                slots = DoctorAvailability.query.filter_by(
                    doctor_profile_id=doc.doctor_profile.id,
                    is_booked=False
                ).filter(DoctorAvailability.date >= today).order_by(
                    DoctorAvailability.date, DoctorAvailability.start_time
                ).limit(5).all()
                
                if slots:
                    profile = doc.doctor_profile
                    doctor_list.append({
                        "id": doc.id,
                        "username": doc.username,
                        "specialization": profile.specialization,
                        "department_name": profile.department_ref.name if profile.department_ref else "General",
                        "department_id": profile.department_id,
                        "experience_years": profile.experience_years,
                        "gender": profile.gender,
                        "available_slots": [{
                            "slot_id": s.id,
                            "date": s.date.strftime('%Y-%m-%d'),
                            "date_formatted": s.date.strftime('%A, %b %d'),
                            "start_time": s.start_time.strftime('%I:%M %p'),
                            "end_time": s.end_time.strftime('%I:%M %p')
                        } for s in slots]
                    })
            
            if doctor_list:
                response_text = f"I found {len(doctor_list)} doctor(s) with available appointments. Please select a doctor and time slot below to book your appointment."
                if symptoms:
                    response_text = f"I understand you're experiencing {', '.join(symptoms)}. " + response_text
            else:
                response_text = "I couldn't find any doctors with available slots right now. Please try again later or contact reception."
            
            return make_response(jsonify({
                "response": response_text,
                "doctors": doctor_list
            }), 200)
        
        # ===== HANDLE SYMPTOM CHECK =====
        elif intent == "symptom_check":
            symptoms = entities.get("symptoms", [])
            
            if not symptoms:
                return make_response(jsonify({
                    "response": "Please describe your symptoms and I'll recommend the right department. For example: 'I have a headache and fever'",
                    "doctors": []
                }), 200)
            
            # Generate AI recommendation based on symptoms
            prompt = f"""Patient has these symptoms: {', '.join(symptoms)}

Based on these symptoms, recommend ONE department from this list: {', '.join(dept_list)}

Format your response as:
"Based on your symptoms ({', '.join(symptoms)}), I recommend visiting the [DEPARTMENT] department. [Brief 1-sentence explanation]."

Keep it brief and reassuring."""
            
            recommendation = generate_ai_response(prompt, temperature=0.3)
            
            if not recommendation:
                recommendation = f"Based on your symptoms, I recommend consulting with a General Medicine doctor first. Would you like to book an appointment?"
            
            # Find doctors in recommended department
            doctors_query = db.session.query(User).join(DoctorProfile).filter(
                User.role == "doctor", User.active == True
            )
            
            doctors = doctors_query.limit(5).all()
            doctor_list = []
            
            for doc in doctors:
                slots = DoctorAvailability.query.filter_by(
                    doctor_profile_id=doc.doctor_profile.id,
                    is_booked=False
                ).filter(DoctorAvailability.date >= today).limit(3).all()
                
                if slots:
                    profile = doc.doctor_profile
                    doctor_list.append({
                        "id": doc.id,
                        "username": doc.username,
                        "specialization": profile.specialization,
                        "department_name": profile.department_ref.name if profile.department_ref else "General",
                        "department_id": profile.department_id,
                        "experience_years": profile.experience_years,
                        "gender": profile.gender,
                        "available_slots": [{
                            "slot_id": s.id,
                            "date": s.date.strftime('%Y-%m-%d'),
                            "date_formatted": s.date.strftime('%A, %b %d'),
                            "start_time": s.start_time.strftime('%I:%M %p'),
                            "end_time": s.end_time.strftime('%I:%M %p')
                        } for s in slots]
                    })
            
            return make_response(jsonify({
                "response": recommendation,
                "doctors": doctor_list
            }), 200)
        
        # ===== HANDLE VIEW APPOINTMENTS =====
        elif intent == "view_appointments":
            appointments = Appointment.query.filter_by(
                patient_id=user_id
            ).filter(
                Appointment.status == "BOOKED",
                Appointment.appointment_date >= today
            ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
            
            if appointments:
                appt_list = []
                for a in appointments:
                    doctor = User.query.get(a.doctor_id)
                    doctor_name = doctor.username if doctor else "Unknown"
                    appt_list.append(f"• ID #{a.id}: {a.appointment_date.strftime('%A, %b %d')} at {a.appointment_time.strftime('%I:%M %p')} with Dr. {doctor_name} ({a.status})")
                
                return make_response(jsonify({
                    "response": f"📋 Your upcoming appointments:\n\n" + "\n".join(appt_list) + "\n\nTo cancel an appointment, say 'cancel appointment' followed by the ID.",
                    "doctors": []
                }), 200)
            else:
                return make_response(jsonify({
                    "response": "📭 You don't have any upcoming appointments. Would you like to book one? Just say 'book appointment' or describe your symptoms.",
                    "doctors": []
                }), 200)
        
        # ===== HANDLE CANCEL APPOINTMENT =====
        elif intent == "cancel_appointment":
            appointment_ids = entities.get("appointment_ids", [])
            
            if not appointment_ids:
                # Show appointments and ask which to cancel
                appointments = Appointment.query.filter_by(
                    patient_id=user_id
                ).filter(Appointment.status == "BOOKED").all()
                
                if appointments:
                    appt_list = []
                    for a in appointments:
                        doctor = User.query.get(a.doctor_id)
                        doctor_name = doctor.username if doctor else "Unknown"
                        appt_list.append(f"• ID #{a.id}: {a.appointment_date.strftime('%b %d')} with Dr. {doctor_name}")
                    
                    return make_response(jsonify({
                        "response": f"Which appointment would you like to cancel?\n\n" + "\n".join(appt_list) + "\n\nSay 'cancel appointment 5' to cancel a specific one.",
                        "doctors": []
                    }), 200)
                else:
                    return make_response(jsonify({
                        "response": "You don't have any appointments to cancel.",
                        "doctors": []
                    }), 200)
            
            # Cancel appointment
            cancelled = []
            for appt_id in appointment_ids:
                appt = Appointment.query.filter_by(
                    id=appt_id,
                    patient_id=user_id
                ).first()
                if appt and appt.status == "BOOKED":
                    appt.status = "CANCELLED"
                    # Free up the availability slot by matching date and time
                    doctor_profile = DoctorProfile.query.filter_by(user_id=appt.doctor_id).first()
                    if doctor_profile:
                        slot = DoctorAvailability.query.filter_by(
                            doctor_profile_id=doctor_profile.id,
                            date=appt.appointment_date,
                            is_booked=True
                        ).filter(
                            DoctorAvailability.start_time <= appt.appointment_time,
                            DoctorAvailability.end_time > appt.appointment_time
                        ).first()
                        if slot:
                            slot.is_booked = False
                    cancelled.append(appt_id)
            
            if cancelled:
                db.session.commit()
                return make_response(jsonify({
                    "response": f"✅ Successfully cancelled appointment(s): #{', #'.join(map(str, cancelled))}. The time slot is now available for others.",
                    "doctors": []
                }), 200)
            else:
                return make_response(jsonify({
                    "response": "❌ Couldn't find that appointment. Use 'view my appointments' to see your bookings.",
                    "doctors": []
                }), 200)
        
        # ===== HANDLE VIEW PROFILE =====
        elif intent == "view_profile":
            profile_info = f"""📋 Your Profile:
• Name: {user.username}
• Email: {user.email}
• Age: {patient_profile.age or 'Not set'}
• Gender: {patient_profile.gender or 'Not set'}
• Blood Group: {patient_profile.blood_group or 'Not set'}
• Phone: {patient_profile.phone_number or 'Not set'}
• Address: {patient_profile.address or 'Not set'}"""
            
            return make_response(jsonify({
                "response": profile_info,
                "doctors": []
            }), 200)
        
        # ===== HANDLE GENERAL QUERY =====
        else:
            # Generate friendly response for greetings/general questions
            prompt = f"""You are a helpful medical assistant chatbot for patients. The patient said: "{user_message}"

Respond briefly (1-2 sentences). You can help them with:
- Booking appointments ("book appointment" or "see a doctor")
- Checking symptoms ("I have a headache")
- Viewing their appointments ("show my appointments")
- Canceling appointments ("cancel appointment 5")

Be friendly and empathetic."""
            
            response = generate_ai_response(prompt, temperature=0.8)
            if not response:
                response = "Hello! I can help you book appointments, check symptoms, or manage your bookings. How can I assist you today?"
            
            return make_response(jsonify({
                "response": response,
                "doctors": []
            }), 200)
