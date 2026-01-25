"""
Doctor Appointment Handlers - View and cancel appointments
"""
from flask import jsonify, make_response
from datetime import datetime
from Backend.controllers.models import Appointment
from Backend.controllers.database import db
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_view_appointments(appointments, ai_ack=""):
    """View upcoming appointments"""
    try:
        if appointments:
            appts_info = "\n".join([
                f"- {a.patient.username} on {a.appointment_date.strftime('%A, %b %d')} at {a.appointment_time.strftime('%I:%M %p')} (Status: {a.status})"
                for a in appointments
            ])
            prompt = f"""Doctor has {len(appointments)} upcoming appointments:

{appts_info}

Write a friendly summary (2-3 sentences) highlighting key details like upcoming appointments, any pending ones."""
        else:
            prompt = "Doctor has NO upcoming appointments. Write a brief, friendly message (1 sentence)."
        
        response_text = generate_ai_response(prompt, temperature=0.9)
        return make_response(jsonify({"response": response_text}), 200)
    except:
        if appointments:
            return make_response(jsonify({"response": f"You have {len(appointments)} upcoming appointments."}), 200)
        return make_response(jsonify({"response": "No upcoming appointments."}), 200)


def handle_cancel_appointment(doctor_id, entities, appointments, ai_ack=""):
    """Cancel patient appointments"""
    appointment_ids = entities.get("appointment_ids", [])
    patient_name = entities.get("patient_name")
    dates = entities.get("dates", [])
    
    # Try to match by patient name or date
    if not appointment_ids:
        for appt in appointments:
            if patient_name and patient_name.lower() in appt.patient.username.lower():
                appointment_ids.append(appt.id)
            elif dates:
                for d_str in dates:
                    try:
                        target_date = datetime.strptime(d_str, '%Y-%m-%d').date()
                        if appt.appointment_date == target_date:
                            appointment_ids.append(appt.id)
                    except:
                        pass
    
    if not appointment_ids:
        return make_response(jsonify({
            "response": "Which appointment should I cancel? Please specify the patient name or date."
        }), 200)
    
    cancelled = []
    for appt_id in appointment_ids:
        appt = Appointment.query.filter_by(id=appt_id, doctor_id=doctor_id).first()
        if appt and appt.status != "cancelled":
            appt.status = "cancelled"
            cancelled.append(f"{appt.patient.username} on {appt.appointment_date.strftime('%b %d')}")
    
    if cancelled:
        db.session.commit()
    
    try:
        if cancelled:
            prompt = f"Cancelled {len(cancelled)} appointment(s): {', '.join(cancelled)}. Write a confirmation (1-2 sentences)."
        else:
            prompt = "Couldn't cancel any appointments - not found or already cancelled. Write a brief message (1 sentence)."
        
        response_text = generate_ai_response(prompt, temperature=0.9)
        return make_response(jsonify({"response": response_text}), 200)
    except:
        if cancelled:
            return make_response(jsonify({"response": f"✅ Cancelled {len(cancelled)} appointment(s)"}), 200)
        return make_response(jsonify({"response": "Couldn't find appointments to cancel"}), 200)
