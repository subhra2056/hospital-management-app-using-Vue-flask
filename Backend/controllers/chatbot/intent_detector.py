"""
Intent Detector - Generates prompts for intent classification
Uses simple, strict prompts that force JSON-only output
"""
from datetime import date, timedelta

def get_next_weekday(day_name):
    """Get the date of the next occurrence of a weekday"""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    today = date.today()
    target_day = days.index(day_name.lower())
    days_ahead = target_day - today.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return today + timedelta(days=days_ahead)

def get_patient_intent_prompt(user_message, dept_list):
    """Generate intent detection prompt for patient chatbot"""
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    dept_names = ", ".join(dept_list[:5]) if dept_list else "General Medicine, Cardiology, Neurology"
    
    return f"""SYSTEM: JSON classifier. Return ONLY valid JSON. No explanations.

MESSAGE: "{user_message}"
TODAY: {today}

INTENTS (choose ONE):
- book_appointment: wants to see a doctor, book appointment, schedule visit
- view_appointments: wants to see their appointments, my bookings, upcoming appointments
- cancel_appointment: wants to cancel ANY appointment (with or without ID)
- symptom_check: describes symptoms like headache, fever, pain, feeling sick
- view_profile: wants to see profile info
- general_query: ONLY for greetings (hello, hi, thanks, bye) - NOT appointment related

RULES:
1. "cancel appointment", "cancel my appointment", "cancel booking" = cancel_appointment
2. "view appointments", "my appointments", "show bookings" = view_appointments  
3. "book appointment", "see a doctor", "schedule visit" = book_appointment
4. NEVER classify appointment-related requests as general_query

FORMAT: {{"intent":"INTENT_NAME","entities":{{"symptoms":[],"department":"","doctor_name":"","preferred_date":"YYYY-MM-DD","appointment_ids":[]}}}}

EXAMPLES:
"I have headache and fever" -> {{"intent":"symptom_check","entities":{{"symptoms":["headache","fever"]}}}}
"Book appointment with cardiology" -> {{"intent":"book_appointment","entities":{{"department":"cardiology"}}}}
"Show my appointments" -> {{"intent":"view_appointments","entities":{{}}}}
"view my booked appointment" -> {{"intent":"view_appointments","entities":{{}}}}
"Cancel appointment" -> {{"intent":"cancel_appointment","entities":{{}}}}
"cancel my appointment" -> {{"intent":"cancel_appointment","entities":{{}}}}
"Cancel appointment 5" -> {{"intent":"cancel_appointment","entities":{{"appointment_ids":[5]}}}}
"Hello" -> {{"intent":"general_query","entities":{{}}}}

JSON:JSON OUTPUT:"""


def get_doctor_intent_prompt(user_message):
    """Generate intent detection prompt for doctor chatbot"""
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    # Calculate dates for each day of the week
    monday = get_next_weekday('monday')
    tuesday = get_next_weekday('tuesday')
    wednesday = get_next_weekday('wednesday')
    thursday = get_next_weekday('thursday')
    friday = get_next_weekday('friday')
    saturday = get_next_weekday('saturday')
    sunday = get_next_weekday('sunday')
    
    return f"""SYSTEM: Strict JSON classifier. Return ONLY valid JSON. No explanations, no text before or after JSON.

MESSAGE: "{user_message}"
TODAY: {today} ({today.strftime('%A')})

DATE MAPPING:
monday={monday}, tuesday={tuesday}, wednesday={wednesday}, thursday={thursday}, friday={friday}, saturday={saturday}, sunday={sunday}, tomorrow={tomorrow}, today={today}

INTENTS (choose ONE):
- create_availability: ANY request to set/create/add/book availability/schedule/slots, "available from X to Y"
- view_availability: show/view/display/see schedule/slots/availability/current availability
- delete_availability: delete/remove/cancel slot
- view_appointments: see/view appointments/patients
- cancel_appointment: cancel appointment (extract appointment ID number)
- general_query: ONLY greetings (hi/hello/thanks/bye) - NOT schedule related

RULES:
1. "book availability", "available from", "available daily" = create_availability
2. "show schedule", "my schedule", "current availability" = view_availability
3. "delete availability", "remove slot" = delete_availability
4. "cancel appointment 6" = cancel_appointment with appointment_ids:[6]
5. NEVER classify schedule/availability requests as general_query
6. If the message is ambiguous, prefer create_availability if it mentions time or date, otherwise ask for clarification.
7. Time must be in 24-hour format (e.g., 09:00, 16:00). If user says "9am", use "09:00". If "4pm", use "16:00".
8. If the message is missing a date or time, set intent to create_availability but leave missing fields empty in entities.

TIME CONVERSION RULES:
- Times with "am/pm": Convert to 24-hour format
  - "3:00 pm" or "3 pm" = 15:00 (NOT 03:00)
  - "4:47 pm" or "4:47pm" = 16:47
  - "3:00 am" = 03:00
  - "12:00 pm" = 12:00 (noon)
  - "12:00 am" = 00:00 (midnight)
- Always preserve minutes: "3:47 pm" -> "15:47", not "15:00"
- Examples: 4am=04:00, 7am=07:00, 9am=09:00, 10am=10:00, 11am=11:00, 12pm=12:00, 1pm=13:00, 2pm=14:00, 3pm=15:00, 3:00pm=15:00, 3:47pm=15:47, 4pm=16:00, 4:47pm=16:47, 5pm=17:00, 6pm=18:00

RECURRING PATTERNS:
- "every monday", "every tuesday", etc. = weekly pattern with specific day(s)
- "weekdays", "every weekday" = Monday-Friday pattern
- "daily", "every day" = every day pattern
- "every monday and wednesday" = custom weekly pattern with multiple days
- "for next week", "for the next 2 weeks" = time-limited recurring pattern

FORMAT: {{"intent":"NAME","entities":{{"dates":["YYYY-MM-DD"],"times":{{"start":"HH:MM","end":"HH:MM"}},"recurrence":{{"type":"daily|weekly|weekdays|custom","days":["monday","wednesday"],"end_date":"YYYY-MM-DD"}},"slot_ids":[],"appointment_ids":[]}}}}

EXAMPLES:
"create availability thursday 4am to 7am" -> {{"intent":"create_availability","entities":{{"dates":["{thursday}"],"times":{{"start":"04:00","end":"07:00"}}}}}}
"book availability friday 9am to 5pm" -> {{"intent":"create_availability","entities":{{"dates":["{friday}"],"times":{{"start":"09:00","end":"17:00"}}}}}}
"available daily 10am to 4pm" -> {{"intent":"create_availability","entities":{{"times":{{"start":"10:00","end":"16:00"}},"recurrence":{{"type":"daily"}}}}}}
"every monday 9am to 5pm" -> {{"intent":"create_availability","entities":{{"times":{{"start":"09:00","end":"17:00"}},"recurrence":{{"type":"weekly","days":["monday"]}}}}}}
"weekdays 10am to 4pm" -> {{"intent":"create_availability","entities":{{"times":{{"start":"10:00","end":"16:00"}},"recurrence":{{"type":"weekdays"}}}}}}
"every monday and wednesday 2pm to 6pm" -> {{"intent":"create_availability","entities":{{"times":{{"start":"14:00","end":"18:00"}},"recurrence":{{"type":"custom","days":["monday","wednesday"]}}}}}}
"daily for next week 9am to 5pm" -> {{"intent":"create_availability","entities":{{"times":{{"start":"09:00","end":"17:00"}},"recurrence":{{"type":"daily","end_date":"{today + timedelta(days=7)}"}}}}}}
"Available from 10am-4pm" -> {{"intent":"create_availability","entities":{{"times":{{"start":"10:00","end":"16:00"}}}}}}
"show my schedule" -> {{"intent":"view_availability","entities":{{}}}}
"Show my current availability" -> {{"intent":"view_availability","entities":{{}}}}
"delete availability" -> {{"intent":"delete_availability","entities":{{}}}}
"delete slot 10" -> {{"intent":"delete_availability","entities":{{"slot_ids":[10]}}}}
"view my appointments" -> {{"intent":"view_appointments","entities":{{}}}}
"cancel appointment 6" -> {{"intent":"cancel_appointment","entities":{{"appointment_ids":[6]}}}}
"cancel appointment" -> {{"intent":"cancel_appointment","entities":{{}}}}
"Hello" -> {{"intent":"general_query","entities":{{}}}}
"I want to be available" -> {{"intent":"create_availability","entities":{{}}}}  # ambiguous, but prefer create_availability
"Set a slot" -> {{"intent":"create_availability","entities":{{}}}}  # ambiguous, but prefer create_availability
"Can you help me?" -> {{"intent":"general_query","entities":{{}}}}  # not schedule related

JSON ONLY OUTPUT:"""
