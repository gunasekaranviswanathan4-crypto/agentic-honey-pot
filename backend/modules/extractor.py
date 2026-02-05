import re
import os
from openai import OpenAI
from typing import List, Dict
from models import Intelligence

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
)

def extract_with_regex(text: str) -> Dict[str, List[str]]:
    upi_pattern = r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}'
    link_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    phone_pattern = r'(?:\+91|0)?\s?[6-9]\d{4}\s?\d{5}'
    
    return {
        "upi": list(set(re.findall(upi_pattern, text))),
        "links": list(set(re.findall(link_pattern, text))),
        "phones": list(set(re.findall(phone_pattern, text)))
    }

async def extract_intelligence(text: str, history: List[dict]) -> Intelligence:
    # 1. Regex extraction
    regex_data = extract_with_regex(text)
    
    # 2. LLM extraction for contextual data (Bank Names, Account Numbers)
    intel = Intelligence(
        upiIds=regex_data["upi"],
        phishingLinks=regex_data["links"],
        phoneNumbers=regex_data["phones"]
    )
    
    try:
        prompt = f"""
        Analyze the following text and extract any bank account numbers, bank names, or suspicious keywords used by a scammer.
        Return the result as a JSON object: {{"bankAccounts": [], "bankNames": [], "keywords": []}}
        
        Text: {text}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "You are an intelligence extraction bot. Extract facts from text."},
                      {"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        import json
        data = json.loads(response.choices[0].message.content)
        
        intel.bankAccounts.extend(data.get("bankAccounts", []))
        intel.suspiciousKeywords.extend(data.get("keywords", []))
        # Deduplicate
        intel.bankAccounts = list(set(intel.bankAccounts))
        intel.suspiciousKeywords = list(set(intel.suspiciousKeywords))
        
    except Exception as e:
        print(f"Error in LLM extract_intelligence: {e}")
        
    return intel

def merge_intelligence(existing: Intelligence, new: Intelligence) -> Intelligence:
    return Intelligence(
        bankAccounts=list(set(existing.bankAccounts + new.bankAccounts)),
        upiIds=list(set(existing.upiIds + new.upiIds)),
        phishingLinks=list(set(existing.phishingLinks + new.phishingLinks)),
        phoneNumbers=list(set(existing.phoneNumbers + new.phoneNumbers)),
        suspiciousKeywords=list(set(existing.suspiciousKeywords + new.suspiciousKeywords))
    )
