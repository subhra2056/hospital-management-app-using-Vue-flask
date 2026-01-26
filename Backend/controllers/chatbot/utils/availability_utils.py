"""
Smart Availability Utilities - Conflict detection, slot splitting, recurring patterns
"""
from datetime import date, datetime, timedelta, time
from Backend.controllers.models import DoctorAvailability, Appointment


def check_time_overlap(start1: time, end1: time, start2: time, end2: time) -> bool:
    """
    Check if two time ranges overlap.
    
    Args:
        start1, end1: First time range
        start2, end2: Second time range
    
    Returns:
        True if ranges overlap, False otherwise
    """
    # Convert times to datetime for comparison (using same date)
    base_date = date.today()
    dt1_start = datetime.combine(base_date, start1)
    dt1_end = datetime.combine(base_date, end1)
    dt2_start = datetime.combine(base_date, start2)
    dt2_end = datetime.combine(base_date, end2)
    
    # Check overlap: ranges overlap if start1 < end2 and start2 < end1
    return dt1_start < dt2_end and dt2_start < dt1_end


def split_availability_window(start_time: time, end_time: time, slot_duration_minutes: int = 30) -> list:
    """
    Split a time window into smaller appointment slots.
    
    Args:
        start_time: Start of availability window
        end_time: End of availability window
        slot_duration_minutes: Duration of each slot in minutes (default: 30)
    
    Returns:
        List of tuples: [(start_time, end_time), ...]
    """
    slots = []
    base_date = date.today()
    current = datetime.combine(base_date, start_time)
    end_dt = datetime.combine(base_date, end_time)
    
    while current < end_dt:
        slot_end = current + timedelta(minutes=slot_duration_minutes)
        if slot_end > end_dt:
            slot_end = end_dt
        
        slots.append((current.time(), slot_end.time()))
        current = slot_end
    
    return slots


def check_appointment_conflicts(doctor_profile, target_date: date, start_time: time, end_time: time) -> list:
    """
    Check if the requested availability conflicts with existing appointments.
    
    Args:
        doctor_profile: DoctorProfile instance
        target_date: Date to check
        start_time: Start time of availability
        end_time: End time of availability
    
    Returns:
        List of conflicting appointments: [Appointment, ...]
    """
    conflicts = []
    
    appointments = Appointment.query.filter_by(
        doctor_id=doctor_profile.user_id,
        appointment_date=target_date,
        status="BOOKED"
    ).all()
    
    for appointment in appointments:
        appt_time = appointment.appointment_time
        # Check if appointment time falls within the availability window
        if start_time <= appt_time < end_time:
            conflicts.append(appointment)
    
    return conflicts


def detect_overlapping_slots(doctor_profile, target_date: date, start_time: time, end_time: time) -> list:
    """
    Find existing availability slots that overlap with the requested time range.
    
    Args:
        doctor_profile: DoctorProfile instance
        target_date: Date to check
        start_time: Start time of requested availability
        end_time: End time of requested availability
    
    Returns:
        List of overlapping availability slots: [DoctorAvailability, ...]
    """
    overlapping = []
    
    existing_slots = DoctorAvailability.query.filter_by(
        doctor_profile_id=doctor_profile.id,
        date=target_date
    ).all()
    
    for slot in existing_slots:
        if check_time_overlap(start_time, end_time, slot.start_time, slot.end_time):
            overlapping.append(slot)
    
    return overlapping


def expand_recurring_dates(pattern: dict, start_date: date = None, weeks_ahead: int = 8) -> list:
    """
    Expand recurring patterns into specific dates.
    
    Args:
        pattern: Dict with keys:
            - "type": "daily", "weekly", "weekdays", "custom"
            - "days": List of weekday names (for weekly/custom) e.g., ["monday", "wednesday"]
            - "end_date": Optional end date (defaults to weeks_ahead)
        start_date: Starting date (defaults to today)
        weeks_ahead: Number of weeks to look ahead (default: 8)
    
    Returns:
        List of dates: [date, ...]
    """
    if start_date is None:
        start_date = date.today()
    
    dates = []
    pattern_type = pattern.get("type", "").lower()
    days = pattern.get("days", [])
    end_date = pattern.get("end_date")
    
    if end_date:
        try:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except:
            end_date = start_date + timedelta(weeks=weeks_ahead)
    else:
        end_date = start_date + timedelta(weeks=weeks_ahead)
    
    weekday_map = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }
    
    current_date = start_date
    
    if pattern_type == "daily":
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
    
    elif pattern_type == "weekdays":
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Monday = 0, Friday = 4
                dates.append(current_date)
            current_date += timedelta(days=1)
    
    elif pattern_type == "weekly" and days:
        target_weekdays = [weekday_map.get(day.lower()) for day in days if day.lower() in weekday_map]
        if not target_weekdays:
            return dates
        
        # Find all occurrences of target weekdays within the date range
        check_date = start_date
        while check_date <= end_date:
            if check_date.weekday() in target_weekdays:
                dates.append(check_date)
            check_date += timedelta(days=1)
    
    elif pattern_type == "custom" and days:
        target_weekdays = [weekday_map.get(day.lower()) for day in days if day.lower() in weekday_map]
        if not target_weekdays:
            return dates
        
        # Find all occurrences of target weekdays within the date range
        check_date = start_date
        while check_date <= end_date:
            if check_date.weekday() in target_weekdays:
                dates.append(check_date)
            check_date += timedelta(days=1)
    
    # Sort and remove duplicates
    dates = sorted(list(set(dates)))
    return dates


def validate_time_range(start_time: time, end_time: time) -> tuple[bool, str]:
    """
    Validate that a time range is reasonable.
    
    Args:
        start_time: Start time
        end_time: End time
    
    Returns:
        Tuple: (is_valid, error_message)
    """
    if end_time <= start_time:
        return False, "End time must be after start time"
    
    # Check minimum duration (at least 15 minutes)
    base_date = date.today()
    start_dt = datetime.combine(base_date, start_time)
    end_dt = datetime.combine(base_date, end_time)
    duration = (end_dt - start_dt).total_seconds() / 60
    
    if duration < 15:
        return False, "Availability window must be at least 15 minutes"
    
    if duration > 12 * 60:  # 12 hours
        return False, "Availability window cannot exceed 12 hours"
    
    return True, ""
