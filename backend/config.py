import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load Environment Variables
load_dotenv()

# 2. Centralized Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

# 3. Fail Gracefully if API Key is missing
if not OPENAI_API_KEY or "sk-" not in OPENAI_API_KEY:
    print("\n" + "="*50)
    print("CRITICAL ERROR: OPENAI_API_KEY is missing or invalid.")
    print("Please add your key to the .env file.")
    print("Example: OPENAI_API_KEY=sk-proj-...")
    print("="*50 + "\n")
    sys.exit(1)

# 4. SINGLE OpenAI Client Instance
client = OpenAI(api_key=OPENAI_API_KEY)
