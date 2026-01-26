from flask import request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime, timedelta

from Backend.controllers.models import User, DoctorProfile, Appointment, DoctorAvailability
from Backend.controllers.database import db

# Chatbot utilities
from Backend.controllers.chatbot.intent_detector import get_doctor_intent_prompt
from Backend.controllers.chatbot.entity_extractor import extract_json_from_llm
from Backend.controllers.chatbot.ai_client import generate_ai_response
from Backend.controllers.chatbot.utils.availability_utils import (
    check_time_overlap,
    split_availability_window,
    check_appointment_conflicts,
    detect_overlapping_slots,
    expand_recurring_dates,
    validate_time_range
)


class DoctorChatbotAPI(Resource):
    """
    Doctor Scheduling Chatbot API
    Supports:
      - create availability
      - view availability
      - delete slots
      - view appointments
      - cancel appointments
    """

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        # Access check
        if not user or user.role != "doctor":
            return make_response(jsonify({"response": "Only doctors can use this feature"}), 403)

        doctor_profile = DoctorProfile.query.filter_by(user_id=user_id).first()
        if not doctor_profile:
            return make_response(jsonify({"response": "Doctor profile not found"}), 404)

        # Incoming message from UI
        data = request.get_json()
        user_message = (data.get("message") or "").strip()

        if not user_message:
            return make_response(jsonify({"response": "Please type something so I can assist you."}), 400)

        # Dates reference
        today = date.today()

        # ----------------------
        # STEP 1 — INTENT DETECTION (LLM)
        # ----------------------
        intent_prompt = get_doctor_intent_prompt(user_message)
        ai_text = generate_ai_response(intent_prompt, temperature=0.1)


        raw = extract_json_from_llm(ai_text)

        # Validate structure and ensure entities is a dict
        if not isinstance(raw, dict):
            raw = {}
        
        # Ensure entities is always a dict
        if "entities" in raw and not isinstance(raw.get("entities"), dict):
            raw["entities"] = {}
        
        intent = raw.get("intent")
        entities = raw.get("entities", {})
        
        # If no intent detected, use keyword fallback
        if not intent:
            # Keyword fallback for common intents
            msg = user_message.lower()
            if any(k in msg for k in ["show my availability", "current availability", "my schedule", "view availability"]):
                return self._handle_view_availability(doctor_profile, user_message, {})
            if any(k in msg for k in ["view my appointments", "my appointments", "show appointments"]):
                return self._handle_view_appointments(doctor_profile, user_message, {})
            if any(k in msg for k in ["create availability", "set availability", "add slot", "book availability"]):
                return self._handle_create_availability(doctor_profile, user_message, {})
            if any(k in msg for k in ["delete", "remove slot", "cancel slot"]):
                return self._handle_delete_availability(doctor_profile, user_message, {})
            # Fallback with debug info
            return make_response(jsonify({
                "response": "Sorry, I couldn't understand your request. Please rephrase or specify your intent.",
                "debug_raw_ai": ai_text
            }), 200)

        # Fallback: If user message is a create availability request but LLM misclassifies
        create_keywords = ["create availability", "set availability", "add slot", "book availability"]
        msg_lower = user_message.lower()
        if any(k in msg_lower for k in create_keywords) and intent != "create_availability":
            print("[INTENT FALLBACK] Overriding intent to create_availability due to user message keywords.")
            intent = "create_availability"

        print("======== CHATBOT DEBUG ========")
        print("User:", user_message)
        print("AI Raw:", ai_text)
        print("Parsed:", raw)
        print("Intent:", intent)
        print("Entities:", entities)
        print("================================")

        # Route to handler
        handler_map = {
            "create_availability": self._handle_create_availability,
            "view_availability": self._handle_view_availability,
            "delete_availability": self._handle_delete_availability,
            "view_appointments": self._handle_view_appointments,
            "cancel_appointment": self._handle_cancel_appointment,
        }

        handler = handler_map.get(intent)

        if handler:
            return handler(doctor_profile, user_message, entities)

        # If intent isn't mapped → fallback general response
        return self._fallback_message(user_message)

    # -----------------------------------------------------------------------
    # FALLBACK GENERAL REPLY
    # -----------------------------------------------------------------------
    def _fallback_message(self, user_message):
        """When intent is unclear, provide a friendly help message."""
        prompt = f"""
You are a doctor scheduling assistant.
The doctor said: "{user_message}"

Provide a friendly, short response.
Explain that you can help with:
- creating availability slots
- viewing schedule
- deleting availability
- viewing appointments
- canceling appointments
        """
        text = generate_ai_response(prompt)
        if not text:
            text = "I'm here to help you manage your schedule. Try saying 'show my availability'."
        return make_response(jsonify({"response": text}), 200)

    # -----------------------------------------------------------------------
    # CREATE AVAILABILITY
    # -----------------------------------------------------------------------

    def _handle_create_availability(self, doctor_profile, user_message, entities):
        today = date.today()

        dates = entities.get("dates", [])
        times = entities.get("times", {})
        recurrence = entities.get("recurrence", {})

        # Regex fallback for date and time if LLM fails
        import re
        msg = user_message.lower()
        # Try to extract date keywords
        if not dates:
            if "tomorrow" in msg:
                dates = [(today + timedelta(days=1)).strftime("%Y-%m-%d")]
            elif "today" in msg:
                dates = [today.strftime("%Y-%m-%d")]
            else:
                # Try to extract weekday (e.g., monday)
                weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
                for i, wd in enumerate(weekdays):
                    if wd in msg:
                        days_ahead = (i - today.weekday() + 7) % 7
                        if days_ahead == 0:
                            days_ahead = 7
                        target_date = today + timedelta(days=days_ahead)
                        dates = [target_date.strftime("%Y-%m-%d")]
                        break

        # Try to extract time range (e.g., 9am to 5pm, 3:00 pm to 4:47 pm, 10:00 to 16:00)
        if not times or "start" not in times or "end" not in times:
            # Pattern to match: "3:00 pm", "3 pm", "3pm", "15:00", etc.
            # Matches: hour:minute am/pm OR hour am/pm OR hour:minute (24h)
            time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*(?:to|-)\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?'
            time_match = re.search(time_pattern, msg, re.IGNORECASE)
            if time_match:
                start_hr = int(time_match.group(1))
                start_min = time_match.group(2) or "00"
                start_ampm = (time_match.group(3) or "").lower()
                end_hr = int(time_match.group(4))
                end_min = time_match.group(5) or "00"
                end_ampm = (time_match.group(6) or "").lower()
                
                def to_24h(hr, ampm, min_str="00"):
                    hr_int = int(hr)
                    min_int = int(min_str)
                    if ampm == "pm" and hr_int != 12:
                        hr_int = hr_int + 12
                    elif ampm == "am" and hr_int == 12:
                        hr_int = 0
                    return hr_int, min_int
                
                start_24_hr, start_24_min = to_24h(start_hr, start_ampm, start_min)
                end_24_hr, end_24_min = to_24h(end_hr, end_ampm, end_min)
                
                times = {
                    "start": f"{start_24_hr:02d}:{start_24_min:02d}",
                    "end": f"{end_24_hr:02d}:{end_24_min:02d}"
                }

        # Handle recurring patterns
        if recurrence and recurrence.get("type"):
            # Expand recurring pattern to dates
            expanded_dates = expand_recurring_dates(recurrence, today)
            if expanded_dates:
                dates = [d.strftime("%Y-%m-%d") for d in expanded_dates]
            else:
                return make_response(jsonify({
                    "response": "I couldn't understand the recurring pattern. Please specify dates or a clear pattern like 'every Monday' or 'weekdays'."
                }), 200)

        # Not enough info
        if not dates or "start" not in times or "end" not in times:
            return make_response(jsonify({
                "response": (
                    "Sure! To create availability, tell me the date and time.\n"
                    "Examples:\n"
                    "- 'create availability tomorrow 9am to 5pm'\n"
                    "- 'every Monday 9am to 5pm'\n"
                    "- 'weekdays 10am to 4pm'"
                )
            }), 200)

        try:
            start_t = datetime.strptime(times["start"], "%H:%M").time()
            end_t = datetime.strptime(times["end"], "%H:%M").time()
        except:
            return make_response(jsonify({
                "response": "Invalid time format. Please use format like '9am to 5pm' or '09:00 to 17:00'."
            }), 200)

        # Validate time range
        is_valid, error_msg = validate_time_range(start_t, end_t)
        if not is_valid:
            return make_response(jsonify({
                "response": f"❌ {error_msg}"
            }), 200)

        created_slots = []
        errors = []
        warnings = []

        for d in dates:
            try:
                target_date = datetime.strptime(d, "%Y-%m-%d").date()
            except:
                errors.append(f"Invalid date: {d}")
                continue

            if target_date < today:
                errors.append(f"Cannot create slot for past date: {target_date.strftime('%b %d')}")
                continue

            # Check for appointment conflicts
            appointment_conflicts = check_appointment_conflicts(doctor_profile, target_date, start_t, end_t)
            if appointment_conflicts:
                conflict_times = [a.appointment_time.strftime('%I:%M %p') for a in appointment_conflicts]
                warnings.append(
                    f"⚠️ {target_date.strftime('%b %d')}: You have appointments at {', '.join(conflict_times)}. "
                    f"Availability will be created anyway, but these times may conflict."
                )

            # Check for overlapping availability slots
            overlapping = detect_overlapping_slots(doctor_profile, target_date, start_t, end_t)
            if overlapping:
                overlap_info = [f"{s.start_time.strftime('%I:%M %p')}-{s.end_time.strftime('%I:%M %p')}" for s in overlapping]
                warnings.append(
                    f"⚠️ {target_date.strftime('%b %d')}: Overlaps with existing slots ({', '.join(overlap_info)}). "
                    f"Creating new slot anyway."
                )

            # Check for exact duplicate
            exists = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id,
                date=target_date,
                start_time=start_t,
                end_time=end_t
            ).first()

            if exists:
                errors.append(f"Slot already exists on {target_date.strftime('%b %d')} ({start_t.strftime('%I:%M %p')} - {end_t.strftime('%I:%M %p')})")
                continue

            # Create single slot for the entire time range
            slot = DoctorAvailability(
                doctor_profile_id=doctor_profile.id,
                date=target_date,
                start_time=start_t,
                end_time=end_t,
                is_booked=False
            )
            db.session.add(slot)

            created_slots.append({
                "date": str(target_date),
                "date_formatted": target_date.strftime('%A, %b %d'),
                "start_time": start_t.strftime('%H:%M'),
                "end_time": end_t.strftime('%H:%M')
            })

        if created_slots:
            db.session.commit()
            
            # Build response message
            response_parts = []
            
            if len(created_slots) == 1:
                slot = created_slots[0]
                # Format time for display
                start_formatted = datetime.strptime(slot['start_time'], "%H:%M").strftime('%I:%M %p').lstrip('0')
                end_formatted = datetime.strptime(slot['end_time'], "%H:%M").strftime('%I:%M %p').lstrip('0')
                response_parts.append(
                    f"✅ Created availability: {slot['date_formatted']} "
                    f"({start_formatted} - {end_formatted})"
                )
            else:
                response_parts.append(
                    f"✅ Created {len(created_slots)} availability slots"
                )
                if recurrence:
                    response_parts.append(f"for recurring pattern")
                else:
                    unique_dates = len(set(s['date'] for s in created_slots))
                    if unique_dates > 1:
                        response_parts.append(f"across {unique_dates} dates")
            
            if warnings:
                response_parts.append("\n\n" + "\n".join(warnings[:3]))  # Show max 3 warnings

            return make_response(jsonify({
                "response": "\n".join(response_parts),
                "created_slots": created_slots
            }), 200)

        # Nothing created
        if errors:
            error_msg = errors[0] if len(errors) == 1 else f"{len(errors)} errors occurred"
            return make_response(jsonify({
                "response": f"❌ Couldn't create slots. {error_msg}"
            }), 200)
        
        return make_response(jsonify({
            "response": "❌ Couldn't create slots. All requested slots already exist or conflict with appointments."
        }), 200)

    # -----------------------------------------------------------------------
    # VIEW AVAILABILITY
    # -----------------------------------------------------------------------
    def _handle_view_availability(self, doctor_profile, user_message, entities):
        today = date.today()

        slots = DoctorAvailability.query.filter_by(
            doctor_profile_id=doctor_profile.id
        ).filter(
            DoctorAvailability.date >= today
        ).order_by(
            DoctorAvailability.date,
            DoctorAvailability.start_time
        ).all()

        if not slots:
            return make_response(jsonify({
                "response": (
                    "📭 You don't have any upcoming availability.\n"
                    "Try: 'create availability tomorrow 9am to 4pm'"
                )
            }), 200)

        lines = []
        for s in slots:
            status = "🔴 Booked" if s.is_booked else "🟢 Available"
            lines.append(
                f"• Slot #{s.id}: {s.date} {s.start_time.strftime('%H:%M')} - {s.end_time.strftime('%H:%M')} ({status})"
            )

        return make_response(jsonify({
            "response": "📅 Your availability:\n\n" + "\n".join(lines)
        }), 200)

    # -----------------------------------------------------------------------
    # DELETE AVAILABILITY
    # -----------------------------------------------------------------------
    def _handle_delete_availability(self, doctor_profile, user_message, entities):
        today = date.today()

        slot_ids = entities.get("slot_ids", [])
        dates = entities.get("dates", [])

        # Regex fallback (delete slot 5, delete slot #5)
        if not slot_ids:
            import re
            matches = re.findall(r"slot\s*#?\s*(\d+)", user_message.lower())
            slot_ids = [int(m) for m in matches] if matches else []

        # Try to find slots by date if no IDs provided
        if not slot_ids and dates:
            for d_str in dates:
                try:
                    target_date = datetime.strptime(d_str, "%Y-%m-%d").date()
                    matching_slots = DoctorAvailability.query.filter_by(
                        doctor_profile_id=doctor_profile.id,
                        date=target_date
                    ).filter(
                        DoctorAvailability.date >= today
                    ).all()
                    slot_ids.extend([s.id for s in matching_slots])
                except:
                    pass

        # If still empty → show list to user
        if not slot_ids:
            slots = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id
            ).filter(
                DoctorAvailability.date >= today
            ).order_by(
                DoctorAvailability.date,
                DoctorAvailability.start_time
            ).all()

            if not slots:
                return make_response(jsonify({
                    "response": "📭 You don't have any slots to delete."
                }), 200)

            listing = "\n".join(
                f"• Slot #{s.id}: {s.date.strftime('%A, %b %d')} {s.start_time.strftime('%I:%M %p')} - {s.end_time.strftime('%I:%M %p')} {'🔴 Booked' if s.is_booked else '🟢 Available'}"
                for s in slots[:15]
            )

            return make_response(jsonify({
                "response": (
                    "Which slot would you like to delete?\n\n"
                    f"{listing}\n\n"
                    "Examples:\n"
                    "- 'delete slot 4'\n"
                    "- 'delete slot #5'\n"
                    "- 'delete tomorrow's slot'"
                )
            }), 200)

        deleted = []
        errors = []
        for sid in slot_ids:
            slot = DoctorAvailability.query.filter_by(
                id=sid,
                doctor_profile_id=doctor_profile.id
            ).first()

            if not slot:
                errors.append(f"Slot #{sid} not found")
                continue

            if slot.is_booked:
                errors.append(f"Slot #{sid} cannot be deleted — it has a booking")
                continue

            db.session.delete(slot)
            deleted.append({
                "id": sid,
                "date": slot.date.strftime('%A, %b %d'),
                "time": f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
            })

        if deleted:
            db.session.commit()
            deleted_info = ", ".join([f"#{d['id']} ({d['date']})" for d in deleted])
            return make_response(jsonify({
                "response": f"🗑️ Successfully deleted slot(s): {deleted_info}"
            }), 200)

        if errors:
            return make_response(jsonify({
                "response": f"❌ {errors[0]}"
            }), 200)

        return make_response(jsonify({
            "response": "❌ No matching slots found."
        }), 200)

    # -----------------------------------------------------------------------
    # VIEW APPOINTMENTS
    # -----------------------------------------------------------------------
    def _handle_view_appointments(self, doctor_profile, user_message, entities):
        today = date.today()

        appointments = Appointment.query.filter_by(
            doctor_id=doctor_profile.user_id,
            status="BOOKED"
        ).filter(
            Appointment.appointment_date >= today
        ).order_by(
            Appointment.appointment_date,
            Appointment.appointment_time
        ).all()

        if not appointments:
            return make_response(jsonify({
                "response": "📭 You have no upcoming appointments."
            }), 200)

        lines = []
        for a in appointments:
            p = User.query.get(a.patient_id)
            patient_name = p.username if p else "Unknown"
            lines.append(
                f"• Appt #{a.id}: {a.appointment_date} at {a.appointment_time.strftime('%H:%M')} — Patient: {patient_name}"
            )

        return make_response(jsonify({
            "response": "📋 Your appointments:\n\n" + "\n".join(lines)
        }), 200)

    # -----------------------------------------------------------------------
    # CANCEL APPOINTMENT
    # -----------------------------------------------------------------------
    def _handle_cancel_appointment(self, doctor_profile, user_message, entities):
        appointment_ids = entities.get("appointment_ids", [])

        # If none provided → show list
        if not appointment_ids:
            appts = Appointment.query.filter_by(
                doctor_id=doctor_profile.user_id,
                status="BOOKED"
            ).order_by(
                Appointment.appointment_date
            ).all()

            if not appts:
                return make_response(jsonify({"response": "You have no appointments to cancel."}), 200)

            listing = "\n".join(
                f"• Appt #{a.id}: {a.appointment_date} at {a.appointment_time.strftime('%H:%M')}"
                for a in appts[:10]
            )

            return make_response(jsonify({
                "response": (
                    "Which appointment do you want to cancel?\n\n"
                    f"{listing}\n\n"
                    "Example: 'cancel appointment 3'"
                )
            }), 200)

        cancelled = []

        for appt_id in appointment_ids:
            appt = Appointment.query.filter_by(
                id=appt_id,
                doctor_id=doctor_profile.user_id
            ).first()

            if not appt or appt.status != "BOOKED":
                continue

            appt.status = "CANCELLED"

            # free slot
            slot = DoctorAvailability.query.filter_by(
                doctor_profile_id=doctor_profile.id,
                date=appt.appointment_date,
                is_booked=True
            ).filter(
                DoctorAvailability.start_time <= appt.appointment_time,
                DoctorAvailability.end_time > appt.appointment_time
            ).first()

            if slot:
                slot.is_booked = False

            cancelled.append(appt_id)

        if cancelled:
            db.session.commit()
            return make_response(jsonify({
                "response": f"🛑 Cancelled appointment(s): {', '.join(map(str, cancelled))}"
            }), 200)

        return make_response(jsonify({
            "response": "❌ No matching appointments found to cancel."
        }), 200)
