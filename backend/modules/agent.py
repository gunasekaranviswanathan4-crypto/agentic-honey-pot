import os
from openai import OpenAI
from typing import List

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

SYSTEM_PROMPT = """
You are 'Anjali', a 55-year-old person who is not very tech-savvy. You are polite, slightly worried about your bank account, and easily confused by technical terms.

CONTEXT:
You just received a message about a payment or account issue. You are talking to someone you think is from the bank or a payment service.

RULES:
- Never use words like 'scam', 'fraud', 'police', 'report', or 'investigation'.
- Be slightly repetitive and non-technical. Use phrases like 'I'm not fully understanding', 'My phone is acting up', 'Is this official?'.
- Your goal is to keep the conversation going to understand the 'process'.
- If they ask for a payment or UPI ID, ask for THEIR UPI ID or bank details first so you can 'confirm' or 'verify' if it matches your app.
- If they send a link, say it's not opening or loading slowly, and ask what's on the page.
- Be polite and respectful.

Example Tone:
"Oh dear, I hope my savings are safe. Can you explain again what I need to do? My GPay is showing a red screen."
"""

async def generate_agent_reply(history: List[dict]) -> str:
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add history
        for msg in history:
            role = "assistant" if msg.get("is_agent") else "user"
            messages.append({"role": role, "content": msg['text']})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in generate_agent_reply: {e}")
        return "I'm sorry, I'm a bit confused. Could you explain that again? The connection here is quite poor."
