#!/usr/bin/env python3
"""Keep only metadata for archives whose license is not an open-source license.

An archive keeps its SKILL.md body when its metadata license is in
``utils.OPEN_SOURCE_LICENSES`` (OSI-approved, including copyleft, or an open
content license such as CC-BY/CC-BY-SA). Every other archive (no license,
NOASSERTION, proprietary, non-commercial or no-derivatives) is "withheld": the
directory keeps ``metadata.json`` with its source link and no upstream content.

Dry-run is the default; ``--apply`` removes bodies and ``--check`` fails when any
withheld archive still carries files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

from utils import extract_description, is_open_source_license, split_frontmatter_content

METADATA_FILENAME = "metadata.json"


def body_fingerprint(content: str) -> str:
    """Hash the Markdown body after line-ending normalization; empty bodies have none."""
    _frontmatter, body = split_frontmatter_content(content)
    normalized_body = body.replace("\r\n", "\n").strip()
    return hashlib.sha256(normalized_body.encode("utf-8")).hexdigest() if normalized_body else ""


def read_metadata(skill_dir: Path) -> dict:
    """Read metadata strictly: an unreadable file must never be treated as restricted."""
    path = skill_dir / METADATA_FILENAME
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: metadata must be a JSON object")
    return payload


def iter_archive_dirs(skills_dir: Path):
    """Yield canonical <category>/<skill> directories that contain metadata.json."""
    for category_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        if category_dir.name.startswith("."):
            continue
        for skill_dir in sorted(p for p in category_dir.iterdir() if p.is_dir()):
            if (skill_dir / METADATA_FILENAME).is_file():
                yield skill_dir


def body_allowed(metadata: dict) -> bool:
    """Return whether the archive may keep the skill body under its recorded license."""
    return is_open_source_license(metadata.get("license"))


def is_withheld_metadata(metadata: dict) -> bool:
    """A withheld archive links to an upstream repo but has no open-source license.

    Metadata without a repo has no source link to list; once its body is removed it
    is orphan metadata and is not indexed.
    """
    return bool(str(metadata.get("repo") or "").strip()) and not body_allowed(metadata)


def iter_withheld_metadata_only_dirs(skills_dir: Path):
    """Yield (skill_dir, metadata) for withheld archives that carry no SKILL.md."""
    for skill_dir in iter_archive_dirs(skills_dir):
        if (skill_dir / "SKILL.md").exists():
            continue
        metadata = read_metadata(skill_dir)
        if is_withheld_metadata(metadata):
            yield skill_dir, metadata


def withheld_metadata(metadata: dict, skill_text: str | None) -> dict:
    """Keep the identity facts a withheld archive still needs for indexing."""
    updated = dict(metadata)
    if skill_text is not None:
        fingerprint = body_fingerprint(skill_text)
        if fingerprint:
            updated["content_fingerprint"] = fingerprint
        if not str(updated.get("description") or "").strip():
            description = extract_description(skill_text)
            if description:
                updated["description"] = description
    # Bundled-file evidence must not describe files that are no longer archived.
    if "bundled_files" in updated:
        updated["bundled_files"] = []
    for key in ("bundled_file_blobs", "license_source_paths"):
        updated.pop(key, None)
    if updated.get("archive_mode") == "directory":
        updated["archive_mode"] = "skill-md"
    return updated


def withhold_archive(skill_dir: Path, metadata: dict) -> None:
    """Remove everything except metadata.json from one withheld archive."""
    skill_md = skill_dir / "SKILL.md"
    skill_text = skill_md.read_text(encoding="utf-8") if skill_md.is_file() else None
    updated = withheld_metadata(metadata, skill_text)
    for child in skill_dir.iterdir():
        if child.name == METADATA_FILENAME:
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    if updated != metadata:
        (skill_dir / METADATA_FILENAME).write_text(
            json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )


def plan_withholding(skills_dir: Path) -> dict:
    """Return counts and the withheld archives that still carry content."""
    archives = 0
    body_kept = 0
    withheld_clean = 0
    pending: list[tuple[Path, dict]] = []
    for skill_dir in iter_archive_dirs(skills_dir):
        archives += 1
        metadata = read_metadata(skill_dir)
        if body_allowed(metadata):
            body_kept += 1
            continue
        if any(child.name != METADATA_FILENAME for child in skill_dir.iterdir()):
            pending.append((skill_dir, metadata))
        else:
            withheld_clean += 1
    return {
        "archives": archives,
        "body_kept": body_kept,
        "withheld_metadata_only": withheld_clean,
        "pending": pending,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="remove withheld bodies")
    mode.add_argument("--check", action="store_true", help="fail if any body remains")
    parser.add_argument("--report", type=Path, help="write a JSON summary here")
    args = parser.parse_args(argv)

    plan = plan_withholding(args.skills_dir)
    pending = plan.pop("pending")
    if args.apply:
        for skill_dir, metadata in pending:
            withhold_archive(skill_dir, metadata)
    summary = {
        **plan,
        "withheld_with_content": len(pending),
        "applied": bool(args.apply),
        "examples": [p.relative_to(args.skills_dir).as_posix() for p, _ in pending[:20]],
    }
    if args.report:
        args.report.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if args.check and pending:
        print(
            f"error: {len(pending)} archives without an open-source license still carry content",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
