# backend/routes/citations.py
from fastapi import APIRouter, Query
import re
from typing import List
router = APIRouter()

URL_RE = re.compile(r"https?://[^\s,]+", re.IGNORECASE)

@router.get("/extract")
async def extract_urls(text: str):
    found = URL_RE.findall(text or "")
    return {"urls": found, "count": len(found)}

@router.get("/brand-missing")
async def brand_missing(brand: str, prompt_types: str = ""):
    # Simple mock analysis: returns which prompt types are missing a brand mention.
    prompt_list = prompt_types.split(",") if prompt_types else ["how-to","comparison","definition","use-case"]
    missing = []
    for p in prompt_list:
        # naive rule: if brand shorter than 4 chars, simulate brand missing more often
        if len(brand) < 4 and prompt_list.index(p) % 2 == 0:
            missing.append(p)
        elif len(brand) >= 4 and prompt_list.index(p) % 3 == 0:
            missing.append(p)
    return {"brand": brand, "missing_prompt_types": missing}
