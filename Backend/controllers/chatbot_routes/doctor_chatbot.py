"""
Doctor Chatbot API - Clean modular implementation
"""
from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime, timedelta

from Backend.controllers.models import User, DoctorProfile, Appointment, DoctorAvailability
from Backend.controllers.database import db

# Import chatbot modules
from Backend.controllers.chatbot.intent_detector import get_doctor_intent_prompt
from Backend.controllers.chatbot.entity_extractor import extract_json_from_llm
from Backend.controllers.chatbot.ai_client import generate_ai_response


class DoctorChatbotAPI(Resource):
    """
    Doctor chatbot endpoint - handles all doctor chat interactions
    Supports: availability management, appointment viewing/canceling
    """
    
    @jwt_required()
    def post(self):
        # Authenticate user
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != "doctor":
            return make_response(jsonify({"message": "Only doctors can use this feature"}), 403)
        
        doctor_profile = DoctorProfile.query.filter_by(user_id=user_id).first()
        if not doctor_profile:
            return make_response(jsonify({"message": "Doctor profile not found"}), 404)
        
        # Get message from request
        data = request.get_json()
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return make_response(jsonify({"response": "Please send a message!"}), 400)
        
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        # Step 1: Detect intent using AI
        intent_prompt = get_doctor_intent_prompt(user_message)
        ai_response = generate_ai_response(intent_prompt, temperature=0.1)
        
        # Debug logging
        print(f"[DOCTOR CHATBOT] User message: {user_message}")
        print(f"[RAW AI RESPONSE] {ai_response}")
        
        # Step 2: Extract entities from AI response
        raw_data = extract_json_from_llm(ai_response)
        intent = raw_data.get("intent", "general_query")
        entities = raw_data.get("entities", {})
        
        print(f"[INTENT DETECTED] {intent}")
        print(f"[RAW DATA] {raw_data}")
        print(f"[ENTITIES] {entities}")
        
        # ===== HANDLE CREATE AVAILABILITY =====
        if intent == "create_availability":
            dates = entities.get("dates", [])
            times = entities.get("times", {})
            
            # If no date/time provided, ask for details
            if not dates or not times or not times.get("start") or not times.get("end"):
                return make_response(jsonify({
                    "response": "I'd be happy to create availability for you! Please specify the date and time range. For example: 'tomorrow 9am to 5pm' or 'January 27 10am to 2pm'"
                }), 200)
            
            # Parse and create availability
            created_slots = []
            errors = []
            
            for date_str in dates:
                try:
                    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except:
                    errors.append(f"Invalid date format: {date_str}")
                    continue
                
                if target_date < today:
                    errors.append(f"Cannot create slot for past date: {target_date}")
                    continue
                
                try:
                    start_time = datetime.strptime(times["start"], '%H:%M').time()
                    end_time = datetime.strptime(times["end"], '%H:%M').time()
                except:
                    errors.append("Invalid time format")
                    continue
                
                # Check for existing slot
                existing = DoctorAvailability.query.filter_by(
                    doctor_profile_id=doctor_profile.id,
                    date=target_date,
                    start_time=start_time,
                    end_time=end_time
                ).first()
                
                if existing:
                    errors.append(f"Slot already exists for {target_date.strftime('%b %d')}")
                    continue
                
                # Create new slot
                availability = DoctorAvailability(
                    doctor_profile_id=doctor_profile.id,
                    date=target_date,
                    start_time=start_time,
                    end_time=end_time,
                    is_booked=False
                )
                db.session.add(availability)
                created_slots.append({
                    "date": str(target_date),
                    "date_formatted": target_date.strftime('%A, %b %d'),
                    "start_time": start_time.strftime('%I:%M %p'),
                    "end_time": end_time.strftime('%I:%M %p')
                })
            
            if created_slots:
                db.session.commit()
                slots_text = ", ".join([f"{s['date_formatted']} ({s['start_time']} - {s['end_time']})" for s in created_slots])
                return make_response(jsonify({
                    "response": f"✅ Successfully created {len(created_slots)} availability slot(s): {slots_text}",
                    "created_slots": created_slots
                }), 200)
            else:
                return make_response(jsonify({
                    "response": f"❌ Couldn't create slots. {errors[0] if errors else 'Please try again.'}"
                }), 200)
        
        # ===== HANDLE VIEW AVAILABILITY =====
        elif intent == "view_availability":
            slots = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id
            ).filter(DoctorAvailability.date >= today).order_by(
                DoctorAvailability.date, DoctorAvailability.start_time
            ).all()
            
            if slots:
                slots_list = []
                for s in slots:
                    status = "🔴 Booked" if s.is_booked else "🟢 Available"
                    slots_list.append(f"• ID #{s.id}: {s.date.strftime('%A, %b %d')} - {s.start_time.strftime('%I:%M %p')} to {s.end_time.strftime('%I:%M %p')} ({status})")
                
                return make_response(jsonify({
                    "response": f"📅 Your upcoming availability slots:\n\n" + "\n".join(slots_list)
                }), 200)
            else:
                return make_response(jsonify({
                    "response": "📭 You don't have any upcoming availability slots. Would you like to create some? Just say 'create availability tomorrow 9am to 5pm'"
                }), 200)
        
        # ===== HANDLE DELETE AVAILABILITY =====
        elif intent == "delete_availability":
            slot_ids = entities.get("slot_ids", [])
            # Convert string IDs to integers
            slot_ids = [int(s) for s in slot_ids if str(s).isdigit()]
            dates = entities.get("dates", [])
            
            if not slot_ids and not dates:
                # Show slots and ask which to delete
                slots = DoctorAvailability.query.filter_by(
                    doctor_profile_id=doctor_profile.id
                ).filter(DoctorAvailability.date >= today).order_by(
                    DoctorAvailability.date, DoctorAvailability.start_time
                ).all()
                
                if slots:
                    slots_list = [f"• ID #{s.id}: {s.date.strftime('%A, %b %d')} {s.start_time.strftime('%I:%M %p')}-{s.end_time.strftime('%I:%M %p')} ({'🔴 Booked' if s.is_booked else '🟢 Available'})" for s in slots[:10]]
                    return make_response(jsonify({
                        "response": f"Which slot would you like to delete? Here are your slots:\n\n" + "\n".join(slots_list) + "\n\nSay 'delete slot 10' to delete a specific slot by ID."
                    }), 200)
                else:
                    return make_response(jsonify({
                        "response": "📭 You don't have any availability slots to delete."
                    }), 200)
            
            # Delete by ID
            deleted = []
            for slot_id in slot_ids:
                slot = DoctorAvailability.query.filter_by(
                    id=slot_id,
                    doctor_profile_id=doctor_profile.id
                ).first()
                if slot:
                    if slot.is_booked:
                        return make_response(jsonify({
                            "response": f"❌ Cannot delete slot #{slot_id} - it has a booked appointment. Cancel the appointment first."
                        }), 200)
                    db.session.delete(slot)
                    deleted.append(slot_id)
            
            if deleted:
                db.session.commit()
                return make_response(jsonify({
                    "response": f"✅ Deleted slot(s): #{', #'.join(map(str, deleted))}"
                }), 200)
            else:
                return make_response(jsonify({
                    "response": "❌ Couldn't find those slots. Use 'show my schedule' to see your slots."
                }), 200)
        
        # ===== HANDLE VIEW APPOINTMENTS =====
        elif intent == "view_appointments":
            appointments = Appointment.query.filter_by(
                doctor_id=user_id
            ).filter(
                Appointment.status == "BOOKED",
                Appointment.appointment_date >= today
            ).order_by(Appointment.appointment_date, Appointment.appointment_time).all()
            
            if appointments:
                appt_list = []
                for a in appointments:
                    patient = User.query.get(a.patient_id)
                    patient_name = patient.username if patient else "Unknown"
                    appt_list.append(f"• ID #{a.id}: {a.appointment_date.strftime('%b %d')} at {a.appointment_time.strftime('%I:%M %p')} - Patient: {patient_name} ({a.status})")
                
                return make_response(jsonify({
                    "response": f"📋 Your upcoming appointments:\n\n" + "\n".join(appt_list)
                }), 200)
            else:
                return make_response(jsonify({
                    "response": "📭 You don't have any upcoming appointments."
                }), 200)
        
        # ===== HANDLE CANCEL APPOINTMENT =====
        elif intent == "cancel_appointment":
            appointment_ids = entities.get("appointment_ids", [])
            
            if not appointment_ids:
                # Show appointments and ask which to cancel
                appointments = Appointment.query.filter_by(
                    doctor_id=user_id
                ).filter(Appointment.status == "BOOKED").all()
                
                if appointments:
                    appt_list = [f"• ID #{a.id}: {a.appointment_date.strftime('%b %d')} at {a.appointment_time.strftime('%I:%M %p')}" for a in appointments[:10]]
                    return make_response(jsonify({
                        "response": f"Which appointment would you like to cancel?\n\n" + "\n".join(appt_list) + "\n\nSay 'cancel appointment 5' to cancel."
                    }), 200)
                else:
                    return make_response(jsonify({
                        "response": "You don't have any appointments to cancel."
                    }), 200)
            
            # Cancel appointment
            cancelled = []
            for appt_id in appointment_ids:
                appt = Appointment.query.filter_by(
                    id=appt_id,
                    doctor_id=user_id
                ).first()
                if appt and appt.status == "BOOKED":
                    appt.status = "CANCELLED"
                    
                    # Free up the availability slot by matching date and time
                    slot = DoctorAvailability.query.filter_by(
                        doctor_id=user_id,
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
                    "response": f"✅ Cancelled appointment(s): #{', #'.join(map(str, cancelled))}"
                }), 200)
            else:
                return make_response(jsonify({
                    "response": "❌ Couldn't find those appointments. Use 'view appointments' to see your appointments."
                }), 200)
        
        # ===== HANDLE GENERAL QUERY =====
        else:
            # Generate friendly response for greetings/general questions
            prompt = f"""You are a helpful medical assistant chatbot for doctors. The doctor said: "{user_message}"

Respond briefly (1-2 sentences). You can help them with:
- Creating availability slots (e.g., "set availability tomorrow 9am to 5pm")
- Viewing their schedule ("show my schedule")
- Deleting availability slots ("delete slot 5")
- Viewing appointments ("view my appointments")
- Canceling appointments ("cancel appointment 3")

Be friendly and professional."""
            
            response = generate_ai_response(prompt, temperature=0.8)
            if not response:
                response = "Hello! I can help you manage your schedule. Try saying 'create availability tomorrow 9am to 5pm' or 'show my appointments'."
            
            return make_response(jsonify({"response": response}), 200)
