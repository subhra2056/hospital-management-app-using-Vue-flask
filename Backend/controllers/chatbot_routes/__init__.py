"""
Routes Package - Modular API endpoints
"""

from .patient_chatbot import PatientChatbotAPI
from .doctor_chatbot import DoctorChatbotAPI

__all__ = ['PatientChatbotAPI', 'DoctorChatbotAPI']
