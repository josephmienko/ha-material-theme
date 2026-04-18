from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "src" / "material-theme.json"
OUTPUT_PATH = ROOT / "themes" / "ha-material-theme.yaml"
BUILD_SCRIPT_PATH = ROOT / "scripts" / "build_theme.py"


def load_build_theme_module():
    spec = importlib.util.spec_from_file_location("build_theme", BUILD_SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_theme_document_uses_expected_theme_names():
    module = load_build_theme_module()
    source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))

    document = module.build_theme_document(source)

    assert list(document.keys()) == [
        "Crooked Material",
        "Crooked Material Medium Contrast",
        "Crooked Material High Contrast",
    ]


def test_generated_yaml_matches_source_fixture():
    module = load_build_theme_module()
    source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
    expected = module.build_theme_document(source)
    generated = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))

    assert generated == expected
