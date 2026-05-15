import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_generated_file_sizes  # noqa: E402


def write_bytes(path: Path, size: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"x" * size)


def test_scan_generated_files_accepts_files_below_warning_threshold(tmp_path):
    write_bytes(tmp_path / "registry.json", 10)
    write_bytes(tmp_path / "docs" / "search-index.json", 20)

    result = check_generated_file_sizes.scan_generated_files(
        root=tmp_path,
        includes=["registry.json", "docs"],
        warn_bytes=100,
        fail_bytes=200,
    )

    assert [record.status for record in result.records] == ["ok", "ok"]
    assert result.warnings == []
    assert result.failures == []


def test_scan_generated_files_warns_without_failing(tmp_path):
    write_bytes(tmp_path / "docs" / "categories" / "other.json", 120)

    result = check_generated_file_sizes.scan_generated_files(
        root=tmp_path,
        includes=["docs"],
        warn_bytes=100,
        fail_bytes=200,
    )

    assert len(result.warnings) == 1
    assert result.warnings[0].path == Path("docs/categories/other.json")
    assert result.failures == []


def test_scan_generated_files_fails_at_failure_threshold(tmp_path):
    write_bytes(tmp_path / "registry.json", 200)

    result = check_generated_file_sizes.scan_generated_files(
        root=tmp_path,
        includes=["registry.json"],
        warn_bytes=100,
        fail_bytes=200,
    )

    assert len(result.failures) == 1
    assert result.failures[0].path == Path("registry.json")


def test_scan_generated_files_skips_missing_future_shard_paths(tmp_path):
    write_bytes(tmp_path / "registry.json", 10)

    result = check_generated_file_sizes.scan_generated_files(
        root=tmp_path,
        includes=["registry.json", "registry-shards"],
        warn_bytes=100,
        fail_bytes=200,
    )

    assert [record.path for record in result.records] == [Path("registry.json")]


def test_scan_generated_files_ignores_cache_and_git_directories(tmp_path):
    write_bytes(tmp_path / "docs" / "visible.json", 10)
    write_bytes(tmp_path / ".git" / "objects" / "large", 500)
    write_bytes(tmp_path / "docs" / "__pycache__" / "large.pyc", 500)

    result = check_generated_file_sizes.scan_generated_files(
        root=tmp_path,
        includes=["."],
        warn_bytes=100,
        fail_bytes=200,
    )

    assert [record.path for record in result.records] == [Path("docs/visible.json")]


def test_main_returns_failure_when_any_file_exceeds_limit(tmp_path, monkeypatch, capsys):
    write_bytes(tmp_path / "registry.json", 200)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "check_generated_file_sizes.py",
            "--root",
            str(tmp_path),
            "--include",
            "registry.json",
            "--warn-mib",
            "0.0001",
            "--fail-mib",
            "0.00015",
        ],
    )

    exit_code = check_generated_file_sizes.main()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Failures: 1 file(s)" in captured.out
