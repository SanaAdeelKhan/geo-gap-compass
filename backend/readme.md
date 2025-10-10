# 🧠 GEO-Gap Compass — Backend API

This is the **FastAPI backend** for the GEO-Gap Compass project.
It provides AI-powered endpoints for prompt processing, citation extraction, and creative reimagination features used by the frontend (Next.js).

---

## 🚀 Tech Stack

- **FastAPI** — lightweight, high-performance web framework
- **Uvicorn** — ASGI web server
- **Python 3.10+**
- **Virtual Environment (.venv)** for isolated dependencies

---

## 📂 Project Structure

```
geo-gap-compass/
├── backend/
│   ├── app.py                # Main FastAPI entry point
│   ├── routes/               # All route definitions
│   │   ├── prompts.py
│   │   ├── citations.py
│   │   └── reimagine.py
│   ├── utils/                # Helper functions and AI clients
│   │   └── ai_client.py
│   └── .venv/                # Virtual environment (optional local setup)
└── frontend/                 # Next.js UI
```

---

## 🧩 Setup Instructions

### 1️⃣ Create and activate a virtual environment

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, generate one:

```bash
pip freeze > requirements.txt
```

---

## ⚙️ Running the Backend

Always run **from the project root**, not from inside `/backend`, so Python can resolve the `backend.` imports correctly.

```bash
backend\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload --port 8000
```

Then open:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Interactive API Docs
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000) — Root endpoint

---

## 🧠 Common Issues

| Issue                                              | Cause                                  | Solution                                                           |
| -------------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------ |
| `ModuleNotFoundError: No module named 'backend'` | Running from inside `/backend`       | Run from**project root** using full import path              |
| `ModuleNotFoundError: No module named 'routes'`  | Missing `backend.` prefix in imports | Use `from backend.routes import ...`                             |
| `127.0.0.1 refused to connect`                   | Port already in use or server crashed  | Restart Uvicorn and ensure no other service is using port `8000` |

---

## 🔗 Example Endpoints

| Route                | Description                  |
| -------------------- | ---------------------------- |
| `GET /`            | Health check endpoint        |
| `POST /prompts/`   | Process text prompts         |
| `POST /citations/` | Extract and rank citations   |
| `POST /reimagine/` | Reimagine or rewrite content |

---

## 🧾 License

MIT License © 2025 GEO-Gap Compass Team

---

## 👩‍💻 Maintainers

- **Sana Adeel**
- **Ali Jafar**
