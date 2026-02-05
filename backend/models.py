from pydantic import BaseModel
from typing import Optional, Any

# Simple request model as requested
class ChatRequest(BaseModel):
    session_id: str
    message: str

# Intelligent data extraction structure
class ExtractedInfo(BaseModel):
    bank: Optional[str] = None
    upi_id: Optional[str] = None
    phone_number: Optional[str] = None
    phishing_url: Optional[str] = None

# Final response structure
class ChatResponse(BaseModel):
    reply: str
    is_scam: bool
    extracted_info: dict
    confidence_score: float
