# backend/routes/analyze.py
from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter()

@router.post("/analyze_domains/")
async def analyze_domains(data: dict):
    """
    Fetch domain info using DuckDuckGo Instant Answer API.
    Example: {"domains": "openai.com, github.com"}
    """
    domains = [d.strip() for d in data.get("domains", "").split(",") if d.strip()]
    if not domains:
        raise HTTPException(status_code=400, detail="No domains provided")

    results = {}
    async with httpx.AsyncClient() as client:
        for domain in domains:
            try:
                url = f"https://api.duckduckgo.com/?q={domain}&format=json"
                response = await client.get(url, timeout=10.0)
                info = response.json()
                results[domain] = {
                    "title": info.get("Heading") or domain,
                    "description": info.get("AbstractText") or "No description available.",
                    "image": info.get("Image") or "https://dummyimage.com/600x400/ccc/000.png&text=No+Image",
                    "source": "DuckDuckGo",
                }
            except Exception as e:
                results[domain] = {"error": str(e), "source": "fallback"}

    return {"domains": results, "note": "Using DuckDuckGo API with fallback demo data"}


@router.post("/analyze_competitors/")
async def analyze_competitors(data: dict):
    """
    Mock competitor insights for frontend visualization.
    """
    company = data.get("company", "Unknown")
    return {
        "company": company,
        "competitors": [
            {"name": "Competitor A", "score": 82},
            {"name": "Competitor B", "score": 65},
        ],
        "note": "Mock competitor data for demo purposes",
    }


@router.get("/gap_heatmap/")
async def gap_heatmap():
    """
    Mock gap heatmap for testing frontend visuals.
    """
    return {
        "data": [
            {"promptType": "how-to", "yourBrandScore": 30, "competitorScore": 80},
            {"promptType": "comparison", "yourBrandScore": 10, "competitorScore": 60},
            {"promptType": "definition", "yourBrandScore": 60, "competitorScore": 50},
        ],
        "note": "Mock gap heatmap data"
    }
