"""
Patient Profile Handler
"""
from flask import jsonify, make_response
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_view_profile(patient_profile, ai_ack=""):
    """Show patient profile information"""
    try:
        profile_info = f"""
Name: {patient_profile.user.username}
Age: {patient_profile.age}
Gender: {patient_profile.gender}
Phone: {patient_profile.phone or 'Not provided'}
Address: {patient_profile.address or 'Not provided'}
"""
        
        prompt = f"""Patient wants to see their profile:
{profile_info}

Write a brief, friendly summary (2 sentences). Be conversational and vary your response."""
        
        response_text = generate_ai_response(prompt, temperature=0.9)
    except:
        response_text = f"Here's your profile information: {patient_profile.user.username}, {patient_profile.age} years old, {patient_profile.gender}."
    
    return make_response(jsonify({"response": response_text, "doctors": []}), 200)
