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
    build_static_skill_pages,
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
        "security_status": "passed",
        "install_status": "known_good",
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

    assert len(selected) == 20
    assert [item["name"] for item in selected] == [
        f"safe-{index}" for index in range(24, 4, -1)
    ]


def test_slug_is_stable_readable_and_collision_safe():
    first = skill("C++ Review", id="stable-one")
    second = skill("C++ Review", id="stable-two")

    assert skill_page_slug(first) == "c-review-stable-o"
    assert skill_page_slug(first) == skill_page_slug(dict(first))
    assert skill_page_slug(second) == "c-review-stable-t"


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

    assert summary == {"generated_count": 1, "slugs": [slug]}
    assert "<script>" not in detail
    assert "&lt;script&gt;" in detail
    assert "&lt;tag&gt;" in detail
    assert f'href="skills/{slug}/"' in homepage
    assert locations == [PUBLIC_SITE, f"{PUBLIC_SITE}skills/{slug}/"]
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


def test_generator_refuses_to_replace_an_unowned_skills_directory(tmp_path):
    output_dir = tmp_path / "docs"
    manual = output_dir / "skills" / "manual" / "index.html"
    manual.parent.mkdir(parents=True)
    manual.write_text("manual", encoding="utf-8")

    with pytest.raises(ValueError, match="not marked as generated"):
        build_static_skill_pages([skill("current")], output_dir)

    assert manual.read_text(encoding="utf-8") == "manual"
