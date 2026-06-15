from langchain_openai import ChatOpenAI
from .core.config import settings

from typing import Optional

def get_llm(temperature: float = 0.3, model_name: Optional[str] = None) -> ChatOpenAI:
    """
    Returns an instance of ChatOpenAI configured to use OpenRouter.
    Supports overriding the model name for baseline evaluation comparison.
    """
    if not settings.OPENROUTER_API_KEY:
        # Return a mock or placeholder or fail with descriptive error
        raise ValueError(
            "OPENROUTER_API_KEY is not set. Please update your settings."
        )
        
    target_model = model_name or settings.OPENROUTER_MODEL
    return ChatOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        model=target_model,
        temperature=temperature,
        default_headers={
            "HTTP-Referer": "https://github.com/giapmanne69/SmartTransAI",
            "X-Title": "Smart Trans AI Agentic CAT Tool",
        }
    )

def get_local_llm(temperature: float = 0.3) -> ChatOpenAI:
    """
    Returns an instance of ChatOpenAI configured to use local Ollama with llama3.
    Falls back to OpenRouter with a free Llama-3 model if local Ollama is not running.
    """
    import http.client
    import urllib.parse
    
    ollama_running = False
    try:
        url = urllib.parse.urlparse("http://localhost:11434")
        conn = http.client.HTTPConnection(url.hostname, url.port, timeout=1.5)
        conn.request("GET", "/")
        response = conn.getresponse()
        if response.status == 200:
            ollama_running = True
    except Exception:
        pass

    if ollama_running:
        return ChatOpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            model="llama3",
            temperature=temperature,
            timeout=10
        )
    else:
        # Fallback to OpenRouter using Llama-3 model to simulate local Llama-3 model behavior
        fallback_model = "meta-llama/llama-3-8b-instruct:free"
        if not settings.OPENROUTER_API_KEY:
            raise ValueError(
                "Local Ollama is not running and OPENROUTER_API_KEY is missing. "
                "Please configure OPENROUTER_API_KEY in your .env file."
            )
            
        return ChatOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            model=fallback_model,
            temperature=temperature,
            default_headers={
                "HTTP-Referer": "https://github.com/giapmanne69/SmartTransAI",
                "X-Title": "Smart Trans AI (Ollama Fallback)",
            }
        )
