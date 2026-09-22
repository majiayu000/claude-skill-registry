from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("check_clamav_report")


SIGNATURE = "Img.Phishing.SvgJsPhishing-10044283-0"


def _write_report(path: Path, *findings: str) -> None:
    lines = [
        "-------------------------------------------------------------------------------",
        *findings,
        "",
        "----------- SCAN SUMMARY -----------",
        "Known viruses: 3628071",
        f"Infected files: {len(findings)}",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_exceptions(path: Path, *entries: dict) -> None:
    path.write_text(json.dumps({"exceptions": list(entries)}, indent=2), encoding="utf-8")


def _run(module, tmp_path: Path, monkeypatch, report: Path, exceptions: Path) -> int:
    monkeypatch.setattr(
        sys,
        "argv",
        ["check_clamav_report.py", "--report", str(report), "--exceptions", str(exceptions)],
    )
    return module.main()


def test_clean_report_passes(tmp_path, monkeypatch, capsys):
    module = _load_module()
    report = tmp_path / "clamav-report.txt"
    _write_report(report)
    exceptions = tmp_path / "clamav-exceptions.json"
    _write_exceptions(exceptions)

    assert _run(module, tmp_path, monkeypatch, report, exceptions) == 0
    assert "0 total" in capsys.readouterr().out


def test_reviewed_finding_passes_and_reports_its_reason(tmp_path, monkeypatch, capsys):
    module = _load_module()
    report = tmp_path / "clamav-report.txt"
    _write_report(report, f"skills/devops/web-xss-stored/SKILL.md: {SIGNATURE} FOUND")
    exceptions = tmp_path / "clamav-exceptions.json"
    _write_exceptions(
        exceptions,
        {
            "path": "skills/devops/web-xss-stored/SKILL.md",
            "signature": SIGNATURE,
            "reason": "Quoted XSS payloads in a pentest teaching note.",
        },
    )

    assert _run(module, tmp_path, monkeypatch, report, exceptions) == 0
    output = capsys.readouterr().out
    assert "Reviewed ClamAV exception" in output
    assert "Quoted XSS payloads in a pentest teaching note." in output


def test_unreviewed_finding_fails_and_names_the_file(tmp_path, monkeypatch, capsys):
    module = _load_module()
    report = tmp_path / "clamav-report.txt"
    _write_report(report, "skills/other/dropper/SKILL.md: Win.Trojan.Agent-1 FOUND")
    exceptions = tmp_path / "clamav-exceptions.json"
    _write_exceptions(exceptions)

    assert _run(module, tmp_path, monkeypatch, report, exceptions) == 1
    output = capsys.readouterr().out
    assert "Unreviewed ClamAV finding: skills/other/dropper/SKILL.md: Win.Trojan.Agent-1" in output


def test_new_signature_on_a_reviewed_path_still_fails(tmp_path, monkeypatch):
    module = _load_module()
    report = tmp_path / "clamav-report.txt"
    _write_report(report, "skills/devops/web-xss-stored/SKILL.md: Win.Trojan.Agent-1 FOUND")
    exceptions = tmp_path / "clamav-exceptions.json"
    _write_exceptions(
        exceptions,
        {
            "path": "skills/devops/web-xss-stored/SKILL.md",
            "signature": SIGNATURE,
            "reason": "Quoted XSS payloads in a pentest teaching note.",
        },
    )

    assert _run(module, tmp_path, monkeypatch, report, exceptions) == 1


def test_exception_paths_accept_globs_for_renamed_archive_directories(tmp_path, monkeypatch):
    module = _load_module()
    report = tmp_path / "clamav-report.txt"
    _write_report(
        report,
        f"skills/devops/web-xss-stored-ajtazer-heckit/SKILL.md: {SIGNATURE} FOUND",
    )
    exceptions = tmp_path / "clamav-exceptions.json"
    _write_exceptions(
        exceptions,
        {
            "path": "skills/devops/web-xss-stored*/SKILL.md",
            "signature": SIGNATURE,
            "reason": "Quoted XSS payloads in a pentest teaching note.",
        },
    )

    assert _run(module, tmp_path, monkeypatch, report, exceptions) == 0


def test_missing_report_fails_closed(tmp_path, monkeypatch, capsys):
    module = _load_module()
    exceptions = tmp_path / "clamav-exceptions.json"
    _write_exceptions(exceptions)

    assert _run(module, tmp_path, monkeypatch, tmp_path / "absent.txt", exceptions) == 1
    assert "ClamAV report is missing" in capsys.readouterr().out


def test_exception_entry_without_a_reason_fails_closed(tmp_path, monkeypatch, capsys):
    module = _load_module()
    report = tmp_path / "clamav-report.txt"
    _write_report(report, f"skills/devops/web-xss-stored/SKILL.md: {SIGNATURE} FOUND")
    exceptions = tmp_path / "clamav-exceptions.json"
    _write_exceptions(
        exceptions,
        {"path": "skills/devops/web-xss-stored/SKILL.md", "signature": SIGNATURE},
    )

    assert _run(module, tmp_path, monkeypatch, report, exceptions) == 1
    assert "Unusable ClamAV exception list" in capsys.readouterr().out


def test_repository_exception_list_is_usable(tmp_path, monkeypatch):
    module = _load_module()
    exceptions = Path(__file__).resolve().parents[1] / module.DEFAULT_EXCEPTIONS
    entries = module.load_exceptions(exceptions)

    assert entries
    finding = module.Finding("skills/devops/web-xss-stored/SKILL.md", SIGNATURE)
    assert module.matching_exception(finding, entries) is not None
