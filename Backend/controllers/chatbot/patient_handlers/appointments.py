"""
Patient Appointment Handlers - Book, view, and cancel appointments
"""
from flask import jsonify, make_response
from datetime import datetime
from Backend.controllers.models import User, PatientProfile, DoctorProfile, Department, Appointment, DoctorAvailability
from Backend.controllers.database import db
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_book_appointment(user_id, patient_profile, entities, dept_list, today, ai_ack=""):
    """Handle appointment booking with doctor search and slot selection"""
    symptoms = entities.get("symptoms", [])
    department = entities.get("department")
    doctor_name = entities.get("doctor_name")
    urgency = entities.get("urgency", "low")
    dates = entities.get("dates", [])
    
    # Find matching department
    if department:
        dept = Department.query.filter(Department.name.ilike(f"%{department}%")).first()
        if not dept:
            department = None
    
    # Search for doctors
    doctors_query = db.session.query(User).join(DoctorProfile).join(
        Department, DoctorProfile.department_id == Department.id
    ).filter(User.role == "doctor", User.active == True)
    
    if department:
        doctors_query = doctors_query.filter(Department.name.ilike(f"%{department}%"))
    
    if doctor_name:
        doctors_query = doctors_query.filter(User.username.ilike(f"%{doctor_name}%"))
    
    doctors = doctors_query.limit(5).all()
    
    # Get available slots for these doctors
    doctor_slots = {}
    for doc in doctors:
        slots = DoctorAvailability.query.filter_by(
            doctor_profile_id=doc.doctor_profile.id,
            is_booked=False
        ).filter(DoctorAvailability.date >= today).order_by(
            DoctorAvailability.date, DoctorAvailability.start_time
        ).limit(5).all()
        
        if slots:
            doctor_slots[doc.id] = [{
                "slot_id": s.id,
                "date": s.date.strftime('%Y-%m-%d'),
                "date_formatted": s.date.strftime('%A, %b %d'),
                "start_time": s.start_time.strftime('%I:%M %p'),
                "end_time": s.end_time.strftime('%I:%M %p')
            } for s in slots]
    
    # Build doctor list
    doctor_list = []
    for doc in doctors:
        profile = doc.doctor_profile
        doctor_list.append({
            "id": doc.id,
            "username": doc.username,
            "specialization": profile.specialization,
            "department_name": profile.department_ref.name,
            "department_id": profile.department_id,
            "experience_years": profile.experience_years,
            "gender": profile.gender,
            "available_slots": doctor_slots.get(doc.id, [])
        })
    
    # Generate AI response
    try:
        if doctor_list:
            doctors_summary = f"{len(doctor_list)} doctors available"
            slots_summary = sum([len(d.get('available_slots', [])) for d in doctor_list])
            
            prompt = f"""Patient wants to book appointment. {symptoms and f'Symptoms: {", ".join(symptoms)}.' or ''} {urgency == 'high' and 'URGENT case!' or ''}

Found {doctors_summary} with {slots_summary} available time slots.

Write an empathetic response (2-3 sentences):
1. Acknowledge their health concern warmly
2. Let them know you found doctors who can help
3. Tell them they can select a doctor and time slot from the list below
{urgency == 'high' and '4. Mention urgency - they should book soon or seek emergency care if severe' or ''}

Be compassionate and reassuring. Vary your phrasing each time."""
        else:
            prompt = f"""Patient wants appointment but NO doctors available currently. {symptoms and f'They have: {", ".join(symptoms)}' or ''}

Write a sympathetic response (2 sentences):
1. Apologize that no doctors are available right now
2. Suggest checking back later or contacting reception

Be understanding and helpful."""
        
        response_text = generate_ai_response(prompt, temperature=0.9)
    except:
        import random
        if doctor_list:
            responses = [
                f"I found {len(doctor_list)} doctors who can help you. Please select a doctor and available time slot below to book your appointment.",
                f"Good news! {len(doctor_list)} doctors are available. Choose your preferred doctor and time from the options below.",
                f"I've found {len(doctor_list)} specialists who can assist you. Pick a doctor and convenient time slot to proceed."
            ]
            response_text = random.choice(responses)
        else:
            response_text = "I'm sorry, no doctors are currently available. Please check back later or contact our reception."
    
    # Add urgency warning
    if urgency == "high":
        response_text = "🚨 **URGENT:** Your symptoms may need immediate attention. " + response_text
    
    return make_response(jsonify({
        "response": response_text,
        "doctors": doctor_list,
        "detected_department": department,
        "urgency": urgency
    }), 200)


def handle_view_appointments(user_id, appointments, ai_ack=""):
    """Show patient's appointments"""
    try:
        if appointments:
            appts_info = "\n".join([
                f"- Dr. {a.doctor.username} ({a.doctor.doctor_profile.department_ref.name}) on {a.appointment_date.strftime('%A, %b %d')} at {a.appointment_time.strftime('%I:%M %p')} - Status: {a.status}"
                for a in appointments
            ])
            prompt = f"""Patient has {len(appointments)} upcoming appointments:

{appts_info}

Write a friendly summary (2-3 sentences). Mention nearest appointment, any pending ones. Vary your tone and phrasing each time."""
        else:
            prompt = "Patient has NO appointments. Write a brief, friendly message (1-2 sentences) and offer to help them book one. Be conversational."
        
        response_text = generate_ai_response(prompt, temperature=0.9)
        return make_response(jsonify({"response": response_text, "doctors": []}), 200)
    except:
        if appointments:
            return make_response(jsonify({"response": f"You have {len(appointments)} upcoming appointments.", "doctors": []}), 200)
        return make_response(jsonify({"response": "You don't have any upcoming appointments. Would you like to book one?", "doctors": []}), 200)


def handle_cancel_appointment(user_id, entities, appointments, ai_ack=""):
    """Cancel patient appointments"""
    appointment_ids = entities.get("appointment_ids", [])
    dates = entities.get("dates", [])
    
    # Match by date if no IDs
    if not appointment_ids and dates:
        for d_str in dates:
            try:
                target_date = datetime.strptime(d_str, '%Y-%m-%d').date()
                matching = [a for a in appointments if a.appointment_date == target_date]
                appointment_ids.extend([a.id for a in matching])
            except:
                pass
    
    if not appointment_ids:
        return make_response(jsonify({
            "response": "Which appointment would you like to cancel? Please specify the date or doctor's name.",
            "doctors": []
        }), 200)
    
    cancelled = []
    for appt_id in appointment_ids:
        appt = Appointment.query.filter_by(id=appt_id, patient_id=user_id).first()
        if appt and appt.status != "cancelled":
            appt.status = "cancelled"
            # Free up the slot
            slot = DoctorAvailability.query.filter_by(
                doctor_profile_id=appt.doctor.doctor_profile.id,
                date=appt.appointment_date,
                start_time=appt.appointment_time
            ).first()
            if slot:
                slot.is_booked = False
            
            cancelled.append(f"Dr. {appt.doctor.username} on {appt.appointment_date.strftime('%b %d')}")
    
    if cancelled:
        db.session.commit()
    
    try:
        if cancelled:
            prompt = f"Successfully cancelled {len(cancelled)} appointment(s): {', '.join(cancelled)}. Write a brief, understanding confirmation (1-2 sentences). Vary your response."
        else:
            prompt = "Couldn't cancel - appointment not found or already cancelled. Write a brief, helpful message (1 sentence)."
        
        response_text = generate_ai_response(prompt, temperature=0.9)
    except:
        if cancelled:
            response_text = f"Your appointment(s) with {', '.join(cancelled)} have been cancelled successfully."
        else:
            response_text = "Couldn't find that appointment. It may already be cancelled."
    
    return make_response(jsonify({"response": response_text, "doctors": []}), 200)
