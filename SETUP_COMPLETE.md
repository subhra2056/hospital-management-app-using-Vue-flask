
# Local Setup Guide: Run This App & Chatbot on a New PC

## 1. Prerequisites

- **Python 3.10+** (https://www.python.org/downloads/)
- **Node.js 16+** (https://nodejs.org/)
- **Git** (https://git-scm.com/)
- **Ollama** (https://ollama.com/download) (for AI chatbot)

---

## 2. Clone the Project

```
git clone <your-repo-url>
cd <your-repo-folder>
```

---

## 3. Backend Setup (Flask)

### a. Create and Activate Virtual Environment
- **Windows:**
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

### b. Install Python Dependencies
```
pip install -r requirements.txt
```

### c. Environment Variables
- Copy `.env.example` to `.env`:
  ```
  copy .env.example .env   # Windows
  # or
  cp .env.example .env     # Linux/Mac
  ```
- Edit `.env` and set:
  - `SECRET_KEY`, `JWT_SECRET_KEY` (any random string)
  - `DATABASE_URI` (default is fine for SQLite)

### d. (Optional) Seed Database
If you want demo users/data:
```
python seed_data.py
```

---

## 4. Frontend Setup (Vue)

### a. Install Node Modules
```
cd Frontend/frontend
npm install
```

---

## 5. Ollama Setup (AI Chatbot)

### a. Install Ollama
- Download and install from: https://ollama.com/download

### b. Download the Model
```
ollama pull llama3.2:3b
```

### c. Start Ollama
- Ollama should run automatically as a background service.
- If not, run:
  ```
  ollama serve
  ```
- Test: Open http://localhost:11434 in your browser. You should see a version response.

---

## 6. Run the App

### a. Start Backend (Flask)
```
python app.py
```
- The backend will auto-check/start Ollama. If Ollama is not running, you’ll see a warning.
- Backend API: http://localhost:5000

### b. Start Frontend (Vue)
```
cd Frontend/frontend
npm run dev
```
- Frontend: http://localhost:5173

---

## 7. Using the Chatbot

- Make sure **Ollama** is running and the model is downloaded.
- The chatbot will work in the app UI (Doctor/Patient dashboards) if Ollama is reachable at http://localhost:11434.
- If you see errors like “AI not available”, check that Ollama is running and the model is pulled.

---

## 8. Troubleshooting

- **Ollama not found:**
  - Reinstall Ollama and ensure it’s in your PATH.
  - Try running `ollama serve` manually.
- **Port conflicts:**
  - Default ports: Flask (5000), Frontend (5173), Ollama (11434). Change if needed.
- **CORS errors:**
  - Make sure you access the frontend via http://localhost:5173.
- **.env issues:**
  - Double-check `.env` values and file location.

---

## 9. Useful Commands

- **Quick test data:**
  ```
  python quick_seed.py
  ```

---

## 10. Support

- See README.md for more details.
- If you have issues, check the Troubleshooting section above.

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
