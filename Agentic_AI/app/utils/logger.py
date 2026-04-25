import logging


def get_logger(name: str, level: str = "DEBUG") -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name (str): Usually __name__ from caller
        level (str): Log level (DEBUG, INFO, etc.)

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Avoid duplicate handlers

    log_level = getattr(logging, level.upper(), logging.DEBUG)
    logger.setLevel(log_level)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger