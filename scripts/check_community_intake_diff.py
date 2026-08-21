#!/usr/bin/env python3
"""
Reject noisy sources/community.json pull requests that reformat or rewrite the
existing catalog instead of appending new entries at the end.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from category_taxonomy import category_slug, get_taxonomy
from utils import classify_license


@dataclass(frozen=True)
class CommunityIntakeInput:
    base_ref: str
    head_ref: str
    path: Path


def _git_show(ref: str, path: Path) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path.as_posix()}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown git show failure"
        raise RuntimeError(f"failed to read {path} at {ref}: {stderr}")
    return result.stdout


def _git_merge_base(base_ref: str, head_ref: str) -> str:
    """Resolve the fork point so entries merged into base after the branch was cut
    are not misread as deletions made by the pull request."""
    result = subprocess.run(
        ["git", "merge-base", base_ref, head_ref],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown git merge-base failure"
        raise RuntimeError(f"failed to resolve merge base of {base_ref} and {head_ref}: {stderr}")
    merge_base = result.stdout.strip()
    if not merge_base:
        raise RuntimeError(f"empty merge base for {base_ref} and {head_ref}")
    return merge_base


def _load_payload(label: str, text: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, [f"{label} community catalog is not valid JSON: {exc}"]

    if not isinstance(payload, dict):
        return None, [f"{label} community catalog must be a JSON object"]

    skills = payload.get("skills")
    if not isinstance(skills, list):
        return None, [f"{label} community catalog is missing a list-valued `skills` field"]

    return payload, []


def _find_last_skill_line(lines: list[str]) -> int | None:
    for index in range(len(lines) - 1, -1, -1):
        stripped = lines[index].strip()
        if stripped.startswith('{"name":'):
            return index
    return None


def _is_allowed_category_canonicalization(base_entry: Any, head_entry: Any) -> bool:
    if not isinstance(base_entry, dict) or not isinstance(head_entry, dict):
        return False
    if base_entry == head_entry:
        return True

    base_without_category = {key: value for key, value in base_entry.items() if key != "category"}
    head_without_category = {key: value for key, value in head_entry.items() if key != "category"}
    if base_without_category != head_without_category:
        return False

    base_category = base_entry.get("category")
    head_category = head_entry.get("category")
    if not isinstance(base_category, str) or not isinstance(head_category, str):
        return False

    taxonomy = get_taxonomy()
    base_slug = category_slug(base_category)
    head_slug = category_slug(head_category)
    return (
        head_category == head_slug
        and taxonomy.category_status(base_slug) != "active"
        and taxonomy.is_publishable(head_slug)
    )


def _is_allowed_distribution_completion(base_entry: Any, head_entry: Any) -> bool:
    """Allow only the deterministic legal-metadata completion used by bundling."""
    if not isinstance(base_entry, dict) or not isinstance(head_entry, dict):
        return False
    if base_entry.get("distribution") not in (None, ""):
        return False
    if head_entry.get("distribution") != "compatible":
        return False
    base_without_distribution = {
        key: value for key, value in base_entry.items() if key != "distribution"
    }
    head_without_distribution = {
        key: value for key, value in head_entry.items() if key != "distribution"
    }
    return (
        base_without_distribution == head_without_distribution
        and classify_license(str(base_entry.get("license") or "")) == "compatible"
    )


def _same_skill_identity(base_entry: Any, head_entry: Any) -> bool:
    if not isinstance(base_entry, dict) or not isinstance(head_entry, dict):
        return False
    return (
        str(base_entry.get("name") or "").strip(),
        str(base_entry.get("repo") or "").strip(),
    ) == (
        str(head_entry.get("name") or "").strip(),
        str(head_entry.get("repo") or "").strip(),
    )


def _changed_skill_fields(base_entry: Any, head_entry: Any) -> set[str]:
    if not isinstance(base_entry, dict) or not isinstance(head_entry, dict):
        return set()
    keys = set(base_entry) | set(head_entry)
    return {key for key in keys if base_entry.get(key) != head_entry.get(key)}


def _is_final_skill_metadata_correction(
    base_text: str,
    head_text: str,
    base_skills: list[Any],
    head_skills: list[Any],
) -> bool:
    if not base_skills or len(head_skills) != len(base_skills):
        return False
    if head_skills[:-1] != base_skills[:-1]:
        return False
    if head_skills[-1] == base_skills[-1]:
        return False
    if not _same_skill_identity(base_skills[-1], head_skills[-1]):
        return False
    if not _changed_skill_fields(base_skills[-1], head_skills[-1]) <= {"path", "source_url"}:
        return False

    base_lines = base_text.splitlines()
    head_lines = head_text.splitlines()
    last_skill_line = _find_last_skill_line(base_lines)
    if last_skill_line is None:
        return True
    return base_lines[:last_skill_line] == head_lines[:last_skill_line]


def _existing_entries_are_preserved_or_canonicalized(
    base_skills: list[Any], head_skills: list[Any]
) -> tuple[bool, bool]:
    changed = False
    for base_entry, head_entry in zip(
        base_skills, head_skills[: len(base_skills)], strict=True
    ):
        if base_entry == head_entry:
            continue
        if not (
            _is_allowed_category_canonicalization(base_entry, head_entry)
            or _is_allowed_distribution_completion(base_entry, head_entry)
        ):
            return False, changed
        changed = True
    return True, changed


def validate_community_intake_text(base_text: str, head_text: str) -> list[str]:
    if base_text == head_text:
        return []

    base_payload, base_errors = _load_payload("base", base_text)
    head_payload, head_errors = _load_payload("head", head_text)
    errors = [*base_errors, *head_errors]
    if errors:
        return errors

    assert base_payload is not None
    assert head_payload is not None

    for key in ("name", "description"):
        if base_payload.get(key) != head_payload.get(key):
            errors.append(f"top-level `{key}` must not change in community intake PRs")

    base_metadata = {
        key: value
        for key, value in base_payload.items()
        if key not in {"name", "description", "skills"}
    }
    head_metadata = {
        key: value
        for key, value in head_payload.items()
        if key not in {"name", "description", "skills"}
    }
    if base_metadata != head_metadata:
        errors.append(
            "top-level metadata fields other than `skills` must not change in community intake PRs"
        )

    base_skills = base_payload["skills"]
    head_skills = head_payload["skills"]

    if len(head_skills) < len(base_skills):
        errors.append("community intake PRs must not remove catalog entries")
        return errors

    if _is_final_skill_metadata_correction(base_text, head_text, base_skills, head_skills):
        return errors

    existing_entries_ok, normalized_existing_entries = (
        _existing_entries_are_preserved_or_canonicalized(base_skills, head_skills)
    )
    completed_distribution = any(
        base_entry != head_entry
        and _is_allowed_distribution_completion(base_entry, head_entry)
        for base_entry, head_entry in zip(
            base_skills, head_skills[: len(base_skills)], strict=True
        )
    )
    if not existing_entries_ok:
        errors.append(
            "community intake PRs must preserve the existing `skills` list and append new entries at the end"
        )
        return errors

    if len(head_skills) == len(base_skills):
        if normalized_existing_entries:
            return errors
        errors.append("community intake PRs must add at least one new `skills` entry")
        return errors

    if normalized_existing_entries and not completed_distribution:
        return errors

    base_lines = base_text.splitlines()
    head_lines = head_text.splitlines()
    last_skill_line = _find_last_skill_line(base_lines)
    if last_skill_line is None:
        return errors

    if base_lines[:last_skill_line] != head_lines[:last_skill_line]:
        errors.append(
            "community intake PRs must not rewrite lines before the final existing catalog entry"
        )
        return errors

    base_last = base_lines[last_skill_line].rstrip()
    head_last = head_lines[last_skill_line].rstrip()
    if head_last.removesuffix(",") != base_last.removesuffix(","):
        errors.append(
            "community intake PRs may only add a trailing comma to the final existing catalog entry"
        )

    return errors


def validate_community_intake_diff(config: CommunityIntakeInput) -> list[str]:
    try:
        merge_base = _git_merge_base(config.base_ref, config.head_ref)
        base_text = _git_show(merge_base, config.path)
        head_text = _git_show(config.head_ref, config.path)
    except RuntimeError as exc:
        return [str(exc)]

    return validate_community_intake_text(base_text, head_text)


def parse_args() -> CommunityIntakeInput:
    parser = argparse.ArgumentParser(
        description="Validate that sources/community.json PRs are minimal append-only intake diffs."
    )
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", default="HEAD")
    parser.add_argument("--path", default="sources/community.json")
    args = parser.parse_args()
    return CommunityIntakeInput(
        base_ref=args.base_ref,
        head_ref=args.head_ref,
        path=Path(args.path),
    )


def main() -> int:
    config = parse_args()
    errors = validate_community_intake_diff(config)
    if errors:
        print("Community intake diff check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Community intake diff check passed ({config.path} satisfies intake constraints)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
