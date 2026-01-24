import requests
import random
import sys
from faker import Faker

fake = Faker()

BASE_URL = "http://localhost:5000/api"

# Specializations mapped by department name
specializations = {
    "Cardiology": ["Cardiac Surgery", "Interventional Cardiology", "Heart Failure Specialist"],
    "Neurology": ["Neuro Surgery", "Epilepsy Specialist", "Stroke Medicine"],
    "Orthopedics": ["Joint Replacement", "Sports Medicine", "Spine Surgery"],
    "Pediatrics": ["Neonatology", "Pediatric Cardiology", "Pediatric Surgery"],
    "Dermatology": ["Cosmetic Dermatology", "Dermatopathology", "Pediatric Dermatology"],
    "Oncology": ["Medical Oncology", "Radiation Oncology", "Surgical Oncology"],
    "Psychiatry": ["Child Psychiatry", "Addiction Medicine", "Forensic Psychiatry"],
    "General Medicine": ["Internal Medicine", "Family Medicine", "Emergency Medicine"],
    "Surgery": ["General Surgery", "Laparoscopic Surgery", "Trauma Surgery"],
    "Gynecology": ["Reproductive Medicine", "Gynecologic Oncology", "Maternal-Fetal Medicine"],
    "Ophthalmology": ["Retina Specialist", "Cornea Specialist", "Glaucoma Specialist"],
    "ENT": ["Head and Neck Surgery", "Otology", "Rhinology"]
}

genders = ["Male", "Female"]


def print_header(text):
    """Print a formatted header"""
    print()
    print("=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_success(text):
    """Print success message"""
    print(f"  ✅ {text}")


def print_error(text):
    """Print error message"""
    print(f"  ❌ {text}")


def print_info(text):
    """Print info message"""
    print(f"  ℹ️  {text}")


def check_server():
    """Check if the Flask server is running"""
    try:
        response = requests.get(BASE_URL.replace('/api', ''), timeout=5)
        return True
    except:
        return False


def login_admin():
    """Login as admin and return the access token"""
    data = {
        "email": "admin@gmail.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result.get("access_token")
        else:
            print_error(f"Admin login failed: {response.json().get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print_error(f"Error logging in as admin: {e}")
        return None


def get_departments(token):
    """Fetch all departments from the API"""
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Try the correct endpoint: /departments
        response = requests.get(f"{BASE_URL}/departments", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Response format is {"departments": [...]}
            return data.get("departments", [])
        else:
            print_error(f"API returned status {response.status_code}: {response.text[:100]}")
            return []
    except Exception as e:
        print_error(f"Error fetching departments: {e}")
        return []


def register_patient():
    """Register a single patient"""
    gender = random.choice(genders)
    
    # Generate gender-appropriate names
    if gender == "Male":
        name = fake.name_male()
    else:
        name = fake.name_female()
    
    data = {
        "username": name,
        "email": fake.unique.email(),
        "password": "password123",
        "age": random.randint(18, 75),
        "gender": gender,
        "phone": f"{random.randint(7000000000, 9999999999)}",
        "address": fake.address().replace('\n', ', ')
    }
    
    try:
        response = requests.post(f"{BASE_URL}/patient/register", json=data, timeout=10)
        if response.status_code == 201:
            return True, data['username']
        else:
            error_msg = response.json().get('message', 'Unknown error')
            return False, error_msg
    except Exception as e:
        return False, str(e)


def register_doctor(token, departments):
    """Register a single doctor (requires admin token)"""
    if not departments:
        return False, "No departments available"
    
    # Pick a random department
    department = random.choice(departments)
    department_id = department['id']
    department_name = department['name']
    
    # Get specialization for this department
    if department_name in specializations:
        specialization = random.choice(specializations[department_name])
    else:
        specialization = f"{department_name} Specialist"
    
    gender = random.choice(genders)
    
    # Generate gender-appropriate names with Dr. prefix
    if gender == "Male":
        name = f"Dr. {fake.name_male()}"
    else:
        name = f"Dr. {fake.name_female()}"
    
    data = {
        "username": name,
        "email": fake.unique.email(),
        "password": "password123",
        "department_id": department_id,
        "specialization": specialization,
        "experience_years": random.randint(2, 25),
        "gender": gender
    }
    
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{BASE_URL}/doctor/register", json=data, headers=headers, timeout=10)
        
        if response.status_code == 201:
            return True, f"{data['username']} ({department_name})"
        else:
            error_msg = response.json().get('message', 'Unknown error')
            return False, error_msg
    except Exception as e:
        return False, str(e)


def get_valid_number(prompt, default=10, min_val=0, max_val=100):
    """Get a valid number from user input"""
    while True:
        try:
            user_input = input(f"  {prompt} (default: {default}): ").strip()
            if user_input == "":
                return default
            
            num = int(user_input)
            if min_val <= num <= max_val:
                return num
            else:
                print_error(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print_error("Please enter a valid number")


def main():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "🏥 MEDICORE - Data Seeding Tool" + " " * 16 + "║")
    print("║" + " " * 15 + "Hospital Management System" + " " * 17 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Check server
    print_header("Checking Server Connection")
    if not check_server():
        print_error("Server is not running!")
        print_info("Please start the Flask server first: python app.py")
        sys.exit(1)
    print_success("Server is running")
    
    # Login as admin
    print_header("Admin Authentication")
    print_info("Logging in as admin...")
    token = login_admin()
    
    if not token:
        print_error("Failed to login as admin!")
        print_info("Make sure admin account exists with:")
        print_info("  Email: admin@gmail.com")
        print_info("  Password: password123")
        sys.exit(1)
    print_success("Admin authenticated successfully")
    
    # Fetch departments
    print_header("Fetching Departments")
    departments = get_departments(token)
    
    if not departments:
        print_error("No departments found!")
        print_info("Please add departments first before adding doctors")
        print_info("Continuing with patient registration only...")
        can_add_doctors = False
    else:
        print_success(f"Found {len(departments)} departments:")
        for dept in departments:
            print(f"      • {dept['name']}")
        can_add_doctors = True
    
    # Get user input
    print_header("Configuration")
    
    if can_add_doctors:
        num_doctors = get_valid_number("How many doctors to add?", default=10, min_val=0, max_val=50)
    else:
        num_doctors = 0
        print_info("Doctor registration skipped (no departments)")
    
    num_patients = get_valid_number("How many patients to add?", default=20, min_val=0, max_val=100)
    
    if num_doctors == 0 and num_patients == 0:
        print_info("No users to add. Exiting...")
        sys.exit(0)
    
    # Confirm
    print()
    print(f"  📋 Summary: {num_doctors} doctors + {num_patients} patients")
    confirm = input("  Proceed? (Y/n): ").strip().lower()
    if confirm == 'n':
        print_info("Cancelled by user")
        sys.exit(0)
    
    # Register Doctors
    doctor_success = 0
    doctor_failed = 0
    
    if num_doctors > 0:
        print_header(f"Registering {num_doctors} Doctors")
        
        for i in range(num_doctors):
            success, result = register_doctor(token, departments)
            if success:
                doctor_success += 1
                print_success(f"[{doctor_success}/{num_doctors}] {result}")
            else:
                doctor_failed += 1
                print_error(f"Failed: {result}")
    
    # Register Patients
    patient_success = 0
    patient_failed = 0
    
    if num_patients > 0:
        print_header(f"Registering {num_patients} Patients")
        
        for i in range(num_patients):
            success, result = register_patient()
            if success:
                patient_success += 1
                print_success(f"[{patient_success}/{num_patients}] {result}")
            else:
                patient_failed += 1
                print_error(f"Failed: {result}")
    
    # Final Summary
    print_header("🎉 Seeding Complete!")
    print()
    print(f"  👨‍⚕️ Doctors:  {doctor_success} added, {doctor_failed} failed")
    print(f"  👤 Patients: {patient_success} added, {patient_failed} failed")
    print()
    print("  ─" * 25)
    print()
    print("  🔐 Default Credentials:")
    print("     Email: <generated_email>")
    print("     Password: password123")
    print()
    print("  You can now login with any registered account!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_info("Cancelled by user")
        sys.exit(0)
