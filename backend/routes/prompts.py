# backend/routes/prompts.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.utils.ai_client import generate_responses

router = APIRouter()

class PromptTestRequest(BaseModel):
    brand: str
    prompt_variations: Optional[List[str]] = None  # optional: client can pass

# small helper to auto-generate variations
DEFAULT_PROMPT_TYPES = [
    "how-to", "comparison", "definition", "use-case", "benefits", "problem-solution"
]

def make_prompts(brand: str):
    prompts = []
    for t in DEFAULT_PROMPT_TYPES:
        prompts.append(f"{t}: How does {brand} compare in {t} use cases?")
    # keep to 10 by repeating small variants
    prompts += [f"{brand} {p}" for p in ["overview", "pricing", "alternatives", "case study"]]
    return prompts[:10]

@router.post("/test")
async def test_prompts(req: PromptTestRequest):
    prompts = req.prompt_variations or make_prompts(req.brand)
    try:
        results = await generate_responses(prompts, req.brand)
        return {"brand": req.brand, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
