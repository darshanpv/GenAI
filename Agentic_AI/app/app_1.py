import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

# Get project root (parent of current file's folder)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(dotenv_path="../../.env")

# Read config
#API_KEY = os.getenv("GITHUB_API_KEY")
#BASE_URL = os.getenv("GITHUB_BASE_URL")
#MODEL = os.getenv("GITHUB_MODEL_NAME")

API_KEY = os.getenv("LLAMA_API_KEY")
BASE_URL = os.getenv("LLAMA_BASE_URL")
MODEL = os.getenv("LLAMA_MODEL_NAME")


print("API_KEY loaded:", API_KEY is not None)
print("BASE_URL:", BASE_URL)
print("MODEL:", MODEL)

# Create client
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# Simple chat function
def chat(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    print("\n==== RAW RESPONSE ====")
    try:
        print(response.model_dump_json(indent=2))
    except Exception:
        print(response)

    # SAFE EXTRACTION
    print("\n==== PARSED FIELDS ====")
    print("choices:", getattr(response, "choices", None))

    if response.choices:
        msg = response.choices[0].message
        print("message object:", msg)
        print("content:", getattr(msg, "content", None))
    else:
        print("No choices returned!")

    print("======================\n")

    # safer return
    try:
        return response.choices[0].message.content
    except Exception as e:
        print("Error extracting content:", e)
        return None

# Run example
if __name__ == "__main__":
    user_input = "Explain fibonaci series in simple terms"
    reply = chat(user_input)
    print("User:", user_input)
    print("AI:", reply)