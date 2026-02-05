import httpx
import os
from models import Session

GUVI_CALLBACK_URL = os.getenv("GUVI_CALLBACK_URL", "https://hackathon.guvi.in/api/updateHoneyPotFinalResult")

async def send_final_callback(session: Session):
    if session.callback_sent:
        return
    
    payload = {
        "sessionId": session.sessionId,
        "scamDetected": session.isScam,
        "totalMessagesExchanged": len(session.messages),
        "extractedIntelligence": {
            "bankAccounts": session.intelligence.bankAccounts,
            "upiIds": session.intelligence.upiIds,
            "phishingLinks": session.intelligence.phishingLinks,
            "phoneNumbers": session.intelligence.phoneNumbers,
            "suspiciousKeywords": session.intelligence.suspiciousKeywords
        },
        "agentNotes": session.agentNotes or "Automated honey-pot engagement completed."
    }
    
    print(f"Sending callback for session {session.sessionId}...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GUVI_CALLBACK_URL,
                json=payload,
                timeout=10.0
            )
            if response.status_code == 200:
                session.callback_sent = True
                print(f"Successfully sent callback for {session.sessionId}")
            else:
                print(f"Failed to send callback: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending callback: {e}")
