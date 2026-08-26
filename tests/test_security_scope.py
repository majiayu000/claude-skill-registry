from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from resolve_security_scope import _git_paths  # noqa: E402
from resolve_security_scope import main as resolve_scope_main  # noqa: E402
from security_scope import (  # noqa: E402
    SecurityScopeError,
    resolve_scan_file_list,
    resolve_scan_paths,
)


def _skill_tree(tmp_path: Path) -> Path:
    skills = tmp_path / "skills"
    skill = skills / "development" / "demo"
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: demo\ndescription: Demo.\n---\n", encoding="utf-8")
    (skill / "references" / "notes.md").write_text("notes\n", encoding="utf-8")
    return skills


@pytest.mark.parametrize("delimiter", [b"\n", b"\0"])
def test_resolve_scan_file_list_supports_safe_delimiters(tmp_path, delimiter):
    skills = _skill_tree(tmp_path)
    file_list = tmp_path / "paths.bin"
    file_list.write_bytes(delimiter.join([b"development/demo/references/notes.md", b""]))

    selected = resolve_scan_file_list(skills, file_list, fail_unmapped=True)

    assert selected == [skills / "development" / "demo" / "SKILL.md"]


def test_resolve_scan_paths_fails_on_unmapped_change(tmp_path):
    skills = _skill_tree(tmp_path)
    (skills / "orphan.txt").write_text("orphan\n", encoding="utf-8")

    with pytest.raises(SecurityScopeError, match="no owning SKILL.md"):
        resolve_scan_paths(skills, ["orphan.txt"], fail_unmapped=True)


def test_resolve_scan_paths_rejects_symlink(tmp_path):
    skills = _skill_tree(tmp_path)
    target = tmp_path / "outside.txt"
    target.write_text("outside\n", encoding="utf-8")
    link = skills / "development" / "demo" / "references" / "linked.txt"
    link.symlink_to(target)

    with pytest.raises(SecurityScopeError, match="symlink"):
        resolve_scan_paths(
            skills,
            ["development/demo/references/linked.txt"],
            fail_unmapped=True,
        )


def test_git_scope_includes_type_changes_and_quarantines_symlink(tmp_path):
    skills = _skill_tree(tmp_path)
    subprocess.run(["git", "init", "-q", str(skills)], check=True)
    subprocess.run(["git", "-C", str(skills), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(skills),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "-qm",
            "baseline",
        ],
        check=True,
    )
    changed = skills / "development" / "demo" / "references" / "notes.md"
    changed.unlink()
    changed.symlink_to(tmp_path / "outside.txt")

    paths = _git_paths(skills)

    assert "development/demo/references/notes.md" in paths
    with pytest.raises(SecurityScopeError, match="symlink"):
        resolve_scan_paths(skills, paths, fail_unmapped=True)


def test_resolve_scope_main_writes_full_target_list(monkeypatch, tmp_path, capsys):
    skills = _skill_tree(tmp_path)
    output = tmp_path / "targets.bin"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "resolve_security_scope.py",
            "--skills-dir",
            str(skills),
            "--mode",
            "full",
            "--output",
            str(output),
        ],
    )

    assert resolve_scope_main() == 0
    assert output.read_bytes() == b"development/demo/SKILL.md\0"
    assert capsys.readouterr().out == "1\n"
