"""
Chatbot Module - Modular AI-powered medical chatbot system
"""

from .ai_client import generate_ai_response
from .intent_detector import get_patient_intent_prompt, get_doctor_intent_prompt
from .entity_extractor import extract_json_from_llm

__all__ = [
    'generate_ai_response',
    'get_patient_intent_prompt',
    'get_doctor_intent_prompt',
    'extract_json_from_llm'
]
