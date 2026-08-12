#!/usr/bin/env python3
"""Verify canonical bundled assets and preserve the legacy JSONL verifier."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from archive_preflight import iter_canonical_archive_paths
from audit_skill_assets import canonical_source_identity_from_metadata
from skill_asset_audit import classify_files, fetch_repo_tree, verdict_from_counts
from sync_download_support import bundled_file_blobs_match, exact_source_branch
from sync_pipeline_support import (
    has_case_conflicting_paths,
    is_safe_portable_relative_path,
)

SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
LIVENESS_STATUSES = {"live", "partial", "moved", "gone"}
ERROR_STATUSES = {"verification_error", "local_error", "apply_error"}
VERIFICATION_EVIDENCE_FIELDS = {
    "github_commit_sha",
    "assets_verified_at",
    "bundled_file_blobs",
    "asset_liveness",
    "assets_liveness_checked_at",
    "assets_liveness_sha",
}


class GitHubApiError(RuntimeError):
    """A GitHub response that can be classified without hiding its status."""

    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


class GitHubClient:
    def __init__(self, token: str = ""):
        self.token = token

    def get_json(self, path: str) -> dict:
        request = urllib.request.Request(
            f"https://api.github.com{path}",
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "claude-skill-registry-asset-verifier",
                "X-GitHub-Api-Version": "2022-11-28",
                **({"Authorization": f"Bearer {self.token}"} if self.token else {}),
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
                payload = json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
            raise GitHubApiError(exc.code, f"GitHub API {exc.code}: {detail}") from exc
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise GitHubApiError(0, f"GitHub API transport failure: {exc}") from exc
        if not isinstance(payload, dict):
            raise GitHubApiError(0, "GitHub API returned a non-object response")
        return payload

    def repository(self, repo: str) -> dict:
        return self.get_json(f"/repos/{repo}")

    def branch_sha(self, repo: str, branch: str) -> str:
        encoded = urllib.parse.quote(branch, safe="")
        payload = self.get_json(f"/repos/{repo}/branches/{encoded}")
        if payload.get("name") != branch:
            raise GitHubApiError(0, "GitHub branch response identity mismatch")
        commit = payload.get("commit")
        sha = commit.get("sha") if isinstance(commit, dict) else None
        if not isinstance(sha, str) or not SHA_PATTERN.fullmatch(sha):
            raise GitHubApiError(0, "GitHub commit response lacks a valid SHA")
        return sha.lower()

    def tree(self, repo: str, sha: str) -> set[str]:
        payload = self.get_json(f"/repos/{repo}/git/trees/{sha}?recursive=1")
        if payload.get("truncated") is not False:
            raise GitHubApiError(0, "GitHub tree response is truncated or malformed")
        entries = payload.get("tree")
        if not isinstance(entries, list):
            raise GitHubApiError(0, "GitHub tree response lacks entries")
        paths = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise GitHubApiError(0, "GitHub tree contains a malformed entry")
            path = entry.get("path")
            entry_type = entry.get("type")
            mode = entry.get("mode")
            if not all(isinstance(value, str) for value in (path, entry_type, mode)):
                raise GitHubApiError(0, "GitHub tree entry lacks path, type, or mode")
            if entry_type == "blob" and mode in {"100644", "100755"}:
                paths.add(path)
            elif entry_type == "blob" and mode != "120000":
                raise GitHubApiError(0, f"GitHub tree contains unsupported blob mode {mode}")
            elif entry_type == "tree" and mode != "040000":
                raise GitHubApiError(0, f"GitHub tree contains unsupported tree mode {mode}")
            elif entry_type not in {"blob", "tree", "commit"}:
                raise GitHubApiError(0, f"GitHub tree contains unsupported type {entry_type}")
        return paths


@dataclass(frozen=True)
class Target:
    stable_key: str
    repo: str
    source_path: str
    branch: str
    pinned_sha: str
    verified_at: str
    bundled_files: tuple[str, ...]
    metadata_path: Path
    metadata_hash: str
    metadata: dict


def _metadata_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _safe_bundle_path(value: object) -> str:
    if not is_safe_portable_relative_path(value):
        return ""
    if PurePosixPath(value).parts[0].casefold() in {"skill.md", "metadata.json"}:
        return ""
    return value


def _actual_bundled_files(skill_dir: Path) -> list[str]:
    files = []

    def raise_walk_error(error: OSError) -> None:
        raise error

    for dirpath, dirnames, filenames in os.walk(skill_dir, onerror=raise_walk_error):
        directory = Path(dirpath)
        for name in dirnames + filenames:
            path = directory / name
            relative = path.relative_to(skill_dir).as_posix()
            if path.is_symlink():
                raise ValueError(f"archive contains a symbolic link: {relative}")
            if path.is_file() and relative not in {"SKILL.md", "metadata.json"}:
                files.append(relative)
    if has_case_conflicting_paths(files):
        raise ValueError("archive contains case-conflicting bundled paths")
    return sorted(files)


def _looks_like_target(metadata: object, skill_dir: Path) -> bool:
    if isinstance(metadata, dict):
        return any(field in metadata for field in VERIFICATION_EVIDENCE_FIELDS)
    return any(
        path.is_file() and path.name not in {"SKILL.md", "metadata.json"}
        for path in skill_dir.rglob("*")
    )


def _target_from_metadata(metadata_path: Path, skills_dir: Path) -> Target:
    skill_dir = metadata_path.parent
    category_dir = skill_dir.parent
    if category_dir.is_symlink() or skill_dir.is_symlink():
        raise ValueError("canonical archive category and skill directories cannot be symlinks")
    try:
        skill_dir.resolve().relative_to(skills_dir.resolve())
    except ValueError as exc:
        raise ValueError("canonical archive path escapes skills root") from exc
    relative_dir = skill_dir.relative_to(skills_dir).as_posix()
    if len(PurePosixPath(relative_dir).parts) != 2:
        raise ValueError("canonical archive path must be <category>/<skill>")
    if metadata_path.is_symlink() or not metadata_path.is_file():
        raise ValueError("metadata.json must be a regular file")
    skill_path = skill_dir / "SKILL.md"
    if skill_path.is_symlink() or not skill_path.is_file():
        raise ValueError("SKILL.md must be a regular file")
    raw = metadata_path.read_bytes()
    try:
        metadata = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid metadata JSON: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be an object")
    repo, source_path, source_error = canonical_source_identity_from_metadata(metadata)
    if source_error:
        if source_error == "conflicting_source_path_aliases":
            raise ValueError("conflicting path and github_path identities")
        if source_error == "missing_source_path" and "path" in metadata:
            raise ValueError("path must be a non-empty string")
        raise ValueError(source_error)
    canonical_branch = metadata.get("github_branch")
    legacy_branch = metadata.get("branch")
    for field, value in (("github_branch", canonical_branch), ("branch", legacy_branch)):
        if field in metadata and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{field} must be a non-empty string")
    if "github_branch" in metadata and "branch" in metadata and canonical_branch != legacy_branch:
        raise ValueError("conflicting github_branch and branch identities")
    if any(
        isinstance(value, str) and SHA_PATTERN.fullmatch(value.strip())
        for value in (canonical_branch, legacy_branch)
    ):
        raise ValueError("source branch cannot be a raw commit SHA")
    branch = exact_source_branch(metadata)
    if not branch:
        raise ValueError("missing exact source branch")
    pinned_sha = metadata.get("github_commit_sha")
    if not isinstance(pinned_sha, str) or not SHA_PATTERN.fullmatch(pinned_sha):
        raise ValueError("missing immutable github_commit_sha")
    verified_at = metadata.get("assets_verified_at")
    if not isinstance(verified_at, str) or not verified_at.strip():
        raise ValueError("missing assets_verified_at")
    declared = metadata.get("bundled_files")
    if not isinstance(declared, list) or not declared:
        raise ValueError("bundled_files must be a non-empty list")
    normalized = [_safe_bundle_path(value) for value in declared]
    if any(not value for value in normalized) or len(set(normalized)) != len(normalized):
        raise ValueError("bundled_files contains an invalid or duplicate path")
    if has_case_conflicting_paths(normalized):
        raise ValueError("bundled_files contains case-conflicting paths")
    actual = _actual_bundled_files(skill_dir)
    if sorted(normalized) != actual:
        raise ValueError(f"bundled_files mismatch: declared={sorted(normalized)}, actual={actual}")
    if not bundled_file_blobs_match(metadata, skill_dir, normalized):
        raise ValueError("bundled_file_blobs do not match archived support file bytes")
    return Target(
        stable_key=f"{repo.casefold()}:{source_path}",
        repo=repo,
        source_path=source_path,
        branch=branch,
        pinned_sha=pinned_sha.lower(),
        verified_at=verified_at,
        bundled_files=tuple(sorted(normalized)),
        metadata_path=metadata_path,
        metadata_hash=_metadata_hash(raw),
        metadata=metadata,
    )


def load_targets(skills_dir: Path) -> tuple[list[Target], list[dict]]:
    root = skills_dir.resolve()
    targets = []
    errors = []
    seen = set()
    metadata_paths = []
    try:
        list(iter_canonical_archive_paths(skills_dir))
    except ValueError as exc:
        return [], [{"stable_key": str(skills_dir), "status": "local_error", "error": str(exc)}]
    try:
        category_paths = sorted(root.iterdir())
    except OSError as exc:
        return [], [{"stable_key": str(skills_dir), "status": "local_error", "error": str(exc)}]
    if has_case_conflicting_paths(
        path.name for path in category_paths if path.is_dir() or path.is_symlink()
    ):
        return [], [
            {
                "stable_key": str(skills_dir),
                "status": "local_error",
                "error": "canonical archive contains case-conflicting category paths",
            }
        ]
    for category_path in category_paths:
        if category_path.is_symlink():
            errors.append(
                {
                    "stable_key": relative_path(category_path, root),
                    "status": "local_error",
                    "error": "canonical archive category directory cannot be a symlink",
                }
            )
            continue
        if not category_path.is_dir():
            continue
        try:
            skill_paths = sorted(category_path.iterdir())
        except OSError as exc:
            errors.append(
                {
                    "stable_key": relative_path(category_path, root),
                    "status": "local_error",
                    "error": str(exc)[:500],
                }
            )
            continue
        if has_case_conflicting_paths(
            path.name for path in skill_paths if path.is_dir() or path.is_symlink()
        ):
            errors.append(
                {
                    "stable_key": relative_path(category_path, root),
                    "status": "local_error",
                    "error": "canonical archive contains case-conflicting skill paths",
                }
            )
            continue
        for skill_path in skill_paths:
            if skill_path.is_symlink():
                errors.append(
                    {
                        "stable_key": relative_path(skill_path, root),
                        "status": "local_error",
                        "error": "canonical archive skill directory cannot be a symlink",
                    }
                )
            elif skill_path.is_dir():
                metadata_path = skill_path / "metadata.json"
                if (
                    metadata_path.is_symlink()
                    or not metadata_path.exists()
                    or not metadata_path.is_file()
                ):
                    if _looks_like_target(None, skill_path):
                        errors.append(
                            {
                                "stable_key": relative_path(skill_path, root),
                                "status": "local_error",
                                "error": "metadata.json must be a regular file",
                            }
                        )
                    continue
                metadata_paths.append(metadata_path)
    for metadata_path in metadata_paths:
        skill_dir = metadata_path.parent
        try:
            raw_metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            raw_metadata = None
        if not _looks_like_target(raw_metadata, skill_dir):
            continue
        try:
            target = _target_from_metadata(metadata_path, root)
            if target.stable_key in seen:
                raise ValueError(f"duplicate stable key: {target.stable_key}")
            seen.add(target.stable_key)
            targets.append(target)
        except (OSError, ValueError) as exc:
            errors.append(
                {
                    "stable_key": relative_path(metadata_path, root),
                    "status": "local_error",
                    "error": str(exc)[:500],
                }
            )
    return targets, errors


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def _error_rows(targets: list[Target], status: str, error: Exception) -> list[dict]:
    return [
        {
            "stable_key": target.stable_key,
            "repo": target.repo,
            "source_path": target.source_path,
            "status": status,
            "pinned_source_sha": target.pinned_sha,
            "error": str(error)[:500],
        }
        for target in targets
    ]


def verify_targets(targets: list[Target], client: GitHubClient, checked_at: str) -> list[dict]:
    rows = []
    by_repo: dict[str, list[Target]] = collections.defaultdict(list)
    for target in targets:
        by_repo[target.repo].append(target)
    for repo, repo_targets in sorted(by_repo.items()):
        try:
            repository = client.repository(repo)
            full_name = repository.get("full_name")
            if not isinstance(full_name, str):
                raise GitHubApiError(0, "GitHub repository response lacks full_name")
            if full_name.casefold() != repo.casefold():
                raise GitHubApiError(301, "GitHub repository identity moved or mismatched")
        except GitHubApiError as exc:
            status = (
                "gone"
                if exc.status == 404
                else "moved"
                if exc.status == 301
                else "verification_error"
            )
            rows.extend(_error_rows(repo_targets, status, exc))
            continue
        by_branch: dict[str, list[Target]] = collections.defaultdict(list)
        for target in repo_targets:
            by_branch[target.branch].append(target)
        for branch, branch_targets in sorted(by_branch.items()):
            try:
                current_sha = client.branch_sha(repo, branch)
            except GitHubApiError as exc:
                status = "moved" if exc.status == 404 else "verification_error"
                rows.extend(_error_rows(branch_targets, status, exc))
                continue
            try:
                upstream_paths = client.tree(repo, current_sha)
            except GitHubApiError as exc:
                rows.extend(_error_rows(branch_targets, "verification_error", exc))
                continue
            for target in branch_targets:
                source_dir = PurePosixPath(target.source_path).parent
                expected_assets = {
                    (source_dir / bundled_file).as_posix() for bundled_file in target.bundled_files
                }
                missing_assets = sorted(expected_assets - upstream_paths)
                if target.source_path not in upstream_paths:
                    status = "moved"
                elif missing_assets:
                    status = "partial"
                else:
                    status = "live"
                rows.append(
                    {
                        "stable_key": target.stable_key,
                        "repo": repo,
                        "source_path": target.source_path,
                        "branch": branch,
                        "status": status,
                        "pinned_source_sha": target.pinned_sha,
                        "current_source_sha": current_sha,
                        "checked_at": checked_at,
                        "missing_assets": missing_assets,
                        "metadata_path": str(target.metadata_path),
                        "metadata_hash": target.metadata_hash,
                    }
                )
    return rows


def _write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(file_descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def apply_updates(targets: list[Target], rows: list[dict], checked_at: str) -> list[str]:
    target_by_key = {target.stable_key: target for target in targets}
    updates = []
    for row in rows:
        if row["status"] not in LIVENESS_STATUSES:
            continue
        target = target_by_key[row["stable_key"]]
        try:
            current = target.metadata_path.read_bytes()
        except OSError as exc:
            return [f"{target.stable_key}: unable to read metadata before apply: {exc}"]
        if _metadata_hash(current) != target.metadata_hash:
            return [f"{target.stable_key}: metadata changed after verification"]
        metadata = dict(target.metadata)
        metadata["asset_liveness"] = row["status"]
        metadata["assets_liveness_checked_at"] = checked_at
        current_sha = row.get("current_source_sha")
        if current_sha:
            metadata["assets_liveness_sha"] = current_sha
        else:
            metadata.pop("assets_liveness_sha", None)
        content = (json.dumps(metadata, indent=2, ensure_ascii=False) + "\n").encode()
        updates.append((target, current, content))
    applied = []
    try:
        for target, original, content in updates:
            _write_atomic(target.metadata_path, content)
            applied.append((target, original))
    except Exception as exc:  # noqa: BLE001 — restore the entire applied batch
        recovery_errors = []
        for target, original in reversed(applied):
            try:
                _write_atomic(target.metadata_path, original)
            except Exception as recovery_exc:  # noqa: BLE001 — report every failed restore
                recovery_errors.append(f"{target.stable_key}: {recovery_exc}")
        detail = f"metadata apply failed: {type(exc).__name__}: {exc}"
        if recovery_errors:
            detail += f"; recovery failed: {recovery_errors}"
        return [detail]
    return []


def summarize(rows: list[dict]) -> dict[str, int]:
    counts = collections.Counter(row.get("status", "invalid") for row in rows)
    return dict(sorted(counts.items()))


def resolve_skill_dir(target: dict, skill_dirs: list[str]) -> str | None:
    """Resolve one inventory target using the historical JSONL verifier rules."""
    declared = target.get("dir") or ""
    if declared and declared in skill_dirs:
        return declared
    name = target.get("name") or ""
    candidates = [directory for directory in skill_dirs if os.path.basename(directory) == name]
    if not candidates and name:
        candidates = [directory for directory in skill_dirs if name in directory]
    return candidates[0] if candidates else None


def verify_repo(repo: str, targets: list[dict]) -> list[dict]:
    """Verify legacy inventory targets with one upstream tree fetch per repository."""
    try:
        paths = fetch_repo_tree(repo)
    except Exception as exc:  # noqa: BLE001 -- legacy rows record repository failures
        return [{**target, "status": "repo_error", "error": str(exc)[:200]} for target in targets]
    skill_dirs = [os.path.dirname(path) for path in paths if os.path.basename(path) == "SKILL.md"]
    rows = []
    for target in targets:
        resolved = resolve_skill_dir(target, skill_dirs)
        if resolved is None:
            rows.append({**target, "status": "not_found"})
            continue
        if resolved == "":
            rows.append({**target, "status": "root_ambiguous"})
            continue
        siblings = [path for path in paths if path.startswith(f"{resolved}/")]
        counts = classify_files(siblings)
        rows.append(
            {
                **target,
                "resolved_dir": resolved,
                "status": verdict_from_counts(counts),
                **counts,
            }
        )
    return rows


def _legacy_verify_jsonl(targets_path: Path, output_path: Path) -> int:
    """Run the historical ``<targets.jsonl> <out.jsonl>`` interface."""
    targets = [json.loads(line) for line in targets_path.read_text(encoding="utf-8").splitlines()]
    by_repo: dict[str, list[dict]] = collections.defaultdict(list)
    for target in targets:
        by_repo[target["repo"]].append(target)

    summary: collections.Counter = collections.Counter()
    with output_path.open("w", encoding="utf-8") as output:
        for index, (repo, repo_targets) in enumerate(sorted(by_repo.items()), 1):
            for row in verify_repo(repo, repo_targets):
                summary[row["status"]] += 1
                output.write(json.dumps(row) + "\n")
            if index % 25 == 0:
                print(f"[{index}/{len(by_repo)}] verified", file=sys.stderr)
    print(json.dumps(dict(summary), indent=2), file=sys.stderr)
    return 0


def gate_errors(
    report: dict,
    *,
    max_decayed_percent: float,
    max_error_percent: float,
    min_targets: int,
) -> list[str]:
    rows = report.get("rows")
    summary = report.get("summary")
    if not isinstance(rows, list) or not isinstance(summary, dict):
        return ["report rows or summary is malformed"]
    actual_summary = summarize(rows)
    if summary != actual_summary:
        return [f"report summary mismatch: expected {actual_summary}, got {summary}"]
    unknown = sorted(set(actual_summary) - LIVENESS_STATUSES - ERROR_STATUSES)
    if unknown:
        return [f"report contains unknown statuses: {unknown}"]
    total = report.get("target_count")
    if not isinstance(total, int) or total < 0:
        return ["report target_count is malformed"]
    errors = []
    if total < min_targets:
        errors.append(f"verified target count {total} is below minimum {min_targets}")
    denominator = max(total, 1)
    decayed = sum(actual_summary.get(status, 0) for status in {"partial", "moved", "gone"})
    failed = actual_summary.get("verification_error", 0)
    decay_percent = decayed * 100 / denominator
    error_percent = failed * 100 / denominator
    if decay_percent > max_decayed_percent:
        errors.append(
            f"asset decay {decay_percent:.2f}% exceeds {max_decayed_percent:.2f}% "
            f"({decayed}/{total})"
        )
    if actual_summary.get("local_error", 0):
        errors.append("canonical archive validation failed")
    if actual_summary.get("apply_error", 0):
        errors.append("metadata apply or rollback failed")
    if error_percent > max_error_percent:
        errors.append(
            f"verification errors {error_percent:.2f}% exceed {max_error_percent:.2f}% "
            f"({failed}/{total})"
        )
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    parser.add_argument("--report", type=Path, default=Path("asset-liveness-report.json"))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--max-decayed-percent", type=float, default=35.0)
    parser.add_argument("--max-error-percent", type=float, default=10.0)
    parser.add_argument("--min-targets", type=int, default=1)
    args = parser.parse_args(argv)
    if not 0 <= args.max_decayed_percent <= 100:
        parser.error("--max-decayed-percent must be between 0 and 100")
    if not 0 <= args.max_error_percent <= 100:
        parser.error("--max-error-percent must be between 0 and 100")
    if args.min_targets < 1:
        parser.error("--min-targets must be at least 1")
    return args


def main(argv: list[str] | None = None, *, client: GitHubClient | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    if len(effective_argv) == 2 and all(not value.startswith("-") for value in effective_argv):
        return _legacy_verify_jsonl(Path(effective_argv[0]), Path(effective_argv[1]))
    args = parse_args(effective_argv)
    checked_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    targets, local_errors = load_targets(args.skills_dir)
    api_client = client or GitHubClient(os.environ.get("GITHUB_TOKEN", ""))
    rows = local_errors + verify_targets(targets, api_client, checked_at)
    apply_errors = apply_updates(targets, rows, checked_at) if args.apply else []
    rows.extend(
        {"stable_key": "apply", "status": "apply_error", "error": error} for error in apply_errors
    )
    report = {
        "schema_version": 1,
        "checked_at": checked_at,
        "target_count": len(targets) + len(local_errors),
        "repo_count": len({target.repo for target in targets}),
        "applied": args.apply and not apply_errors,
        "summary": summarize(rows),
        "rows": rows,
    }
    gate_failures = gate_errors(
        report,
        max_decayed_percent=args.max_decayed_percent,
        max_error_percent=args.max_error_percent,
        min_targets=args.min_targets,
    )
    report["gate"] = {
        "passed": not gate_failures,
        "errors": gate_failures,
        "max_decayed_percent": args.max_decayed_percent,
        "max_error_percent": args.max_error_percent,
        "min_targets": args.min_targets,
    }
    _write_atomic(args.report, (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode())
    print(json.dumps({"summary": report["summary"], "gate": report["gate"]}, indent=2))
    return 0 if not gate_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
