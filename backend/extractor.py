import json
from config import client, OPENAI_MODEL

def extract_info(message: str) -> dict:
    """
    Extracts target intelligence using LLM JSON mode.
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Extract intelligence (bank, upi_id, phone_number, phishing_url) as JSON."},
                {"role": "user", "content": f"Message: {message}"}
            ],
            temperature=0,
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Extractor Error: {e}")
        return {}
