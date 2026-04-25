import requests
from typing import Optional

from config.app_config import AppConfig
from utils.logger import get_logger

logger = get_logger(__name__, AppConfig.LOG_LEVEL)


class PushoverError(Exception):
    """Custom exception for Pushover-related errors."""
    pass


def _validate_config():
    if not AppConfig.PUSHOVER_USER_KEY:
        raise PushoverError("Missing PUSHOVER_USER_KEY")
    if not AppConfig.PUSHOVER_APP_TOKEN:
        raise PushoverError("Missing PUSHOVER_APP_TOKEN")


def send_push(
    message: str,
    title: Optional[str] = None,
    priority: int = 0,
) -> bool:
    """
    Send a push notification via Pushover.
    """

    logger.debug("Preparing to send push notification")

    try:
        _validate_config()

        payload = {
            "user": AppConfig.PUSHOVER_USER_KEY,
            "token": AppConfig.PUSHOVER_APP_TOKEN,
            "message": message,
            "priority": priority,
        }

        if title:
            payload["title"] = title

        logger.debug(f"Payload prepared: {payload}")

        response = requests.post(
            AppConfig.PUSHOVER_BASE_URL,
            data=payload,
            timeout=AppConfig.REQUEST_TIMEOUT,
        )

        logger.debug(f"HTTP response status: {response.status_code}")

        if response.status_code != 200:
            raise PushoverError(
                f"HTTP {response.status_code}: {response.text}"
            )

        data = response.json()
        logger.debug(f"Response JSON: {data}")

        if data.get("status") != 1:
            raise PushoverError(f"API error: {data}")

        logger.info("Push notification sent successfully")
        return True

    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return False

    except PushoverError as e:
        logger.error(f"Pushover error: {e}")
        return False

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return False