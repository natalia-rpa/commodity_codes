import logging
import os

LOG_DIR = "static"
LOG_FILE = os.path.join(LOG_DIR, "logs.txt")

_configured = False


def get_logger(name: str) -> logging.Logger:
    """Return a module logger; configures file + console handlers once."""
    global _configured

    if not _configured:
        os.makedirs(LOG_DIR, exist_ok=True)

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        root.addHandler(file_handler)
        root.addHandler(console_handler)
        _configured = True

    return logging.getLogger(name)


def log_phase(logger: logging.Logger, title: str) -> None:
    """Mark a clear phase boundary in the log (easy to scan for non-developers)."""
    logger.info("")
    logger.info("========== %s ==========", title)
