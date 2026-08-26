#!/usr/bin/env python3
"""Strict plugin index loading and atomic writing helpers."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


class PluginIndexError(RuntimeError):
    """A typed plugin source/index read, shape, or write failure."""

    def __init__(self, source: str, kind: str, path: Path, message: str) -> None:
        self.source = source
        self.kind = kind
        self.path = path
        self.detail = message
        super().__init__(f"{source}:{kind}:{path}: {message}")


@dataclass(frozen=True)
class PluginLoadResult:
    """Distinguish a missing optional input from a present (possibly empty) index."""

    source: str
    path: Path
    present: bool
    plugins: list[dict[str, Any]]


def _validate_plugins(payload: Any, *, source: str, path: Path) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        raise PluginIndexError(source, "invalid_shape", path, "top-level JSON must be an object")
    plugins = payload.get("plugins")
    if not isinstance(plugins, list):
        raise PluginIndexError(source, "invalid_shape", path, "plugins must be a list")

    validated: list[dict[str, Any]] = []
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            raise PluginIndexError(
                source,
                "invalid_shape",
                path,
                f"plugins[{index}] must be an object",
            )
        for key in ("name", "repo"):
            value = plugin.get(key)
            if not isinstance(value, str) or not value.strip():
                raise PluginIndexError(
                    source,
                    "invalid_shape",
                    path,
                    f"plugins[{index}].{key} must be a non-empty string",
                )
        homepage = plugin.get("homepage")
        if homepage is not None:
            try:
                parsed_homepage = urlparse(homepage) if isinstance(homepage, str) else None
            except ValueError:
                parsed_homepage = None
            if (
                parsed_homepage is None
                or parsed_homepage.scheme not in {"http", "https"}
                or not parsed_homepage.netloc
            ):
                raise PluginIndexError(
                    source,
                    "invalid_shape",
                    path,
                    f"plugins[{index}].homepage must be an HTTP(S) URL",
                )
        validated.append(plugin)
    return validated


def _load_optional_plugins(path: Path, *, source: str) -> PluginLoadResult:
    if not path.exists():
        return PluginLoadResult(source=source, path=path, present=False, plugins=[])
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PluginIndexError(source, "malformed_json", path, "file is not UTF-8") from exc
    except OSError as exc:
        raise PluginIndexError(source, "read_error", path, str(exc)) from exc
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise PluginIndexError(source, "malformed_json", path, str(exc)) from exc
    return PluginLoadResult(
        source=source,
        path=path,
        present=True,
        plugins=_validate_plugins(payload, source=source, path=path),
    )


def load_plugins_from_registry(registry_path: Path) -> PluginLoadResult:
    """Load optional plugins from registry.json without swallowing malformed input."""
    return _load_optional_plugins(registry_path, source="registry_index")


def load_plugins_from_source(sources_dir: Path) -> PluginLoadResult:
    """Load optional plugins from sources/plugins.json without stale fallback."""
    return _load_optional_plugins(sources_dir / "plugins.json", source="plugin_source")


def load_plugins_with_fallback(sources_dir: Path, registry_path: Path) -> list[dict[str, Any]]:
    """Use registry fallback only when the canonical source file is missing."""
    source = load_plugins_from_source(sources_dir)
    if source.present:
        return source.plugins
    registry = load_plugins_from_registry(registry_path)
    return registry.plugins if registry.present else []


def build_plugins_index(
    plugins: list[dict[str, Any]],
    output_dir: Path,
    *,
    updated_at: str = "",
) -> None:
    """Validate and atomically write plugins.json, including a valid empty index."""
    output_path = output_dir / "plugins.json"
    validated = _validate_plugins(
        {"plugins": plugins},
        source="generated_plugin_index",
        path=output_path,
    )
    payload = {
        "updated_at": updated_at,
        "count": len(validated),
        "plugins": validated,
    }
    try:
        serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    except (TypeError, ValueError) as exc:
        raise PluginIndexError(
            "generated_plugin_index",
            "write_error",
            output_path,
            f"unable to serialize plugin index: {exc}",
        ) from exc

    temp_path: Path | None = None
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=output_dir,
            prefix=".plugins.json.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(output_path)
    except OSError as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise PluginIndexError(
            "generated_plugin_index",
            "write_error",
            output_path,
            str(exc),
        ) from exc
