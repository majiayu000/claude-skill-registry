#!/usr/bin/env python3
"""
Build a lightweight registry summary without rewriting the full registry payload.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_registry_totals(registry_path: Path) -> tuple[int, str | None]:
    """Read total_count and updated_at from registry.json."""
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    total_count = payload.get("total_count")
    if not isinstance(total_count, int):
        raise ValueError(f"registry total_count is missing or invalid: {registry_path}")

    updated_at = payload.get("updated_at")
    if updated_at is not None and not isinstance(updated_at, str):
        raise ValueError(f"registry updated_at is invalid: {registry_path}")

    return total_count, updated_at


def load_plugin_count(plugins_path: Path) -> int:
    """Read plugin_count from sources/plugins.json."""
    payload = json.loads(plugins_path.read_text(encoding="utf-8"))
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        raise ValueError(f"plugins list is missing or invalid: {plugins_path}")
    return len(plugins)


def build_registry_summary(registry_path: Path, plugins_path: Path) -> dict:
    """Build the lightweight registry summary document."""
    total_count, registry_updated_at = load_registry_totals(registry_path)
    plugin_count = load_plugin_count(plugins_path)
    return {
        "schema_version": 1,
        "registry_updated_at": registry_updated_at,
        "total_count": total_count,
        "plugin_count": plugin_count,
    }


def write_summary(output_path: Path, summary: dict) -> None:
    """Write summary atomically."""
    temp_path = output_path.with_suffix(".json.tmp")
    temp_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temp_path.replace(output_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build registry_summary.json")
    parser.add_argument("--registry", default="registry.json")
    parser.add_argument("--plugins", default="sources/plugins.json")
    parser.add_argument("--output", default="registry_summary.json")
    args = parser.parse_args()

    summary = build_registry_summary(
        registry_path=Path(args.registry),
        plugins_path=Path(args.plugins),
    )
    write_summary(Path(args.output), summary)
    print(
        f"Written {args.output} "
        f"(total_count={summary['total_count']}, plugin_count={summary['plugin_count']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
