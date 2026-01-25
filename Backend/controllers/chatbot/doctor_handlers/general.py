"""
Doctor General Query Handler - Greetings, thanks, and general questions
"""
from flask import jsonify, make_response
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_general_query(user_message, ai_ack=""):
    """Handle general questions and greetings with Llama"""
    # Use ai_ack if Llama already generated a response, otherwise generate one
    if ai_ack:
        return make_response(jsonify({"response": ai_ack}), 200)
    
    try:
        prompt = f"""The doctor said: "{user_message}"

Generate a friendly, natural response. If it's a greeting, greet them back warmly and mention you can help with:
- Creating, viewing, updating, or deleting availability
- Viewing or canceling appointments  
- General scheduling questions

If it's a question, answer helpfully. Keep it conversational and brief (2-3 sentences).

Response:"""
        
        response_text = generate_ai_response(prompt, temperature=0.8)
        return make_response(jsonify({"response": response_text}), 200)
    except:
        return make_response(jsonify({
            "response": "Hi! I can help you manage your schedule. What would you like to do?"
        }), 200)
