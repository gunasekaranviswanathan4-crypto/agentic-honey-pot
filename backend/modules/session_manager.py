from typing import Dict, Optional
from models import Session, Message, Intelligence

# In-memory session store
sessions: Dict[str, Session] = {}

def get_or_create_session(session_id: str) -> Session:
    if session_id not in sessions:
        sessions[session_id] = Session(sessionId=session_id)
    return sessions[session_id]

def update_session(session_id: str, message: Message, is_agent: bool = False):
    session = get_or_create_session(session_id)
    session.messages.append(message)
    if not is_agent:
        session.turn_count += 1
    return session

def end_session(session_id: str):
    if session_id in sessions:
        sessions[session_id].status = "completed"
    return sessions.get(session_id)
