from pathlib import Path

from cade_core import CadeCore
from loader import resolve_path


def test_resolve_path_json_dir():
    p = resolve_path("json/cade_manifest.json")
    assert Path(p).exists()


def test_cade_core_initialization():
    core = CadeCore()
    assert core.load_core_files() is True
    status = core.get_status()
    assert status.get("initialized") is True
    assert status.get("manifest_loaded") is True
