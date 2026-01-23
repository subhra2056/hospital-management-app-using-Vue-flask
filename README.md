# HealthEase - Hospital Management System

A full-stack web application for managing hospital operations including patient appointments, doctor availability, treatments, and administrative tasks.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-brightgreen.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)

## 🏥 Features

### For Patients
- **Account Registration** - Create and manage personal accounts
- **Browse Doctors** - View doctors by department with their specializations
- **Book Appointments** - Select available time slots and book appointments
- **View Appointments** - Track upcoming, pending, and completed appointments
- **Treatment History** - Access past diagnoses, prescriptions, and doctor notes
- **Export Records** - Download treatment history as CSV

### For Doctors
- **Dashboard** - Overview of today's appointments and statistics
- **Set Availability** - Create, edit, and delete available time slots
- **Manage Appointments** - View all appointments (today, upcoming, completed)
- **Add Treatments** - Record diagnosis, prescription, and notes for patients
- **Profile Management** - View and update professional profile

### For Administrators
- **Dashboard** - System-wide statistics and overview
- **Doctor Management** - Add, edit, block/unblock doctors
- **Patient Management** - View, edit, block/unblock patients
- **Department Management** - Create and manage hospital departments
- **Appointments Overview** - Monitor all appointments in the system

### Security Features
- JWT-based authentication
- Session storage for enhanced security (auto-logout on tab close)
- Role-based access control
- Blocked user management

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **Flask** - Web framework
- **Flask-RESTful** - REST API development
- **Flask-JWT-Extended** - JWT authentication
- **Flask-SQLAlchemy** - ORM for database operations
- **SQLite** - Database

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Vite** - Build tool and dev server
- **Bootstrap 5** - CSS framework

## 📁 Project Structure

```
project/
├── app.py                 # Flask application entry point
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
├── Backend/
│   └── controllers/
│       ├── config.py      # Application configuration
│       ├── database.py    # Database initialization
│       ├── models.py      # SQLAlchemy models
│       ├── routes.py      # API endpoints
│       ├── cache.py       # Caching configuration
│       ├── celery_app.py  # Celery for background tasks
│       └── tasks.py       # Background task definitions
├── Frontend/
│   └── frontend/
│       ├── package.json   # Node.js dependencies
│       ├── vite.config.js # Vite configuration
│       └── src/
│           ├── App.vue
│           ├── main.js
│           ├── assets/        # Images and icons
│           ├── components/    # Reusable Vue components
│           ├── forms/         # Form components
│           ├── router/        # Vue Router configuration
│           ├── utils/         # Utility functions (auth)
│           └── views/         # Page components
│               ├── auth/      # Login, Register
│               ├── dashboard/ # Role-based dashboards
│               ├── home/      # Landing page
│               └── profile/   # User profile
└── instance/
    └── database.db        # SQLite database file
```

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/healthease.git
   cd healthease
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database with seed data**
   ```bash
   python seed_data.py
   ```

5. **Run the Flask server**
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd Frontend/frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Run the development server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

## 🔑 Default Login Credentials

After running `seed_data.py`, the following accounts are available:

| Role    | Email              | Password   |
|---------|-------------------|------------|
| Admin   | admin@admin.com   | admin123   |
| Doctor  | doctor@doctor.com | doctor123  |
| Patient | patient@patient.com | patient123 |

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/login` | User login |
| POST | `/api/logout` | User logout |
| POST | `/api/patient/register` | Patient registration |

### Patient APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/profile` | Get user profile |
| PUT | `/api/user/profile` | Update user profile |
| POST | `/api/patient/appointments/book` | Book appointment |
| GET | `/api/patient/appointments` | Get patient appointments |
| POST | `/api/appointments/<id>/cancel` | Cancel appointment |
| GET | `/api/patient/treatments/export` | Export treatments CSV |

### Doctor APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/doctor/appointments` | Get doctor appointments |
| POST | `/api/doctor/appointments/<id>/treatment` | Add treatment |
| GET | `/api/doctor/availability` | Get availability slots |
| POST | `/api/doctor/availability` | Add availability slot |
| PUT | `/api/doctor/availability/<id>` | Update availability |
| DELETE | `/api/doctor/availability/<id>` | Delete availability |

### Admin APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/doctor/register` | Register new doctor |
| GET | `/api/admin/doctor-list` | Get all doctors |
| GET | `/api/admin/patient-list` | Get all patients |
| GET | `/api/admin/departments` | Get departments |
| POST | `/api/admin/departments` | Create department |
| DELETE | `/api/admin/departments/<id>` | Delete department |
| POST | `/api/admin/users/<id>/block` | Block user |
| POST | `/api/admin/users/<id>/unblock` | Unblock user |

### Public APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/departments` | Get all departments |
| GET | `/api/doctors/department/<id>` | Get doctors by department |

## 📸 Screenshots

### Landing Page
![Landing Page](screenshots/landing.png)

### Patient Dashboard
![Patient Dashboard](screenshots/patient-dashboard.png)

### Doctor Dashboard
![Doctor Dashboard](screenshots/doctor-dashboard.png)

### Admin Dashboard
![Admin Dashboard](screenshots/admin-dashboard.png)

> Note: Add screenshots to a `screenshots/` folder in your repository

## 🔧 Configuration

### Backend Configuration (`Backend/controllers/config.py`)
- `SECRET_KEY` - JWT secret key
- `SQLALCHEMY_DATABASE_URI` - Database connection string
- `JWT_ACCESS_TOKEN_EXPIRES` - Token expiration time

### Frontend Configuration
- API base URL is set to `http://localhost:5000` in the Vue components

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Your Name - [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Flask documentation
- Vue.js documentation
- Bootstrap for UI components
