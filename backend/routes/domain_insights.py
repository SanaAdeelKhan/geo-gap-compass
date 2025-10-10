# backend/routes/domain_insights.py

from fastapi import APIRouter, Query
import httpx
import json
from pathlib import Path

router = APIRouter()

# Optional fallback demo data (if DuckDuckGo fails)
BASE_DIR = Path(__file__).resolve().parents[2]
DEMO_PATH = BASE_DIR / "demo_data" / "fake_time_series.json"

def load_demo_data():
    try:
        with DEMO_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"default": {"visibility": 50, "trend": [45, 47, 49, 50]}}

@router.get("/domain-stats")
async def get_domain_stats(domains: str = Query(..., description="Comma separated domains")):
    """
    Fetch live info from DuckDuckGo Instant Answer API (no key needed).
    Fallback to local demo data if unavailable.
    """
    domain_list = [d.strip() for d in domains.split(",") if d.strip()]
    demo = load_demo_data()
    results = {}

    for domain in domain_list:
        try:
            # ✅ Real DuckDuckGo API
            url = f"https://api.duckduckgo.com/?q={domain}&format=json&no_html=1"
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                data = resp.json()

            title = data.get("Heading") or domain
            description = data.get("Abstract") or "No description available."
            image = data.get("Image") or "https://dummyimage.com/600x400/ccc/000.png&text=No+Image"

            results[domain] = {
                "title": title,
                "description": description,
                "image": image,
                "source": "DuckDuckGo"
            }

        except Exception:
            # 🔁 Fallback to demo data if API fails
            base = demo.get("default", {"visibility": 50, "trend": [45, 47, 49, 50]})
            results[domain] = {
                "title": domain,
                "description": f"Demo data for {domain}. API unavailable or rate-limited.",
                "image": "https://dummyimage.com/600x400/ddd/000.png&text=Demo",
                "trend": base["trend"],
                "source": "mock-fallback"
            }

    return {"domains": results, "note": "Using DuckDuckGo API with fallback demo data"}
