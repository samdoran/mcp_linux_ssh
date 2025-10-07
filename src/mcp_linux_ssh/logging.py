import logging
import pathlib
import sys
from logging.handlers import RotatingFileHandler


def setup_logging_to_file():
    logger = logging.getLogger("mcp-linux-ssh")
    logger.setLevel(logging.INFO)

    log_paths = {
        "darwin": pathlib.Path("~/Library/Logs/mcp-linux-ssh.log").expanduser(),
        "linux": pathlib.Path("~/.local/share/logs/mcp-linux-ssh.log").expanduser(),
    }

    log_file = log_paths.get(sys.platform, log_paths["linux"])

    if not log_file.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.touch(mode=0o0600)

    handler = RotatingFileHandler(
        filename=log_file,
        encoding="utf-8",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    logger.addHandler(handler)

    formatter = logging.Formatter(
        fmt="{asctime} [{levelname}] {name}: {message}",
        datefmt="%F %H:%M:%S",
        style="{",
    )
    handler.setFormatter(formatter)

    return logger
