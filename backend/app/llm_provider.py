from langchain_openai import ChatOpenAI
from .core.config import settings

def get_llm(temperature: float = 0.3) -> ChatOpenAI:
    """
    Returns an instance of ChatOpenAI configured to use OpenRouter.
    """
    if not settings.OPENROUTER_API_KEY:
        # Return a mock or placeholder or fail with descriptive error
        raise ValueError(
            "OPENROUTER_API_KEY is not set. Please update your settings."
        )
        
    return ChatOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        model=settings.OPENROUTER_MODEL,
        temperature=temperature,
        default_headers={
            "HTTP-Referer": "https://github.com/giapmanne69/SmartTransAI",
            "X-Title": "Smart Trans AI Agentic CAT Tool",
        }
    )

def get_local_llm(temperature: float = 0.3) -> ChatOpenAI:
    """
    Returns an instance of ChatOpenAI configured to use local Ollama with llama3.
    """
    return ChatOpenAI(
        api_key="ollama", # placeholder
        base_url="http://localhost:11434/v1",
        model="llama3",
        temperature=temperature
    )
