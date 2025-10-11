# backend/utils/ai_client.py
import os
import json
import asyncio
import re
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Define paths first
HERE = Path(__file__).resolve().parent.parent  # backend/
DEMO_PATH = HERE / "demo_data" / "fake_citations.json"

# Load environment variables from .env - use explicit path
ENV_PATH = HERE / ".env"
load_dotenv(dotenv_path=ENV_PATH)

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Try to import OpenAI at module level
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = bool(OPENAI_KEY)
except ImportError:
    OPENAI_AVAILABLE = False


async def _mock_generate(prompts: List[str], brand: str) -> List[Dict[str, Any]]:
    """Fallback mock responses if OPENAI_KEY is missing."""
    demo_responses = {}
    try:
        demo_responses = json.loads(DEMO_PATH.read_text())
    except Exception:
        pass
    
    results = []
    for i, p in enumerate(prompts):
        if str(i) in demo_responses:
            results.append(demo_responses[str(i)])
        else:
            has_brand = (i % 3 != 0)
            citations = (
                [f"https://example.com/{brand.lower()}/article-{i}", "https://competitor.com/page"] 
                if has_brand 
                else ["https://competitor.com/top-resource"]
            )
            results.append({
                "prompt": p,
                "response": f"Mock response for '{p}' about {brand}",
                "citations": citations,
                "is_mock": True
            })
    
    await asyncio.sleep(0.1)
    return results


async def generate_with_citations(
    prompt: str,
    brand: str,
    include_web_search: bool = False,
    model: str = "gpt-4o-mini",
    timeout: float = 30.0
) -> Dict[str, Any]:
    """
    Generate AI response with citations.
    
    Args:
        prompt: The question/prompt
        brand: Brand name for context
        include_web_search: Whether to search web for citations
        model: OpenAI model to use
        timeout: Timeout per request
    
    Returns:
        Dict with prompt, response, citations, and metadata
    """
    if not OPENAI_AVAILABLE:
        return {
            "prompt": prompt,
            "response": f"Mock response for '{prompt}' about {brand}",
            "citations": ["https://example.com/mock"],
            "is_mock": True
        }

    client = AsyncOpenAI(api_key=OPENAI_KEY)
    
    try:
        resp = await asyncio.wait_for(
            client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are an expert analyst helping with {brand} research. Provide detailed, factual information. When applicable, mention authoritative sources or websites."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            ),
            timeout=timeout
        )
        
        text = resp.choices[0].message.content or ""
        
        # Extract URLs from response
        urls = re.findall(r"https?://[^\s,\)]+", text)
        urls = [url.rstrip(".,;:!?)") for url in urls]
        
        return {
            "prompt": prompt,
            "response": text,
            "citations": urls,
            "model": model,
            "tokens_used": resp.usage.total_tokens if resp.usage else None
        }
        
    except asyncio.TimeoutError:
        return {
            "prompt": prompt,
            "response": "",
            "citations": [],
            "error": f"Request timed out after {timeout}s"
        }
    except Exception as e:
        return {
            "prompt": prompt,
            "response": "",
            "citations": [],
            "error": str(e)
        }


async def generate_responses(
    prompts: List[str], 
    brand: str,
    model: str = "gpt-4o-mini",
    timeout: float = 30.0
) -> List[Dict[str, Any]]:
    """
    Generate AI responses for multiple prompts.
    
    Args:
        prompts: List of prompt strings to process
        brand: Brand name for context
        model: OpenAI model to use
        timeout: Timeout per request in seconds
    
    Returns:
        List of dicts with keys: prompt, response, citations, (optional: error, is_mock)
    """
    if not OPENAI_AVAILABLE:
        return await _mock_generate(prompts, brand)

    client = AsyncOpenAI(api_key=OPENAI_KEY)
    results = []

    for p in prompts:
        try:
            resp = await asyncio.wait_for(
                client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system", 
                            "content": f"You are an assistant helping with {brand} content. Cite URLs when applicable."
                        },
                        {"role": "user", "content": p}
                    ],
                    max_tokens=300,
                    temperature=0.7
                ),
                timeout=timeout
            )
            
            text = resp.choices[0].message.content or ""
            urls = re.findall(r"https?://[^\s,\)]+", text)
            urls = [url.rstrip(".,;:!?)") for url in urls]
            
            results.append({
                "prompt": p,
                "response": text,
                "citations": urls,
                "model": model,
                "tokens_used": resp.usage.total_tokens if resp.usage else None
            })
            
        except asyncio.TimeoutError:
            results.append({
                "prompt": p,
                "response": "",
                "citations": [],
                "error": f"Request timed out after {timeout}s"
            })
        except Exception as e:
            results.append({
                "prompt": p,
                "response": "",
                "citations": [],
                "error": str(e)
            })

    return results


async def analyze_competitors(
    brand: str,
    competitors: List[str],
    model: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """Analyze competitors for a brand."""
    if not OPENAI_AVAILABLE:
        return {
            "brand": brand,
            "competitors": competitors,
            "analysis": f"Mock competitor analysis for {brand} vs {', '.join(competitors)}",
            "is_mock": True
        }
    
    client = AsyncOpenAI(api_key=OPENAI_KEY)
    
    prompt = f"""Analyze the competitive landscape for {brand}.
    
Main competitors: {', '.join(competitors)}

Provide a detailed analysis including:
1. Key differentiators for {brand}
2. Each competitor's strengths and weaknesses
3. Market positioning insights
4. Strategic recommendations for {brand}
"""
    
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a competitive analysis expert specializing in brand strategy."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return {
            "brand": brand,
            "competitors": competitors,
            "analysis": resp.choices[0].message.content,
            "tokens_used": resp.usage.total_tokens if resp.usage else None
        }
        
    except Exception as e:
        return {
            "brand": brand,
            "competitors": competitors,
            "analysis": "",
            "error": str(e)
        }


async def analyze_domains(
    domains: List[str],
    brand: str,
    model: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """Analyze domain relevance and quality for a brand."""
    if not OPENAI_AVAILABLE:
        return {
            "brand": brand,
            "domains": domains,
            "analysis": f"Mock domain analysis for {', '.join(domains)}",
            "is_mock": True
        }
    
    client = AsyncOpenAI(api_key=OPENAI_KEY)
    
    prompt = f"""Analyze these domains for {brand} marketing visibility:

Domains: {', '.join(domains)}

For each domain, provide:
1. Authority and credibility assessment
2. Relevance to {brand} and its industry
3. Potential value for brand visibility
4. Specific recommendations for {brand} to leverage or engage with each domain
"""
    
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a digital marketing and SEO expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return {
            "brand": brand,
            "domains": domains,
            "analysis": resp.choices[0].message.content,
            "tokens_used": resp.usage.total_tokens if resp.usage else None
        }
        
    except Exception as e:
        return {
            "brand": brand,
            "domains": domains,
            "analysis": "",
            "error": str(e)
        }


async def generate_gap_analysis(
    brand: str,
    missing_topics: List[str],
    model: str = "gpt-4o-mini"
) -> Dict[str, Any]:
    """Generate content gap analysis and recommendations."""
    if not OPENAI_AVAILABLE:
        return {
            "brand": brand,
            "gaps": missing_topics,
            "recommendations": f"Mock gap analysis for {', '.join(missing_topics)}",
            "is_mock": True
        }
    
    client = AsyncOpenAI(api_key=OPENAI_KEY)
    
    prompt = f"""Analyze content gaps for {brand}:

Missing or weak content areas: {', '.join(missing_topics)}

Provide:
1. Why each gap matters for {brand}'s online visibility
2. Priority ranking (High/Medium/Low) for addressing each gap
3. Specific content recommendations for each gap
4. Expected impact on brand visibility and SEO
"""
    
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a content strategy and SEO expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return {
            "brand": brand,
            "gaps": missing_topics,
            "recommendations": resp.choices[0].message.content,
            "tokens_used": resp.usage.total_tokens if resp.usage else None
        }
        
    except Exception as e:
        return {
            "brand": brand,
            "gaps": missing_topics,
            "recommendations": "",
            "error": str(e)
        }


async def generate_single_response(
    prompt: str,
    brand: str,
    **kwargs
) -> Dict[str, Any]:
    """Convenience method for single prompt."""
    results = await generate_responses([prompt], brand, **kwargs)
    return results[0]