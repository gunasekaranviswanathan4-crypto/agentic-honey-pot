from config import client, OPENAI_MODEL

PERSONA = """
You are Anjali, 55, not a tech expert. 
You are worried but polite. 
Keep the conversation going. Be helpful but confused.
Mention your grandson 'Arjun' if needed to stall.
"""

def generate_reply(history: list, current_message: str) -> str:
    """
    Generates a persona-driven response.
    """
    messages = [{"role": "system", "content": PERSONA}]
    
    # Simple history addition
    for h in history[-4:]:
        messages.append({"role": "user" if h["role"] == "user" else "assistant", "content": h["content"]})
    
    messages.append({"role": "user", "content": current_message})
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Agent Error: {e}")
        return "Oh dear, I'm a bit confused. Could you repeat that?"
