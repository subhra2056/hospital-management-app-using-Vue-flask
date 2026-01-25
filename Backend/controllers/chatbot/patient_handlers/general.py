"""
Patient General Query Handler - Greetings, thanks, and general questions
"""
from flask import jsonify, make_response
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_general_query(user_message, ai_ack=""):
    """Handle greetings and general conversational queries"""
    try:
        prompt = f"""The patient said: "{user_message}"

This is a casual message (greeting, thanks, or general question).

Generate a warm, friendly response (1-2 sentences):
- If greeting: Welcome them and mention you can help with appointments, symptoms, or questions
- If thanking: Acknowledge warmly and offer further assistance
- If general question: Answer helpfully and mention what you can do

Be natural, conversational, and vary your responses. Don't be repetitive."""
        
        response_text = generate_ai_response(prompt, temperature=0.8)
    except:
        # Fallback responses
        import random
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good evening']):
            responses = [
                "Hello! I'm your medical assistant. I can help you book appointments, check symptoms, or answer health questions.",
                "Hi there! How can I assist you today? I can help with booking appointments or answering health questions.",
                "Hey! Welcome. I'm here to help with appointments, symptoms, or any medical questions you have."
            ]
        elif any(word in message_lower for word in ['thank', 'thanks', 'appreciate']):
            responses = [
                "You're very welcome! Let me know if you need anything else.",
                "Happy to help! Feel free to ask if you have more questions.",
                "My pleasure! I'm here whenever you need assistance."
            ]
        else:
            responses = [
                "I'm here to help! I can assist with booking appointments, checking symptoms, or answering health questions. What would you like to do?",
                "I can help you book doctor appointments, discuss symptoms, or answer general health questions. How can I assist you?",
                "I'm your medical assistant! I can help with appointments, symptom checking, or health queries. What do you need?"
            ]
        
        response_text = random.choice(responses)
    
    return make_response(jsonify({"response": response_text, "doctors": []}), 200)
