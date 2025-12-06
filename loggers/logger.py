# logger.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = "app.log", level=logging.INFO):
    """Create and return a configured logger."""

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.hasHandlers():
        return logger

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s — %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler with rotation (max 5MB per file)
    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
