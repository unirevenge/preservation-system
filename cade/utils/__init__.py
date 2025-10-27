"""
CADE Utils Package

This package contains utility functions and helpers used throughout the CADE system.
"""

import os
import sys
import json
import logging
from typing import Any, Dict, List, Optional, Union, TypeVar, Type, Callable
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('cade')

# Type variables for generic functions
T = TypeVar('T')

# Common paths
PACKAGE_ROOT = Path(__file__).parent.parent
DATA_DIR = PACKAGE_ROOT / 'data'
CONFIG_DIR = PACKAGE_ROOT / 'config'

# Ensure directories exist
for directory in [DATA_DIR, CONFIG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

def load_json(file_path: Union[str, Path]) -> Union[Dict, List, None]:
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logger.error(f"Error loading JSON from {file_path}: {e}")
        return None

def save_json(data: Any, file_path: Union[str, Path], **kwargs) -> bool:
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, **kwargs)
        return True
    except (TypeError, IOError) as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        return False

# Export public API
__all__ = [
    'logger',
    'PACKAGE_ROOT',
    'DATA_DIR',
    'CONFIG_DIR',
    'load_json',
    'save_json',
]
