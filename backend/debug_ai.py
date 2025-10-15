import os
from pathlib import Path
from dotenv import load_dotenv

print("=== Debug Info ===")
print("Current dir:", os.getcwd())

# Simulate what ai_client.py does
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_KEY loaded: {bool(OPENAI_KEY)}")
if OPENAI_KEY:
    print(f"Key preview: {OPENAI_KEY[:15]}...")

# Check import
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = bool(OPENAI_KEY)
    print(f"AsyncOpenAI imported: True")
    print(f"OPENAI_AVAILABLE: {OPENAI_AVAILABLE}")
except ImportError as e:
    OPENAI_AVAILABLE = False
    print(f"AsyncOpenAI import failed: {e}")
    print(f"OPENAI_AVAILABLE: {OPENAI_AVAILABLE}")

print("\n=== From actual module ===")
from utils.ai_client import OPENAI_AVAILABLE as MODULE_AVAILABLE, OPENAI_KEY as MODULE_KEY
print(f"Module OPENAI_KEY: {bool(MODULE_KEY)}")
print(f"Module OPENAI_AVAILABLE: {MODULE_AVAILABLE}")
