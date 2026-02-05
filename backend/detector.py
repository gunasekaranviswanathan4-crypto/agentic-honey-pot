from config import client, OPENAI_MODEL

def detect_scam(message: str) -> tuple[bool, float]:
    """
    Returns (is_scam, confidence_score)
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Analyze if the message is a scam. Respond with YES or NO followed by confidence 0-1."},
                {"role": "user", "content": f"Message: {message}"}
            ],
            temperature=0,
            max_tokens=10
        )
        content = response.choices[0].message.content.strip().upper()
        
        is_scam = "YES" in content
        confidence = 0.9 if is_scam else 0.1 # Simple fallback confidence
        
        # Try a bit harder to parse confidence if present
        if "0." in content or "1.0" in content:
            try:
                import re
                scores = re.findall(r"0\.\d+|1\.0", content)
                if scores:
                    confidence = float(scores[0])
            except:
                pass
                
        return is_scam, confidence
    except Exception as e:
        print(f"Detector Error: {e}")
        return False, 0.0
