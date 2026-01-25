"""
Patient Symptom Check Handler
"""
from flask import jsonify, make_response
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_symptom_check(entities, dept_list, ai_ack=""):
    """Provide information about symptoms without booking"""
    symptoms = entities.get("symptoms", [])
    department = entities.get("department")
    urgency = entities.get("urgency", "low")
    
    try:
        prompt = f"""Patient asking about symptoms: {', '.join(symptoms) if symptoms else 'general health question'}
{department and f'Related to {department}' or ''}
Urgency: {urgency}

Write a helpful, informative response (2-3 sentences):
1. Provide general information about the symptoms
2. If serious ({urgency == 'high'}), strongly recommend seeing a doctor
3. Ask if they'd like to book an appointment

Be educational but not diagnostic. Encourage professional consultation. Vary phrasing."""
        
        response_text = generate_ai_response(prompt, temperature=0.9)
    except:
        if urgency == "high":
            response_text = "⚠️ These symptoms could be serious. I strongly recommend booking an appointment with a doctor as soon as possible. Would you like me to help you find available doctors?"
        else:
            response_text = f"I understand you're experiencing {', '.join(symptoms) if symptoms else 'some concerns'}. While I can provide general information, a doctor can give you a proper diagnosis. Would you like to book an appointment?"
    
    return make_response(jsonify({"response": response_text, "doctors": []}), 200)
