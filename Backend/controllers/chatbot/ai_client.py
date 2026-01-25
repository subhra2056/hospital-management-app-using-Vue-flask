"""
AI Client - Handles communication with Ollama/Llama model
"""
import ollama

def generate_ai_response(prompt, temperature=0.7):
    """
    Generate AI response using Ollama with Llama 3.2 model
    
    Args:
        prompt (str): The prompt to send to the AI
        temperature (float): Controls randomness (0.0-1.0)
            - Lower (0.1-0.3): More consistent, good for intent detection
            - Higher (0.7-0.9): More creative, good for conversations
    
    Returns:
        str: AI generated response
    """
    try:
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[{
                'role': 'user',
                'content': prompt
            }],
            options={
                'temperature': temperature
            }
        )
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"[AI CLIENT ERROR] Ollama response error: {str(e)}")
        return ""
    except Exception as e:
        print(f"[AI CLIENT ERROR] Failed to connect to Ollama. Please check that Ollama is downloaded, running and accessible. https://ollama.com/download")
        print(f"[ERROR DETAILS] {str(e)}")
        return ""
