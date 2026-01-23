"""
Script to clean up duplicate and orphaned availability slots.
Run this once to remove existing duplicates and stale booked slots.
"""
from app import create_app
from Backend.controllers.database import db
from Backend.controllers.models import DoctorAvailability, Appointment, DoctorProfile
from sqlalchemy import func

app, api = create_app()

with app.app_context():
    # 1. Find and delete duplicates - keep the first one (lowest id) and delete the rest
    subquery = db.session.query(
        DoctorAvailability.doctor_profile_id,
        DoctorAvailability.date,
        DoctorAvailability.start_time,
        DoctorAvailability.end_time,
        func.min(DoctorAvailability.id).label('min_id')
    ).group_by(
        DoctorAvailability.doctor_profile_id,
        DoctorAvailability.date,
        DoctorAvailability.start_time,
        DoctorAvailability.end_time
    ).subquery()
    
    duplicates = DoctorAvailability.query.filter(
        ~DoctorAvailability.id.in_(
            db.session.query(subquery.c.min_id)
        )
    ).all()
    
    if duplicates:
        print(f"Found {len(duplicates)} duplicate availability slots")
        for dup in duplicates:
            db.session.delete(dup)
        db.session.commit()
        print(f"✅ Deleted {len(duplicates)} duplicate slots")
    else:
        print("✅ No duplicate availability slots found")
    
    # 2. Find booked availabilities without active appointments (orphaned)
    booked_slots = DoctorAvailability.query.filter_by(is_booked=True).all()
    orphaned_count = 0
    
    for slot in booked_slots:
        doctor_profile = DoctorProfile.query.get(slot.doctor_profile_id)
        if not doctor_profile:
            db.session.delete(slot)
            orphaned_count += 1
            continue
            
        # Check if there's an active (BOOKED) appointment for this slot
        active_appointment = Appointment.query.filter_by(
            doctor_id=doctor_profile.user_id,
            appointment_date=slot.date,
            appointment_time=slot.start_time,
            status="BOOKED"
        ).first()
        
        if not active_appointment:
            print(f"  Removing orphaned slot: Date {slot.date}, Time {slot.start_time}")
            db.session.delete(slot)
            orphaned_count += 1
    
    if orphaned_count > 0:
        db.session.commit()
        print(f"✅ Deleted {orphaned_count} orphaned booked slots")
    else:
        print("✅ No orphaned booked slots found")
    
    print("\nCleanup complete!")
