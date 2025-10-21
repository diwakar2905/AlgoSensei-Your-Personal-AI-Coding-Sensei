import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the environment variables from your python.env file
load_dotenv(dotenv_path='python.env')

# Configure the API key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("Finding available models for your API key...\n")

# List all available models and check their supported methods
for m in genai.list_models():
  # We are looking for a model that supports the 'generateContent' method
  if 'generateContent' in m.supported_generation_methods:
    print(f"- {m.name}")

print("\nCopy one of the model names from the list above and paste it into your main.py file.")