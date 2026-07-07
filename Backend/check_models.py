import os
from google import genai
from dotenv import load_dotenv

# Load the environment variables from your python.env file
load_dotenv(dotenv_path='python.env')

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key or "AIzaSy" not in api_key:
    print("Warning: GOOGLE_API_KEY is not set or seems to be invalid in Backend/python.env.")
    print("Please set your valid Google Gemini API key in Backend/python.env and try again.")
    exit(1)

# Configure the API client
client = genai.Client(api_key=api_key)

print("Finding available models for your API key...\n")

try:
    # List all available models
    for m in client.models.list():
        print(f"- {m.name}")
except Exception as e:
    print(f"Error checking models: {e}")
    print("This might be because your API key is invalid, leaked, or deactivated.")