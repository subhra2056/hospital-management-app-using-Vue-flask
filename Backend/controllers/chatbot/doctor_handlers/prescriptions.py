"""
Doctor Prescription Handler
"""
from flask import jsonify, make_response
from Backend.controllers.models import User, Treatment, Appointment
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_write_prescription(doctor_id, entities, ai_ack=""):
    """Write or edit patient prescriptions"""
    patient_name = entities.get("patient_name")
    medications = entities.get("medications", [])
    dosage = entities.get("dosage")
    
    if not patient_name:
        return make_response(jsonify({
            "response": "Which patient is this prescription for? Please specify the patient name."
        }), 200)
    
    # Find patient
    patient = User.query.filter(
        User.username.ilike(f"%{patient_name}%"),
        User.role == "patient"
    ).first()
    
    if not patient:
        return make_response(jsonify({
            "response": f"Couldn't find a patient named '{patient_name}'. Please check the name and try again."
        }), 200)
    
    # Get recent treatments
    treatments = Treatment.query.join(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.patient_id == patient.id
    ).order_by(Treatment.created_at.desc()).limit(5).all()
    
    if not medications:
        # Show existing prescriptions
        try:
            if treatments:
                prescriptions_info = "\n".join([
                    f"- {t.prescription} (from {t.appointment.appointment_date.strftime('%b %d')})"
                    for t in treatments
                ])
                prompt = f"""Doctor wants to write prescription for {patient.username}. Current prescriptions:

{prescriptions_info}

Write a helpful message (2-3 sentences) asking what medications to prescribe or what changes to make."""
            else:
                prompt = f"Doctor wants to write NEW prescription for {patient.username} (no previous prescriptions). Ask what medications to prescribe (1-2 sentences)."
            
            response_text = generate_ai_response(prompt, temperature=0.9)
            return make_response(jsonify({"response": response_text}), 200)
        except:
            if treatments:
                return make_response(jsonify({"response": f"Found {len(treatments)} prescription(s) for {patient.username}. What would you like to prescribe?"}), 200)
            return make_response(jsonify({"response": f"What prescription would you like to write for {patient.username}?"}), 200)
    
    # If medications provided, would create prescription here
    # (This requires appointment context which isn't fully implemented)
    return make_response(jsonify({
        "response": f"Prescription feature is being developed. You wanted to prescribe: {', '.join(medications)} for {patient.username}."
    }), 200)
