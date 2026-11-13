"""Archives without redistribution approval keep metadata and a source link only."""

import asyncio
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import refresh_official_licenses  # noqa: E402
import withheld_archives  # noqa: E402
from build_search_index import build_search_index  # noqa: E402
from rebuild_registry import cleanup_orphan_metadata  # noqa: E402
from rebuild_registry import scan_skills as scan_registry_skills  # noqa: E402
from refresh_official_licenses import detect_license_text, refresh_archives  # noqa: E402
from search_sources import scan_skills_v2  # noqa: E402
from test_sync_and_download import FakeResponse, install_fake_aiohttp  # noqa: E402
from test_sync_and_download import load_module as load_sync_module  # noqa: E402

BODY = "# PDF\n\nUse this skill to work with PDF files.\n"
APACHE_TEXT = "                                 Apache License\n                           Version 2.0, January 2004\n"


def write_archive(root: Path, rel: str, metadata: dict, skill_text: str | None = None, extra=()):
    skill_dir = root / rel
    skill_dir.mkdir(parents=True)
    (skill_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
    if skill_text is not None:
        (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
    for name in extra:
        target = skill_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("support", encoding="utf-8")
    return skill_dir


def skill_md(license_line: str, description: str = "Work with PDF files.") -> str:
    return f"---\nname: pdf\ndescription: {description}\nlicense: {license_line}\n---\n\n{BODY}"


def restricted_metadata(repo: str = "brixtonpham/claude-config", **extra) -> dict:
    return {
        "name": "pdf", "repo": repo, "path": "skills/pdf/SKILL.md", "github_branch": "main",
        "category": "documents", "author": repo.split("/")[0],
        "source_url": f"https://github.com/{repo}/blob/main/skills/pdf/SKILL.md",
        "license": "NOASSERTION", "distribution": "restricted", **extra,
    }


def compatible_metadata(repo: str = "acme/skills", license_name: str = "MIT") -> dict:
    return {**restricted_metadata(repo), "license": license_name, "distribution": "compatible"}


def test_apply_removes_body_and_keeps_identity_metadata(tmp_path):
    withheld = write_archive(
        tmp_path, "documents/pdf-brixtonpham", restricted_metadata(bundled_files=["scripts/x.py"]),
        skill_md("Proprietary"), extra=("scripts/x.py", "LICENSE"),
    )
    kept = write_archive(tmp_path, "documents/pdf-acme", compatible_metadata(), skill_md("MIT"),
                         extra=("scripts/x.py",))
    gpl = write_archive(
        tmp_path, "documents/pdf-gpl",
        {**restricted_metadata("gnu/skills"), "license": "GPL-3.0"}, skill_md("GPL-3.0"),
        extra=("LICENSE",),
    )
    agpl = write_archive(tmp_path, "documents/pdf-agpl",
                         {**restricted_metadata("copyleft/skills"), "license": "AGPL-3.0"},
                         skill_md("AGPL-3.0"))
    spelled = write_archive(tmp_path, "documents/pdf-spelled",
                            {**restricted_metadata("acme/spelled"), "license": "BSD-3-Clause license"},
                            skill_md("BSD-3-Clause license"))
    noncommercial = write_archive(tmp_path, "documents/pdf-nc",
                                  {**restricted_metadata("acme/nc"), "license": "CC-BY-NC-4.0"},
                                  skill_md("CC-BY-NC-4.0"))

    assert withheld_archives.main(["--skills-dir", str(tmp_path), "--check"]) == 1
    assert withheld_archives.main(["--skills-dir", str(tmp_path), "--apply"]) == 0
    assert withheld_archives.main(["--skills-dir", str(tmp_path), "--check"]) == 0

    assert [p.name for p in withheld.iterdir()] == ["metadata.json"]
    metadata = json.loads((withheld / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["source_url"].startswith("https://github.com/brixtonpham/")
    assert metadata["content_fingerprint"] == withheld_archives.body_fingerprint(skill_md("x"))
    assert metadata["description"] == "Work with PDF files."
    assert metadata["bundled_files"] == []
    # Open-source licenses keep their files.
    assert (kept / "SKILL.md").exists() and (kept / "scripts" / "x.py").exists()
    assert (gpl / "SKILL.md").exists() and (gpl / "LICENSE").exists()
    # Copyleft and odd spellings of open-source licenses keep the body; NC does not.
    assert (agpl / "SKILL.md").exists() and (spelled / "SKILL.md").exists()
    assert [p.name for p in noncommercial.iterdir()] == ["metadata.json"]


def test_archive_without_legal_metadata_is_withheld(tmp_path):
    skill_dir = write_archive(tmp_path, "documents/pdf", {"name": "pdf", "repo": "anthropics/skills"},
                              skill_md("Proprietary"))
    withheld_archives.main(["--skills-dir", str(tmp_path), "--apply"])
    assert not (skill_dir / "SKILL.md").exists()


def test_unreadable_metadata_fails_instead_of_deleting(tmp_path):
    skill_dir = write_archive(tmp_path, "documents/pdf", {}, skill_md("MIT"))
    (skill_dir / "metadata.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        withheld_archives.main(["--skills-dir", str(tmp_path), "--apply"])
    assert (skill_dir / "SKILL.md").exists()


def test_withheld_archives_are_indexed_as_listings_and_survive_cleanup(tmp_path):
    write_archive(tmp_path, "documents/pdf-acme", compatible_metadata(), skill_md("MIT"))
    withheld = write_archive(tmp_path, "documents/pdf-brixtonpham", restricted_metadata(),
                             skill_md("Proprietary"))
    orphan = write_archive(tmp_path, "documents/orphan", compatible_metadata("acme/orphan"))
    withheld_archives.main(["--skills-dir", str(tmp_path), "--apply"])

    assert cleanup_orphan_metadata(tmp_path) == 1
    assert not (orphan / "metadata.json").exists()
    assert (withheld / "metadata.json").exists()

    registry = {record["repo"]: record for record in scan_registry_skills(tmp_path)}
    assert registry["brixtonpham/claude-config"]["tier"] == "listed"
    assert registry["brixtonpham/claude-config"]["description"] == "Work with PDF files."
    assert "tier" not in registry["acme/skills"]

    search = {record["repo"]: record for record in scan_skills_v2(tmp_path)}
    listed = search["brixtonpham/claude-config"]
    assert listed["tier"] == "listed" and listed["archive_path"] == ""
    # The stored fingerprint keeps the withheld copy grouped with the archived copy.
    assert listed["content_fingerprint"] == search["acme/skills"]["content_fingerprint"]


def test_official_count_and_primary_source_in_stats(tmp_path):
    output_dir = tmp_path / "docs"
    output_dir.mkdir()
    records = [
        {"name": "pdf", "description": "x" * 100, "repo": repo, "path": "skills/pdf/SKILL.md",
         "install": f"{repo}/skills/pdf/SKILL.md", "content_fingerprint": "f" * 64,
         "tags": [], "stars": stars, "license": license_name}
        for repo, stars, license_name in (
            ("moessimple/dotfiles", 0, "Proprietary"),
            ("anthropics/skills", 0, "Apache-2.0"),
            ("sundial-org/skills", 50, "MIT"),
        )
    ]
    records.append({"name": "other", "description": "y" * 100, "repo": "acme/other", "path": "",
                    "install": "acme/other", "tags": [], "stars": 1})
    build_search_index(records, output_dir)
    stats = json.loads((output_dir / "stats.json").read_text(encoding="utf-8"))
    assert stats["independent_skill_count"] == 2
    assert stats["official_skill_count"] == 1


class FakeUpstream:
    def __init__(self, files: dict[str, str]):
        self.files = files
        self.requested: list[str] = []

    def __call__(self, url: str):
        self.requested.append(url)
        prefix = "https://raw.githubusercontent.com/anthropics/skills/main/"
        return self.files.get(url.removeprefix(prefix))


def test_refresh_applies_upstream_license_and_current_file(tmp_path):
    official = restricted_metadata("anthropics/skills")
    current = write_archive(tmp_path, "documents/pdf-anthropics-skills-2", official,
                            skill_md("Proprietary. LICENSE.txt has complete terms"))
    old_text = skill_md("Proprietary").replace("PDF files.\n", "PDFs (old).\n")
    unattributed = {key: value for key, value in official.items() if key != "author"}
    older = write_archive(tmp_path, "documents/pdf-anthropics-skills", unattributed, old_text)
    bundled = write_archive(tmp_path, "documents/pdf", {**official, "bundled_files": ["scripts/x.py"]},
                            old_text, extra=("scripts/x.py",))
    third_party = write_archive(tmp_path, "documents/pdf-moessimple", restricted_metadata("moessimple/dotfiles"),
                                skill_md("Proprietary"))
    upstream_text = skill_md("Complete terms in LICENSE.txt")
    upstream = FakeUpstream({"skills/pdf/SKILL.md": upstream_text, "skills/pdf/LICENSE.txt": APACHE_TEXT})

    summary = refresh_archives(tmp_path, apply=True, fetch=upstream)

    assert summary["official"] == 3 and not summary["errors"]
    assert summary["updated"] == ["documents/pdf-anthropics-skills-2: NOASSERTION -> Apache-2.0"]
    assert summary["body_refreshed"] == ["documents/pdf-anthropics-skills: NOASSERTION -> Apache-2.0"]
    # A multi-file archive of an older version keeps the terms it was published under.
    assert summary["body_differs"] == ["documents/pdf"]
    for skill_dir in (current, older):
        refreshed = json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
        assert (refreshed["license"], refreshed["distribution"]) == ("Apache-2.0", "compatible")
    assert (current / "SKILL.md").read_text() == skill_md("Proprietary. LICENSE.txt has complete terms")
    assert (older / "SKILL.md").read_text() == upstream_text
    assert json.loads((older / "metadata.json").read_text())["downloaded_at"].endswith("Z")
    assert json.loads((older / "metadata.json").read_text())["author"] == "anthropics"
    assert json.loads((bundled / "metadata.json").read_text())["license"] == "NOASSERTION"
    assert json.loads((third_party / "metadata.json").read_text())["license"] == "NOASSERTION"
    assert not any("moessimple" in url for url in upstream.requested)
    # Refreshed official archives are redistributable; the stale multi-file one is withheld.
    withheld_archives.main(["--skills-dir", str(tmp_path), "--apply"])
    assert (current / "SKILL.md").exists() and (older / "SKILL.md").exists()
    assert [p.name for p in bundled.iterdir()] == ["metadata.json"]


def test_refresh_dry_run_writes_nothing_and_cli_fails_on_fetch_errors(tmp_path, monkeypatch, capsys):
    skill_dir = write_archive(tmp_path, "documents/pdf", restricted_metadata("anthropics/skills"),
                              skill_md("x").replace("PDF files.\n", "old\n"))
    before = {p.name: p.read_bytes() for p in skill_dir.iterdir()}
    upstream = FakeUpstream({"skills/pdf/SKILL.md": skill_md("Apache-2.0")})
    assert refresh_archives(tmp_path, apply=False, fetch=upstream)["body_refreshed"]
    assert {p.name: p.read_bytes() for p in skill_dir.iterdir()} == before

    def failing(url: str, timeout: int = 20):
        raise OSError("network down")

    monkeypatch.setattr(refresh_official_licenses, "fetch_raw", failing)
    assert refresh_official_licenses.main(["--skills-dir", str(tmp_path)]) == 1
    assert "could not be refreshed" in capsys.readouterr().err
    assert refresh_archives(tmp_path, apply=True, fetch=lambda url: None)["upstream_missing"] == [
        "documents/pdf"
    ]
    write_archive(tmp_path, "data/no-path", {"name": "x", "repo": "anthropics/skills", "path": 5})
    assert refresh_archives(tmp_path, apply=False, fetch=lambda url: None)["no_source_path"]


def test_detect_license_text():
    assert detect_license_text(APACHE_TEXT) == "Apache-2.0"
    assert detect_license_text(
        'Permission is hereby granted, free of charge, to any person\n... PROVIDED "AS IS"'
    ) == "MIT"
    assert detect_license_text("All rights reserved.") == ""


def test_unattributed_archive_loses_body_and_then_is_orphan_metadata(tmp_path):
    skill_dir = write_archive(tmp_path, "design/figure3d", {"name": "figure3d"}, skill_md("x"))
    withheld_archives.main(["--skills-dir", str(tmp_path), "--apply"])
    assert [p.name for p in skill_dir.iterdir()] == ["metadata.json"]
    assert scan_skills_v2(tmp_path) == [] and scan_registry_skills(tmp_path) == []
    assert cleanup_orphan_metadata(tmp_path) == 1


def test_sync_archives_metadata_only_and_never_readds_the_body(tmp_path, monkeypatch):
    module = load_sync_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    registry_path.write_text(json.dumps({"skills": [{
        "name": "demo", "repo": "acme/demo", "path": "SKILL.md", "category": "development",
        "license": "NOASSERTION", "distribution": "restricted",
    }]}), encoding="utf-8")
    install_fake_aiohttp(monkeypatch, {
        "https://raw.githubusercontent.com/acme/demo/main/SKILL.md": FakeResponse(
            200, text="---\nname: demo\ndescription: Restricted standalone skill.\n---\n# Demo\n",
        ),
        "https://api.github.com/repos/acme/demo/license": FakeResponse(404),
    })

    stats = asyncio.run(module.download_skills(registry_path, output_dir, manifest_path=None))

    assert stats["downloaded"] == 1
    [skill_dir] = output_dir.glob("development/*")
    assert [path.name for path in skill_dir.iterdir()] == ["metadata.json"]
    metadata = json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["source_url"] == "https://github.com/acme/demo/blob/main/SKILL.md"
    assert metadata["description"] == "Restricted standalone skill."
    assert metadata["content_fingerprint"]

    second = asyncio.run(module.download_skills(registry_path, output_dir, manifest_path=None))
    assert second["downloaded"] == 0
    assert [path.name for path in skill_dir.iterdir()] == ["metadata.json"]
    assert len(list(output_dir.glob("development/*"))) == 1
