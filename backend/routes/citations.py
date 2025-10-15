# backend/routes/citations.py
from fastapi import APIRouter, Query, HTTPException
import re
from typing import List, Optional, Dict, Any
import sys
from pathlib import Path
import json
import logging

# Add backend to path if needed
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from utils.ai_client import generate_with_citations, OPENAI_AVAILABLE

# <-- IMPORTANT: prefix so frontend can call /citations/...
router = APIRouter(prefix="/citations")

logger = logging.getLogger("citations")
logger.setLevel(logging.INFO)

URL_RE = re.compile(r"https?://[^\s,\)]+", re.IGNORECASE)
MAX_CITATIONS = 10


# -----------------------
# Pydantic response models
# -----------------------
from pydantic import BaseModel


class ExtractResponse(BaseModel):
    urls: List[str]
    count: int
    original_text_length: int


class BrandMissingResponse(BaseModel):
    brand: str
    prompt_types_analyzed: List[str]
    missing_prompt_types: List[str]
    strong_prompt_types: List[str]
    brand_found_in_citations: bool
    total_citations: int
    citations: List[str]
    ai_analysis: str
    structured_analysis: Optional[Dict[str, Any]] = None
    tokens_used: Optional[int]
    using_openai: bool
    is_mock: bool


class AnalyzeBrandPresenceResponse(BaseModel):
    brand: str
    competitors: List[str]
    topic: str
    analysis: str
    structured_analysis: Optional[Dict[str, Any]] = None
    citations: List[str]
    citation_count: int
    tokens_used: Optional[int]
    using_openai: bool
    recommendations: List[str]
    is_mock: bool


class HealthResponse(BaseModel):
    status: str
    openai_available: bool
    routes: List[str]


# -----------------------
# Helper utilities
# -----------------------
def extract_recommendations(text: str) -> List[str]:
    """Extract recommendation points from AI response."""
    recommendations = []
    if not text:
        return recommendations

    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        # Look for numbered points or bullet points
        if re.match(r"^\d+\.", line) or line.startswith("•") or line.startswith("-"):
            # Clean up the line
            clean_line = re.sub(r"^\d+\.\s*|\•\s*|-\s*", "", line)
            if len(clean_line) > 10:  # Only include substantial recommendations
                recommendations.append(clean_line)
    return recommendations[:10]


def try_parse_structured(response_text: str) -> Optional[Dict[str, Any]]:
    """
    If the AI returned a JSON string, parse it and return the dict.
    If parsing fails or it's not JSON, return None.
    """
    if not response_text:
        return None
    # Heuristic: if it starts with { or [, try json.loads
    trimmed = response_text.strip()
    if trimmed.startswith("{") or trimmed.startswith("["):
        try:
            return json.loads(trimmed)
        except Exception:
            # Try a relaxed attempt: find first { and last } and attempt parse
            try:
                start = trimmed.find("{")
                end = trimmed.rfind("}")
                if start != -1 and end != -1 and end > start:
                    snippet = trimmed[start : end + 1]
                    return json.loads(snippet)
            except Exception:
                return None
    return None


# -----------------------
# Routes
# -----------------------
@router.get("/extract", response_model=ExtractResponse)
async def extract_urls(text: str = Query(..., description="Text to extract URLs from")):
    """
    Extract URLs from text using regex.
    Simple utility endpoint that doesn't require OpenAI.
    """
    found = URL_RE.findall(text or "")
    # Clean up URLs (remove trailing punctuation)
    cleaned = [url.rstrip(".,;:!?)") for url in found]
    return {
        "urls": cleaned,
        "count": len(cleaned),
        "original_text_length": len(text or ""),
    }


@router.get("/brand-missing", response_model=BrandMissingResponse)
async def brand_missing(
    brand: str = Query(..., description="Brand name to analyze"),
    prompt_types: str = Query("", description="Comma-separated prompt types (e.g., how-to,comparison,definition)"),
):
    """
    Analyze which prompt types are missing brand mentions using OpenAI.

    Example: /brand-missing?brand=Nike&prompt_types=how-to,comparison,reviews
    """
    # Parse prompt types
    if prompt_types:
        prompt_list = [p.strip() for p in prompt_types.split(",") if p.strip()]
    else:
        prompt_list = ["how-to", "comparison", "definition", "use-case", "reviews"]

    analysis_prompt = f"""Analyze {brand}'s online visibility across these content types: {', '.join(prompt_list)}

For each content type, assess:
1. Whether {brand} has strong presence
2. Quality of existing content
3. Whether citations/sources mention {brand}
4. Gaps or opportunities

Identify which content types have the WEAKEST {brand} presence.
Return a clear summary and (optionally) a JSON object with fields 'missing' and 'strong' if possible.
"""

    ai_response_text = ""
    citations = []
    tokens_used = None
    structured = None
    is_mock = False

    if OPENAI_AVAILABLE:
        try:
            result = await generate_with_citations(prompt=analysis_prompt, brand=brand, include_web_search=True)
            ai_response_text = result.get("response", "") or ""
            citations = result.get("citations", []) or []
            tokens_used = result.get("tokens_used")
            structured = try_parse_structured(ai_response_text)
        except Exception as e:
            logger.exception("OpenAI call failed in /brand-missing: %s", e)
            # Fall back to mock analysis
            ai_response_text = f"Mock analysis: Could not reach OpenAI. Fallback for {brand}."
            is_mock = True
    else:
        # OpenAI not available -> provide mock analysis
        ai_response_text = f"Mock analysis for {brand}: unable to use OpenAI in this environment."
        is_mock = True

    # Parse the AI response to identify missing prompt types (best-effort)
    response_text = (ai_response_text or "").lower()

    missing = []
    strong = []
    weak_indicators = ["weak", "limited", "missing", "gap", "opportunity", "needs improvement", "lacking"]
    strong_indicators = ["strong", "good", "well-covered", "comprehensive", "abundant"]

    for prompt_type in prompt_list:
        type_lower = prompt_type.lower()
        # If structured JSON provided and contains missing/strong lists, prefer those
        if structured and isinstance(structured, dict):
            try:
                s_missing = structured.get("missing", [])
                s_strong = structured.get("strong", [])
                if isinstance(s_missing, list) and prompt_type in s_missing:
                    missing.append(prompt_type)
                    continue
                if isinstance(s_strong, list) and prompt_type in s_strong:
                    strong.append(prompt_type)
                    continue
            except Exception:
                # ignore structured parsing errors and fallback to text heuristics
                pass

        # Fallback heuristics using text proximity
        is_weak = False
        is_strong = False
        if type_lower in response_text:
            # find positions
            try:
                idx_type = response_text.find(type_lower)
                for indicator in weak_indicators:
                    if indicator in response_text:
                        idx_ind = response_text.find(indicator)
                        if abs(idx_ind - idx_type) < 150:
                            is_weak = True
                            break
                for indicator in strong_indicators:
                    if indicator in response_text:
                        idx_ind = response_text.find(indicator)
                        if abs(idx_ind - idx_type) < 150:
                            is_strong = True
                            break
            except Exception:
                pass

        if is_weak or (type_lower not in response_text and len(missing) < 3):
            missing.append(prompt_type)
        elif is_strong:
            strong.append(prompt_type)

    brand_in_citations = any(brand.lower() in (url.lower() if isinstance(url, str) else "") for url in citations)

    return {
        "brand": brand,
        "prompt_types_analyzed": prompt_list,
        "missing_prompt_types": missing,
        "strong_prompt_types": strong,
        "brand_found_in_citations": brand_in_citations,
        "total_citations": len(citations),
        "citations": citations[:MAX_CITATIONS],
        "ai_analysis": ai_response_text,
        "structured_analysis": structured,
        "tokens_used": tokens_used,
        "using_openai": OPENAI_AVAILABLE,
        "is_mock": is_mock,
    }


@router.get("/analyze-brand-presence", response_model=AnalyzeBrandPresenceResponse)
async def analyze_brand_presence(
    brand: str = Query(..., description="Brand name"),
    competitors: str = Query("", description="Comma-separated competitor names"),
    topic: str = Query("general marketing", description="Topic or industry to analyze"),
):
    """
    Deep analysis of brand presence compared to competitors using OpenAI.

    Example: /analyze-brand-presence?brand=Nike&competitors=Adidas,Puma&topic=athletic footwear
    """
    competitor_list = [c.strip() for c in competitors.split(",") if c.strip()] if competitors else []

    analysis_prompt = f"""Analyze {brand}'s online presence and citation visibility in {topic}.

Compare against: {', '.join(competitor_list) if competitor_list else 'industry competitors'}

Provide:
1. Where {brand} is being cited/mentioned
2. Quality and authority of sources
3. Gaps compared to competitors
4. Recommendations to improve visibility

If possible, return a JSON object with keys: citations (list), recommendations (list), summary (string).
"""

    ai_response_text = ""
    citations = []
    tokens_used = None
    structured = None
    is_mock = False

    if OPENAI_AVAILABLE:
        try:
            result = await generate_with_citations(prompt=analysis_prompt, brand=brand, include_web_search=True)
            ai_response_text = result.get("response", "") or ""
            citations = result.get("citations", []) or []
            tokens_used = result.get("tokens_used")
            structured = try_parse_structured(ai_response_text)
        except Exception as e:
            logger.exception("OpenAI call failed in /analyze-brand-presence: %s", e)
            ai_response_text = f"Mock analysis for {brand}: OpenAI call failed."
            is_mock = True
    else:
        ai_response_text = f"Mock analysis for {brand}: OpenAI not available."
        is_mock = True

    recommendations = extract_recommendations(ai_response_text)
    if structured and isinstance(structured, dict):
        # If structured JSON contains recommendations, prefer them
        try:
            s_recs = structured.get("recommendations") or structured.get("recommend") or structured.get("recommendation")
            if isinstance(s_recs, list) and len(s_recs) > 0:
                # convert to strings
                recommendations = [str(r) for r in s_recs[:10]]
        except Exception:
            pass

    return {
        "brand": brand,
        "competitors": competitor_list,
        "topic": topic,
        "analysis": ai_response_text,
        "structured_analysis": structured,
        "citations": citations[:MAX_CITATIONS],
        "citation_count": len(citations),
        "tokens_used": tokens_used,
        "using_openai": OPENAI_AVAILABLE,
        "recommendations": recommendations,
        "is_mock": is_mock,
    }
@router.get("/brand-gap")
async def brand_gap(
    brand: str = Query(..., description="Your brand name"),
    competitor: str = Query(..., description="Competitor brand name"),
):
    """
    Compare brand visibility across common prompt types (how-to, comparison, definition, etc.)
    Returns structured data for the frontend heatmap.
    """
    prompt_types = ["how-to", "comparison", "definition", "reviews", "use-case"]

    # If OpenAI available, generate structured output
    if OPENAI_AVAILABLE:
        try:
            prompt = f"""
            Compare online citation visibility of {brand} vs {competitor}
            across the following prompt types: {', '.join(prompt_types)}.

            Return a JSON object with this structure:
            [
              {{ "promptType": "how-to", "yourBrandScore": 50, "competitorScore": 70 }},
              ...
            ]
            The scores represent % strength (0–100) of citation presence.
            """
            result = await generate_with_citations(prompt=prompt, brand=brand, include_web_search=True)
            ai_text = result.get("response", "")
            parsed = try_parse_structured(ai_text)
            if isinstance(parsed, list) and all("promptType" in x for x in parsed):
                return {
                    "brand": brand,
                    "competitor": competitor,
                    "data": parsed,
                    "using_openai": True,
                    "is_mock": False,
                }
        except Exception as e:
            logger.exception("AI failed in /brand-gap: %s", e)

    # Fallback mock data (if OpenAI unavailable or invalid response)
    mock_data = [
        {"promptType": "how-to", "yourBrandScore": 40, "competitorScore": 75},
        {"promptType": "comparison", "yourBrandScore": 30, "competitorScore": 60},
        {"promptType": "definition", "yourBrandScore": 65, "competitorScore": 70},
        {"promptType": "reviews", "yourBrandScore": 50, "competitorScore": 80},
        {"promptType": "use-case", "yourBrandScore": 35, "competitorScore": 55},
    ]
    return {
        "brand": brand,
        "competitor": competitor,
        "data": mock_data,
        "using_openai": False,
        "is_mock": True,
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if citations routes and OpenAI are available."""
    return {
        "status": "healthy",
        "openai_available": OPENAI_AVAILABLE,
        "routes": ["extract", "brand-missing", "analyze-brand-presence"],
    }
