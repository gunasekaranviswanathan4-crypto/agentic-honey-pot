from config import client, OPENAI_MODEL


def detect_scam(message: str) -> dict:
    """
    Analyze message and return scam/threat detection result
    """

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a cybersecurity threat detection system. "
                        "Analyze the message and decide if it indicates malicious or suspicious activity "
                        "(brute force, failed logins, hacking attempts, attacks, malware, etc).\n\n"
                        "Respond STRICTLY in this format:\n"
                        "RESULT: YES or NO\n"
                        "CONFIDENCE: number between 0 and 1\n"
                        "REASON: short explanation"
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0,
            max_tokens=80
        )

        content = response.choices[0].message.content.strip()

        # Defaults
        is_scam = False
        confidence = 0.0
        reason = "No threat detected"

        # Parse response
        lines = content.splitlines()
        for line in lines:
            line = line.strip().upper()
            if line.startswith("RESULT:"):
                is_scam = "YES" in line
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.split(":")[1].strip())
                except:
                    confidence = 0.5
            elif line.startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()

        return {
            "reply": reason,
            "is_scam": is_scam,
            "confidence_score": confidence,
            "extracted_info": {
                "analysis": reason
            }
        }

    except Exception as e:
        print(f"Detector Error: {e}")
        return {
            "reply": "Detection failed due to system error",
            "is_scam": False,
            "confidence_score": 0.0,
            "extracted_info": {}
        }
