import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load the environment variables from python.env file
load_dotenv(dotenv_path='python.env')

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key or "AIzaSy" not in api_key:
    print("Warning: GOOGLE_API_KEY is not set or seems to be invalid in Backend/python.env.")
    print("Please set your valid Google Gemini API key in Backend/python.env and try again.")
    exit(1)

# Configure settings from environment
model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
temperature = float(os.environ.get("GEMINI_TEMPERATURE", "0.4"))

print(f"Initializing ChatGoogleGenerativeAI using key from python.env...")
print(f"- Model: {model_name}")
print(f"- Temperature: {temperature}\n")

try:
    # Initialize the Chat model
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature,
    )
    # Test connection with a simple call
    print("Sending a test prompt to Gemini API...")
    response = llm.invoke("Say 'Connection successful!' in a single sentence.")
    print("\n[SUCCESS] Connected to Gemini API!")
    print(f"Response: {response.content.strip()}")
except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}")
    print("This might be because your API key is invalid, leaked, or deactivated.")
    exit(1)