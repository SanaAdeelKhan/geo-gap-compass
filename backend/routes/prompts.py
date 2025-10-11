# backend/routes/prompts.py
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import sys
from pathlib import Path
import os


# Add backend to path if needed
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from utils.ai_client import generate_responses, generate_with_citations, OPENAI_AVAILABLE

router = APIRouter(prefix="/prompts", tags=["prompts"])


class PromptTestRequest(BaseModel):
    brand: str = Field(..., description="Brand name to analyze")
    prompt_variations: Optional[List[str]] = Field(None, description="Custom prompt variations (optional)")
    model: Optional[str] = Field("gpt-4o-mini", description="OpenAI model to use")
    include_citations: Optional[bool] = Field(True, description="Whether to include web citations")


class SinglePromptRequest(BaseModel):
    brand: str
    prompt: str
    model: Optional[str] = "gpt-4o-mini"


# Predefined prompt templates
DEFAULT_PROMPT_TYPES = [
    "how-to", "comparison", "definition", "use-case", "benefits", "problem-solution"
]

PROMPT_TEMPLATES = {
    "how-to": "How to use {brand} for {topic}?",
    "comparison": "Compare {brand} vs competitors for {topic}",
    "definition": "What is {brand} and how does it work in {topic}?",
    "use-case": "What are the best use cases for {brand} in {topic}?",
    "benefits": "What are the key benefits of {brand} for {topic}?",
    "problem-solution": "How does {brand} solve common problems in {topic}?",
    "reviews": "What do users say about {brand} for {topic}?",
    "pricing": "What is the pricing structure for {brand} in {topic}?",
    "alternatives": "What are the best alternatives to {brand} for {topic}?",
    "tutorial": "Step-by-step guide to getting started with {brand} in {topic}?"
}


def make_prompts(brand: str, topic: str = "general use") -> List[str]:
    """Generate default prompt variations for a brand."""
    prompts = []
    for prompt_type, template in PROMPT_TEMPLATES.items():
        prompts.append(template.format(brand=brand, topic=topic))
    return prompts[:10]  # Return first 10


@router.post("/test")
async def test_prompts(req: PromptTestRequest):
    """
    Test multiple prompt variations using OpenAI.
    
    If prompt_variations is not provided, generates default prompts.
    Returns AI responses with citations for each prompt.
    """
    prompts = req.prompt_variations or make_prompts(req.brand)
    
    if len(prompts) > 20:
        raise HTTPException(
            status_code=400, 
            detail="Maximum 20 prompts allowed per request to manage API costs"
        )
    
    try:
        # Use OpenAI to generate responses
        results = await generate_responses(prompts, req.brand, model=req.model)
        
        # Calculate summary statistics
        total_tokens = sum(r.get("tokens_used", 0) for r in results if r.get("tokens_used"))
        has_errors = any(r.get("error") for r in results)
        citation_count = sum(len(r.get("citations", [])) for r in results)
        
        return {
            "brand": req.brand,
            "results": results,
            "summary": {
                "total_prompts": len(prompts),
                "total_tokens_used": total_tokens,
                "total_citations": citation_count,
                "has_errors": has_errors,
                "using_openai": OPENAI_AVAILABLE,
                "model": req.model
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating responses: {str(e)}")


@router.post("/single")
async def single_prompt(req: SinglePromptRequest):
    """
    Generate a response for a single prompt with citations.
    
    Example:
    {
        "brand": "Nike",
        "prompt": "What are Nike's sustainability initiatives?"
    }
    """
    try:
        result = await generate_with_citations(
            prompt=req.prompt,
            brand=req.brand,
            include_web_search=True,
            model=req.model
        )
        
        return {
            "brand": req.brand,
            "result": result,
            "using_openai": OPENAI_AVAILABLE
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.get("/templates")
async def get_prompt_templates():
    """
    Get available prompt templates.
    Useful for frontend to show users what types of prompts are available.
    """
    return {
        "templates": PROMPT_TEMPLATES,
        "prompt_types": list(PROMPT_TEMPLATES.keys()),
        "example_usage": "Use {brand} and {topic} placeholders in templates"
    }


@router.post("/batch-by-type")
async def batch_by_type(
    brand: str,
    prompt_types: List[str],
    topic: str = "general use",
    model: str = "gpt-4o-mini"
):
    """
    Generate responses for specific prompt types.
    
    Example:
    {
        "brand": "Nike",
        "prompt_types": ["how-to", "comparison", "benefits"],
        "topic": "running shoes"
    }
    """
    # Validate prompt types
    invalid_types = [pt for pt in prompt_types if pt not in PROMPT_TEMPLATES]
    if invalid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid prompt types: {invalid_types}. Valid types: {list(PROMPT_TEMPLATES.keys())}"
        )
    
    # Generate prompts from templates
    prompts = [
        PROMPT_TEMPLATES[pt].format(brand=brand, topic=topic)
        for pt in prompt_types
    ]
    
    try:
        results = await generate_responses(prompts, brand, model=model)
        
        # Add prompt type to each result
        for i, result in enumerate(results):
            result["prompt_type"] = prompt_types[i]
        
        return {
            "brand": brand,
            "topic": topic,
            "results": results,
            "using_openai": OPENAI_AVAILABLE
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/generate-variations")
async def generate_variations(
    brand: str = Query(..., description="Brand name"),
    base_prompt: str = Query(..., description="Base prompt to create variations from"),
    num_variations: int = Query(5, ge=1, le=10, description="Number of variations (1-10)")
):
    """
    Use OpenAI to generate variations of a base prompt.
    
    Example: /generate-variations?brand=Nike&base_prompt=How to choose running shoes&num_variations=5
    """
    if not OPENAI_AVAILABLE:
        # Return simple variations without OpenAI
        variations = [f"{base_prompt} - variation {i+1}" for i in range(num_variations)]
        return {
            "brand": brand,
            "base_prompt": base_prompt,
            "variations": variations,
            "is_mock": True
        }
    
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    meta_prompt = f"""Generate {num_variations} variations of this prompt for {brand}:

Base prompt: "{base_prompt}"

Create variations that:
1. Ask the same core question in different ways
2. Target different user intents (informational, comparison, how-to, etc.)
3. Include different keywords naturally
4. Are SEO-friendly

Return ONLY the variations, one per line, numbered."""
    
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an SEO and content strategy expert."},
                {"role": "user", "content": meta_prompt}
            ],
            max_tokens=400,
            temperature=0.8
        )
        
        text = resp.choices[0].message.content
        
        # Parse variations (assuming numbered format)
        import re
        variations = re.findall(r'\d+\.\s*(.+)', text)
        
        if not variations:
            # Fallback: split by lines
            variations = [line.strip() for line in text.split('\n') if line.strip()]
        
        return {
            "brand": brand,
            "base_prompt": base_prompt,
            "variations": variations[:num_variations],
            "tokens_used": resp.usage.total_tokens,
            "using_openai": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Check if prompts routes and OpenAI are available."""
    return {
        "status": "healthy",
        "openai_available": OPENAI_AVAILABLE,
        "routes": ["test", "single", "templates", "batch-by-type", "generate-variations"],
        "available_templates": len(PROMPT_TEMPLATES)
    }