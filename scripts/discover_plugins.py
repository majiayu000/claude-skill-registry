#!/usr/bin/env python3
"""Discover packaged Claude Code plugins without hiding source failures."""

from __future__ import annotations

import argparse
import base64
import json
import logging
import os
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from plugin_index import PluginIndexError, _validate_plugins

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

NPM_QUERIES = [
    "claude skills",
    "claude code skills",
    "claude commands hooks",
    "claude agent skills",
]
ERROR_KINDS = {
    "nonzero_exit",
    "timeout",
    "malformed_json",
    "invalid_shape",
    "api_failure",
    "read_error",
    "write_error",
}


class DiscoveryError(RuntimeError):
    """Typed, source-scoped discovery failure safe for reports."""

    def __init__(
        self,
        *,
        source: str,
        operation: str,
        kind: str,
        subject: str,
        message: str,
    ) -> None:
        if kind not in ERROR_KINDS:
            raise ValueError(f"unsupported discovery error kind: {kind}")
        self.source = source
        self.operation = operation
        self.kind = kind
        self.subject = subject[:240]
        self.message = " ".join(message.split())[:500]
        super().__init__(
            f"{self.source}:{self.operation}:{self.kind}:{self.subject}: {self.message}"
        )

    def as_dict(self) -> dict[str, str]:
        return {
            "source": self.source,
            "operation": self.operation,
            "kind": self.kind,
            "subject": self.subject,
            "message": self.message,
        }


@dataclass(frozen=True)
class SourceOutcome:
    """Outcome for one attempted discovery source unit."""

    unit: str
    status: str
    candidate_count: int = 0
    error: DiscoveryError | None = None

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "unit": self.unit,
            "status": self.status,
            "candidate_count": self.candidate_count,
        }
        if self.error is not None:
            result["error"] = self.error.as_dict()
        return result


@dataclass(frozen=True)
class DiscoveryReport:
    """Versioned CLI result that preserves partial/failed truth."""

    status: str
    allow_partial: bool
    candidates: list[dict[str, Any]]
    outcomes: list[SourceOutcome]
    errors: list[DiscoveryError] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "status": self.status,
            "allow_partial": self.allow_partial,
            "candidates": self.candidates,
            "sources": [outcome.as_dict() for outcome in self.outcomes],
            "errors": [error.as_dict() for error in self.errors],
        }


def _run_command(
    command: Sequence[str],
    *,
    source: str,
    operation: str,
    subject: str,
    timeout: int,
) -> str:
    try:
        result = subprocess.run(
            list(command),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise DiscoveryError(
            source=source,
            operation=operation,
            kind="timeout",
            subject=subject,
            message=f"command timed out after {timeout}s",
        ) from exc
    except OSError as exc:
        raise DiscoveryError(
            source=source,
            operation=operation,
            kind="api_failure",
            subject=subject,
            message=f"unable to execute command: {exc.__class__.__name__}",
        ) from exc
    if result.returncode != 0:
        raise DiscoveryError(
            source=source,
            operation=operation,
            kind="nonzero_exit",
            subject=subject,
            message=f"command exited with status {result.returncode}",
        )
    return result.stdout


def _load_json(raw: str, *, source: str, operation: str, subject: str) -> Any:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise DiscoveryError(
            source=source,
            operation=operation,
            kind="malformed_json",
            subject=subject,
            message=f"invalid JSON at line {exc.lineno} column {exc.colno}",
        ) from exc


def npm_search(query: str) -> list[dict[str, Any]]:
    raw = _run_command(
        ["npm", "search", query, "--json", "--long"],
        source="npm",
        operation="search",
        subject=query,
        timeout=30,
    )
    payload = _load_json(raw, source="npm", operation="search", subject=query)
    if not isinstance(payload, list) or any(not isinstance(item, dict) for item in payload):
        raise DiscoveryError(
            source="npm",
            operation="search",
            kind="invalid_shape",
            subject=query,
            message="expected a JSON list of package objects",
        )
    return payload


def npm_view(pkg_name: str) -> dict[str, Any]:
    raw = _run_command(
        ["npm", "view", pkg_name, "--json"],
        source="npm",
        operation="view",
        subject=pkg_name,
        timeout=10,
    )
    payload = _load_json(raw, source="npm", operation="view", subject=pkg_name)
    if not isinstance(payload, dict):
        raise DiscoveryError(
            source="npm",
            operation="view",
            kind="invalid_shape",
            subject=pkg_name,
            message="expected a JSON package object",
        )
    return payload


def extract_repo_slug(npm_info: dict[str, Any]) -> str:
    """Extract owner/repo from npm package repository field."""
    repo = npm_info.get("repository", {})
    url = repo.get("url", "") if isinstance(repo, dict) else str(repo)
    url = url.replace("git+", "").replace(".git", "").replace("git://", "https://")
    for prefix in ("https://github.com/", "http://github.com/"):
        if url.startswith(prefix):
            parts = url[len(prefix) :].strip("/").split("/")
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
    return ""


def gh_api(endpoint: str, jq: str = "") -> str:
    command = ["gh", "api", endpoint]
    if jq:
        command += ["--jq", jq]
    return _run_command(
        command,
        source="github",
        operation="api",
        subject=endpoint,
        timeout=15,
    ).strip()


def inspect_repo_structure(repo: str) -> dict[str, Any]:
    """Read required GitHub metadata/tree or raise a source-scoped error."""
    meta_raw = gh_api(
        f"repos/{repo}",
        "{description: .description, stargazers_count: .stargazers_count, "
        "default_branch: .default_branch}",
    )
    if not meta_raw:
        raise DiscoveryError(
            source="github",
            operation="repo_metadata",
            kind="api_failure",
            subject=repo,
            message="empty repository metadata response",
        )
    meta = _load_json(
        meta_raw,
        source="github",
        operation="repo_metadata",
        subject=repo,
    )
    if not isinstance(meta, dict):
        raise DiscoveryError(
            source="github",
            operation="repo_metadata",
            kind="invalid_shape",
            subject=repo,
            message="expected repository metadata object",
        )
    branch = meta.get("default_branch")
    stars = meta.get("stargazers_count")
    if not isinstance(branch, str) or not branch or not isinstance(stars, int):
        raise DiscoveryError(
            source="github",
            operation="repo_metadata",
            kind="invalid_shape",
            subject=repo,
            message="default_branch and integer stargazers_count are required",
        )

    tree_raw = gh_api(f"repos/{repo}/git/trees/{branch}?recursive=true")
    tree = _load_json(
        tree_raw,
        source="github",
        operation="repo_tree",
        subject=repo,
    )
    if not isinstance(tree, dict) or not isinstance(tree.get("truncated"), bool):
        raise DiscoveryError(
            source="github",
            operation="repo_tree",
            kind="invalid_shape",
            subject=repo,
            message="expected a recursive tree object with a boolean truncated flag",
        )
    if tree["truncated"]:
        raise DiscoveryError(
            source="github",
            operation="repo_tree",
            kind="api_failure",
            subject=repo,
            message="recursive repository tree response was truncated",
        )
    entries = tree.get("tree")
    if not isinstance(entries, list) or any(
        not isinstance(entry, dict) or not isinstance(entry.get("path"), str)
        for entry in entries
    ):
        raise DiscoveryError(
            source="github",
            operation="repo_tree",
            kind="invalid_shape",
            subject=repo,
            message="expected tree entries with string paths",
        )
    paths = [entry["path"] for entry in entries]
    result: dict[str, Any] = {
        "skills": [],
        "commands": [],
        "hooks": [],
        "has_package_json": False,
        "description": meta.get("description") or "",
        "stars": stars,
        "default_branch": branch,
    }
    for path in paths:
        lower = path.lower()
        if lower.endswith("skill.md"):
            result["skills"].append(path)
        elif "/commands/" in path and lower.endswith(".md"):
            result["commands"].append(path)
        elif "/hooks/" in path and lower.endswith((".sh", ".json", ".js")):
            result["hooks"].append(path)
        elif path == "package.json":
            result["has_package_json"] = True
    return result


def get_install_command(repo: str, branch: str) -> str:
    """Read package.json and return the npx command when a bin exists."""
    del branch  # GitHub contents API resolves the repository default branch.
    content_raw = gh_api(f"repos/{repo}/contents/package.json", ".content")
    if not content_raw:
        raise DiscoveryError(
            source="github",
            operation="package_content",
            kind="api_failure",
            subject=repo,
            message="empty package.json content response",
        )
    try:
        decoded = base64.b64decode(content_raw, validate=True).decode("utf-8")
    except (ValueError, UnicodeDecodeError) as exc:
        raise DiscoveryError(
            source="github",
            operation="package_content",
            kind="malformed_json",
            subject=repo,
            message="package.json content is not valid base64 UTF-8",
        ) from exc
    package = _load_json(
        decoded,
        source="github",
        operation="package_content",
        subject=repo,
    )
    if not isinstance(package, dict):
        raise DiscoveryError(
            source="github",
            operation="package_content",
            kind="invalid_shape",
            subject=repo,
            message="package.json must be an object",
        )
    name = package.get("name")
    if package.get("bin") and isinstance(name, str) and name:
        return f"npx {name}@latest"
    return name if isinstance(name, str) else ""


def score_candidate(
    repo: str,
    structure: dict[str, Any],
    npm_name: str = "",
) -> dict[str, Any]:
    """Score a repo as a plugin candidate using the existing policy."""
    score = 0
    reasons: list[str] = []
    skill_count = len(structure["skills"])
    command_count = len(structure["commands"])
    hook_count = len(structure["hooks"])
    stars = structure["stars"]
    if skill_count < 2:
        return {"repo": repo, "score": 0, "reasons": ["too_few_skills"]}
    if skill_count >= 10:
        score += 3
    elif skill_count >= 5:
        score += 2
    else:
        score += 1
    reasons.append(f"skills={skill_count}")
    if command_count:
        score += 3
        reasons.append(f"commands={command_count}")
    if hook_count:
        score += 3
        reasons.append(f"hooks={hook_count}")
    install = ""
    if npm_name:
        install = f"npx {npm_name}@latest"
        score += 2
        reasons.append(f"npm={npm_name}")
    elif structure["has_package_json"]:
        install = get_install_command(repo, structure["default_branch"])
        if install:
            score += 2
            reasons.append(f"install={install}")
    if stars >= 1000:
        score += 1
        reasons.append(f"stars={stars}")
    return {
        "repo": repo,
        "score": score,
        "reasons": reasons,
        "description": structure["description"],
        "stars": stars,
        "install": install,
        "skill_count": skill_count,
        "command_count": command_count,
        "hook_count": hook_count,
        "sample_skills": [
            path.split("/")[-2] if "/" in path else path
            for path in structure["skills"][:10]
        ],
        "sample_commands": [
            path.split("/")[-1].removesuffix(".md") for path in structure["commands"][:10]
        ],
        "sample_hooks": [path.split("/")[-1] for path in structure["hooks"][:10]],
    }


def _error_outcome(unit: str, error: DiscoveryError) -> SourceOutcome:
    return SourceOutcome(unit=unit, status="error", error=error)


def load_existing_plugins(path: Path) -> tuple[set[str], SourceOutcome]:
    """Load the optional exclusion source; malformed present input is authoritative."""
    if not path.exists():
        return set(), SourceOutcome(unit="existing_plugins", status="optional_missing")
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise DiscoveryError(
            source="plugin_source",
            operation="read_existing",
            kind="malformed_json",
            subject=str(path),
            message="existing plugin source is not UTF-8",
        ) from exc
    except OSError as exc:
        raise DiscoveryError(
            source="plugin_source",
            operation="read_existing",
            kind="read_error",
            subject=str(path),
            message=exc.__class__.__name__,
        ) from exc
    payload = _load_json(
        raw,
        source="plugin_source",
        operation="read_existing",
        subject=str(path),
    )
    try:
        plugins = _validate_plugins(payload, source="plugin_source", path=path)
    except PluginIndexError as exc:
        raise DiscoveryError(
            source=exc.source,
            operation="read_existing",
            kind=exc.kind,
            subject=str(exc.path),
            message=exc.detail,
        ) from exc
    repos = {plugin["repo"] for plugin in plugins}
    return repos, SourceOutcome(unit="existing_plugins", status="success")


def discover_from_npm(
    existing: set[str],
    outcomes: list[SourceOutcome],
) -> list[dict[str, Any]]:
    """Discover candidates while retaining every npm/GitHub unit failure."""
    all_packages: dict[str, dict[str, Any]] = {}
    for query in NPM_QUERIES:
        try:
            packages = npm_search(query)
        except DiscoveryError as error:
            outcomes.append(_error_outcome(f"npm_search:{query}", error))
            continue
        outcomes.append(SourceOutcome(unit=f"npm_search:{query}", status="success"))
        for package in packages:
            name = package.get("name")
            if isinstance(name, str) and name and name not in all_packages:
                all_packages[name] = package

    seen_repos: set[str] = set()
    candidates: list[dict[str, Any]] = []
    for package_name in all_packages:
        try:
            info = npm_view(package_name)
            outcomes.append(SourceOutcome(unit=f"npm_view:{package_name}", status="success"))
            repo = extract_repo_slug(info)
            if not repo or not info.get("bin") or repo in seen_repos or repo in existing:
                continue
            seen_repos.add(repo)
            structure = inspect_repo_structure(repo)
            candidate = score_candidate(repo, structure, npm_name=package_name)
            outcomes.append(
                SourceOutcome(
                    unit=f"github_inspect:{repo}",
                    status="success",
                    candidate_count=int(candidate["score"] >= 4),
                )
            )
            if candidate["score"] >= 4:
                candidates.append(candidate)
        except DiscoveryError as error:
            outcomes.append(_error_outcome(f"package:{package_name}", error))
    return candidates


def _load_registry_repos(registry_path: Path) -> tuple[list[str], SourceOutcome]:
    if not registry_path.exists():
        return [], SourceOutcome(unit="registry_enrichment", status="optional_missing")
    try:
        raw = registry_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise DiscoveryError(
            source="registry",
            operation="read",
            kind="malformed_json",
            subject=str(registry_path),
            message="registry enrichment source is not UTF-8",
        ) from exc
    except OSError as exc:
        raise DiscoveryError(
            source="registry",
            operation="read",
            kind="read_error",
            subject=str(registry_path),
            message=exc.__class__.__name__,
        ) from exc
    payload = _load_json(
        raw,
        source="registry",
        operation="read",
        subject=str(registry_path),
    )
    if not isinstance(payload, dict) or not isinstance(payload.get("skills"), list):
        raise DiscoveryError(
            source="registry",
            operation="read",
            kind="invalid_shape",
            subject=str(registry_path),
            message="expected an object with a skills list",
        )
    counts: dict[str, int] = {}
    for index, skill in enumerate(payload["skills"]):
        if not isinstance(skill, dict):
            raise DiscoveryError(
                source="registry",
                operation="read",
                kind="invalid_shape",
                subject=str(registry_path),
                message=f"skills[{index}] must be an object",
            )
        repo = skill.get("repo")
        if isinstance(repo, str) and repo:
            counts[repo] = counts.get(repo, 0) + 1
    repos = [repo for repo, count in sorted(counts.items(), key=lambda item: -item[1]) if count >= 10]
    return repos[:30], SourceOutcome(unit="registry_enrichment", status="success")


def discover_from_registry(
    registry_path: Path,
    existing: set[str],
    checked_repos: set[str],
    outcomes: list[SourceOutcome],
) -> list[dict[str, Any]]:
    """Discover optional registry candidates without hiding parse/API failures."""
    try:
        repos, registry_outcome = _load_registry_repos(registry_path)
    except DiscoveryError as error:
        outcomes.append(_error_outcome("registry_enrichment", error))
        return []
    outcomes.append(registry_outcome)
    candidates: list[dict[str, Any]] = []
    for repo in repos:
        if repo in existing or repo in checked_repos or "claude-skill-registry" in repo:
            continue
        try:
            structure = inspect_repo_structure(repo)
            candidate = score_candidate(repo, structure)
            outcomes.append(
                SourceOutcome(
                    unit=f"registry_repo:{repo}",
                    status="success",
                    candidate_count=int(candidate["score"] >= 4),
                )
            )
            if candidate["score"] >= 4:
                candidates.append(candidate)
        except DiscoveryError as error:
            outcomes.append(_error_outcome(f"registry_repo:{repo}", error))
    return candidates


def derive_status(outcomes: Sequence[SourceOutcome], *, authoritative_error: bool = False) -> str:
    """Derive status from source truth, never from candidate count."""
    if authoritative_error:
        return "failed"
    errors = sum(outcome.status == "error" for outcome in outcomes)
    successes = sum(
        outcome.status == "success" and outcome.unit != "existing_plugins"
        for outcome in outcomes
    )
    if errors == 0:
        return "complete"
    return "partial" if successes else "failed"


def build_report(
    *,
    candidates: list[dict[str, Any]],
    outcomes: list[SourceOutcome],
    allow_partial: bool,
    authoritative_error: bool = False,
) -> DiscoveryReport:
    errors = [outcome.error for outcome in outcomes if outcome.error is not None]
    return DiscoveryReport(
        status=derive_status(outcomes, authoritative_error=authoritative_error),
        allow_partial=allow_partial,
        candidates=sorted(candidates, key=lambda item: (-item["score"], -item["stars"])),
        outcomes=outcomes,
        errors=errors,
    )


def run_discovery(
    *,
    plugins_path: Path,
    registry_path: Path,
    npm_only: bool,
    allow_partial: bool,
) -> DiscoveryReport:
    outcomes: list[SourceOutcome] = []
    try:
        existing, existing_outcome = load_existing_plugins(plugins_path)
    except DiscoveryError as error:
        outcomes.append(_error_outcome("existing_plugins", error))
        return build_report(
            candidates=[],
            outcomes=outcomes,
            allow_partial=allow_partial,
            authoritative_error=True,
        )
    outcomes.append(existing_outcome)
    npm_candidates = discover_from_npm(existing, outcomes)
    registry_candidates: list[dict[str, Any]] = []
    if not npm_only:
        registry_candidates = discover_from_registry(
            registry_path,
            existing,
            {candidate["repo"] for candidate in npm_candidates},
            outcomes,
        )
    return build_report(
        candidates=npm_candidates + registry_candidates,
        outcomes=outcomes,
        allow_partial=allow_partial,
    )


def write_discovery_report(path: Path, report: DiscoveryReport) -> None:
    """Atomically replace a complete or explicitly allowed partial report."""
    try:
        serialized = json.dumps(report.as_dict(), ensure_ascii=False, indent=2) + "\n"
    except (TypeError, ValueError) as exc:
        raise DiscoveryError(
            source="output",
            operation="serialize",
            kind="write_error",
            subject=str(path),
            message=f"unable to serialize report: {exc}",
        ) from exc
    temp_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        temp_path.replace(path)
    except OSError as exc:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise DiscoveryError(
            source="output",
            operation="write",
            kind="write_error",
            subject=str(path),
            message=exc.__class__.__name__,
        ) from exc


def _display_candidates(candidates: Sequence[dict[str, Any]]) -> None:
    for candidate in candidates:
        marker = "★" if candidate["command_count"] and candidate["hook_count"] else "○"
        logger.info(f"{marker} [{candidate['score']:>2d}] {candidate['repo']}")


def _exit_code(report: DiscoveryReport) -> int:
    if report.status == "complete":
        return 0
    if report.status == "partial" and report.allow_partial:
        return 0
    return 2 if report.status == "partial" else 1


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover Claude Code plugins (skills + commands + hooks products)",
    )
    parser.add_argument("--plugins", default="sources/plugins.json")
    parser.add_argument("--registry", default="registry.json")
    parser.add_argument("--output", "-o")
    parser.add_argument("--npm-only", action="store_true")
    parser.add_argument("--allow-partial", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = run_discovery(
        plugins_path=Path(args.plugins),
        registry_path=Path(args.registry),
        npm_only=args.npm_only,
        allow_partial=args.allow_partial,
    )
    _display_candidates(report.candidates)
    should_write = report.status == "complete" or (
        report.status == "partial" and report.allow_partial
    )
    if args.output and should_write:
        try:
            write_discovery_report(Path(args.output), report)
        except DiscoveryError as error:
            report = build_report(
                candidates=report.candidates,
                outcomes=report.outcomes + [_error_outcome("output", error)],
                allow_partial=args.allow_partial,
                authoritative_error=True,
            )
    for error in report.errors:
        logger.error(str(error))
    logger.info(
        "status=%s candidates=%d errors=%d allow_partial=%s",
        report.status,
        len(report.candidates),
        len(report.errors),
        str(report.allow_partial).lower(),
    )
    return _exit_code(report)


if __name__ == "__main__":
    raise SystemExit(main())
