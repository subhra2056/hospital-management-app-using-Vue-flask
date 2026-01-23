import requests
import random
from faker import Faker

fake = Faker()

BASE_URL = "http://localhost:5000/api"

departments = [
    "Cardiology", "Neurology", "Orthopedics", "Pediatrics", 
    "Dermatology", "Oncology", "Psychiatry", "General Medicine",
    "Surgery", "Gynecology", "Ophthalmology", "ENT"
]

specializations = {
    "Cardiology": ["Cardiac Surgery", "Interventional Cardiology", "Heart Failure"],
    "Neurology": ["Neuro Surgery", "Epilepsy", "Stroke Medicine"],
    "Orthopedics": ["Joint Replacement", "Sports Medicine", "Spine Surgery"],
    "Pediatrics": ["Neonatology", "Pediatric Cardiology", "Pediatric Surgery"],
    "Dermatology": ["Cosmetic Dermatology", "Dermatopathology", "Pediatric Dermatology"],
    "Oncology": ["Medical Oncology", "Radiation Oncology", "Surgical Oncology"],
    "Psychiatry": ["Child Psychiatry", "Addiction Medicine", "Forensic Psychiatry"],
    "General Medicine": ["Internal Medicine", "Family Medicine", "Emergency Medicine"],
    "Surgery": ["General Surgery", "Laparoscopic Surgery", "Trauma Surgery"],
    "Gynecology": ["Reproductive Medicine", "Gynecologic Oncology", "Maternal-Fetal Medicine"],
    "Ophthalmology": ["Retina", "Cornea", "Glaucoma"],
    "ENT": ["Head and Neck Surgery", "Otology", "Rhinology"]
}

genders = ["Male", "Female", "Other"]

def register_doctor():
    department = random.choice(departments)
    specialization = random.choice(specializations[department])
    
    data = {
        "username": fake.name(),
        "email": fake.email(),
        "password": "doctor123",
        "department": department,
        "specialization": specialization,
        "experience_years": random.randint(2, 30),
        "gender": random.choice(genders)
    }
    
    try:
        response = requests.post(f"{BASE_URL}/doctor/register", json=data)
        if response.status_code == 201:
            print(f"✅ Doctor registered: {data['username']} - {specialization}")
            return True
        else:
            print(f"❌ Failed to register doctor: {response.json().get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error registering doctor: {e}")
        return False

def register_patient():
    data = {
        "username": fake.name(),
        "email": fake.email(),
        "password": "patient123",
        "age": random.randint(18, 80),
        "gender": random.choice(genders),
        "phone": fake.phone_number()[:15],
        "address": fake.address()
    }
    
    try:
        response = requests.post(f"{BASE_URL}/patient/register", json=data)
        if response.status_code == 201:
            print(f"✅ Patient registered: {data['username']}")
            return True
        else:
            print(f"❌ Failed to register patient: {response.json().get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Error registering patient: {e}")
        return False

def login_admin():
    data = {
        "email": "admin@gmail.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get("access_token")
        return None
    except Exception as e:
        print(f"❌ Error logging in as admin: {e}")
        return None

def main():
    print("=" * 60)
    print("Hospital Management System - Data Seeding Script")
    print("=" * 60)
    print()
    
    print("Checking if server is running...")
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}")
        print("✅ Server is running")
    except:
        print("❌ Server is not running. Please start Flask server first!")
        print("   Run: python app.py")
        return
    
    print()
    num_doctors = int(input("How many doctors to add? (default: 10): ") or "10")
    num_patients = int(input("How many patients to add? (default: 20): ") or "20")
    
    print()
    print("=" * 60)
    print("Registering Doctors...")
    print("=" * 60)
    
    doctor_count = 0
    for i in range(num_doctors):
        if register_doctor():
            doctor_count += 1
    
    print()
    print("=" * 60)
    print("Registering Patients...")
    print("=" * 60)
    
    patient_count = 0
    for i in range(num_patients):
        if register_patient():
            patient_count += 1
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✅ Successfully registered {doctor_count} doctors")
    print(f"✅ Successfully registered {patient_count} patients")
    print()
    print("Default passwords:")
    print("  - Doctors: doctor123")
    print("  - Patients: patient123")
    print()
    print("You can now login with any registered email and password!")

if __name__ == "__main__":
    main()
