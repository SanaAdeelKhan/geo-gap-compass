# backend/routes/domain_insights.py

from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import httpx
import json
from pathlib import Path
import sys

# Add backend to path
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from utils.ai_client import generate_with_citations, analyze_domains, OPENAI_AVAILABLE

router = APIRouter(prefix="/insights", tags=["domain insights"])

# Demo data path
BASE_DIR = Path(__file__).resolve().parents[2]
DEMO_PATH = BASE_DIR / "demo_data" / "fake_time_series.json"


class DomainInsightRequest(BaseModel):
    brand: str
    domains: List[str]
    analysis_type: Optional[str] = "comprehensive"  # comprehensive, seo, authority, trend


def load_demo_data():
    """Load fallback demo data."""
    try:
        with DEMO_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"default": {"visibility": 50, "trend": [45, 47, 49, 50]}}


async def fetch_domain_info_duckduckgo(domain: str) -> Dict[str, Any]:
    """Fetch basic domain info from DuckDuckGo API."""
    try:
        url = f"https://api.duckduckgo.com/?q={domain}&format=json&no_html=1"
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url)
            data = resp.json()

        return {
            "title": data.get("Heading") or domain,
            "description": data.get("Abstract") or "No description available.",
            "image": data.get("Image") or "https://dummyimage.com/600x400/ccc/000.png&text=No+Image",
            "source": "DuckDuckGo"
        }
    except Exception:
        return {
            "title": domain,
            "description": f"Could not fetch data for {domain}",
            "image": "https://dummyimage.com/600x400/ddd/000.png&text=No+Data",
            "source": "error"
        }


@router.get("/domain-stats")
async def get_domain_stats(
    domains: str = Query(..., description="Comma-separated domains"),
    brand: str = Query(None, description="Brand name for AI analysis"),
    include_ai_analysis: bool = Query(True, description="Include OpenAI analysis")
):
    """
    Get comprehensive domain statistics with optional AI analysis.
    
    Example: /insights/domain-stats?domains=nike.com,adidas.com&brand=Nike&include_ai_analysis=true
    """
    domain_list = [d.strip() for d in domains.split(",") if d.strip()]
    
    if not domain_list:
        raise HTTPException(status_code=400, detail="No domains provided")
    
    demo = load_demo_data()
    results = {}

    # Fetch basic info for each domain
    for domain in domain_list:
        try:
            # Get DuckDuckGo data
            ddg_info = await fetch_domain_info_duckduckgo(domain)
            
            # Add demo trend data
            base = demo.get(domain, demo.get("default", {"visibility": 50, "trend": [45, 47, 49, 50]}))
            
            results[domain] = {
                **ddg_info,
                "visibility_score": base.get("visibility", 50),
                "trend": base.get("trend", [45, 47, 49, 50])
            }
            
        except Exception as e:
            # Fallback to demo data
            base = demo.get("default", {"visibility": 50, "trend": [45, 47, 49, 50]})
            results[domain] = {
                "title": domain,
                "description": f"Demo data for {domain}",
                "image": "https://dummyimage.com/600x400/ddd/000.png&text=Demo",
                "visibility_score": base["visibility"],
                "trend": base["trend"],
                "source": "mock-fallback",
                "error": str(e)
            }

    # Add OpenAI analysis if requested and brand provided
    ai_analysis = None
    tokens_used = 0
    
    if include_ai_analysis and brand and OPENAI_AVAILABLE:
        ai_result = await analyze_domains(
            domains=domain_list,
            brand=brand
        )
        ai_analysis = ai_result.get("analysis", "")
        tokens_used = ai_result.get("tokens_used", 0)

    return {
        "domains": results,
        "brand": brand,
        "ai_analysis": ai_analysis,
        "tokens_used": tokens_used,
        "using_openai": OPENAI_AVAILABLE and include_ai_analysis,
        "note": "Combined DuckDuckGo API data with OpenAI analysis"
    }


@router.post("/analyze-domains")
async def analyze_domains_detailed(request: DomainInsightRequest):
    """
    Detailed domain analysis using priority: DuckDuckGo → OpenAI → Mock Data.
    
    Example:
    {
        "brand": "Nike",
        "domains": ["nike.com", "sneakernews.com", "complex.com"],
        "analysis_type": "comprehensive"
    }
    """
    if not request.domains:
        raise HTTPException(status_code=400, detail="No domains provided")
    
    demo = load_demo_data()
    
    # Priority 1: Get basic domain info from DuckDuckGo
    basic_info = {}
    for domain in request.domains:
        ddg_data = await fetch_domain_info_duckduckgo(domain)
        
        # If DuckDuckGo failed, fallback to demo data
        if ddg_data.get("source") == "error":
            base = demo.get(domain, demo.get("default", {"visibility": 50}))
            basic_info[domain] = {
                "title": domain,
                "description": f"Demo data (DuckDuckGo unavailable): {domain}",
                "image": "https://dummyimage.com/600x400/ddd/000.png&text=Demo",
                "source": "mock-fallback",
                "visibility_score": base.get("visibility", 50)
            }
        else:
            basic_info[domain] = ddg_data
    
    # Priority 2: Get AI analysis from OpenAI (if available)
    ai_result = None
    analysis_text = ""
    tokens_used = 0
    is_mock = False
    
    if OPENAI_AVAILABLE:
        ai_result = await analyze_domains(
            domains=request.domains,
            brand=request.brand
        )
        analysis_text = ai_result.get("analysis", "")
        tokens_used = ai_result.get("tokens_used", 0)
        is_mock = ai_result.get("is_mock", False)
    else:
        # Priority 3: Fallback to mock analysis
        analysis_text = f"Mock analysis for {request.brand} domains: {', '.join(request.domains)}"
        is_mock = True
    
    # Extract insights per domain
    domain_insights = {}
    for domain in request.domains:
        # Count mentions in analysis
        mentions = analysis_text.lower().count(domain.lower())
        
        # Look for authority indicators
        authority_keywords = ["authoritative", "credible", "trusted", "reputable", "high authority"]
        has_authority = any(keyword in analysis_text.lower() for keyword in authority_keywords)
        
        # Look for relevance indicators
        relevance_keywords = [request.brand.lower(), "relevant", "related", "pertinent"]
        relevance_score = sum(1 for keyword in relevance_keywords if keyword in analysis_text.lower())
        
        domain_insights[domain] = {
            **basic_info[domain],
            "mentions_in_analysis": mentions,
            "authority_indicators": has_authority,
            "relevance_score": min(100, relevance_score * 20 + 50),
            "recommended": mentions >= 2 and (has_authority or relevance_score > 2)
        }
    
    return {
        "brand": request.brand,
        "analysis_type": request.analysis_type,
        "domains": domain_insights,
        "full_analysis": analysis_text,
        "tokens_used": tokens_used,
        "using_openai": OPENAI_AVAILABLE,
        "is_mock": is_mock,
        "data_sources": {
            "basic_info": "DuckDuckGo API (with mock fallback)",
            "analysis": "OpenAI" if OPENAI_AVAILABLE else "Mock"
        }
    }


@router.get("/domain-comparison")
async def domain_comparison(
    brand: str = Query(..., description="Brand name"),
    your_domains: str = Query(..., description="Comma-separated domains owned by brand"),
    competitor_domains: str = Query(..., description="Comma-separated competitor domains")
):
    """
    Compare your brand's domains with competitor domains using AI.
    
    Example: /insights/domain-comparison?brand=Nike&your_domains=nike.com&competitor_domains=adidas.com,puma.com
    """
    your_list = [d.strip() for d in your_domains.split(",") if d.strip()]
    competitor_list = [d.strip() for d in competitor_domains.split(",") if d.strip()]
    
    all_domains = your_list + competitor_list
    
    # Create comparison prompt
    comparison_prompt = f"""Compare these domains for {brand}:

YOUR DOMAINS: {', '.join(your_list)}
COMPETITOR DOMAINS: {', '.join(competitor_list)}

Analyze:
1. Authority and credibility differences
2. Content quality and relevance to {brand}
3. SEO strength indicators
4. Brand visibility opportunities
5. Recommendations for {brand} to improve vs competitors

Provide specific, actionable insights."""
    
    result = await generate_with_citations(
        prompt=comparison_prompt,
        brand=brand,
        include_web_search=False
    )
    
    # Calculate simple scores
    your_score = 50  # Base score
    competitor_score = 50
    
    analysis_lower = result.get("response", "").lower()
    
    # Adjust scores based on positive/negative mentions
    positive_words = ["strong", "good", "excellent", "better", "superior", "leading"]
    negative_words = ["weak", "poor", "lacking", "behind", "inferior", "struggling"]
    
    for domain in your_list:
        if domain.lower() in analysis_lower:
            nearby_positive = sum(1 for word in positive_words if word in analysis_lower)
            nearby_negative = sum(1 for word in negative_words if word in analysis_lower)
            your_score += (nearby_positive * 5) - (nearby_negative * 3)
    
    for domain in competitor_list:
        if domain.lower() in analysis_lower:
            nearby_positive = sum(1 for word in positive_words if word in analysis_lower)
            nearby_negative = sum(1 for word in negative_words if word in analysis_lower)
            competitor_score += (nearby_positive * 5) - (nearby_negative * 3)
    
    return {
        "brand": brand,
        "your_domains": your_list,
        "competitor_domains": competitor_list,
        "comparison_analysis": result.get("response", ""),
        "scores": {
            "your_brand": min(100, max(0, your_score)),
            "competitors": min(100, max(0, competitor_score)),
            "gap": your_score - competitor_score
        },
        "citations": result.get("citations", []),
        "tokens_used": result.get("tokens_used"),
        "using_openai": OPENAI_AVAILABLE
    }


@router.get("/trending-topics")
async def trending_topics(
    brand: str = Query(..., description="Brand name"),
    domains: str = Query(None, description="Comma-separated domains to analyze"),
    num_topics: int = Query(5, ge=1, le=10, description="Number of trending topics")
):
    """
    Identify trending topics for brand visibility using AI.
    
    Example: /insights/trending-topics?brand=Nike&num_topics=5
    """
    domain_context = ""
    if domains:
        domain_list = [d.strip() for d in domains.split(",") if d.strip()]
        domain_context = f" on these domains: {', '.join(domain_list)}"
    
    prompt = f"""Identify the top {num_topics} trending topics relevant to {brand}{domain_context}.

For each topic, provide:
1. Topic name
2. Why it's trending
3. Opportunity for {brand}
4. Recommended content strategy

Focus on topics that would improve {brand}'s online visibility."""
    
    result = await generate_with_citations(
        prompt=prompt,
        brand=brand,
        include_web_search=False
    )
    
    # Parse topics from response (simplified)
    import re
    response_text = result.get("response", "")
    
    # Try to extract numbered topics
    topics = []
    lines = response_text.split('\n')
    current_topic = {}
    
    for line in lines:
        line = line.strip()
        # Look for numbered topics
        topic_match = re.match(r'^(\d+)\.\s*(.+)', line)
        if topic_match and len(topics) < num_topics:
            if current_topic:
                topics.append(current_topic)
            current_topic = {
                "rank": int(topic_match.group(1)),
                "name": topic_match.group(2),
                "description": ""
            }
        elif current_topic and line:
            current_topic["description"] += line + " "
    
    if current_topic:
        topics.append(current_topic)
    
    return {
        "brand": brand,
        "trending_topics": topics[:num_topics],
        "full_analysis": response_text,
        "domains_analyzed": domains.split(",") if domains else [],
        "tokens_used": result.get("tokens_used"),
        "using_openai": OPENAI_AVAILABLE
    }


@router.get("/health")
async def health_check():
    """Check if domain insights routes and OpenAI are available."""
    return {
        "status": "healthy",
        "openai_available": OPENAI_AVAILABLE,
        "routes": ["domain-stats", "analyze-domains", "domain-comparison", "trending-topics"]
    }