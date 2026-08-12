#!/usr/bin/env python3
"""Census of bundled-asset references across the archived skill corpus.

Usage:
  python scripts/audit_skill_assets.py census <data_repo_root>
  python scripts/audit_skill_assets.py targets <data_repo_root> [min_stars]
  python scripts/audit_skill_assets.py current-state <data_repo_root> [min_stars]
  python scripts/audit_skill_assets.py backfill-targets <data_repo_root> [min_stars]

`census` prints bucket statistics (EXEC / REF / BARE) as JSON.
`targets` prints JSONL of deduped EXEC candidates at or above min_stars
(default 100) for upstream verification by verify_upstream_assets.py.
`current-state` reports what is actually archived and how it compares with
metadata. `backfill-targets` emits only deterministic, exact-path candidates
that claim support files but currently archive none.
"""

from __future__ import annotations

import collections
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archive_preflight import iter_canonical_archive_paths as _iter_canonical_archive_paths
from asset_claims import requires_complete_bundled_archive
from portable_paths import is_safe_portable_relative_path
from skill_asset_audit import (
    classify_files,
    classify_skill_text,
    verdict_from_counts,
)
from sync_pipeline_support import (
    has_case_conflicting_paths,
    is_valid_git_source_ref,
)
from utils import build_skill_key, classify_license, normalize_license

REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _read_skill(dirpath: str) -> str:
    with open(os.path.join(dirpath, "SKILL.md"), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def run_census(root: str) -> dict:
    buckets: collections.Counter = collections.Counter()
    sizes: dict[str, list[int]] = collections.defaultdict(list)
    for dirpath, _meta in _canonical_archive_rows(root):
        text = _read_skill(dirpath)
        bucket = classify_skill_text(text)
        buckets[bucket] += 1
        sizes[bucket].append(len(text))
    total = sum(buckets.values())
    if not total:
        raise SystemExit(f"no SKILL.md found under {root}")

    def median(values: list[int]) -> int:
        values = sorted(values)
        return values[len(values) // 2] if values else 0

    return {
        "total_skills": total,
        "buckets": dict(buckets),
        "bucket_pct": {k: round(v * 100 / total, 1) for k, v in buckets.items()},
        "median_skill_md_bytes": {k: median(v) for k, v in sizes.items()},
    }


def run_targets(root: str, min_stars: int) -> None:
    seen: set[tuple[str, str]] = set()
    for dirpath, meta in _canonical_archive_rows(root):
        if not meta:
            continue
        stars = meta.get("stars") or 0
        repo = meta.get("repo") or ""
        if stars < min_stars or not repo:
            continue
        if classify_skill_text(_read_skill(dirpath)) != "EXEC":
            continue
        skill_dir = os.path.dirname(meta.get("path") or "")
        key = (repo, skill_dir)
        if key in seen:
            continue
        seen.add(key)
        print(
            json.dumps(
                {
                    "repo": repo,
                    "dir": skill_dir,
                    "stars": stars,
                    "name": meta.get("name", ""),
                }
            )
        )

def _assert_unique_canonical_archive_paths(paths: list[str], root: str | Path) -> None:
    if has_case_conflicting_paths(paths):
        raise ValueError(f"archive contains case-conflicting skill roots: {root}")


def _canonical_archive_rows(root: str | Path):
    """Stream canonical rows from the single fail-closed archive preflight."""
    archive_root = Path(root).resolve()
    paths = list(_iter_canonical_archive_paths(root))
    _assert_unique_canonical_archive_paths(paths, root)
    for relative in paths:
        dirpath = archive_root / relative
        metadata_path = dirpath / "metadata.json"
        metadata = None
        if metadata_path.is_symlink() or (
            metadata_path.exists() and not metadata_path.is_file()
        ):
            raise ValueError(
                f"canonical metadata.json must be a regular file: {relative}"
            )
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ValueError(f"invalid metadata object: {metadata_path}: {exc}") from exc
        yield str(dirpath), metadata


def canonical_source_identity(
    repo_value: object,
    path_value: object,
) -> tuple[str, str, str]:
    repo = repo_value.strip() if isinstance(repo_value, str) else ""
    if not REPO_PATTERN.fullmatch(repo):
        return repo, "", "invalid_repo"
    if any(component in {".", ".."} for component in repo.split("/")):
        return repo, "", "invalid_repo"
    if not isinstance(path_value, str) or not path_value.strip():
        return repo, "", "missing_source_path"

    source_path = path_value.strip().replace("\\", "/")
    if source_path.startswith("/") or re.match(r"^[A-Za-z]:", source_path):
        return repo, source_path, "absolute_source_path"
    if not is_safe_portable_relative_path(source_path):
        return repo, source_path, "invalid_source_path"
    parts = source_path.split("/")
    if parts[-1].casefold() != "skill.md":
        return repo, source_path, "source_path_not_skill_md"
    return repo, "/".join(parts), ""


def canonical_source_identity_from_metadata(metadata: dict) -> tuple[str, str, str]:
    """Return one exact source identity, rejecting conflicting path aliases."""
    aliases = []
    for field in ("path", "github_path"):
        if field not in metadata:
            continue
        path_value = _metadata_source_path(field, metadata[field])
        repo, source_path, error = canonical_source_identity(metadata.get("repo"), path_value)
        if error:
            return repo, source_path, error
        aliases.append((repo, source_path))
    if not aliases:
        return canonical_source_identity(metadata.get("repo"), None)
    if any(identity != aliases[0] for identity in aliases[1:]):
        return aliases[0][0], aliases[0][1], "conflicting_source_path_aliases"
    return aliases[0][0], aliases[0][1], ""


def _metadata_source_path(field: str, value: object) -> object:
    """Expand repository-written directory aliases into exact SKILL.md paths."""
    if field not in {"path", "github_path"} or not isinstance(value, str):
        return value
    source_path = value.strip()
    if not source_path:
        return "SKILL.md" if field == "github_path" else value
    normalized = source_path.replace("\\", "/")
    if normalized.rsplit("/", 1)[-1].casefold() == "skill.md":
        return source_path
    if normalized.rsplit("/", 1)[-1].casefold() in {"metadata.json", "readme.md"}:
        return source_path
    return f"{source_path}/SKILL.md"


def canonical_source_branch_from_metadata(metadata: dict) -> tuple[str, str]:
    """Return one exact source branch, rejecting missing or conflicting aliases."""
    branches = []
    for field in ("github_branch", "branch"):
        if field not in metadata:
            continue
        raw_branch = metadata[field]
        if not isinstance(raw_branch, str):
            return "", "invalid_source_branch"
        branch = raw_branch.strip()
        if not is_valid_git_source_ref(branch):
            return "", "invalid_source_branch"
        branches.append(branch)
    if not branches:
        return "", "missing_source_branch"
    if any(branch != branches[0] for branch in branches[1:]):
        return "", "conflicting_source_branch_aliases"
    return branches[0], ""


# Preserve the private helper used by existing callers while the strict public
# parser is shared by later pipeline phases.
_canonical_source = canonical_source_identity


def _source_dir(source_path: str) -> str:
    parent = PurePosixPath(source_path).parent.as_posix()
    return "" if parent == "." else parent


def _identity_keys(metadata: dict, *, name: str, category: str) -> set[str]:
    """Return every plausible key so malformed aliases still make duplicates ambiguous."""
    repo_value = metadata.get("repo")
    repo = repo_value.strip() if isinstance(repo_value, str) else ""
    values = [
        (field, _metadata_source_path(field, metadata[field]))
        for field in ("path", "github_path")
        if field in metadata
    ]
    if not values:
        values = [("path", None)]

    keys = set()
    for _field, value in values:
        exact_repo, source_path, error = canonical_source_identity(repo_value, value)
        if not error:
            keys.add(f"{exact_repo.casefold()}:{source_path}")
            continue
        fallback = build_skill_key(
            repo.casefold(),
            str(value or ""),
            name=name,
            category=category,
        )
        if fallback:
            keys.add(fallback)
    return keys


def _actual_bundled_files(dirpath: str) -> list[str]:
    root = Path(dirpath)
    files = []
    archive_paths = []

    def raise_walk_error(error: OSError) -> None:
        raise ValueError(f"unable to inspect archive skill {dirpath}: {error}") from error

    for current_dir, dirnames, filenames in os.walk(root, onerror=raise_walk_error):
        for name in [*dirnames, *filenames]:
            path = Path(current_dir, name)
            relative = path.relative_to(root).as_posix()
            archive_paths.append(relative)
            try:
                mode = path.lstat().st_mode
            except OSError as exc:
                raise ValueError(
                    f"unable to inspect archive support path {relative}: {exc}"
                ) from exc
            if stat.S_ISLNK(mode):
                raise ValueError(f"symbolic link is not allowed in archive skill: {relative}")
            if not is_safe_portable_relative_path(relative):
                raise ValueError(f"non-portable path is not allowed in archive skill: {relative}")
            if not stat.S_ISREG(mode) or relative in {"SKILL.md", "metadata.json"}:
                continue
            files.append(relative)
    if has_case_conflicting_paths(archive_paths):
        raise ValueError(f"case-conflicting paths are not allowed in archive skill: {dirpath}")
    return sorted(files)


def _local_verdict(paths: list[str]) -> str:
    counts = classify_files(paths)
    counts["doc"] += sum(1 for path in paths if path.lower().endswith("/skill.md"))
    counts["asset"] += sum(1 for path in paths if path.endswith("/metadata.json"))
    return verdict_from_counts(counts)


def _parse_stars(value: object, metadata_path: Path) -> int:
    if value is None:
        return 0
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"invalid stars in {metadata_path}: {value!r}")
    return value


def _declared_bundled_files(metadata: dict) -> tuple[list[str], bool]:
    if "bundled_files" not in metadata:
        return [], True
    declared = metadata["bundled_files"]
    if not isinstance(declared, list):
        return [], False
    normalized = []
    for value in declared:
        if not is_safe_portable_relative_path(value):
            return [], False
        path = PurePosixPath(value)
        if path.is_absolute():
            return [], False
        normalized_path = path.as_posix()
        if (
            normalized_path.casefold() in {"skill.md", "metadata.json"}
            or normalized_path in normalized
        ):
            return [], False
        normalized.append(normalized_path)
    if has_case_conflicting_paths(normalized):
        return [], False
    return sorted(normalized), True


def _scan_inventory(root: str, min_stars: int) -> tuple[dict, list[dict]]:
    archive_root = Path(root).resolve()
    claim_counts: collections.Counter = collections.Counter()
    local_verdict_counts: collections.Counter = collections.Counter()
    asset_state_counts: collections.Counter = collections.Counter()
    archive_mode_counts: collections.Counter = collections.Counter()
    key_counts: collections.Counter = collections.Counter()
    candidates = []
    total_skills = 0
    actual_bundled_file_count = 0
    metadata_mismatch_count = 0
    source_identity_errors = []
    metadata_errors = []

    for dirpath, raw_meta in _canonical_archive_rows(root):
        skill_dir = Path(dirpath).resolve()
        metadata_path = skill_dir / "metadata.json"
        if metadata_path.exists() and not isinstance(raw_meta, dict):
            raise ValueError(f"invalid metadata object: {metadata_path}")
        metadata = raw_meta if isinstance(raw_meta, dict) else {}
        relative_dir = skill_dir.relative_to(archive_root).as_posix()
        path_parts = PurePosixPath(relative_dir).parts
        category = str(metadata.get("category") or (path_parts[0] if path_parts else "other"))
        name = str(metadata.get("name") or (path_parts[-1] if path_parts else skill_dir.name))
        repo, source_path, source_error = canonical_source_identity_from_metadata(metadata)
        source_branch, branch_error = canonical_source_branch_from_metadata(metadata)
        identity_keys = _identity_keys(metadata, name=name, category=category)
        stable_key = f"{repo.casefold()}:{source_path}" if not source_error else ""
        for identity_key in identity_keys:
            key_counts[identity_key] += 1

        actual_files = _actual_bundled_files(dirpath)
        declared_files, declared_files_valid = _declared_bundled_files(metadata)
        actual_archive_mode = "directory" if actual_files else "skill-md"
        declared_archive_mode = str(metadata.get("archive_mode") or "")
        skill_text = _read_skill(dirpath)
        claim = classify_skill_text(skill_text)
        pipeline_claim = requires_complete_bundled_archive(skill_text)
        local_verdict = _local_verdict(actual_files)
        if actual_files:
            asset_state = "archived"
        elif (
            claim != "BARE"
            or pipeline_claim
            or (declared_files_valid and bool(declared_files))
        ):
            asset_state = "missing_claimed_assets"
        else:
            asset_state = "no_assets_claimed"

        total_skills += 1
        actual_bundled_file_count += len(actual_files)
        claim_counts[claim] += 1
        local_verdict_counts[local_verdict] += 1
        asset_state_counts[asset_state] += 1
        archive_mode_counts[actual_archive_mode] += 1
        if (
            declared_archive_mode != actual_archive_mode
            or not declared_files_valid
            or declared_files != actual_files
        ):
            metadata_mismatch_count += 1

        stars = _parse_stars(metadata.get("stars"), metadata_path)
        provenance_error = source_error or branch_error
        license_name = normalize_license(metadata.get("license", ""))
        distribution = str(metadata.get("distribution") or "").strip()
        distribution_error = (
            "asset_redistribution_not_approved"
            if classify_license(license_name) != "compatible" or distribution != "compatible"
            else ""
        )
        if (
            asset_state == "missing_claimed_assets"
            and stars >= min_stars
            and not declared_files_valid
        ):
            metadata_errors.append(
                {
                    "archive_path": relative_dir,
                    "error": "invalid_bundled_files",
                    "eligible_for_backfill": True,
                }
            )
        if provenance_error:
            source_identity_errors.append(
                {
                    "archive_path": relative_dir,
                    "error": provenance_error,
                    "eligible_for_backfill": (
                        asset_state == "missing_claimed_assets" and stars >= min_stars
                    ),
                }
            )
        if (
            asset_state == "missing_claimed_assets"
            and stars >= min_stars
            and not provenance_error
            and declared_files_valid
            and distribution_error
        ):
            metadata_errors.append(
                {
                    "archive_path": relative_dir,
                    "error": distribution_error,
                    "eligible_for_backfill": True,
                }
            )
        if (
            asset_state == "missing_claimed_assets"
            and stars >= min_stars
            and not provenance_error
            and declared_files_valid
            and not distribution_error
        ):
            candidates.append(
                {
                    "stable_key": stable_key,
                    "archive_path": relative_dir,
                    "repo": repo,
                    "source_path": source_path,
                    "github_branch": source_branch,
                    "dir": _source_dir(source_path),
                    "name": name,
                    "category": category,
                    "stars": stars,
                    "claim": claim,
                    "license": license_name,
                    "distribution": distribution,
                }
            )

    if not total_skills:
        raise SystemExit(f"no SKILL.md found under {root}")

    ambiguous_keys = {key for key, count in key_counts.items() if count > 1}
    targets = sorted(
        (row for row in candidates if row["stable_key"] not in ambiguous_keys),
        key=lambda row: (row["stable_key"], row["archive_path"]),
    )
    report = {
        "schema_version": 1,
        "total_skills": total_skills,
        "claim_counts": dict(claim_counts),
        "local_verdict_counts": dict(local_verdict_counts),
        "asset_state_counts": dict(asset_state_counts),
        "archive_mode_counts": dict(archive_mode_counts),
        "actual_bundled_file_count": actual_bundled_file_count,
        "metadata_mismatch_count": metadata_mismatch_count,
        "source_identity_error_count": len(source_identity_errors),
        "source_identity_errors": sorted(
            source_identity_errors,
            key=lambda row: (row["archive_path"], row["error"]),
        ),
        "metadata_error_count": len(metadata_errors),
        "metadata_errors": sorted(
            metadata_errors,
            key=lambda row: (row["archive_path"], row["error"]),
        ),
        "ambiguous_stable_key_count": len(ambiguous_keys),
        "backfill_candidate_count": len(targets),
    }
    return report, targets


def build_backfill_targets(root: str, min_stars: int = 100) -> list[dict]:
    report, targets = _scan_inventory(root, min_stars)
    blocking_errors = [
        row for row in report["source_identity_errors"] if row["eligible_for_backfill"]
    ]
    if blocking_errors:
        details = ", ".join(f"{row['archive_path']} ({row['error']})" for row in blocking_errors)
        raise ValueError(f"invalid source identity for backfill candidates: {details}")
    blocking_metadata = [row for row in report["metadata_errors"] if row["eligible_for_backfill"]]
    if blocking_metadata:
        details = ", ".join(f"{row['archive_path']} ({row['error']})" for row in blocking_metadata)
        raise ValueError(f"invalid metadata for backfill candidates: {details}")
    return targets


def run_current_state(root: str, min_stars: int = 100) -> dict:
    report, _targets = _scan_inventory(root, min_stars)
    return report


def main() -> None:
    modes = {"census", "targets", "current-state", "backfill-targets"}
    if len(sys.argv) < 3 or sys.argv[1] not in modes:
        raise SystemExit(__doc__)
    mode, root = sys.argv[1], sys.argv[2]
    min_stars = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    if mode == "census":
        print(json.dumps(run_census(root), indent=2))
    elif mode == "targets":
        run_targets(root, min_stars)
    elif mode == "current-state":
        sys.stdout.write(json.dumps(run_current_state(root, min_stars), indent=2) + "\n")
    else:
        for target in build_backfill_targets(root, min_stars):
            sys.stdout.write(json.dumps(target) + "\n")


if __name__ == "__main__":
    main()
