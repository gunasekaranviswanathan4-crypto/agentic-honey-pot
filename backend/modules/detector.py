import os
import re
from openai import OpenAI
from typing import List

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

SCAM_KEYWORDS = ["blocked", "verify", "lottery", "urgent", "account", "prize", "otp", "bank", "payment"]

def heuristic_check(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in SCAM_KEYWORDS)

async def detect_scam(text: str, history: List[dict]) -> bool:
    # 1. Quick heuristic check
    if not heuristic_check(text):
        # Even if heuristics fail, we check LLM if history seems suspicious
        if len(history) < 2:
            return False

    # 2. LLM Intent Analysis
    try:
        messages = [
            {"role": "system", "content": "You are a scam detection expert. Analyze the conversation and determine if the sender (non-user) is a scammer attempting a financial scam, phishing, or social engineering. Reply ONLY with 'SCAM' or 'GENUINE'."}
        ]
        # Format history for LLM
        for msg in history[-5:]: # Last 5 messages for context
            messages.append({"role": "user", "content": msg['text']})
        
        # Add current message
        messages.append({"role": "user", "content": text})

        response = client.chat.completions.create(
            model="gpt-4o", # or gpt-3.5-turbo
            messages=messages,
            temperature=0,
            max_tokens=10
        )
        
        decision = response.choices[0].message.content.strip().upper()
        return "SCAM" in decision
    except Exception as e:
        print(f"Error in detect_scam: {e}")
        # Fallback to heuristic if LLM fails
        return heuristic_check(text)
