import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_publish_commit_message as attribution  # noqa: E402
from build_publish_commit_message import (  # noqa: E402
    AttributionError,
    SourceRange,
    build_commit_message,
    build_from_provenance,
    collect_coauthors,
    load_previous_provenance,
    parse_coauthor_value,
)


def git(repo: Path, *arguments: str, input_text: str | None = None) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        input=input_text,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def init_repo(path: Path) -> str:
    path.mkdir()
    git(path, "init", "--quiet")
    git(path, "config", "user.name", "Test Maintainer")
    git(path, "config", "user.email", "maintainer@example.com")
    return commit(path, "initial")


def commit(repo: Path, message: str) -> str:
    git(repo, "commit", "--allow-empty", "--file=-", input_text=f"{message}\n")
    return git(repo, "rev-parse", "HEAD")


def source_range(label: str, repo: Path, previous_sha: str, new_sha: str) -> SourceRange:
    return SourceRange(
        label=label,
        repository=f"owner/{label}",
        directory=repo,
        previous_sha=previous_sha,
        new_sha=new_sha,
    )


def write_provenance(path: Path, core_sha: str, data_sha: str) -> None:
    path.write_text(
        json.dumps(
            {
                "generated_at": "2026-08-02T00:00:00Z",
                "core_repo": "owner/core",
                "core_sha": core_sha,
                "data_repo": "owner/data",
                "data_sha": data_sha,
            }
        ),
        encoding="utf-8",
    )


def test_collects_source_trailers_in_deterministic_order_and_deduplicates_email(tmp_path):
    core = tmp_path / "core"
    data = tmp_path / "data"
    old_core = init_repo(core)
    old_data = init_repo(data)
    new_core = commit(
        core,
        "core change\n\nCo-authored-by: Lee <leeroyhannigan@yahoo.ie>",
    )
    new_data = commit(
        data,
        "data change\n\n"
        "Co-authored-by: Duplicate Lee <LEEROYHANNIGAN@yahoo.ie>\n"
        "Co-authored-by: Ada Lovelace <ada@example.com>",
    )

    coauthors = collect_coauthors(
        [
            source_range("core", core, old_core, new_core),
            source_range("data", data, old_data, new_data),
        ]
    )

    assert [item.trailer for item in coauthors] == [
        "Co-authored-by: Lee <leeroyhannigan@yahoo.ie>",
        "Co-authored-by: Ada Lovelace <ada@example.com>",
    ]


def test_rejects_malformed_source_trailer(tmp_path):
    repo = tmp_path / "core"
    previous_sha = init_repo(repo)
    new_sha = commit(repo, "change\n\nCo-authored-by: missing-email")

    with pytest.raises(AttributionError, match="invalid Co-authored-by value"):
        collect_coauthors([source_range("core", repo, previous_sha, new_sha)])


@pytest.mark.parametrize(
    "value",
    [
        "Lee <lee@example.com>\nInjected: value",
        "Lee <lee@example.com>\x7f",
        "<lee@example.com>",
        "Lee lee@example.com",
    ],
)
def test_rejects_invalid_or_injectable_values(value):
    with pytest.raises(AttributionError):
        parse_coauthor_value(value)


def test_ignores_unchanged_and_explicit_rollback_ranges(tmp_path):
    repo = tmp_path / "data"
    old_sha = init_repo(repo)
    new_sha = commit(repo, "change\n\nCo-authored-by: Lee <lee@example.com>")

    unchanged = collect_coauthors([source_range("data", repo, new_sha, new_sha)])
    git(repo, "checkout", "--quiet", "--detach", old_sha)
    rollback = collect_coauthors([source_range("data", repo, new_sha, old_sha)])

    assert unchanged == []
    assert rollback == []


def test_rejects_divergent_source_history(tmp_path):
    repo = tmp_path / "data"
    base_sha = init_repo(repo)
    first_sha = commit(repo, "first branch")
    git(repo, "checkout", "--quiet", "--detach", base_sha)
    second_sha = commit(repo, "second branch")

    with pytest.raises(AttributionError, match="history diverged"):
        collect_coauthors([source_range("data", repo, first_sha, second_sha)])


def test_rejects_checkout_that_does_not_match_pinned_new_sha(tmp_path):
    repo = tmp_path / "core"
    old_sha = init_repo(repo)
    expected_sha = commit(repo, "expected")
    commit(repo, "unexpected head")

    with pytest.raises(AttributionError, match="expected pinned SHA"):
        collect_coauthors([source_range("core", repo, old_sha, expected_sha)])


def test_rejects_missing_checkout_and_invalid_source_identity(tmp_path):
    with pytest.raises(AttributionError, match="owner/name"):
        collect_coauthors(
            [SourceRange("core", "invalid", tmp_path / "missing", "a" * 40, "b" * 40)]
        )

    with pytest.raises(AttributionError, match="40-character Git SHA"):
        collect_coauthors(
            [SourceRange("core", "owner/core", tmp_path / "missing", "bad", "b" * 40)]
        )

    with pytest.raises(AttributionError, match="checkout is missing"):
        collect_coauthors(
            [
                SourceRange(
                    "core",
                    "owner/core",
                    tmp_path / "missing",
                    "a" * 40,
                    "b" * 40,
                )
            ]
        )


def test_rejects_missing_source_commit(tmp_path):
    repo = tmp_path / "core"
    head_sha = init_repo(repo)

    with pytest.raises(AttributionError, match="Not a valid object name"):
        collect_coauthors([source_range("core", repo, "a" * 40, head_sha)])


def test_enforces_source_commit_and_coauthor_limits(tmp_path, monkeypatch):
    repo = tmp_path / "data"
    old_sha = init_repo(repo)
    commit(repo, "first")
    new_sha = commit(repo, "second")
    monkeypatch.setattr(attribution, "MAX_SOURCE_COMMITS", 1)

    with pytest.raises(AttributionError, match="range contains 2 commits"):
        collect_coauthors([source_range("data", repo, old_sha, new_sha)])

    repo = tmp_path / "core"
    old_sha = init_repo(repo)
    new_sha = commit(
        repo,
        "change\n\nCo-authored-by: One <one@example.com>\nCo-authored-by: Two <two@example.com>",
    )
    monkeypatch.setattr(attribution, "MAX_SOURCE_COMMITS", 10_000)
    monkeypatch.setattr(attribution, "MAX_COAUTHORS", 1)

    with pytest.raises(AttributionError, match="more than 1 unique co-authors"):
        collect_coauthors([source_range("core", repo, old_sha, new_sha)])


def test_builds_exact_subject_and_trailer_block():
    coauthor = parse_coauthor_value("Lee <leeroyhannigan@yahoo.ie>")

    message = build_commit_message("a" * 40, "b" * 40, [coauthor])

    assert message == (
        "chore: publish merged artifact core@aaaaaaaaaaaa data@bbbbbbbbbbbb\n\n"
        "Co-authored-by: Lee <leeroyhannigan@yahoo.ie>\n"
    )


def test_builds_subject_only_message_without_source_trailers():
    assert build_commit_message("a" * 40, "b" * 40, []) == (
        "chore: publish merged artifact core@aaaaaaaaaaaa data@bbbbbbbbbbbb\n"
    )


@pytest.mark.parametrize(
    ("contents", "error"),
    [
        (None, "previous provenance is missing"),
        ("not-json", "not valid JSON"),
        ("[]", "must be a JSON object"),
        ("{}", "core_repo must be an owner/name repository"),
    ],
)
def test_rejects_missing_or_invalid_previous_provenance(tmp_path, contents, error):
    path = tmp_path / "previous.json"
    if contents is not None:
        path.write_text(contents, encoding="utf-8")

    with pytest.raises(AttributionError, match=error):
        load_previous_provenance(path)


def test_build_from_provenance_rejects_repository_change(tmp_path):
    core = tmp_path / "core"
    data = tmp_path / "data"
    core_sha = init_repo(core)
    data_sha = init_repo(data)
    provenance = tmp_path / "previous.json"
    write_provenance(provenance, core_sha, data_sha)

    with pytest.raises(AttributionError, match="core repository changed"):
        build_from_provenance(
            previous_provenance=provenance,
            core_repo="other/core",
            core_dir=core,
            core_sha=core_sha,
            data_repo="owner/data",
            data_dir=data,
            data_sha=data_sha,
        )


def test_build_from_provenance_accepts_repository_name_case_changes(tmp_path):
    core = tmp_path / "core"
    data = tmp_path / "data"
    core_sha = init_repo(core)
    data_sha = init_repo(data)
    provenance = tmp_path / "previous.json"
    write_provenance(provenance, core_sha, data_sha)

    message, coauthors = build_from_provenance(
        previous_provenance=provenance,
        core_repo="Owner/Core",
        core_dir=core,
        core_sha=core_sha,
        data_repo="Owner/Data",
        data_dir=data,
        data_sha=data_sha,
    )

    assert coauthors == []
    assert message.endswith(f"data@{data_sha[:12]}\n")


def test_cli_writes_message_from_previous_provenance(tmp_path):
    core = tmp_path / "core"
    data = tmp_path / "data"
    old_core = init_repo(core)
    old_data = init_repo(data)
    new_core = commit(core, "core change")
    new_data = commit(
        data,
        "pricing fix\n\nCo-authored-by: Lee <leeroyhannigan@yahoo.ie>",
    )
    provenance = tmp_path / "previous.json"
    output = tmp_path / "commit-message.txt"
    write_provenance(provenance, old_core, old_data)

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "build_publish_commit_message.py"),
            "--previous-provenance",
            str(provenance),
            "--core-repo",
            "owner/core",
            "--core-dir",
            str(core),
            "--core-sha",
            new_core,
            "--data-repo",
            "owner/data",
            "--data-dir",
            str(data),
            "--data-sha",
            new_data,
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 unique co-author(s)" in result.stdout
    assert output.read_text(encoding="utf-8").endswith(
        "\n\nCo-authored-by: Lee <leeroyhannigan@yahoo.ie>\n"
    )


def test_main_returns_failure_without_writing_for_invalid_provenance(tmp_path, monkeypatch, capsys):
    output = tmp_path / "message.txt"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_publish_commit_message.py",
            "--previous-provenance",
            str(tmp_path / "missing.json"),
            "--core-repo",
            "owner/core",
            "--core-dir",
            str(tmp_path / "core"),
            "--core-sha",
            "a" * 40,
            "--data-repo",
            "owner/data",
            "--data-dir",
            str(tmp_path / "data"),
            "--data-sha",
            "b" * 40,
            "--output",
            str(output),
        ],
    )

    assert attribution.main() == 1
    assert not output.exists()
    assert "Publish attribution validation failed" in capsys.readouterr().out
