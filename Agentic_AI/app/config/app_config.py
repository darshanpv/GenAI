import os
from dotenv import load_dotenv
from utils.logger import get_logger

logger = get_logger(__name__, os.getenv("LOG_LEVEL", "DEBUG"))

# Load environment variables
load_dotenv(dotenv_path="../../.env")


class AppConfig:
    """Application configuration"""

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")  # DEBUG, INFO, WARNING, ERROR

    # Pushover
    PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
    PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
    PUSHOVER_BASE_URL = os.getenv("PUSHOVER_BASE_URL")

    # GitHub API
    GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
    GITHUB_BASE_URL = os.getenv("GITHUB_BASE_URL")
    GITHUB_MODEL_NAME = os.getenv("GITHUB_MODEL_NAME")

    # LLaMA API (if used)
    LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
    LLAMA_BASE_URL = os.getenv("LLAMA_BASE_URL")
    LLAMA_MODEL_NAME = os.getenv("LLAMA_MODEL_NAME")

    # Request settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))