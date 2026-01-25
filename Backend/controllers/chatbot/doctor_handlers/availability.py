"""
Doctor Availability Handlers - Create, view, update, and delete availability slots
"""
from flask import jsonify, make_response
from datetime import datetime
from Backend.controllers.models import DoctorAvailability
from Backend.controllers.database import db
from Backend.controllers.chatbot.ai_client import generate_ai_response


def handle_create_availability(doctor_profile, entities, today, ai_ack=""):
    """Create new availability slots"""
    dates = entities.get("dates", [])
    times = entities.get("times") or {}  # Handle None case
    start_time_str = times.get("start") if times else None
    end_time_str = times.get("end") if times else None
    
    # Parse dates
    target_dates = []
    for d_str in dates:
        try:
            target_dates.append(datetime.strptime(d_str, '%Y-%m-%d').date())
        except:
            pass
    
    # Parse times
    start_time = end_time = None
    if start_time_str and end_time_str:
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except:
            pass
    
    if not target_dates or not start_time or not end_time:
        return make_response(jsonify({
            "response": "I need more details. Please specify both the date(s) and time range. For example: 'tomorrow 9am to 5pm'"
        }), 200)
    
    created_slots = []
    errors = []
    
    for target_date in target_dates:
        if target_date < today:
            errors.append(f"Cannot create slot for past date: {target_date.strftime('%b %d')}")
            continue
        
        existing = DoctorAvailability.query.filter_by(
            doctor_profile_id=doctor_profile.id,
            date=target_date,
            start_time=start_time,
            end_time=end_time
        ).first()
        
        if existing:
            errors.append(f"Slot already exists for {target_date.strftime('%b %d')}")
            continue
        
        availability = DoctorAvailability(
            doctor_profile_id=doctor_profile.id,
            date=target_date,
            start_time=start_time,
            end_time=end_time,
            is_booked=False
        )
        db.session.add(availability)
        created_slots.append({
            "date": str(target_date),
            "date_formatted": target_date.strftime('%A, %b %d'),
            "start_time": start_time.strftime('%I:%M %p'),
            "end_time": end_time.strftime('%I:%M %p')
        })
    
    if created_slots:
        db.session.commit()
    
    # Generate AI response
    try:
        if created_slots:
            slots_list = ", ".join([f"{s['date_formatted']} ({s['start_time']}-{s['end_time']})" for s in created_slots])
            prompt = f"Successfully created {len(created_slots)} availability slots: {slots_list}. Write an enthusiastic confirmation (2 sentences)."
        else:
            prompt = f"Failed to create slots. Errors: {'; '.join(errors)}. Write a helpful apology (2 sentences)."
        
        response_text = generate_ai_response(prompt, temperature=0.9)
        return make_response(jsonify({"response": response_text, "created_slots": created_slots}), 200)
    except:
        if created_slots:
            return make_response(jsonify({"response": f"✅ Created {len(created_slots)} slots!", "created_slots": created_slots}), 200)
        return make_response(jsonify({"response": "❌ " + (errors[0] if errors else "Couldn't create slots")}), 200)


def handle_view_availability(slots, ai_ack=""):
    """Show doctor's availability slots"""
    try:
        if slots:
            slots_info = "\n".join([
                f"- {s.date.strftime('%A, %b %d')} from {s.start_time.strftime('%I:%M %p')} to {s.end_time.strftime('%I:%M %p')} ({'Booked' if s.is_booked else 'Available'})"
                for s in slots
            ])
            prompt = f"""Doctor asked to view their availability. They have {len(slots)} upcoming slots:

{slots_info}

Write a friendly summary (2-3 sentences) highlighting key information. Mention how many are booked vs available."""
        else:
            prompt = "Doctor asked to view availability but has NONE. Encourage them to create some (1-2 sentences)."
        
        response_text = generate_ai_response(prompt, temperature=0.9)
        return make_response(jsonify({"response": response_text}), 200)
    except:
        if slots:
            return make_response(jsonify({"response": f"You have {len(slots)} upcoming availability slots."}), 200)
        return make_response(jsonify({"response": "You don't have any upcoming availability slots yet."}), 200)


def handle_delete_availability(doctor_profile, entities, slots, ai_ack=""):
    """Delete availability slots"""
    slot_ids = entities.get("slot_ids", [])
    dates = entities.get("dates", [])
    
    # Try to match slots by date if no IDs
    if not slot_ids and dates:
        for d_str in dates:
            try:
                target_date = datetime.strptime(d_str, '%Y-%m-%d').date()
                matching = [s for s in slots if s.date == target_date and not s.is_booked]
                slot_ids.extend([s.id for s in matching])
            except:
                pass
    
    if not slot_ids:
        return make_response(jsonify({
            "response": "Which slot(s) should I delete? Specify the date like 'delete tomorrow's slot' or 'remove Jan 27 availability'."
        }), 200)
    
    deleted = []
    errors = []
    
    for slot_id in slot_ids:
        slot = DoctorAvailability.query.filter_by(
            id=slot_id,
            doctor_profile_id=doctor_profile.id
        ).first()
        
        if slot:
            if slot.is_booked:
                errors.append(f"Cannot delete booked slot on {slot.date.strftime('%b %d')}")
            else:
                db.session.delete(slot)
                deleted.append(slot.date.strftime('%A, %b %d'))
    
    if deleted:
        db.session.commit()
    
    try:
        if deleted:
            prompt = f"Deleted {len(deleted)} availability slot(s): {', '.join(deleted)}. Write a confirmation (1-2 sentences)."
        else:
            prompt = f"Couldn't delete slots. Issues: {'; '.join(errors) if errors else 'Not found'}. Write a brief explanation (1-2 sentences)."
        
        response_text = generate_ai_response(prompt, temperature=0.9)
        return make_response(jsonify({"response": response_text}), 200)
    except:
        if deleted:
            return make_response(jsonify({"response": f"🗑️ Deleted {len(deleted)} slot(s)"}), 200)
        return make_response(jsonify({"response": errors[0] if errors else "Couldn't find slots to delete"}), 200)


def handle_update_availability(doctor_profile, entities, slots, ai_ack=""):
    """Update existing availability slots"""
    slot_ids = entities.get("slot_ids", [])
    new_dates = entities.get("dates", [])
    new_times = entities.get("times", {})
    
    if not slot_ids and len(slots) > 0:
        # If no IDs, try to infer from dates mentioned
        for d_str in new_dates:
            try:
                target_date = datetime.strptime(d_str, '%Y-%m-%d').date()
                matching = [s for s in slots if s.date == target_date]
                slot_ids.extend([s.id for s in matching])
            except:
                pass
    
    if not slot_ids:
        return make_response(jsonify({
            "response": "Which slot do you want to update? Please specify the date or say 'first slot', 'tomorrow's slot', etc."
        }), 200)
    
    updated = []
    for slot_id in slot_ids:
        slot = DoctorAvailability.query.filter_by(
            id=slot_id,
            doctor_profile_id=doctor_profile.id
        ).first()
        
        if slot:
            # Update date if provided
            if new_dates:
                try:
                    slot.date = datetime.strptime(new_dates[0], '%Y-%m-%d').date()
                except:
                    pass
            
            # Update times if provided
            if new_times.get("start"):
                try:
                    slot.start_time = datetime.strptime(new_times["start"], '%H:%M').time()
                except:
                    pass
            if new_times.get("end"):
                try:
                    slot.end_time = datetime.strptime(new_times["end"], '%H:%M').time()
                except:
                    pass
            
            updated.append(slot)
    
    if updated:
        db.session.commit()
        try:
            prompt = f"Updated {len(updated)} availability slot(s) successfully. Write a brief confirmation (1-2 sentences)."
            response_text = generate_ai_response(prompt, temperature=0.9)
            return make_response(jsonify({"response": response_text}), 200)
        except:
            return make_response(jsonify({"response": f"✅ Updated {len(updated)} slot(s)!"}), 200)
    
    return make_response(jsonify({"response": "Couldn't find the slots to update. Try being more specific."}), 200)
