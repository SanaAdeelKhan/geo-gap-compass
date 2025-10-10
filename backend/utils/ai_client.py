# backend/utils/ai_client.py
import os, json, asyncio
from typing import List, Dict
from pathlib import Path

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
HERE = Path(__file__).resolve().parents[2]
DEMO_PATH = HERE / "demo_data" / "fake_citations.json"

async def _mock_generate(prompts: List[str], brand: str):
    # read demo responses and map to prompts
    data = {}
    try:
        raw = json.loads(DEMO_PATH.read_text())
    except Exception:
        raw = {}
    results = []
    for i, p in enumerate(prompts):
        # simple mock: pretend some prompts include brand mention URLs, some don't
        has_brand = (i % 3 != 0)
        citations = []
        if has_brand:
            citations = [f"https://example.com/{brand.lower()}/article-{i}", "https://competitor.com/page"]
        else:
            citations = ["https://competitor.com/top-resource"]
        results.append({"prompt": p, "response": f"Mock response for '{p}'", "citations": citations})
    await asyncio.sleep(0.1)
    return results

async def generate_responses(prompts: List[str], brand: str):
    # If OPENAI_KEY is present, you can call OpenAI here. For now we fallback to mock.
    if not OPENAI_KEY:
        return await _mock_generate(prompts, brand)

    # --- Example: call OpenAI ChatCompletion (synchronously here for brevity) ---
    # NOTE: make sure you have openai package installed and OPENAI_API_KEY set.
    import openai
    openai.api_key = OPENAI_KEY
    results = []
    for p in prompts:
        messages = [{"role":"system","content":"You are an assistant that cites URLs when applicable."},
                    {"role":"user","content":p}]
        resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, max_tokens=300)
        text = resp["choices"][0]["message"]["content"]
        # extract URLs simply
        import re
        urls = re.findall(r"https?://[^\s,]+", text)
        results.append({"prompt": p, "response": text, "citations": urls})
    return results
