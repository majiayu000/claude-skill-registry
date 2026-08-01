"""Record-level validation helpers for static artifact API gates."""

from __future__ import annotations


def is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def search_key_errors(
    records: object,
    seen: set[tuple[str, str]],
) -> list[str]:
    if not isinstance(records, list):
        return []
    errors: list[str] = []
    current: set[tuple[str, str]] = set()
    for record in records:
        if not isinstance(record, dict):
            errors.append("invalid_search_stable_key")
            continue
        install = record.get("i")
        branch = record.get("b")
        if not isinstance(install, str) or not install or not isinstance(branch, str) or not branch:
            errors.append("invalid_search_stable_key")
            continue
        key = (install, branch)
        if key in seen or key in current:
            errors.append("duplicate_search_stable_key")
        current.add(key)
    seen.update(current)
    return errors
