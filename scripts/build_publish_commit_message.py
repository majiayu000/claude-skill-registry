#!/usr/bin/env python3
"""Build a main publish commit message with validated source attribution."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

SHA_PATTERN = re.compile(r"[0-9a-f]{40}")
REPOSITORY_PATTERN = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
COAUTHOR_PATTERN = re.compile(
    r"(?P<name>[^<>\x00-\x1f\x7f]{1,200}?)\s+"
    r"<(?P<email>[^\s<>@]{1,64}@[^\s<>@]{1,253})>"
)
CONTROL_PATTERN = re.compile(r"[\x00-\x1f\x7f]")
MAX_SOURCE_COMMITS = 10_000
MAX_COAUTHORS = 200


class AttributionError(ValueError):
    """Raised when source history cannot safely produce publish attribution."""


@dataclass(frozen=True)
class Coauthor:
    name: str
    email: str

    @property
    def trailer(self) -> str:
        return f"Co-authored-by: {self.name} <{self.email}>"


@dataclass(frozen=True)
class SourceRange:
    label: str
    repository: str
    directory: Path
    previous_sha: str
    new_sha: str


def _run_git(directory: Path, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(directory), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "git command failed"
        raise AttributionError(f"{directory}: {detail}")
    return result


def _validate_repository(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not REPOSITORY_PATTERN.fullmatch(value):
        raise AttributionError(f"{field} must be an owner/name repository")
    return value


def _validate_sha(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not SHA_PATTERN.fullmatch(value):
        raise AttributionError(f"{field} must be a lowercase 40-character Git SHA")
    return value


def load_previous_provenance(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise AttributionError(f"previous provenance is missing: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AttributionError(f"previous provenance is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise AttributionError("previous provenance must be a JSON object")

    return {
        "core_repo": _validate_repository(payload.get("core_repo"), field="core_repo"),
        "core_sha": _validate_sha(payload.get("core_sha"), field="core_sha"),
        "data_repo": _validate_repository(payload.get("data_repo"), field="data_repo"),
        "data_sha": _validate_sha(payload.get("data_sha"), field="data_sha"),
    }


def parse_coauthor_value(value: str) -> Coauthor:
    if CONTROL_PATTERN.search(value):
        raise AttributionError("Co-authored-by value contains a control character")
    normalized = value.strip()
    match = COAUTHOR_PATTERN.fullmatch(normalized)
    if match is None:
        raise AttributionError(f"invalid Co-authored-by value: {value!r}")
    name = match.group("name").strip()
    email = match.group("email")
    if not name:
        raise AttributionError("Co-authored-by name must not be blank")
    return Coauthor(name=name, email=email)


def _verify_source(source: SourceRange) -> None:
    _validate_repository(source.repository, field=f"{source.label}_repo")
    _validate_sha(source.previous_sha, field=f"previous_{source.label}_sha")
    _validate_sha(source.new_sha, field=f"new_{source.label}_sha")
    if not source.directory.is_dir():
        raise AttributionError(f"{source.label} checkout is missing: {source.directory}")

    head = _run_git(source.directory, ["rev-parse", "HEAD"]).stdout.strip()
    if head != source.new_sha:
        raise AttributionError(
            f"{source.label} checkout HEAD is {head}, expected pinned SHA {source.new_sha}"
        )
    for sha in (source.previous_sha, source.new_sha):
        _run_git(source.directory, ["cat-file", "-e", f"{sha}^{{commit}}"])


def _is_ancestor(directory: Path, ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(directory), "merge-base", "--is-ancestor", ancestor, descendant],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    detail = result.stderr.strip() or result.stdout.strip() or "git merge-base failed"
    raise AttributionError(f"{directory}: {detail}")


def _forward_commits(source: SourceRange) -> list[str]:
    _verify_source(source)
    if source.previous_sha == source.new_sha:
        return []
    if _is_ancestor(source.directory, source.previous_sha, source.new_sha):
        output = _run_git(
            source.directory,
            [
                "rev-list",
                "--reverse",
                "--topo-order",
                f"{source.previous_sha}..{source.new_sha}",
            ],
        ).stdout
        commits = [line for line in output.splitlines() if line]
        if len(commits) > MAX_SOURCE_COMMITS:
            raise AttributionError(
                f"{source.label} range contains {len(commits)} commits; "
                f"maximum is {MAX_SOURCE_COMMITS}"
            )
        return commits
    if _is_ancestor(source.directory, source.new_sha, source.previous_sha):
        return []
    raise AttributionError(
        f"{source.label} history diverged: neither {source.previous_sha} nor "
        f"{source.new_sha} is an ancestor of the other"
    )


def _commit_coauthors(directory: Path, commit_sha: str) -> list[Coauthor]:
    trailer_format = "%(trailers:key=Co-authored-by,valueonly,separator=%x00,unfold=true)"
    output = _run_git(directory, ["show", "-s", f"--format={trailer_format}", commit_sha]).stdout
    if output.endswith("\n"):
        output = output[:-1]
    if not output:
        return []
    return [parse_coauthor_value(value) for value in output.split("\x00")]


def collect_coauthors(sources: list[SourceRange]) -> list[Coauthor]:
    collected: list[Coauthor] = []
    seen_emails: set[str] = set()
    for source in sources:
        for commit_sha in _forward_commits(source):
            for coauthor in _commit_coauthors(source.directory, commit_sha):
                identity = coauthor.email.casefold()
                if identity in seen_emails:
                    continue
                seen_emails.add(identity)
                collected.append(coauthor)
                if len(collected) > MAX_COAUTHORS:
                    raise AttributionError(
                        f"publish range contains more than {MAX_COAUTHORS} unique co-authors"
                    )
    return collected


def build_commit_message(core_sha: str, data_sha: str, coauthors: list[Coauthor]) -> str:
    _validate_sha(core_sha, field="core_sha")
    _validate_sha(data_sha, field="data_sha")
    subject = f"chore: publish merged artifact core@{core_sha[:12]} data@{data_sha[:12]}"
    if not coauthors:
        return f"{subject}\n"
    trailers = "\n".join(coauthor.trailer for coauthor in coauthors)
    return f"{subject}\n\n{trailers}\n"


def build_from_provenance(
    *,
    previous_provenance: Path,
    core_repo: str,
    core_dir: Path,
    core_sha: str,
    data_repo: str,
    data_dir: Path,
    data_sha: str,
) -> tuple[str, list[Coauthor]]:
    previous = load_previous_provenance(previous_provenance)
    core_repo = _validate_repository(core_repo, field="core_repo")
    data_repo = _validate_repository(data_repo, field="data_repo")
    core_sha = _validate_sha(core_sha, field="core_sha")
    data_sha = _validate_sha(data_sha, field="data_sha")
    if previous["core_repo"].casefold() != core_repo.casefold():
        raise AttributionError("core repository changed from previous provenance")
    if previous["data_repo"].casefold() != data_repo.casefold():
        raise AttributionError("data repository changed from previous provenance")

    sources = [
        SourceRange("core", core_repo, core_dir, previous["core_sha"], core_sha),
        SourceRange("data", data_repo, data_dir, previous["data_sha"], data_sha),
    ]
    coauthors = collect_coauthors(sources)
    return build_commit_message(core_sha, data_sha, coauthors), coauthors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a publish commit message from pinned source commit ranges."
    )
    parser.add_argument("--previous-provenance", type=Path, required=True)
    parser.add_argument("--core-repo", required=True)
    parser.add_argument("--core-dir", type=Path, required=True)
    parser.add_argument("--core-sha", required=True)
    parser.add_argument("--data-repo", required=True)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--data-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        message, coauthors = build_from_provenance(
            previous_provenance=args.previous_provenance,
            core_repo=args.core_repo,
            core_dir=args.core_dir,
            core_sha=args.core_sha,
            data_repo=args.data_repo,
            data_dir=args.data_dir,
            data_sha=args.data_sha,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(message, encoding="utf-8")
    except AttributionError as exc:
        print(f"Publish attribution validation failed: {exc}")
        return 1

    print(f"Built publish commit message with {len(coauthors)} unique co-author(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
