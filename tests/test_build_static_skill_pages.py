import re
import sys
from pathlib import Path
from xml.etree import ElementTree

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from build_static_skill_pages import (  # noqa: E402
    PUBLIC_SITE,
    _meta_description,
    _source_url,
    attach_security_scans,
    build_static_skill_pages,
    group_skill_copies,
    select_featured_skills,
    skill_page_slug,
)


def skill(name: str, **overrides):
    record = {
        "id": f"stable-{name}",
        "name": name,
        "description": f"Use {name} to complete a focused workflow.",
        "repo": "acme/skills",
        "path": f"skills/{name}",
        "branch": "main",
        "category": "development",
        "tags": ["testing", "agent"],
        "stars": 10,
        "install": f"acme/skills/skills/{name}",
        "quality_grade": "A",
        "quality_score": 75,
        "security_status": "passed",
        "install_status": "known_good",
        "security_scan": {
            "scanner_version": "1.1.6",
            "ruleset_sha256": "a" * 64,
            "scanned_at": "2026-10-15T03:00:00Z",
            "content_sha256": "b" * 64,
            "checks": ["frontmatter", "dangerous_patterns", "credentials"],
            "finding_types": {},
        },
    }
    record.update(overrides)
    return record


def homepage_template() -> str:
    return """<!doctype html>
<html><body>
<!-- static-featured:start -->
<p>Generated during the index build.</p>
<!-- static-featured:end -->
</body></html>
"""


def test_selection_is_bounded_and_excludes_unsafe_or_uninstallable_skills():
    records = [skill(f"safe-{index}", stars=index) for index in range(25)]
    records.extend(
        [
            skill("unsafe", security_status="failed", stars=1000),
            skill("unknown", security_status="unknown", stars=999),
            skill("broken", install_status="broken", stars=998),
            skill("no-repo", repo="", stars=997),
        ]
    )

    selected = select_featured_skills(records)

    assert len(selected) == 25
    assert [item["name"] for item in selected] == [
        f"safe-{index}" for index in range(24, -1, -1)
    ]


def test_slug_is_stable_readable_and_collision_safe():
    first = skill("C++ Review", id="stable-one")
    second = skill("C++ Review", id="stable-two")

    assert skill_page_slug(first).startswith("c-review-")
    assert skill_page_slug(first) == skill_page_slug(dict(first))
    assert skill_page_slug(second) != skill_page_slug(first)


def test_generator_escapes_metadata_and_writes_homepage_links_and_sitemap(tmp_path):
    output_dir = tmp_path / "docs"
    output_dir.mkdir()
    (output_dir / "index.html").write_text(homepage_template(), encoding="utf-8")
    record = skill(
        "unsafe-looking <name>",
        id="escape-id",
        description='A <script>alert("x")</script> description.',
        tags=["<tag>", "safe"],
    )

    summary = build_static_skill_pages([record], output_dir)

    slug = skill_page_slug(record)
    detail_path = output_dir / "skills" / slug / "index.html"
    detail = detail_path.read_text(encoding="utf-8")
    homepage = (output_dir / "index.html").read_text(encoding="utf-8")
    sitemap = ElementTree.parse(output_dir / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [
        node.text for node in sitemap.findall("sm:url/sm:loc", namespace)
    ]

    assert summary == {"generated_count": 1, "slugs": [slug], "pinned_count": 0, "history_count": 0}
    assert "<script>alert" not in detail
    assert detail.count("<script") == 2
    assert '<script defer src="../../js/analytics.js"></script>' in detail
    assert 'type="application/ld+json"' in detail
    assert "&lt;script&gt;" in detail
    assert "&lt;tag&gt;" in detail
    assert f'href="skills/{slug}/"' in homepage
    assert locations == [
        PUBLIC_SITE,
        f"{PUBLIC_SITE}choose-a-skill.html",
        f"{PUBLIC_SITE}skills/",
        f"{PUBLIC_SITE}skills/category/development/",
        f"{PUBLIC_SITE}skills/{slug}/",
    ]
    assert re.search(r'<link rel="canonical" href="[^\"]+/">', detail)


def test_generator_removes_only_stale_generated_skill_pages(tmp_path):
    output_dir = tmp_path / "docs"
    stale = output_dir / "skills" / "old-skill" / "index.html"
    stale.parent.mkdir(parents=True)
    stale.write_text("stale", encoding="utf-8")
    (output_dir / "skills" / ".generated-static-skill-pages").write_text(
        "generated\n", encoding="utf-8"
    )
    keep = output_dir / "manual.txt"
    keep.write_text("keep", encoding="utf-8")

    build_static_skill_pages([skill("current")], output_dir)

    assert not stale.exists()
    assert keep.read_text(encoding="utf-8") == "keep"


def test_generator_includes_code_review_guide_in_regenerated_sitemap(tmp_path):
    output_dir = tmp_path / "docs"
    guide_path = output_dir / "guides" / "code-review.html"
    guide_path.parent.mkdir(parents=True)
    guide = (ROOT / "docs" / "guides" / "code-review.html").read_bytes()
    guide_path.write_bytes(guide)
    guide_url = f"{PUBLIC_SITE}guides/code-review.html"
    (output_dir / "sitemap.xml").write_text(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"<url><loc>{guide_url}</loc></url></urlset>",
        encoding="utf-8",
    )
    record = skill("current")

    for _ in range(2):
        build_static_skill_pages([record], output_dir)

        sitemap = ElementTree.parse(output_dir / "sitemap.xml")
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locations = [node.text for node in sitemap.findall("sm:url/sm:loc", namespace)]
        assert locations == [
            PUBLIC_SITE,
            f"{PUBLIC_SITE}choose-a-skill.html",
            f"{PUBLIC_SITE}skills/",
            f"{PUBLIC_SITE}skills/category/development/",
            f"{PUBLIC_SITE}skills/{skill_page_slug(record)}/",
            guide_url,
        ]
        assert guide_path.read_bytes() == guide


def test_generator_refuses_to_replace_an_unowned_skills_directory(tmp_path):
    output_dir = tmp_path / "docs"
    manual = output_dir / "skills" / "manual" / "index.html"
    manual.parent.mkdir(parents=True)
    manual.write_text("manual", encoding="utf-8")

    with pytest.raises(ValueError, match="not marked as generated"):
        build_static_skill_pages([skill("current")], output_dir)

    assert manual.read_text(encoding="utf-8") == "manual"


def test_copy_identity_uses_content_not_shared_description():
    first = skill("review", content_fingerprint="a" * 64, repo="acme/one", install="acme/one")
    copy = skill("review", content_fingerprint="a" * 64, repo="acme/two", install="acme/two", stars=200)
    other = skill("review", content_fingerprint="b" * 64, repo="acme/three", install="acme/three")
    groups = group_skill_copies([first, copy, other])
    assert len(groups) == 2
    copied = next(group for group in groups if group["repository_count"] == 2)
    assert {item["repo"] for item in copied["copies"]} == {"acme/one", "acme/two"}
    changed = group_skill_copies([dict(first, stars=1000), copy])[0]
    assert changed["page_slug"] == copied["page_slug"]
    assert group_skill_copies([copy, first, other]) == groups


def test_selection_quality_and_first_wave_limit():
    records = [skill(f"safe-{i}", id=f"id-{i}", quality_score=80) for i in range(5810)]
    records += [skill("thin", description="Short"), skill("poor", quality_score=60)]
    selected = select_featured_skills(records)
    assert len(selected) == 5800
    assert not {"thin", "poor"}.intersection(record["name"] for record in selected)


def test_representative_branch_ties_are_order_independent():
    first = skill("review", content_fingerprint="same", branch="main")
    second = dict(first, branch="next")
    assert group_skill_copies([first, second]) == group_skill_copies([second, first])


def test_static_detail_lists_every_matching_source(tmp_path):
    copies = [skill("review", repo=f"acme/source-{index}", install=f"acme/source-{index}/review",
                    content_fingerprint="same", branch="next") for index in range(12)]
    [group] = group_skill_copies(copies)
    build_static_skill_pages([group], tmp_path)
    detail = (tmp_path / "skills" / group["page_slug"] / "index.html").read_text()
    assert "Found in 12 repositories" in detail
    for copy in copies:
        assert copy["install"] in detail
    assert "(next)" in detail


@pytest.mark.parametrize("path", ["", "skills/review", "skills/review/SKILL.md", "SKILL.md"])
def test_source_links_handle_file_and_directory_paths(path):
    record = skill("review", repo="acme/repo", path=path, branch="feature/next")
    directory = "skills/review" if path.startswith("skills/review") else ""
    expected_base = "https://github.com/acme/repo"
    assert _source_url(record) == f"{expected_base}/blob/feature%2Fnext/{directory + '/' if directory else ''}SKILL.md"
    assert _source_url(record, directory=True) == f"{expected_base}/tree/feature%2Fnext{('/' + directory) if directory else ''}"


def test_page_attribution_related_guides_and_archive_entrypoints(tmp_path):
    docs = tmp_path / "docs"
    archive = tmp_path / "archive"
    (archive / "development").mkdir(parents=True)
    records = group_skill_copies([skill("one", license="MIT", author="Acme"), skill("two")])
    build_static_skill_pages(records, docs, archive)
    detail = (docs / "skills" / records[0]["page_slug"] / "index.html").read_text()
    assert "MIT" in detail and "Acme" in detail
    assert "Trust score" in detail
    assert "Copies with matching content" in detail
    assert "removal-request.yml" in detail
    assert "npx skills add" in detail
    assert "sk install" not in detail
    assert 'class="related"' in detail
    assert (docs / "skills" / "index.html").is_file()
    assert PUBLIC_SITE in (archive / "development" / "README.md").read_text()


def test_duplicate_slugs_do_not_destroy_previous_output(tmp_path):
    docs = tmp_path / "docs"
    build_static_skill_pages([skill("keep")], docs)
    old = docs / "skills" / skill_page_slug(skill("keep")) / "index.html"
    with pytest.raises(ValueError, match="Duplicate"):
        build_static_skill_pages([skill("bad"), skill("bad")], docs)
    assert old.is_file()


def test_empty_catalog_and_invalid_homepage(tmp_path):
    docs = tmp_path / "docs"
    assert build_static_skill_pages([], docs)["generated_count"] == 0
    assert "Browse skill guides" in (docs / "skills" / "index.html").read_text()
    (docs / "index.html").write_text("manual homepage")
    with pytest.raises(ValueError, match="static featured block"):
        build_static_skill_pages([skill("one")], docs)


def test_cli_uses_catalog_and_rejects_invalid_payload(tmp_path, monkeypatch, capsys):
    import json

    from build_static_skill_pages import main

    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"skills": group_skill_copies([skill("cli")])}))
    monkeypatch.setattr(sys, "argv", ["build-pages", "--catalog", str(catalog), "--output", str(tmp_path / "docs")])
    assert main() == 0
    assert "Generated 1" in capsys.readouterr().out
    catalog.write_text('{"skills":null}')
    with pytest.raises(ValueError, match="Catalog artifact"):
        main()


def test_install_command_quotes_source_arguments(tmp_path):
    import html
    import shlex
    record = skill("quoted", path="skills/a space; touch /tmp/unsafe", branch="feat/space $(id)")
    build_static_skill_pages([record], tmp_path)
    detail = (tmp_path / "skills" / skill_page_slug(record) / "index.html").read_text()
    command = html.unescape(re.search(r"<code>(.*?)</code>", detail).group(1))
    args = shlex.split(command)
    assert args[:3] == ["npx", "skills", "add"]
    assert len(args) == 4
    assert args[3] == "acme/skills/skills/a space; touch /tmp/unsafe#feat%2Fspace%20%24%28id%29"
    assert "--branch" not in command


def test_unknown_license_is_explained_and_copy_paths_are_distinct(tmp_path):
    first = skill("copies", repo="acme/repo", install="acme/repo/skills/copies", content_fingerprint="x", license="NOASSERTION")
    second = skill("copies", repo="acme/repo", install="acme/repo/.claude/skills/copies", content_fingerprint="x", license="NOASSERTION")
    records = group_skill_copies([first, second])
    build_static_skill_pages(records, tmp_path)
    detail = (tmp_path / "skills" / records[0]["page_slug"] / "index.html").read_text()
    assert "NOASSERTION" not in detail
    assert "Not declared in registry metadata" in detail
    assert "acme/repo/skills/copies" in detail
    assert "acme/repo/.claude/skills/copies" in detail


def test_guide_explains_registry_scan_checks_and_findings(tmp_path):
    scan = dict(skill("x")["security_scan"], finding_types={"warning:sensitive_path": 2, "warning:schema_validation": 1})
    record = skill("scanned", security_scan=scan)

    build_static_skill_pages([record], tmp_path)
    detail = (tmp_path / "skills" / skill_page_slug(record) / "index.html").read_text(encoding="utf-8")

    assert "<h2>What the registry checked</h2>" in detail
    assert "Scanned 2026-10-15 by registry scanner 1.1.6" in detail
    assert f"ruleset <code>{'a' * 12}</code>" in detail
    assert "<li>Frontmatter and schema</li><li>Dangerous code patterns</li><li>Hardcoded credentials</li>" in detail
    assert "3 warnings: schema validation (1), sensitive path (2)." in detail


def test_guide_reports_clean_scan_without_inventing_findings(tmp_path):
    record = skill("clean")

    build_static_skill_pages([record], tmp_path)
    detail = (tmp_path / "skills" / skill_page_slug(record) / "index.html").read_text(encoding="utf-8")

    assert "<strong>Findings:</strong> Nothing was flagged." in detail


@pytest.mark.parametrize("scan", [None, {"scanner_version": "1.1.6"}, dict(skill("x")["security_scan"], checks=["made_up"])])
def test_guide_fails_without_valid_scan_evidence(tmp_path, scan):
    record = skill("missing-scan", security_scan=scan)

    with pytest.raises(ValueError, match="security"):
        build_static_skill_pages([record], tmp_path)


def test_attach_security_scans_copies_decision_summary_only():
    decision = {
        "id": "decision",
        "scanner": {"name": "scanner", "version": "1.1.6", "ruleset_sha256": "r" * 64},
        "provenance": {"scanned_at": "2026-10-15T03:00:00Z", "content_sha256": "c" * 64, "source_url": "x"},
        "checks": ["frontmatter"],
        "finding_types": {"warning:prompt_injection": 1},
    }
    records = attach_security_scans([{"id": "one"}, {"id": "two"}], {"one": {"security_decision": decision}, "two": {}})

    assert records[0]["security_scan"] == {
        "scanner_version": "1.1.6",
        "ruleset_sha256": "r" * 64,
        "scanned_at": "2026-10-15T03:00:00Z",
        "content_sha256": "c" * 64,
        "checks": ["frontmatter"],
        "finding_types": {"warning:prompt_injection": 1},
    }
    assert "security_scan" not in records[1]


def test_install_lists_runtime_targets_and_author_badge(tmp_path):
    import html
    import shlex

    from build_static_skill_pages import BADGE_URL, RUNTIME_TARGETS

    record = skill("portable")
    build_static_skill_pages([record], tmp_path)
    slug = skill_page_slug(record)
    detail = (tmp_path / "skills" / slug / "index.html").read_text()
    blocks = [html.unescape(block) for block in re.findall(r"<code>(.*?)</code>", detail, re.S)]
    source = "acme/skills/skills/portable#main"
    commands = [shlex.split(line) for line in blocks[1].splitlines() if not line.startswith("#")]
    assert commands == [["npx", "skills", "add", source, "-g", "-a", agent] for _, agent, _ in RUNTIME_TARGETS]
    for label, _, path in RUNTIME_TARGETS:
        assert f"# {label} → {path}" in blocks[1]
    assert f"[![Listed on Claude Skills Registry]({BADGE_URL})]({PUBLIC_SITE})" in blocks
    assert (ROOT / "docs" / "assets" / "listed-badge.svg").is_file()


def test_unrepresentable_cli_path_uses_manual_install(tmp_path):
    record = skill("hash-path", path="skills/C# helper")
    build_static_skill_pages([record], tmp_path)
    detail = (tmp_path / "skills" / skill_page_slug(record) / "index.html").read_text()
    assert "npx skills add" not in detail
    assert "copy the folder containing SKILL.md" in detail
    assert "/skills/C%23%20helper/SKILL.md" in detail


def test_badge_target_survives_content_and_selection_changes(tmp_path):
    import html

    from build_static_skill_pages import BADGE_URL
    record = skill("badge", content_fingerprint="before")
    badge = f"[![Listed on Claude Skills Registry]({BADGE_URL})]({PUBLIC_SITE})"
    for fingerprint in ("before", "after"):
        record["page_identity"] = fingerprint
        build_static_skill_pages([record], tmp_path)
        page = tmp_path / "skills" / skill_page_slug(record) / "index.html"
        assert badge in html.unescape(page.read_text())
    build_static_skill_pages([], tmp_path)
    assert badge.endswith(f"]({PUBLIC_SITE})")


def pinned(**overrides):
    pin = {
        "status": "pinned", "repo": "acme/skills", "commit": "c" * 40, "path": "skills/pdf tools/SKILL.md",
        "name": "pdf-tools", "description": "Extract text from PDFs.", "digest": "sha256:" + "d" * 64,
    }
    pin.update(overrides)
    return pin


def test_pinned_guides_publish_a_discovery_index_and_verified_install(tmp_path):
    import hashlib
    import json

    from build_static_skill_pages import DISCOVERY_SCHEMA

    record = skill("pdf", archive_path="data/pdf/SKILL.md")
    archive = tmp_path / "archive"
    source = archive / record["archive_path"]
    source.parent.mkdir(parents=True)
    source.write_bytes(b"current scanned content")
    digest = "sha256:" + hashlib.sha256(source.read_bytes()).hexdigest()
    summary = build_static_skill_pages([record], tmp_path, install_pins={record["id"]: pinned(archive_path=record["archive_path"], digest=digest)}, archive_source=archive)
    slug = skill_page_slug(record)
    index = json.loads((tmp_path / "skills" / slug / ".well-known" / "agent-skills" / "index.json").read_text())
    detail = (tmp_path / "skills" / slug / "index.html").read_text()

    assert summary["pinned_count"] == 1
    assert index == {"$schema": DISCOVERY_SCHEMA, "skills": [{
        "name": "pdf-tools", "type": "skill-md", "description": "Extract text from PDFs.",
        "url": "https://raw.githubusercontent.com/acme/skills/" + "c" * 40 + "/skills/pdf%20tools/SKILL.md",
        "digest": digest,
    }]}
    assert f"npx skills add {PUBLIC_SITE}skills/{slug}/" in detail
    assert "at commit cccccccccccc" in detail


@pytest.mark.parametrize("case", ["changed", "missing", "no_archive", "wrong_archive_path", "outside_archive"])
def test_stale_install_pins_are_not_published(tmp_path, case):
    import hashlib

    record = skill("pdf", archive_path="data/pdf/SKILL.md")
    archive = tmp_path / "archive"
    source = archive / record["archive_path"]
    source.parent.mkdir(parents=True)
    source.write_bytes(b"current scanned content")
    pin = pinned(archive_path=record["archive_path"], digest="sha256:" + hashlib.sha256(source.read_bytes()).hexdigest())
    if case == "changed":
        source.write_bytes(b"new archived version with the same stable id")
    elif case == "missing":
        source.unlink()
    elif case == "wrong_archive_path":
        pin["archive_path"] = "data/other/SKILL.md"
    elif case == "outside_archive":
        record["archive_path"] = pin["archive_path"] = "../outside/SKILL.md"
    output = tmp_path / "docs"
    summary = build_static_skill_pages([record], output, install_pins={record["id"]: pin},
                                      archive_source=None if case == "no_archive" else archive)
    detail = output / "skills" / skill_page_slug(record)
    assert summary["pinned_count"] == 0
    assert not (detail / ".well-known").exists()
    assert "Verified install" not in (detail / "index.html").read_text()
    assert "npx skills add" in (detail / "index.html").read_text()


@pytest.mark.parametrize("pins", [None, {}, {"stable-pdf": pinned(status="upstream_changed")}])
def test_unpinned_guides_keep_source_install_only(tmp_path, pins):
    record = skill("pdf")
    summary = build_static_skill_pages([record], tmp_path, install_pins=pins)
    slug = skill_page_slug(record)
    detail = (tmp_path / "skills" / slug / "index.html").read_text()
    assert summary["pinned_count"] == 0
    assert not (tmp_path / "skills" / slug / ".well-known").exists()
    assert "Verified install" not in detail
    import html
    assert "npx skills add 'acme/skills/skills/pdf#main'" in html.unescape(detail)


def test_cli_rejects_install_pin_file_without_pins_map(tmp_path, monkeypatch):
    import json

    from build_static_skill_pages import main

    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"skills": [skill("cli")]}))
    pins = tmp_path / "install-pins.json"
    pins.write_text('{"pins": []}')
    monkeypatch.setattr(sys, "argv", ["build-pages", "--catalog", str(catalog), "--output", str(tmp_path / "docs"),
                                      "--install-pins", str(pins)])
    with pytest.raises(ValueError, match="pins map"):
        main()


def history_entry(status, first, last, **extra):
    return {"status": status, "first_seen": first, "last_seen": last, "digest": "sha256:" + "a" * 64, **extra}


def test_guide_shows_content_history_and_flags_upstream_change(tmp_path):
    record = skill("pdf")
    history = {record["id"]: [
        history_entry("pinned", "2026-10-17T00:00:00+00:00", "2026-10-18T00:00:00+00:00", repo="acme/skills",
                      commit="c" * 40, path="skills/pdf/SKILL.md", files={"SKILL.md": "sha256:x", "run.sh": "sha256:y"}),
        history_entry("upstream_changed", "2026-10-19T00:00:00+00:00", "2026-10-19T00:00:00+00:00", repo="<script>"),
    ]}

    summary = build_static_skill_pages([record], tmp_path, content_history=history)
    detail = (tmp_path / "skills" / skill_page_slug(record) / "index.html").read_text()

    assert summary["history_count"] == 1
    assert "<h2>Content history</h2>" in detail
    assert "no longer matches the version the registry scanned (change detected 2026-10-19)" in detail
    assert detail.index("2026-10-19</span> Author&#x27;s current file differs") < detail.index("2026-10-17 → 2026-10-18")
    assert f'commit <a href="https://raw.githubusercontent.com/acme/skills/{"c" * 40}/skills/pdf/SKILL.md">cccccccccccc</a>' in detail
    assert "sha256:aaaaaaaaaaaa · 2 files" in detail
    assert "<script>" not in detail


def test_guide_without_history_has_no_history_section(tmp_path):
    record = skill("pdf")
    pinned_only = {record["id"]: [history_entry("pinned", "2026-10-17T00:00:00+00:00", "2026-10-17T00:00:00+00:00")]}
    for history, expected in ((None, False), ({"other": []}, False), (pinned_only, True)):
        build_static_skill_pages([record], tmp_path, content_history=history)
        detail = (tmp_path / "skills" / skill_page_slug(record) / "index.html").read_text()
        assert ("Content history" in detail) is expected
        assert "no longer matches" not in detail
        # A pinned entry without upstream coordinates must not render a dangling commit label.
        assert "at commit" not in detail


def test_cli_reads_content_history_and_rejects_invalid_schema(tmp_path, monkeypatch, capsys):
    import json

    from build_static_skill_pages import main

    record = skill("cli")
    catalog = tmp_path / "catalog.json"
    catalog.write_text(json.dumps({"skills": [record]}))
    history = tmp_path / "skill-content-history.json"
    history.write_text(json.dumps({"schema_version": 1, "skills": {record["id"]: [
        history_entry("pinned", "2026-10-17T00:00:00+00:00", "2026-10-17T00:00:00+00:00")]}}))
    argv = ["build-pages", "--catalog", str(catalog), "--output", str(tmp_path / "docs"), "--content-history", str(history)]
    monkeypatch.setattr(sys, "argv", argv)
    assert main() == 0
    assert "1 with content history" in capsys.readouterr().out
    history.write_text('{"schema_version": 1, "skills": []}')
    with pytest.raises(ValueError, match="Content history artifact"):
        main()


def test_guide_jsonld_breadcrumb_star_and_unique_description(tmp_path):
    import json

    record = skill("pdf", description="A" * 180 + " tail", category="Design Tools")
    build_static_skill_pages([record], tmp_path)
    slug = skill_page_slug(record)
    detail = (tmp_path / "skills" / slug / "index.html").read_text()
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', detail)
    payload = json.loads(match.group(1))
    types = {node["@type"] for node in payload["@graph"]}
    description = re.search(r'<meta name="description" content="([^"]*)"', detail).group(1)

    assert types == {"SoftwareSourceCode", "BreadcrumbList"}
    assert payload["@graph"][0]["codeRepository"].endswith("/SKILL.md")
    assert payload["@graph"][1]["itemListElement"][-1]["item"].endswith(f"/skills/{slug}/")
    assert 'href="../category/design-tools/"' in detail
    assert "Star on GitHub" in detail
    assert 'id="install"' in detail
    assert "Verified install" not in detail
    assert len(description) <= 160
    assert description.endswith("Install pdf for Claude Code.")
    assert (tmp_path / "skills" / "category" / "design-tools" / "index.html").is_file()


def test_meta_description_keeps_complete_first_sentence_before_install_text():
    record = skill(
        "frontend-design",
        description=(
            "Create distinctive, production-grade frontend interfaces with high design quality. "
            "Use this skill when the user asks to build web pages."
        ),
    )

    description = _meta_description(record)

    assert description == (
        "Create distinctive, production-grade frontend interfaces with high design quality. "
        "Install frontend-design for Claude Code."
    )


def test_sitemap_lastmod_uses_history_then_scan_date(tmp_path):
    record = skill("pdf")
    history = {record["id"]: [
        history_entry("pinned", "2026-10-17T00:00:00+00:00", "2026-10-19T00:00:00+00:00"),
        history_entry("upstream_changed", "not-a-date", "2026-13-40T00:00:00+00:00"),
    ]}
    build_static_skill_pages([record], tmp_path, content_history=history)
    sitemap = ElementTree.parse(tmp_path / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    by_loc = {
        node.find("sm:loc", namespace).text: node.find("sm:lastmod", namespace)
        for node in sitemap.findall("sm:url", namespace)
    }
    slug = skill_page_slug(record)
    assert by_loc[f"{PUBLIC_SITE}skills/{slug}/"].text == "2026-10-19"
    assert by_loc[f"{PUBLIC_SITE}skills/category/development/"].text == "2026-10-19"
    assert by_loc[PUBLIC_SITE] is None

    scan_only = skill("scan-only")
    build_static_skill_pages([scan_only], tmp_path)
    sitemap = ElementTree.parse(tmp_path / "sitemap.xml")
    by_loc = {
        node.find("sm:loc", namespace).text: node.find("sm:lastmod", namespace).text
        for node in sitemap.findall("sm:url", namespace)
        if node.find("sm:lastmod", namespace) is not None
    }
    assert by_loc[f"{PUBLIC_SITE}skills/{skill_page_slug(scan_only)}/"] == "2026-10-15"


def test_archive_readme_links_category_hub_and_guide_pages(tmp_path):
    docs = tmp_path / "docs"
    archive = tmp_path / "archive"
    (archive / "development").mkdir(parents=True)
    (archive / "notes").mkdir()
    records = [skill("pdf", archive_path="development/pdf/SKILL.md"), skill("other", category="notes")]
    build_static_skill_pages(records, docs, archive)
    readme = (archive / "development" / "README.md").read_text()
    notes = (archive / "notes" / "README.md").read_text()
    pdf_url = f"{PUBLIC_SITE}skills/{skill_page_slug(records[0])}/"

    assert f"{PUBLIC_SITE}skills/category/development/" in readme
    assert pdf_url in readme
    assert "Star the registry on GitHub" in readme
    assert "Search and install skills" in readme
    assert f"{PUBLIC_SITE}skills/category/notes/" in notes
    assert "removal-request.yml" in readme
