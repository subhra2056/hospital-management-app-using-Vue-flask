import requests
import random
from faker import Faker

fake = Faker()
BASE_URL = 'http://localhost:5000/api'

specializations = [
    "Cardiac Surgery",          # Cardiology
    "Neuro Surgery",            # Neurology
    "Joint Replacement",        # Orthopedics
    "Neonatology",              # Pediatrics
    "Cosmetic Dermatology"      # Dermatology
]

genders = ['Male', 'Female']

# Login as admin first
print('Logging in as admin...')
login_resp = requests.post(f'{BASE_URL}/login', json={
    'email': 'admin@gmail.com',
    'password': 'password123'
})

if login_resp.status_code != 200:
    print('Failed to login as admin!')
    exit(1)

token = login_resp.json().get('access_token')
headers = {'Authorization': f'Bearer {token}'}
print('Admin logged in successfully!')

# Get departments (requires auth)
dept_resp = requests.get(f'{BASE_URL}/departments', headers=headers)
departments = dept_resp.json().get('departments', [])
if not departments:
    print('No departments found!')
    exit(1)

print(f'Found {len(departments)} departments')
print()

print('Seeding 3 doctors...')
for i in range(3):
    dept = random.choice(departments)
    data = {
        'username': fake.name(),
        'email': fake.email(),
        'password': 'password123',
        'department_id': dept['id'],
        'specialization': random.choice(specializations),
        'experience_years': random.randint(2, 20),
        'gender': random.choice(genders)
    }
    r = requests.post(f'{BASE_URL}/doctor/register', json=data, headers=headers)
    if r.status_code == 201:
        print(f"  Doctor {i+1}: {data['username']} ({data['email']})")
    else:
        print(f"  Failed: {r.json().get('message', 'error')}")

print()
print('Seeding 3 patients...')
for i in range(3):
    data = {
        'username': fake.name(),
        'email': fake.email(),
        'password': 'password123',
        'age': random.randint(20, 60),
        'gender': random.choice(genders),
        'phone': fake.phone_number()[:15],
        'address': fake.address()
    }
    r = requests.post(f'{BASE_URL}/patient/register', json=data)
    if r.status_code == 201:
        print(f"  Patient {i+1}: {data['username']} ({data['email']})")
    else:
        print(f"  Failed: {r.json().get('message', 'error')}")

print()
print('Done!')
print('Password for all users: password123')
