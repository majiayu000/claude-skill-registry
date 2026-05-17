#!/usr/bin/env python3
"""Plugin index loading and writing helpers."""

from __future__ import annotations

import json
from pathlib import Path


def load_plugins_from_registry(registry_path: Path) -> list[dict]:
    """Load plugins from registry.json."""
    if not registry_path.exists():
        return []
    try:
        with registry_path.open("r", encoding="utf-8") as f:
            registry = json.load(f)
        return registry.get("plugins", [])
    except Exception:
        return []


def load_plugins_from_source(sources_dir: Path) -> list[dict]:
    """Load plugins from sources/plugins.json."""
    plugins_path = sources_dir / "plugins.json"
    if not plugins_path.exists():
        return []
    try:
        with plugins_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("plugins", [])
    except Exception:
        return []


def build_plugins_index(
    plugins: list[dict],
    output_dir: Path,
    *,
    updated_at: str = "",
) -> None:
    """Write plugins.json to output directory."""
    if not plugins:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    plugins_data = {
        "updated_at": updated_at,
        "count": len(plugins),
        "plugins": plugins,
    }
    with (output_dir / "plugins.json").open("w", encoding="utf-8") as f:
        json.dump(plugins_data, f, ensure_ascii=False, indent=2)
