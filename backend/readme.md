# 🌍 GEO Gap Compass - Backend

This is the **FastAPI backend** for the GEO Gap Compass project.
It powers the AI and data APIs that interact with the frontend (Next.js app).

---


## 🚀 Tech Stack

- **FastAPI** — lightweight, high-performance web framework
- **Uvicorn** — ASGI web server
- **Python 3.10+**
- **Virtual Environment (.venv)** for isolated dependencies

---

## 🚀 Features

- FastAPI-based modular architecture
- Three main route modules:
  - `/prompts` → AI Prompt Generation
  - `/citations` → Citation Management
  - `/reimagine` → Idea & Content Reimagination
- CORS enabled for frontend (localhost:3000)
- Interactive API Docs (Swagger + ReDoc)
- Ready for local or production deployment

---

## 🧩 Project Structure

```
geo-gap-compass/
├── backend/
│   ├── app.py              # Main FastAPI app
│   ├── routes/
│   │   ├── prompts.py
│   │   ├── citations.py
│   │   └── analyze.py
│   │   └── domain_insights.py
│   ├── utils/                # Helper functions and AI clients
│   │   └── ai_client.py
│   └── .venv/                # Virtual environment (optional local setup)
└── frontend/                 # Next.js UI
│   ├── requirements.txt
│   └── README.md
```

---

## ⚙️ Installation & Run

### 1️⃣ Navigate to the backend folder

```bash
cd backend
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # On Windows
# or
source .venv/bin/activate  # On macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Running the Backend

Always run **from the project root**, not from inside `/backend`, so Python can resolve the `backend.` imports correctly.

```bash
backend\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload --port 8000
```

### 5️⃣ Test in browser

🌐 **Base URL:**
`http://127.0.0.1:8000` → Backend running message

🌐 **Health Check:**
`http://127.0.0.1:8000/health` → Health check

📘 **Swagger UI:**
`http://127.0.0.1:8000/docs` → Interactive API testing

📗 **ReDoc UI:**
`http://127.0.0.1:8000/redoc` → Clean API documentation

---

## 🧠 Example Response

**GET** `http://127.0.0.1:8000/`

```json
{
  "message": "GEO Gap Compass Backend is running successfully 🚀"
}
```

---

## 🔗 Frontend Connection Example (Next.js)

Inside your frontend (e.g., `utils/api.js`):

```javascript
export async function fetchHealth() {
  const res = await fetch("http://127.0.0.1:8000/health");
  const data = await res.json();
  return data;
}
```

Usage:

```javascript
useEffect(() => {
  fetchHealth().then(console.log);
}, []);
```

---

## 📘 API Docs Auto-Generated

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Example endpoints:

- `/` → Welcome message
- `/health` → Health check
- `/prompts/...`, `/citations/...`, `/reimagine/...` → Functional APIs

---

## 🧾 License

MIT License © GEO Gap Compass Team
