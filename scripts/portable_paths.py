"""Side-effect-free validation for archive-relative portable paths."""

from __future__ import annotations

import re
from pathlib import PurePosixPath

_WINDOWS_INVALID_CHARACTERS = frozenset('<>:"\\|?*')
_WINDOWS_RESERVED_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
    | {f"COM{index}" for index in range(1, 10)}
    | {f"LPT{index}" for index in range(1, 10)}
    | {f"{prefix}{index}" for prefix in ("COM", "LPT") for index in "¹²³"}
)


def _is_windows_portable_component(component: str) -> bool:
    if component[-1] in {" ", "."}:
        return False
    if any(ord(character) < 32 for character in component):
        return False
    if any(character in _WINDOWS_INVALID_CHARACTERS for character in component):
        return False
    stem = component.split(".", 1)[0].upper()
    return stem not in _WINDOWS_RESERVED_NAMES


def is_safe_portable_relative_path(value: object) -> bool:
    """Return whether value is a strict relative path portable across platforms."""
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    if "\\" in value or re.match(r"^[A-Za-z]:", value):
        return False
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    if PurePosixPath(value).is_absolute():
        return False
    return all(_is_windows_portable_component(part) for part in parts)
