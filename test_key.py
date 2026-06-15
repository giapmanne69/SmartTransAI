import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load env variables manually from backend/.env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", ".env")
api_key = None
base_url = "https://openrouter.ai/api/v1"
model = "google/gemini-2.5-flash" # let's use a standard fast model for testing

if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("OPENROUTER_API_KEY="):
                api_key = line.split("=")[1].strip()
            elif line.startswith("OPENROUTER_BASE_URL="):
                base_url = line.split("=")[1].strip()

print(f"Loaded API Key: {api_key[:10]}...{api_key[-10:] if api_key else ''}")
print(f"Base URL: {base_url}")

if not api_key:
    print("API Key not found.")
    exit(1)

try:
    llm = ChatOpenAI(
        api_key=api_key,
        base_url=base_url,
        model="google/gemini-2.5-flash",
        temperature=0.3,
        timeout=10
    )
    print("Sending test message...")
    response = llm.invoke([HumanMessage(content="Say Hello in exactly one word.")])
    print(f"Response: {response.content}")
except Exception as e:
    print(f"Error occurred: {str(e)}")
