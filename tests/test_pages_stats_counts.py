from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STALE_DISPLAY_COUNT = "67" + ",000"
STALE_PLAIN_COUNT = "67" + "000"


def test_pages_shell_does_not_hardcode_stale_skill_count():
    pages_files = [
        ROOT / "docs" / "index.html",
        ROOT / "docs" / "js" / "app.js",
    ]

    for path in pages_files:
        text = path.read_text(encoding="utf-8")
        assert STALE_DISPLAY_COUNT not in text
        assert STALE_PLAIN_COUNT not in text


def test_homepage_uses_neutral_count_fallback_until_stats_loads():
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Search <span id=\"total-count\">skills</span> for Claude Code" in html
    assert "Search and discover Claude Code skills" in html


def test_pages_app_renders_visible_count_from_stats_json():
    app_js = (ROOT / "docs" / "js" / "app.js").read_text(encoding="utf-8")

    assert "registry_skill_count_dedup" in app_js
    assert "archive_skill_md_count_raw" in app_js
    assert "updateRegistryCountDisplay" in app_js
    assert "document.title" in app_js
    assert "metaDescription" in app_js
