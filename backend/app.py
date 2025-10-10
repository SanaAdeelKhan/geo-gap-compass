# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import domain_insights, prompts, citations, analyze


app = FastAPI(title="GEO Gap Compass - Backend")

# ✅ Allow frontend origins
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
app.include_router(citations.router, prefix="/citations", tags=["citations"])
app.include_router(domain_insights.router, prefix="/insights", tags=["domain insights"])
app.include_router(analyze.router, tags=["analyze"])  # ✅ NEW endpoint for /analyze_domains/

# ✅ Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# ✅ Root
@app.get("/")
async def root():
    return {"message": "GEO Gap Compass Backend is running successfully 🚀"}
