import json
from typing import List

from loader import load_json

CORE_FILES: List[str] = [
    "root/json/cade_persona.json",
    "root/json/cade_knowledgebases.json",
    "root/json/cade_manifest.json",
    "root/json/dawid_health_history.json",
    "root/json/.cspell.json",
]


def main() -> None:
    loaded = {}
    for name in CORE_FILES:
        data = load_json(name)
        # Keep a small identity for confirmation and avoid dumping sensitive content
        if isinstance(data, dict):
            keys_preview = list(data.keys())[:5]
            loaded[name] = {
                "type": "object",
                "keys": keys_preview,
            }
        elif isinstance(data, list):
            loaded[name] = {
                "type": "list",
                "len": len(data),
            }
        else:
            loaded[name] = {
                "type": type(data).__name__,
            }

    print(json.dumps({
        "status": "ok",
        "loaded_files": loaded,
    }, indent=2))


if __name__ == "__main__":
    main()
