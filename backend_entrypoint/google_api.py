import os
from typing import Optional

try:
    import google.generativeai as genai  
except Exception: 
    genai = None


EMBEDDING_MODEL = "models/embedding-001"
GENERATION_MODEL = "gemini-1.5-flash-8b"


def _configure_client() -> None:
    if genai is None:
        print("[Gemini] SDK not available.")
        return
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("[Gemini] GOOGLE_API_KEY not found in environment.")
        return
    print("[Gemini] Configuring SDK with API key.")
    genai.configure(api_key=api_key)



def official_token_count(text: str) -> Optional[int]:
    if genai is None:
        return None
    _configure_client()
    try:
        model = genai.TokenCounting(model=GENERATION_MODEL) 
        count = model.count_tokens(text)
        return int(count)
    except Exception:
        return None


def embed_text(text: str) -> Optional[list[float]]:
    if genai is None:
        return None
    _configure_client()
    try:
        model = genai.embed.ContentEmbedding(model=EMBEDDING_MODEL) 
        return model.embed(text)
    except Exception:
        return None


def generate_answer(prompt: str) -> Optional[str]:
    if genai is None:
        print("[Gemini] SDK not loaded.")
        return None

    _configure_client() 

    try:
        model = genai.GenerativeModel(GENERATION_MODEL)
        response = model.generate_content(prompt)
        print("[Gemini] Raw model response:", response)

        if hasattr(response, "text"):
            return response.text

        return str(response)
    except Exception as e:
        print("[Gemini] Error generating content:", e)
        return None

