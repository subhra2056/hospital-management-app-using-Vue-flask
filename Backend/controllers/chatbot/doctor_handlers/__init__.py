"""
Doctor Handlers - Request handlers for doctor chatbot
"""

from .availability import handle_create_availability, handle_view_availability, handle_delete_availability
from .appointments import handle_view_appointments, handle_cancel_appointment
from .prescriptions import handle_write_prescription
from .general import handle_general_query

__all__ = [
    'handle_create_availability',
    'handle_view_availability',
    'handle_delete_availability',
    'handle_view_appointments',
    'handle_cancel_appointment',
    'handle_write_prescription',
    'handle_general_query'
]
