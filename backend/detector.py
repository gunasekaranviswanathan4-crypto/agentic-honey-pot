from config import client, OPENAI_MODEL

def detect_scam(message: str) -> tuple[bool, float]:
    """
    Detects whether a message indicates an attack or scam-like behavior.
    Returns (is_scam, confidence_score)
    """
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a cybersecurity analyst. "
                        "Decide if the following message describes a cyber attack, intrusion, or malicious activity. "
                        "Reply ONLY in this format: YES <confidence between 0 and 1> or NO <confidence between 0 and 1>."
                    )
                },
                {"role": "user", "content": message}
            ],
            temperature=0,
            max_tokens=10
        )

        content = response.choices[0].message.content.strip().upper()

        is_scam = content.startswith("YES")

        import re
        match = re.search(r"(0\.\d+|1\.0)", content)
        confidence = float(match.group(1)) if match else (0.9 if is_scam else 0.1)

        return is_scam, confidence

    except Exception as e:
        print(f"Detector Error: {e}")
        return False, 0.0
