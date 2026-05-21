"""LLM Client for calling the Gemini API."""

import httpx

from zomato_cursor.config import settings

class LLMError(Exception):
    """Exception raised for errors during LLM communication."""
    def __init__(self, message: str, retryable: bool = False):
        super().__init__(message)
        self.retryable = retryable

class LLMClient:
    def complete(self, prompt: str) -> str:
        """Call Gemini API via REST and return the raw text response."""
        api_key = settings.LLM_API_KEY
        if not api_key:
            raise LLMError("LLM_API_KEY is missing", retryable=False)
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.LLM_MODEL}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        
        try:
            with httpx.Client(timeout=settings.LLM_TIMEOUT_SEC) as client:
                response = client.post(url, json=payload)
                
            if response.status_code != 200:
                raise LLMError(f"Provider error {response.status_code}: {response.text}", retryable=True)
                
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                parts = data["candidates"][0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            
            raise LLMError("Empty response from provider", retryable=True)
            
        except httpx.RequestError as e:
            raise LLMError(f"Network error: {str(e)}", retryable=True)
