"""Logging configuration for Upstox TOTP SDK."""

import logging
import os
from logging import Logger


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up logging with rich formatting.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger
    """
    logger: Logger = logging.getLogger("upstox-totp")
    logger.setLevel(getattr(logging, level.upper()))

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


default_level = "DEBUG" if os.getenv("UPSTOX_DEBUG", "false").lower() in ("true", "1", "yes", "on") else "INFO"
logger: Logger = setup_logging(default_level)


def set_log_level(level: str) -> None:
    """Change the log level."""
    logger.setLevel(getattr(logging, level.upper()))
