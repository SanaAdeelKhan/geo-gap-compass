# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import prompts, citations, analyze, domain_insights

app = FastAPI(
    title="GEO Gap Compass - Backend",
    version="0.1.0",
    description="OpenAI-powered brand visibility analysis"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prompts.router)
app.include_router(citations.router)
app.include_router(analyze.router)
app.include_router(domain_insights.router)


@app.get("/")
async def root():
    return {"message": "GEO Gap Compass API with OpenAI", "status": "active"}


@app.get("/health")
async def health():
    from backend.utils.ai_client import OPENAI_AVAILABLE
    return {
        "status": "healthy",
        "openai_enabled": OPENAI_AVAILABLE
    }