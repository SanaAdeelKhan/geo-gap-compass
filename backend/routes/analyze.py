# backend/routes/analyze.py
from fastapi import APIRouter, HTTPException, Body
from typing import List, Optional
from pydantic import BaseModel

# Import OpenAI functions
import sys
from pathlib import Path
# Add backend to path if needed
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from utils.ai_client import (
    analyze_domains as ai_analyze_domains,
    analyze_competitors as ai_analyze_competitors,
    generate_gap_analysis,
    OPENAI_AVAILABLE
)

router = APIRouter()


# Pydantic models for request validation
class DomainAnalysisRequest(BaseModel):
    domains: List[str]
    brand: str


class CompetitorAnalysisRequest(BaseModel):
    brand: str
    competitors: List[str]


@router.post("/analyze_domains/")
async def analyze_domains(request: DomainAnalysisRequest):
    """
    Analyze domains using OpenAI for brand visibility insights.
    
    Example:
    {
        "domains": ["nike.com", "adidas.com", "underarmour.com"],
        "brand": "Nike"
    }
    """
    if not request.domains:
        raise HTTPException(status_code=400, detail="No domains provided")
    
    # Use OpenAI to analyze domains
    result = await ai_analyze_domains(
        domains=request.domains,
        brand=request.brand
    )
    
    # Parse the analysis into structured format
    return {
        "brand": request.brand,
        "domains": request.domains,
        "analysis": result.get("analysis", ""),
        "tokens_used": result.get("tokens_used"),
        "using_openai": OPENAI_AVAILABLE,
        "is_mock": result.get("is_mock", False),
        "error": result.get("error")
    }


@router.post("/analyze_competitors/")
async def analyze_competitors(request: CompetitorAnalysisRequest):
    """
    Analyze competitors using OpenAI for competitive insights.
    
    Example:
    {
        "brand": "Nike",
        "competitors": ["Adidas", "Puma", "Under Armour", "New Balance"]
    }
    """
    if not request.competitors:
        raise HTTPException(status_code=400, detail="No competitors provided")
    
    # Use OpenAI to analyze competitors
    result = await ai_analyze_competitors(
        brand=request.brand,
        competitors=request.competitors
    )
    
    # Parse the analysis to extract scores (if possible)
    analysis_text = result.get("analysis", "")
    
    # Simple scoring based on mentions (you can make this more sophisticated)
    competitor_scores = []
    for comp in request.competitors:
        # Count mentions as a simple proxy for importance
        mentions = analysis_text.lower().count(comp.lower())
        score = min(100, mentions * 20 + 50)  # Simple scoring algorithm
        competitor_scores.append({
            "name": comp,
            "score": score,
            "mentions": mentions
        })
    
    return {
        "brand": request.brand,
        "competitors": competitor_scores,
        "detailed_analysis": analysis_text,
        "tokens_used": result.get("tokens_used"),
        "using_openai": OPENAI_AVAILABLE,
        "is_mock": result.get("is_mock", False),
        "error": result.get("error")
    }


@router.get("/gap_heatmap/")
async def gap_heatmap(
    brand: str,
    missing_topics: Optional[str] = None
):
    """
    Generate gap analysis heatmap using OpenAI.
    
    Query params:
    - brand: Brand name (required)
    - missing_topics: Comma-separated topics (optional)
    
    Example: /gap_heatmap/?brand=Nike&missing_topics=sustainability,innovation,social-media
    """
    if not brand:
        raise HTTPException(status_code=400, detail="Brand parameter is required")
    
    # Parse topics
    if missing_topics:
        topics = [t.strip() for t in missing_topics.split(",") if t.strip()]
    else:
        # Default topics if none provided
        topics = ["how-to", "comparison", "definition", "reviews", "tutorials"]
    
    # Use OpenAI to analyze gaps
    result = await generate_gap_analysis(
        brand=brand,
        missing_topics=topics
    )
    
    # Parse recommendations into heatmap format
    recommendations = result.get("recommendations", "")
    
    # Generate scores based on AI analysis
    # This is a simplified version - you can make it more sophisticated
    heatmap_data = []
    for i, topic in enumerate(topics):
        # Check if topic is mentioned in recommendations
        mentioned = topic.lower() in recommendations.lower()
        
        # Simple scoring logic
        your_brand_score = 30 + (i * 10) if mentioned else 20
        competitor_score = 70 - (i * 5) if mentioned else 80
        
        heatmap_data.append({
            "promptType": topic,
            "yourBrandScore": your_brand_score,
            "competitorScore": competitor_score,
            "priority": "high" if competitor_score - your_brand_score > 40 else "medium"
        })
    
    return {
        "brand": brand,
        "data": heatmap_data,
        "recommendations": recommendations,
        "gaps_analyzed": topics,
        "tokens_used": result.get("tokens_used"),
        "using_openai": OPENAI_AVAILABLE,
        "is_mock": result.get("is_mock", False),
        "error": result.get("error")
    }


@router.get("/health")
async def health_check():
    """Check if OpenAI is available."""
    return {
        "status": "healthy",
        "openai_available": OPENAI_AVAILABLE,
        "routes": ["analyze_domains", "analyze_competitors", "gap_heatmap"]
    }