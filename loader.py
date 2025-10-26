import configparser
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PATHS_MANIFEST = os.path.join(ROOT_DIR, 'json', 'cade_paths.json')


def _load_paths() -> dict:
    try:
        with open(PATHS_MANIFEST, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            'root': os.path.normpath(os.path.join(ROOT_DIR, data.get('root', '.'))),
            'json': os.path.normpath(os.path.join(ROOT_DIR, data.get('json', 'json'))),
            'docs': os.path.normpath(os.path.join(ROOT_DIR, data.get('docs', '.'))),
            'scripts': os.path.normpath(os.path.join(ROOT_DIR, data.get('scripts', 'other'))),
            'starfield': os.path.normpath(os.path.join(ROOT_DIR, data.get('starfield', 'starfield'))),
        }
    except Exception:
        return {
            'root': ROOT_DIR,
            'json': os.path.join(ROOT_DIR, 'json'),
            'docs': ROOT_DIR,
            'scripts': os.path.join(ROOT_DIR, 'other'),
            'starfield': os.path.join(ROOT_DIR, 'starfield'),
        }


PATHS = _load_paths()


def resolve_path(name: str) -> str:
    if os.path.isabs(name):
        return name
    # Strip explicit 'root/' prefix to map to repository root
    if name.startswith('root/') or name.startswith('root\\'):
        name = name[5:]
    if any(sep in name for sep in ('/', '\\')):
        return os.path.normpath(os.path.join(PATHS['root'], name))
    candidates = [
        os.path.join(PATHS['root'], name),
        os.path.join(PATHS['json'], name),
        os.path.join(PATHS['docs'], name),
    ]
    for c in candidates:
        if os.path.exists(c):
            return os.path.normpath(c)
    return os.path.normpath(candidates[1])


def load_text(name: str, errors: str = 'strict') -> str:
    p = resolve_path(name)
    with open(p, 'r', encoding='utf-8', errors=errors) as f:
        return f.read()


def load_json(name: str) -> Union[dict, list]:
    """Load JSON data from a file."""
    with open(resolve_path(name), 'r', encoding='utf-8') as f:
        return json.load(f)


def load_ini(name: str) -> configparser.ConfigParser:
    """Load INI configuration from a file."""
    config = configparser.ConfigParser()
    config.read(resolve_path(name))
    return config
