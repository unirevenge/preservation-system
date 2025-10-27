"""
Directory watchdog utility.

Monitors changes under selected paths and logs events to logs/watchdog.log.
Requires 'watchdog' package.
"""

from __future__ import annotations

import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Iterable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

REPO_ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = REPO_ROOT / "logs"


class LogHandler(FileSystemEventHandler):
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def on_any_event(self, event):
        self.logger.info("%s: %s", event.event_type, getattr(event, "src_path", ""))


def setup_logger() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("watchdog")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        LOGS_DIR / "watchdog.log", maxBytes=1_000_000, backupCount=3
    )
    console = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
    handler.setFormatter(fmt)
    console.setFormatter(fmt)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


def main(paths: Iterable[str] | None = None):
    logger = setup_logger()
    observer = Observer()
    handler = LogHandler(logger)

    watch_paths = [REPO_ROOT / "cade", REPO_ROOT / "ini-py", REPO_ROOT / "json"]
    if paths:
        watch_paths = [Path(p) for p in paths]

    for p in watch_paths:
        if p.exists():
            observer.schedule(handler, str(p), recursive=True)
            logger.info("Watching %s", p)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main(sys.argv[1:])
