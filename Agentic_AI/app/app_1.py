import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from utils.pushover_utils import send_push
from utils.logger import get_logger
from config.app_config import AppConfig

logger = get_logger(__name__, AppConfig.LOG_LEVEL)
# Read config
API_KEY = AppConfig.GITHUB_API_KEY
BASE_URL = AppConfig.GITHUB_BASE_URL
MODEL = AppConfig.GITHUB_MODEL_NAME

#API_KEY = AppConfig.LLAMA_API_KEY
#BASE_URL = AppConfig.LLAMA_BASE_URL
#MODEL = AppConfig.LLAMA_MODEL_NAME

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
    try:
        logger.debug(response.model_dump_json(indent=2))
    except Exception as e:
        logger.error(f"Error occurred while dumping response: {e}")

    # SAFE EXTRACTION
    logger.debug(f"Raw response object: {response}")

    if response.choices:
        msg = response.choices[0].message
    else:
        logger.debug("No choices returned!")
        return None
    # safer return
    try:
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error extracting content: {e}")
        return None

# Run example
if __name__ == "__main__":
    user_input = "What is the capital of France?"
    reply = chat(user_input)
    logger.info(f"User: {user_input}")
    logger.info(f"Assistant: {reply}")
    #send_push("Hello from the GitHub API client!", title="GitHub Client Test")
