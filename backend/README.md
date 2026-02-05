# Agentic Honey-Pot (Final Hackathon Version)

## Setup (Windows CMD)

1. **Activate Environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Config:**
   - Create a `.env` file in this folder.
   - Add: `OPENAI_API_KEY=your_key_here`

4. **Run:**
   ```cmd
   uvicorn main:app --reload
   ```

## Test (Copy into CMD)
```cmd
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"session_id\": \"demo1\", \"message\": \"Hi, I am from HDFC Bank. Send 10,000 to user@upi for verification.\"}"
```

## Response Format
```json
{
  "reply": "...agent story...",
  "is_scam": true,
  "extracted_info": {"bank": "HDFC", "upi_id": "user@upi", ...},
  "confidence_score": 0.9
}
```
