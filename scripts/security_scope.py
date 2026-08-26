"""Resolve security scan targets without losing unusual Git paths."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

from utils import is_declared_bundled_skill_file


class SecurityScopeError(RuntimeError):
    """A changed archive path cannot be mapped to a safe scan target."""


def _lexical_absolute(path: Path) -> Path:
    return Path(os.path.abspath(path))


def _reject_symlink_components(candidate: Path, root: Path) -> None:
    relative = candidate.relative_to(root)
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise SecurityScopeError(f"security scope contains a symlink: {relative.as_posix()}")


def _owning_skill_file(candidate: Path, root: Path) -> Path | None:
    current = candidate if candidate.is_dir() else candidate.parent
    while True:
        skill_file = current / "SKILL.md"
        if skill_file.is_file() and not skill_file.is_symlink():
            if not is_declared_bundled_skill_file(skill_file.resolve(), root.resolve()):
                return skill_file
        if current == root:
            return None
        current = current.parent


def resolve_scan_paths(
    skills_dir: Path,
    paths: Iterable[str],
    *,
    fail_unmapped: bool = False,
) -> list[Path]:
    """Map archive paths to unique owning SKILL.md files using lexical containment."""
    root = _lexical_absolute(skills_dir)
    selected: list[Path] = []
    seen: set[str] = set()

    for raw in paths:
        line = raw
        if not line:
            continue
        input_path = Path(line)
        candidate = _lexical_absolute(input_path if input_path.is_absolute() else root / input_path)
        try:
            candidate.relative_to(root)
            _reject_symlink_components(candidate, root)
        except ValueError as exc:
            raise SecurityScopeError(f"security scope escapes scan root: {line}") from exc

        if not candidate.exists():
            if fail_unmapped:
                raise SecurityScopeError(f"changed security path does not exist: {line}")
            continue

        skill_file = _owning_skill_file(candidate, root)
        if skill_file is None:
            if fail_unmapped:
                raise SecurityScopeError(f"changed security path has no owning SKILL.md: {line}")
            continue

        key = str(skill_file)
        if key not in seen:
            seen.add(key)
            selected.append(skill_file)
    return selected


def resolve_scan_file_list(
    skills_dir: Path,
    file_list_path: Path,
    *,
    fail_unmapped: bool = False,
) -> list[Path]:
    """Read a newline- or NUL-delimited file list and resolve its scan targets."""
    if not file_list_path.exists():
        if fail_unmapped:
            raise SecurityScopeError(f"security file list is missing: {file_list_path}")
        return []
    raw = file_list_path.read_bytes()
    chunks = raw.split(b"\0") if b"\0" in raw else raw.splitlines()
    try:
        paths = [chunk.decode("utf-8") for chunk in chunks if chunk]
    except UnicodeDecodeError as exc:
        raise SecurityScopeError("security file list contains a non-UTF-8 path") from exc
    return resolve_scan_paths(skills_dir, paths, fail_unmapped=fail_unmapped)


def discover_scan_targets(skills_dir: Path) -> list[Path]:
    """Return every top-level archived skill target, rejecting symlinked targets."""
    root = _lexical_absolute(skills_dir)
    targets: list[Path] = []
    for skill_file in root.rglob("SKILL.md"):
        _reject_symlink_components(skill_file, root)
        if not is_declared_bundled_skill_file(skill_file.resolve(), root.resolve()):
            targets.append(skill_file)
    return sorted(targets)
