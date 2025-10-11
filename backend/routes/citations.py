# backend/routes/citations.py
from fastapi import APIRouter, Query
import re
from typing import List
import sys
from pathlib import Path

# Add backend to path if needed
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from utils.ai_client import generate_with_citations, OPENAI_AVAILABLE

router = APIRouter()

URL_RE = re.compile(r"https?://[^\s,\)]+", re.IGNORECASE)


@router.get("/extract")
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
        "original_text_length": len(text)
    }


@router.get("/brand-missing")
async def brand_missing(
    brand: str = Query(..., description="Brand name to analyze"),
    prompt_types: str = Query("", description="Comma-separated prompt types (e.g., how-to,comparison,definition)")
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
    
    # Use OpenAI to analyze brand presence across prompt types
    analysis_prompt = f"""Analyze {brand}'s online visibility across these content types: {', '.join(prompt_list)}

For each content type, assess:
1. Whether {brand} has strong presence
2. Quality of existing content
3. Whether citations/sources mention {brand}
4. Gaps or opportunities

Identify which content types have the WEAKEST {brand} presence."""
    
    result = await generate_with_citations(
        prompt=analysis_prompt,
        brand=brand,
        include_web_search=True
    )
    
    # Parse the AI response to identify missing prompt types
    response_text = result.get("response", "").lower()
    citations = result.get("citations", [])
    
    # Check which prompt types are mentioned as weak/missing
    missing = []
    strong = []
    
    for prompt_type in prompt_list:
        # Look for negative indicators
        weak_indicators = ["weak", "limited", "missing", "gap", "opportunity", "needs improvement", "lacking"]
        strong_indicators = ["strong", "good", "well-covered", "comprehensive", "abundant"]
        
        type_lower = prompt_type.lower()
        
        # Check if this prompt type is mentioned with weak indicators nearby
        is_weak = any(
            indicator in response_text and 
            abs(response_text.find(indicator) - response_text.find(type_lower)) < 100
            for indicator in weak_indicators
            if type_lower in response_text
        )
        
        is_strong = any(
            indicator in response_text and 
            abs(response_text.find(indicator) - response_text.find(type_lower)) < 100
            for indicator in strong_indicators
            if type_lower in response_text
        )
        
        if is_weak or (type_lower not in response_text and len(missing) < 3):
            missing.append(prompt_type)
        elif is_strong:
            strong.append(prompt_type)
    
    # Check if brand appears in citations
    brand_in_citations = any(brand.lower() in url.lower() for url in citations)
    
    return {
        "brand": brand,
        "prompt_types_analyzed": prompt_list,
        "missing_prompt_types": missing,
        "strong_prompt_types": strong,
        "brand_found_in_citations": brand_in_citations,
        "total_citations": len(citations),
        "citations": citations[:5],  # Return first 5 citations
        "ai_analysis": result.get("response", ""),
        "tokens_used": result.get("tokens_used"),
        "using_openai": OPENAI_AVAILABLE,
        "is_mock": result.get("is_mock", False)
    }


@router.get("/analyze-brand-presence")
async def analyze_brand_presence(
    brand: str = Query(..., description="Brand name"),
    competitors: str = Query("", description="Comma-separated competitor names"),
    topic: str = Query("general marketing", description="Topic or industry to analyze")
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

Include relevant URLs if you know authoritative sources."""
    
    result = await generate_with_citations(
        prompt=analysis_prompt,
        brand=brand,
        include_web_search=True
    )
    
    return {
        "brand": brand,
        "competitors": competitor_list,
        "topic": topic,
        "analysis": result.get("response", ""),
        "citations": result.get("citations", []),
        "citation_count": len(result.get("citations", [])),
        "tokens_used": result.get("tokens_used"),
        "using_openai": OPENAI_AVAILABLE,
        "recommendations": extract_recommendations(result.get("response", "")),
        "is_mock": result.get("is_mock", False)
    }


def extract_recommendations(text: str) -> List[str]:
    """Extract recommendation points from AI response."""
    recommendations = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        # Look for numbered points or bullet points
        if re.match(r'^\d+\.', line) or line.startswith('•') or line.startswith('-'):
            # Clean up the line
            clean_line = re.sub(r'^\d+\.\s*|\•\s*|-\s*', '', line)
            if len(clean_line) > 10:  # Only include substantial recommendations
                recommendations.append(clean_line)
    
    return recommendations[:10]  # Return top 10 recommendations


@router.get("/health")
async def health_check():
    """Check if citations routes and OpenAI are available."""
    return {
        "status": "healthy",
        "openai_available": OPENAI_AVAILABLE,
        "routes": ["extract", "brand-missing", "analyze-brand-presence"]
    }