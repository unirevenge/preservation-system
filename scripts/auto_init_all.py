"""
CADE Auto-Init Orchestrator

Performs end-to-end initialization tasks:
- Ensure directories (logs/, json/) exist
- Merge and fix json/cspell.json from json/.cspell.json
- Static syntax check (py_compile) for package and scripts
- Optional lint/format/type checks (command hints)
- Set up rotating logging and optional watchdog
"""

import json
import logging
import py_compile
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Iterable, Set

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
JSON_DIR = REPO_ROOT / "json"
LOGS_DIR = REPO_ROOT / "logs"

CSPELL_PRIMARY = JSON_DIR / "cspell.json"
CSPELL_SECONDARY = JSON_DIR / ".cspell.json"


def setup_logging() -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("auto_init")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        LOGS_DIR / "auto_init.log", maxBytes=1_000_000, backupCount=3
    )
    console = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
    handler.setFormatter(fmt)
    console.setFormatter(fmt)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def merge_words(*lists: Iterable[str]) -> list[str]:
    seen: Set[str] = set()
    merged: list[str] = []
    for lst in lists:
        for w in lst or []:
            if not isinstance(w, str):
                continue
            if w not in seen:
                seen.add(w)
                merged.append(w)
    return merged


def update_cspell(logger: logging.Logger) -> None:
    a = read_json(CSPELL_PRIMARY)
    b = read_json(CSPELL_SECONDARY)
    # Merge keeping primary schema, falling back to secondary
    version = a.get("version") or b.get("version") or "0.2"
    language = a.get("language") or b.get("language") or "en"
    words = merge_words(a.get("words", []), b.get("words", []))
    flag_words = merge_words(a.get("flagWords", []), b.get("flagWords", []))

    # Dictionaries: prefer explicit entries from secondary if paths exist
    dictionaries = a.get("dictionaries") or b.get("dictionaries") or ["en-gb", "en-us"]
    dictionary_definitions = (
        a.get("dictionaryDefinitions")
        or b.get("dictionaryDefinitions")
        or [
            {
                "name": "en-gb",
                "path": "./dictionaries/en_GB.dic",
                "description": "British English",
            },
            {
                "name": "en-us",
                "path": "./dictionaries/en_US.dic",
                "description": "American English",
            },
        ]
    )

    updated = {
        "version": version,
        "language": language,
        "words": words,
        "flagWords": flag_words,
        "dictionaries": dictionaries,
        "dictionaryDefinitions": dictionary_definitions,
    }

    write_json(CSPELL_PRIMARY, updated)
    logger.info(
        "Updated %s (words=%d, flagWords=%d)",
        CSPELL_PRIMARY.relative_to(REPO_ROOT),
        len(words),
        len(flag_words),
    )


def py_syntax_check(logger: logging.Logger) -> None:
    failures: list[str] = []

    def check_dir(path: Path):
        for p in path.rglob("*.py"):
            # Skip venvs or caches
            if any(
                part in {".venv", "venv", "__pycache__", ".mypy_cache"}
                for part in p.parts
            ):
                continue
            try:
                py_compile.compile(str(p), doraise=True)
            except Exception as e:
                failures.append(f"{p.relative_to(REPO_ROOT)}: {e}")

    for target in [REPO_ROOT / "cade", SCRIPTS_DIR]:
        if target.exists():
            check_dir(target)
    if failures:
        for f in failures:
            logger.error("Syntax error: %s", f)
        raise SystemExit(1)
    logger.info("Python syntax check passed")


def print_command_hints(logger: logging.Logger) -> None:
    logger.info("Lint/format/type-check suggestions (run manually):")
    logger.info("  black .")
    logger.info("  ruff check --fix .  # or flake8 .")
    logger.info("  mypy cade scripts")


def main() -> int:
    logger = setup_logging()
    logger.info("Starting auto-init orchestration")
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    update_cspell(logger)
    py_syntax_check(logger)
    print_command_hints(logger)
    logger.info("Auto-init completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
