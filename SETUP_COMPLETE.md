# Project Setup Complete

## How to Install and Run This App

### 1. Clone the Repository
```
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Backend Setup (Python)
- Install Python 3.10+
- Create and activate a virtual environment:
  - Windows: `python -m venv venv && venv\Scripts\activate`
  - Linux/Mac: `python3 -m venv venv && source venv/bin/activate`
- Install dependencies:
```
pip install -r requirements.txt
```

### 3. Frontend Setup (Vue)
- Install Node.js (v16+ recommended)
- Go to the frontend directory:
```
cd Frontend/frontend
npm install
```

### 4. Ollama (Local LLM)
- Download and install Ollama: https://ollama.com/download
- Start Ollama (it runs as a background service)
- Download the model:
```
ollama pull llama3.2:3b
```

### 5. Environment Variables
- Copy `.env.example` to `.env` and fill in secrets if needed
- Make sure `SECRET_KEY`, `JWT_SECRET_KEY`, and `DATABASE_URI` are set

### 6. Initialize the Database
- For SQLite, the DB file is created on first run
- For other DBs, set up and update `DATABASE_URI`

### 7. Run the Backend
```
python app.py
```

### 8. Run the Frontend
```
cd Frontend/frontend
npm run dev
```

### 9. Access the App
- Frontend: http://localhost:5173
- Backend: http://localhost:5000
- Ollama: http://localhost:11434

---

## Production/Deployment Notes
- Use Gunicorn or uWSGI for Flask in production
- Use Nginx as a reverse proxy for Flask and Vue
- Serve built frontend (`npm run build`) with Nginx or similar
- Secure with HTTPS
- Use a production database (PostgreSQL, MySQL, etc.) for multi-user
- Ollama must run on the same server or private network as backend

---

**For more details, see the README.md.**
