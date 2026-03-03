import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")

client = Groq(api_key=api_key)

try:
    print("Sending test request to Groq...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Hello, this is a connectivity test."}],
    )
    print("Response received successfully:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error occurred: {type(e).__name__}")
    print(str(e))
