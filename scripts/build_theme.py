#!/usr/bin/env python3
"""Build the extracted Home Assistant Material theme artifact from the JSON source."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "src" / "material-theme.json"
OUTPUT_PATH = ROOT / "themes" / "ha-material-theme.yaml"

THEME_VARIANTS = (
    ("Crooked Material", "light", "dark"),
    ("Crooked Material Medium Contrast", "light-medium-contrast", "dark-medium-contrast"),
    ("Crooked Material High Contrast", "light-high-contrast", "dark-high-contrast"),
)

ELEVATION_TOKENS = {
    "md-sys-elevation-level0": "none",
    "md-sys-elevation-level1": (
        "rgba(from var(--md-sys-color-shadow) r g b / 0.2) 0px 2px 1px -1px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.14) 0px 1px 1px 0px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.12) 0px 1px 3px 0px"
    ),
    "md-sys-elevation-level2": (
        "rgba(from var(--md-sys-color-shadow) r g b / 0.2) 0px 3px 3px -2px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.14) 0px 3px 4px 0px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.12) 0px 1px 8px 0px"
    ),
    "md-sys-elevation-level3": (
        "rgba(from var(--md-sys-color-shadow) r g b / 0.2) 0px 3px 5px -1px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.14) 0px 6px 10px 0px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.12) 0px 1px 18px 0px"
    ),
    "md-sys-elevation-level4": (
        "rgba(from var(--md-sys-color-shadow) r g b / 0.2) 0px 5px 5px -3px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.14) 0px 8px 10px 1px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.12) 0px 3px 14px 2px"
    ),
    "md-sys-elevation-level5": (
        "rgba(from var(--md-sys-color-shadow) r g b / 0.2) 0px 7px 8px -4px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.14) 0px 12px 17px 2px, "
        "rgba(from var(--md-sys-color-shadow) r g b / 0.12) 0px 5px 22px 4px"
    ),
}

SHAPE_TOKENS = {
    "md-sys-shape-corner-none": "0",
    "md-sys-shape-corner-small": "8px",
    "md-sys-shape-corner-medium": "12px",
    "md-sys-shape-corner-large": "16px",
    "md-sys-shape-corner-extra-large": "28px",
    "md-sys-shape-corner-full": "9999px",
}

LEGACY_ALIAS_TOKENS = {
    "primary-color": "#6D9B7B",
    "accent-color": "#FFDE3F",
    "outline-color": "var(--md-sys-color-outline)",
    "divider-color": "var(--md-sys-color-outline-variant)",
    "primary-text-color": "var(--md-sys-color-on-surface)",
    "secondary-text-color": "var(--md-sys-color-on-surface-variant)",
    "text-primary-color": "var(--md-sys-color-surface)",
    "state-icon-color": "var(--md-sys-color-on-surface-variant)",
    "label-badge-text-color": "var(--md-sys-color-on-surface-variant)",
    "secondary-background-color": "var(--md-sys-color-secondary-container)",
    "primary-background-color": "var(--md-sys-color-surface-container)",
    "card-background-color": "var(--md-sys-color-surface-container-low)",
    "ha-card-background": "var(--md-sys-color-surface-container-low)",
    "ha-card-border-radius": "var(--md-sys-shape-corner-extra-large)",
    "ha-card-box-shadow": "var(--md-sys-elevation-level1)",
    "ha-card-border-color": "#00000000",
    "ha-card-border-width": "0px",
    "ha-card-border-style": "none",
    "ha-card-border": "none",
    "lovelace-background": "var(--md-sys-color-surface)",
    "sidebar-selected-text-color": "var(--md-sys-color-secondary)",
    "sidebar-selected-icon-color": "var(--md-sys-color-on-secondary-container)",
    "sidebar-selected-background": "var(--md-sys-color-secondary-container)",
    "sidebar-icon-color": "var(--md-sys-color-on-surface-variant)",
    "sidebar-text-color": "var(--md-sys-color-on-surface-variant)",
    "sidebar-menu-button-text-color": "var(--md-sys-color-on-surface-variant)",
    "sidebar-state-pressed-background": "var(--md-sys-color-on-secondary-container)",
    "sidebar-background-color": "var(--md-sys-color-surface-container)",
    "app-header-background-color": "var(--md-sys-color-surface)",
    "app-header-text-color": "var(--md-sys-color-on-surface)",
    "app-header-edit-text-color": "var(--md-sys-color-on-surface-variant)",
    "app-header-border-bottom": "none",
    "error-color": "var(--md-sys-color-error)",
    "on-error-color": "var(--md-sys-color-on-error)",
    "warning-color": "var(--md-sys-color-warning, #ffa600)",
    "success-color": "var(--md-sys-color-success, #43a047)",
    "info-color": "var(--md-sys-color-info, #039be5)",
    "disabled-text-color": "rgba(from var(--md-sys-color-on-surface) r g b / 0.38)",
    "disabled-color": "rgba(from var(--md-sys-color-on-surface) r g b / 0.12)",
    "light-primary-color": "hsl(from var(--md-sys-color-primary) h s calc(l + 20))",
    "dark-primary-color": "hsl(from var(--md-sys-color-primary) h s calc(l - 20))",
    "darker-primary-color": "hsl(from var(--md-sys-color-primary) h s calc(l - 40))",
    "mdc-theme-primary": "#6D9B7B",
    "mdc-theme-secondary": "#FFDE3F",
    "mdc-theme-background": "var(--primary-background-color)",
    "mdc-theme-surface": "var(--card-background-color)",
    "mdc-theme-on-primary": "var(--md-sys-color-on-primary)",
    "mdc-theme-on-secondary": "var(--md-sys-color-on-secondary)",
    "mdc-theme-on-surface": "var(--md-sys-color-on-surface)",
    "mdc-theme-text-primary-on-background": "var(--primary-text-color)",
    "mdc-theme-text-secondary-on-background": "var(--secondary-text-color)",
    "mdc-theme-error": "var(--error-color)",
}


def camel_to_kebab(value: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", value).lower()


def tone_label(raw: str) -> str:
    return "05" if raw == "5" else raw


def build_mode_tokens(scheme: dict[str, str], palettes: dict[str, dict[str, str]]) -> dict[str, str]:
    mode: dict[str, str] = {}
    for token_name, token_value in scheme.items():
        mode[f"md-sys-color-{camel_to_kebab(token_name)}"] = token_value

    for palette_name, tones in palettes.items():
        for tone in sorted(tones.keys(), key=lambda item: int(item)):
            mode[f"md-sys-color-{palette_name}-{tone_label(tone)}"] = tones[tone]

    return mode


def build_theme_document(source: dict) -> dict[str, dict]:
    schemes = source["schemes"]
    palettes = source.get("palettes", {})
    doc: dict[str, dict] = {}

    for theme_name, light_key, dark_key in THEME_VARIANTS:
        theme: dict[str, object] = {}
        theme.update(ELEVATION_TOKENS)
        theme.update(SHAPE_TOKENS)
        theme["modes"] = {
            "light": build_mode_tokens(schemes[light_key], palettes),
            "dark": build_mode_tokens(schemes[dark_key], palettes),
        }
        theme.update(LEGACY_ALIAS_TOKENS)
        doc[theme_name] = theme

    return doc


def write_json_as_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    source_path = Path(sys.argv[1]) if len(sys.argv) > 1 else SOURCE_PATH
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else OUTPUT_PATH
    source = json.loads(source_path.read_text(encoding="utf-8"))
    document = build_theme_document(source)
    write_json_as_yaml(output_path, document)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
