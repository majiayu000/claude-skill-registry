#!/usr/bin/env python3
# ruff: noqa: E402
"""Backfill verified support files into existing canonical archive directories.

The input is JSONL from audit_skill_assets.py backfill-targets. Downloads are
staged through the production downloader with exact paths and immutable commit
SHAs. Existing archive directories are replaced only after the complete batch
passes the production security scanner.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path, PurePosixPath

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from audit_skill_assets import (
    canonical_source_identity,
    canonical_source_identity_from_metadata,
)
from sync_download import download_skills
from sync_download_support import bundled_file_blobs_match, exact_source_branch
from sync_pipeline_support import (
    has_case_conflicting_paths,
    is_safe_portable_relative_path,
)
from utils import classify_license, normalize_license


def _assert_no_symlink_components(root: Path, destination: Path) -> None:
    root = root.absolute()
    destination = destination.absolute()
    if root.is_symlink():
        raise ValueError(f"archive root cannot be a symbolic link: {root}")
    try:
        relative = destination.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"archive destination escapes archive root: {destination}") from exc
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"archive destination contains a symbolic link: {current}")


def _archive_destination(archive_root: Path, archive_path: object) -> Path:
    if not isinstance(archive_path, str):
        raise ValueError("archive_path must be a string")
    normalized = archive_path.strip().replace("\\", "/").strip("/")
    parts = PurePosixPath(normalized).parts
    if len(parts) != 2 or any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"invalid canonical archive_path: {archive_path!r}")
    destination = (archive_root.absolute() / Path(*parts)).absolute()
    _assert_no_symlink_components(archive_root, destination)
    try:
        destination.resolve().relative_to(archive_root.resolve())
    except ValueError as exc:
        raise ValueError(f"archive_path escapes archive root: {archive_path!r}") from exc
    return destination


def _load_metadata(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"unable to read metadata object {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"metadata must be an object: {path}")
    return payload


def _validate_report_path(report_path: Path, archive_root: Path) -> None:
    if report_path.is_symlink():
        raise ValueError(f"report path cannot be a symbolic link: {report_path}")
    resolved_report = report_path.resolve(strict=False)
    resolved_archive = archive_root.resolve(strict=False)
    try:
        resolved_report.relative_to(resolved_archive)
    except ValueError:
        return
    raise ValueError(f"report path cannot overlap archive root: {report_path}")


def _actual_support_files(skill_dir: Path) -> list[str]:
    actual = []
    archive_paths = []
    for path in skill_dir.rglob("*"):
        relative_path = path.relative_to(skill_dir).as_posix()
        archive_paths.append(relative_path)
        if path.is_symlink():
            raise ValueError(f"archive contains a symbolic link: {relative_path}")
        if path.is_file() and relative_path not in {"SKILL.md", "metadata.json"}:
            actual.append(relative_path)
    if has_case_conflicting_paths(archive_paths):
        raise ValueError(f"archive contains case-conflicting paths: {skill_dir}")
    return sorted(actual)


def _asset_free_archive_snapshot(destination: Path) -> str:
    support_files = _actual_support_files(destination)
    if support_files:
        raise ValueError(
            f"backfill destination already contains support files: {destination}: {support_files}"
        )
    digest = hashlib.sha256()
    for filename in ("SKILL.md", "metadata.json"):
        path = destination / filename
        digest.update(filename.encode("utf-8") + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def _archive_snapshot(directory: Path) -> str:
    """Hash a prepared archive while rejecting links and special files."""
    digest = hashlib.sha256()

    def update_field(value: bytes) -> None:
        digest.update(len(value).to_bytes(8, "big"))
        digest.update(value)

    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"prepared archive contains a symbolic link: {relative}")
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise ValueError(f"prepared archive contains a special file: {relative}")
        digest.update(b"file")
        update_field(relative.encode("utf-8"))
        digest.update(stat.S_IMODE(mode).to_bytes(4, "big"))
        update_field(path.read_bytes())
    return digest.hexdigest()


def _directory_identity(directory: Path) -> tuple[int, int]:
    details = directory.lstat()
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISDIR(details.st_mode):
        raise ValueError(f"archive parent is not a real directory: {directory}")
    return details.st_dev, details.st_ino


def _replace_in_verified_directory(
    directory: Path,
    expected_identity: tuple[int, int],
    source_name: str,
    destination_name: str,
) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(directory, flags)
    try:
        details = os.fstat(descriptor)
        if (details.st_dev, details.st_ino) != expected_identity:
            raise ValueError(f"archive parent changed before swap: {directory}")
        os.replace(
            source_name,
            destination_name,
            src_dir_fd=descriptor,
            dst_dir_fd=descriptor,
        )
    finally:
        os.close(descriptor)


def load_backfill_targets(targets_path: Path, archive_root: Path) -> list[dict]:
    targets = []
    seen_keys = set()
    seen_destinations = set()
    for line_number, raw_line in enumerate(
        targets_path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not raw_line.strip():
            continue
        try:
            target = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid target JSON on line {line_number}: {exc}") from exc
        if not isinstance(target, dict):
            raise ValueError(f"target line {line_number} must be an object")

        repo, source_path, source_error = canonical_source_identity(
            target.get("repo"), target.get("source_path")
        )
        if source_error:
            raise ValueError(f"target line {line_number} has {source_error}")
        target_branch = exact_source_branch(target)
        if not target_branch:
            raise ValueError(f"target line {line_number} lacks an exact source branch")
        stable_key = f"{repo.casefold()}:{source_path}"
        if target.get("stable_key") != stable_key:
            raise ValueError(f"target line {line_number} stable_key does not match source")
        if stable_key in seen_keys:
            raise ValueError(f"duplicate backfill stable_key: {stable_key}")
        seen_keys.add(stable_key)

        destination = _archive_destination(archive_root, target.get("archive_path"))
        if destination in seen_destinations:
            raise ValueError(f"duplicate backfill destination: {destination}")
        seen_destinations.add(destination)
        metadata_path = destination / "metadata.json"
        skill_path = destination / "SKILL.md"
        if not destination.is_dir() or not skill_path.is_file():
            raise ValueError(f"archive target does not exist: {destination}")
        metadata = _load_metadata(metadata_path)
        existing_repo, existing_path, existing_error = canonical_source_identity_from_metadata(
            metadata
        )
        if existing_error or f"{existing_repo.casefold()}:{existing_path}" != stable_key:
            raise ValueError(f"archive metadata identity mismatch: {metadata_path}")
        branch = exact_source_branch(metadata)
        if not branch:
            raise ValueError(f"archive metadata lacks an exact source branch: {metadata_path}")
        if branch != target_branch:
            raise ValueError(
                f"target line {line_number} source branch does not match archive metadata"
            )
        license_name = normalize_license(metadata.get("license", ""))
        distribution = str(metadata.get("distribution") or "").strip()
        if classify_license(license_name) != "compatible" or distribution != "compatible":
            raise ValueError(
                f"archive metadata does not approve asset redistribution: {metadata_path}"
            )
        if target.get("license") != license_name or target.get("distribution") != distribution:
            raise ValueError(
                f"target line {line_number} legal metadata does not match archive metadata"
            )
        archive_snapshot = _asset_free_archive_snapshot(destination)

        existing_name = str(metadata.get("name") or destination.name)
        existing_category = str(metadata.get("category") or destination.parent.name)
        raw_stars = metadata.get("stars", 0)
        if isinstance(raw_stars, bool) or not isinstance(raw_stars, int) or raw_stars < 0:
            raise ValueError(f"archive metadata stars must be an integer: {metadata_path}")
        existing_stars = raw_stars
        expected_target_fields = {
            "name": existing_name,
            "category": existing_category,
            "stars": existing_stars,
        }
        for field, expected_value in expected_target_fields.items():
            if target.get(field) != expected_value:
                raise ValueError(
                    f"target line {line_number} {field} does not match archive metadata"
                )

        skill = {
            **{
                key: value
                for key, value in metadata.items()
                if key not in {"github_path", "branch"}
            },
            "repo": repo,
            "path": source_path,
            "github_branch": target_branch,
            "name": existing_name,
            "category": existing_category,
            "stars": existing_stars,
        }
        targets.append(
            {
                "stable_key": stable_key,
                "archive_path": target["archive_path"],
                "destination": destination,
                "archive_snapshot": archive_snapshot,
                "skill": skill,
            }
        )
    if not targets:
        raise ValueError("backfill target file is empty")
    return targets


def _staged_archives(stage_root: Path) -> dict[str, Path]:
    staged = {}
    for metadata_path in sorted(stage_root.glob("*/*/metadata.json")):
        metadata = _load_metadata(metadata_path)
        repo, source_path, source_error = canonical_source_identity_from_metadata(metadata)
        commit_sha = metadata.get("github_commit_sha")
        if source_error:
            raise ValueError(f"staged metadata has {source_error}: {metadata_path}")
        if not isinstance(commit_sha, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", commit_sha):
            raise ValueError(f"staged metadata lacks immutable commit SHA: {metadata_path}")
        stable_key = f"{repo.casefold()}:{source_path}"
        if stable_key in staged:
            raise ValueError(f"duplicate staged stable_key: {stable_key}")
        staged[stable_key] = metadata_path.parent
    return staged


def validate_staged_archives(targets: list[dict], stage_root: Path) -> dict[str, Path]:
    staged = _staged_archives(stage_root)
    expected = {target["stable_key"] for target in targets}
    if set(staged) != expected:
        missing = sorted(expected - set(staged))
        unexpected = sorted(set(staged) - expected)
        raise ValueError(f"staged identity mismatch: missing={missing}, unexpected={unexpected}")
    targets_by_key = {target["stable_key"]: target for target in targets}
    for stable_key, skill_dir in staged.items():
        metadata_path = skill_dir / "metadata.json"
        metadata = _load_metadata(metadata_path)
        target_branch = exact_source_branch(targets_by_key[stable_key]["skill"])
        if exact_source_branch(metadata) != target_branch:
            raise ValueError(f"staged source branch mismatch: {stable_key}")
        declared = metadata.get("bundled_files")
        if not isinstance(declared, list) or not declared:
            raise ValueError(f"staged backfill contains no bundled files: {stable_key}")
        if any(not is_safe_portable_relative_path(path) for path in declared):
            raise ValueError(f"staged bundled_files is malformed: {metadata_path}")
        if has_case_conflicting_paths(declared):
            raise ValueError(f"staged bundled_files contains case conflicts: {metadata_path}")
        actual = _actual_support_files(skill_dir)
        if sorted(declared) != actual:
            raise ValueError(
                f"staged bundled_files mismatch: {stable_key}; "
                f"declared={sorted(declared)}, actual={actual}"
            )
        if not bundled_file_blobs_match(metadata, skill_dir, declared):
            raise ValueError(f"staged bundled file blob mismatch: {stable_key}")
    return staged


def _cleanup_directories(paths: list[Path]) -> list[str]:
    errors = []
    for path in paths:
        if not path.exists():
            continue
        try:
            shutil.rmtree(path)
        except Exception as exc:  # noqa: BLE001 — all cleanup failures must be reported
            errors.append(f"{path}: {type(exc).__name__}: {exc}")
    return errors


def _rollback_applied_archives(
    applied: list[tuple[Path, Path, tuple[int, int]]],
) -> list[str]:
    errors = []
    for destination, backup, parent_identity in reversed(applied):
        failed_copy = None
        try:
            if destination.exists():
                failed_copy = destination.parent / f".{destination.name}.failed-{uuid.uuid4().hex}"
                _replace_in_verified_directory(
                    destination.parent, parent_identity, destination.name, failed_copy.name
                )
            try:
                _replace_in_verified_directory(
                    destination.parent, parent_identity, backup.name, destination.name
                )
            except Exception:
                if failed_copy is not None and failed_copy.exists() and not destination.exists():
                    _replace_in_verified_directory(
                        destination.parent,
                        parent_identity,
                        failed_copy.name,
                        destination.name,
                    )
                raise
            if failed_copy is not None:
                errors.extend(_cleanup_directories([failed_copy]))
        except Exception as exc:  # noqa: BLE001 — continue restoring the remaining batch
            errors.append(
                f"{destination} (backup retained at {backup}): {type(exc).__name__}: {exc}"
            )
    return errors


def apply_staged_archives(
    targets: list[dict],
    stage_root: Path,
    clamscan_binary: str = "clamscan",
) -> None:
    staged = validate_staged_archives(targets, stage_root)

    prepared = []
    created_candidates = []
    try:
        for target in targets:
            destination = target["destination"]
            stable_key = target["stable_key"]
            _assert_no_symlink_components(destination.parents[1], destination)
            parent_identity = _directory_identity(destination.parent)
            if _asset_free_archive_snapshot(destination) != target["archive_snapshot"]:
                raise ValueError(
                    f"backfill destination changed after target generation: {destination}"
                )
            candidate = Path(
                tempfile.mkdtemp(prefix=f".{destination.name}.backfill-", dir=destination.parent)
            )
            created_candidates.append(candidate)
            if _directory_identity(destination.parent) != parent_identity:
                raise ValueError(f"archive parent changed during preparation: {destination.parent}")
            shutil.copytree(staged[stable_key], candidate, dirs_exist_ok=True)
            metadata_path = candidate / "metadata.json"
            existing_metadata = _load_metadata(destination / "metadata.json")
            staged_metadata = _load_metadata(metadata_path)
            merged_metadata = {
                **existing_metadata,
                **staged_metadata,
                "dir_name": destination.name,
            }
            merged_metadata.pop("github_path", None)
            merged_metadata.pop("branch", None)
            metadata_path.write_text(
                json.dumps(merged_metadata, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            prepared.append((target, destination, candidate, parent_identity))
        scanned_snapshots = _scan_archives_with_clamav(
            {target["stable_key"]: candidate for target, _dest, candidate, _identity in prepared},
            clamscan_binary,
        )
    except Exception as exc:
        cleanup_errors = _cleanup_directories(created_candidates)
        if cleanup_errors:
            raise RuntimeError(
                "backfill preparation failed and cleanup was incomplete: "
                + "; ".join(cleanup_errors)
            ) from exc
        raise

    applied = []
    try:
        for target, destination, candidate, parent_identity in prepared:
            _assert_no_symlink_components(destination.parents[1], destination)
            if _asset_free_archive_snapshot(destination) != target["archive_snapshot"]:
                raise ValueError(f"backfill destination changed before swap: {destination}")
            if _directory_identity(destination.parent) != parent_identity:
                raise ValueError(f"archive parent changed before swap: {destination.parent}")
            if _archive_snapshot(candidate) != scanned_snapshots[target["stable_key"]]:
                raise ValueError(f"prepared backfill changed before swap: {candidate}")
            backup = destination.parent / f".{destination.name}.backup-{uuid.uuid4().hex}"
            _replace_in_verified_directory(
                destination.parent, parent_identity, destination.name, backup.name
            )
            applied.append((destination, backup, parent_identity))
            _replace_in_verified_directory(
                destination.parent, parent_identity, candidate.name, destination.name
            )
            if _archive_snapshot(destination) != scanned_snapshots[target["stable_key"]]:
                raise ValueError(f"installed backfill differs from ClamAV scan: {destination}")
    except Exception as exc:
        rollback_errors = _rollback_applied_archives(applied)
        cleanup_errors = _cleanup_directories(created_candidates)
        errors = rollback_errors + cleanup_errors
        if errors:
            raise RuntimeError(
                "atomic backfill failed and recovery was incomplete: " + "; ".join(errors)
            ) from exc
        raise

    cleanup_errors = _cleanup_directories(
        created_candidates + [backup for _destination, backup, _identity in applied]
    )
    if cleanup_errors:
        raise RuntimeError(
            "backfill applied but cleanup was incomplete: " + "; ".join(cleanup_errors)
        )


def _scan_archives_with_clamav(
    archives: dict[str, Path],
    binary: str = "clamscan",
) -> dict[str, str]:
    """Fail closed unless ClamAV scans the exact final archive bytes clean."""
    before = {key: _archive_snapshot(path) for key, path in archives.items()}
    for stable_key, archive in archives.items():
        try:
            result = subprocess.run(
                [binary, "--recursive", "--infected", str(archive)],
                capture_output=True,
                text=True,
                check=False,
                timeout=600,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError(f"unable to execute ClamAV: {exc}") from exc
        if result.returncode != 0:
            details = (result.stdout + "\n" + result.stderr).strip()[-1000:]
            raise RuntimeError(
                f"ClamAV rejected {stable_key} with exit code {result.returncode}: {details}"
            )
    after = {key: _archive_snapshot(path) for key, path in archives.items()}
    if after != before:
        raise RuntimeError("final candidate archives changed during ClamAV scan")
    return after


def scan_staged_archives_with_clamav(
    stage_root: Path,
    binary: str = "clamscan",
) -> dict[str, str]:
    """Compatibility wrapper for validating a downloaded staging tree."""
    if not stage_root.is_dir():
        raise ValueError(f"staged archive root does not exist: {stage_root}")
    staged = _staged_archives(stage_root) or {".": stage_root}
    return _scan_archives_with_clamav(staged, binary)


async def run_backfill(
    targets_path: Path,
    archive_root: Path,
    report_path: Path,
    *,
    apply: bool,
    github_token: str = "",
    clamscan_binary: str = "clamscan",
) -> int:
    _validate_report_path(report_path, archive_root)
    targets = []
    stats = {}
    failure_details = {}
    status = "failed"
    error = ""
    try:
        targets = load_backfill_targets(targets_path, archive_root)
        with tempfile.TemporaryDirectory(prefix="skill-asset-backfill-") as temp_dir:
            temp_root = Path(temp_dir)
            registry_path = temp_root / "registry.json"
            stage_root = temp_root / "skills"
            failure_report = temp_root / "failure-report.json"
            registry_path.write_text(
                json.dumps({"skills": [target["skill"] for target in targets]}),
                encoding="utf-8",
            )
            stats = await download_skills(
                registry_path,
                stage_root,
                github_token,
                manifest_path=None,
                failure_report_path=failure_report,
                learning_priors_path=temp_root / "learning-priors.json",
                cleanup_ci_untracked=False,
                exact_paths_only=True,
                pin_commit_sha=True,
            )
            if failure_report.exists():
                failure_details = json.loads(failure_report.read_text(encoding="utf-8"))
            success = stats.get("downloaded") == len(targets) and stats.get("failed") == 0
            if success:
                validate_staged_archives(targets, stage_root)
                status = "validated"
                if apply:
                    apply_staged_archives(targets, stage_root, clamscan_binary)
                    status = "applied"
    except Exception as exc:  # noqa: BLE001 — emit a structured report for every failure
        status = "failed"
        error = f"{type(exc).__name__}: {exc}"
        print(error, file=sys.stderr)

    report = {
        "schema_version": 1,
        "status": status,
        "apply": apply,
        "target_count": len(targets),
        "stats": stats,
        "failure_report": failure_details,
        **({"error": error} if error else {}),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0 if status in {"validated", "applied"} else 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("targets", type=Path)
    parser.add_argument("archive_root", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--clamscan-binary", default="clamscan")
    args = parser.parse_args()
    raise SystemExit(
        asyncio.run(
            run_backfill(
                args.targets,
                args.archive_root,
                args.report,
                apply=args.apply,
                github_token=os.environ.get("GITHUB_TOKEN", ""),
                clamscan_binary=args.clamscan_binary,
            )
        )
    )


if __name__ == "__main__":
    main()
