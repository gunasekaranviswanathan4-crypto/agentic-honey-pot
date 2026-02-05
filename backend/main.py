from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from models import ChatRequest, ChatResponse
from detector import detect_scam
from extractor import extract_info
from agent import generate_reply

app = FastAPI()

# Allow all origins for demo/hackathon purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage
sessions = {}

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    html_file = Path(__file__).parent / "index.html"
    if html_file.exists():
        return html_file.read_text()
    return {"message": "API is live. Use /chat or /health endpoints."}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    sid = request.session_id
    msg = request.message
    
    if sid not in sessions:
        sessions[sid] = []
        
    # 1. Detection
    is_scam, score = detect_scam(msg)
    
    # 2. Extraction
    intel = extract_info(msg)
    
    # 3. Generation
    reply = generate_reply(sessions[sid], msg)
    
    # Store history
    sessions[sid].append({"role": "user", "content": msg})
    sessions[sid].append({"role": "assistant", "content": reply})
    
    return ChatResponse(
        reply=reply,
        is_scam=is_scam,
        extracted_info=intel,
        confidence_score=score
    )

# Run the app (optional when deploying on Render)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
