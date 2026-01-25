"""
Patient Handlers - Request handlers for patient chatbot
"""

from .appointments import handle_book_appointment, handle_view_appointments, handle_cancel_appointment
from .symptoms import handle_symptom_check
from .profile import handle_view_profile
from .general import handle_general_query

__all__ = [
    'handle_book_appointment',
    'handle_view_appointments',
    'handle_cancel_appointment',
    'handle_symptom_check',
    'handle_view_profile',
    'handle_general_query'
]
