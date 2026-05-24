"""
Regression tests for ``scripts/utils.py``.

This module is the canonical home for cross-script invariants documented in
``AGENTS.md`` (case-conflict policy, repo-suffix fallback, deterministic paths)
and ``THIRD_PARTY_NOTICES.md`` (license normalization / classification).
A silent regression here corrupts the entire registry, so each rule below maps
to one or more named tests so reviewers can trace policy -> assertion.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest


def _load_utils():
    """Load ``scripts/utils.py`` fresh so the module-level ``_DIR_CACHE`` is reset."""
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    if "utils" in sys.modules:
        return importlib.reload(sys.modules["utils"])
    return importlib.import_module("utils")


@pytest.fixture
def utils():
    module = _load_utils()
    # Each test starts with a clean directory cache so prior runs do not leak.
    module._DIR_CACHE.clear()
    return module


# ---------------------------------------------------------------------------
# License normalization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("MIT", "MIT"),
        ("MIT License", "MIT"),
        ("mit license", "MIT"),
        ("Apache 2.0", "Apache-2.0"),
        ("Apache License 2.0", "Apache-2.0"),
        ("Apache License Version 2.0", "Apache-2.0"),
        ("BSD 2-Clause", "BSD-2-Clause"),
        ("BSD 3-Clause", "BSD-3-Clause"),
        ("CC-BY-NC-SA", "CC-BY-NC-SA-4.0"),
        ("CC BY-NC 4.0", "CC-BY-NC-4.0"),
        ("CC-BY-SA", "CC-BY-SA-4.0"),
        ("CC-BY", "CC-BY-4.0"),
    ],
)
def test_normalize_license_canonicalizes_known_aliases(utils, raw, expected):
    assert utils.normalize_license(raw) == expected


def test_normalize_license_maps_empty_to_noassertion(utils):
    assert utils.normalize_license("") == "NOASSERTION"
    assert utils.normalize_license("   ") == "NOASSERTION"
    assert utils.normalize_license(None) == "NOASSERTION"


def test_normalize_license_keeps_unknown_text_verbatim(utils):
    # Unrecognised licenses fall through unchanged so reviewers can spot them.
    assert utils.normalize_license("Custom Internal EULA") == "Custom Internal EULA"


# ---------------------------------------------------------------------------
# License classification
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "license_in,klass",
    [
        ("MIT", "compatible"),
        ("Apache-2.0", "compatible"),
        ("ISC", "compatible"),
        ("BSD-2-Clause", "compatible"),
        ("BSD-3-Clause", "compatible"),
        ("CC0-1.0", "compatible"),
        ("Unlicense", "compatible"),
        ("MIT-0", "compatible"),
        ("AGPL-3.0", "restricted"),
        ("GPL-3.0", "restricted"),
        ("LGPL-3.0", "restricted"),
        ("MPL-2.0", "restricted"),
        ("EUPL-1.2", "restricted"),
        ("CC-BY-NC-SA-4.0", "restricted"),
        ("CC-BY-NC-4.0", "restricted"),
        ("CC-BY-ND", "restricted"),
        ("PROPRIETARY", "restricted"),
        ("UNLICENSED", "restricted"),
        ("NOASSERTION", "restricted"),
        ("UNKNOWN", "restricted"),
        ("CC-BY-4.0", "restricted"),  # CC- non-permissive variants are restricted
        ("CC-BY-SA-4.0", "restricted"),
        ("Custom Vendor License", "unknown"),
    ],
)
def test_classify_license_partitions_known_families(utils, license_in, klass):
    assert utils.classify_license(license_in) == klass


def test_classify_license_falls_back_when_blank(utils):
    # Empty input normalizes to NOASSERTION, which must be restricted.
    assert utils.classify_license("") == "restricted"


# ---------------------------------------------------------------------------
# Repo / URL helpers
# ---------------------------------------------------------------------------


def test_normalize_repo_strips_https_prefix_and_slashes(utils):
    assert utils.normalize_repo("https://github.com/owner/repo") == "owner/repo"
    assert utils.normalize_repo("https://github.com/owner/repo/") == "owner/repo"
    assert utils.normalize_repo("/owner/repo/") == "owner/repo"
    assert utils.normalize_repo(" owner/repo ") == "owner/repo"
    assert utils.normalize_repo("") == ""
    assert utils.normalize_repo(None) == ""


def test_build_source_url_handles_repo_only_and_path(utils):
    assert (
        utils.build_source_url(repo="owner/repo")
        == "https://github.com/owner/repo"
    )
    assert (
        utils.build_source_url(repo="owner/repo", path="skills/demo")
        == "https://github.com/owner/repo/blob/main/skills/demo/SKILL.md"
    )
    # Already-pointed-at SKILL.md should not double-suffix.
    assert (
        utils.build_source_url(repo="owner/repo", path="skills/demo/SKILL.md")
        == "https://github.com/owner/repo/blob/main/skills/demo/SKILL.md"
    )
    assert (
        utils.build_source_url(repo="owner/repo", path="packs/core/skills/memory-protocol.md")
        == "https://github.com/owner/repo/blob/main/packs/core/skills/memory-protocol.md"
    )


def test_build_source_url_passthrough_for_external_url(utils):
    external = "https://example.com/raw/skill.md"
    assert utils.build_source_url(repo="owner/repo", path=external) == external


def test_build_source_url_uses_branch_argument(utils):
    assert (
        utils.build_source_url(repo="owner/repo", path="x", branch="develop")
        == "https://github.com/owner/repo/blob/develop/x/SKILL.md"
    )


def test_build_source_url_with_no_repo_returns_empty(utils):
    assert utils.build_source_url() == ""


def test_is_valid_https_url(utils):
    assert utils.is_valid_https_url("https://github.com/owner/repo")
    assert not utils.is_valid_https_url("http://example.com")
    assert not utils.is_valid_https_url("ftp://example.com")
    assert not utils.is_valid_https_url("github.com/owner/repo")
    assert not utils.is_valid_https_url("")
    assert not utils.is_valid_https_url(None)


# ---------------------------------------------------------------------------
# Author inference
# ---------------------------------------------------------------------------


def test_infer_author_prefers_explicit_value(utils):
    assert utils.infer_author(repo="ownerA/repoA", fallback="real human") == "real human"


@pytest.mark.parametrize(
    "placeholder", ["", "n/a", "NA", "None", "null", "TBD", "unknown", "  "]
)
def test_infer_author_drops_placeholders_in_favour_of_repo_owner(utils, placeholder):
    assert utils.infer_author(repo="ownerA/repoA", fallback=placeholder) == "ownerA"


def test_infer_author_when_repo_unknown(utils):
    assert utils.infer_author(repo="", fallback="") == "unknown"
    assert utils.infer_author(repo="bare-name-no-slash", fallback="") == "unknown"


# ---------------------------------------------------------------------------
# Legal metadata composition
# ---------------------------------------------------------------------------


def test_build_legal_metadata_compatible_path(utils):
    meta = utils.build_legal_metadata(
        repo="owner/repo", path="skills/demo", license_name="MIT"
    )
    assert meta["author"] == "owner"
    assert meta["license"] == "MIT"
    assert meta["license_class"] == "compatible"
    assert meta["distribution"] == "compatible"
    assert "Use according to upstream license" in meta["permission_note"]
    assert meta["source_url"].endswith("/skills/demo/SKILL.md")
    assert meta["copyright"].startswith("Copyright belongs to upstream")


def test_build_legal_metadata_restricted_for_gpl(utils):
    meta = utils.build_legal_metadata(repo="owner/repo", license_name="GPL-3.0")
    assert meta["license_class"] == "restricted"
    assert meta["distribution"] == "restricted"
    assert "Restricted or unknown license" in meta["permission_note"]


def test_build_legal_metadata_explicit_overrides_win(utils):
    meta = utils.build_legal_metadata(
        repo="owner/repo",
        license_name="MIT",
        author="Specific Author",
        copyright_text="(c) 2026 Specific Author",
        permission_note="Custom note",
        distribution="restricted",
        source_url="https://example.com/foo",
    )
    assert meta["author"] == "Specific Author"
    assert meta["copyright"] == "(c) 2026 Specific Author"
    assert meta["permission_note"] == "Custom note"
    assert meta["distribution"] == "restricted"
    assert meta["source_url"] == "https://example.com/foo"


def test_build_legal_metadata_unknown_license_treated_as_restricted(utils):
    meta = utils.build_legal_metadata(repo="owner/repo", license_name="Vendor EULA")
    assert meta["license_class"] == "unknown"
    # Unknown -> restricted in distribution per the comment in source.
    assert meta["distribution"] == "restricted"


# ---------------------------------------------------------------------------
# Name / category normalization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Architect", "architect"),
        ("LangChain", "langchain"),
        ("Go-to-Market-Planner", "go-to-market-planner"),
        ("My Skill Name", "my-skill-name"),
        ("__leading-and-trailing__", "leading-and-trailing"),
        ("multiple   spaces", "multiple-spaces"),
        ("Mixed.Case_With.Punc!", "mixed-case-with-punc"),
    ],
)
def test_normalize_name_examples_from_docstring(utils, raw, expected):
    assert utils.normalize_name(raw) == expected


def test_normalize_name_empty_inputs_become_unknown(utils):
    assert utils.normalize_name("") == "unknown"
    assert utils.normalize_name(None) == "unknown"
    assert utils.normalize_name("---") == "unknown"


def test_normalize_name_truncates_to_64_chars(utils):
    long_name = "a" * 100
    out = utils.normalize_name(long_name)
    assert out == "a" * 64
    assert len(out) <= 64


def test_normalize_category_truncates_to_32_chars(utils):
    long_cat = "category-" + "x" * 100
    out = utils.normalize_category(long_cat)
    assert len(out) <= 32


def test_normalize_category_empty(utils):
    assert utils.normalize_category("") == "other"
    assert utils.normalize_category(None) == "other"


def test_normalize_category_keeps_legacy_aliases_for_review(utils):
    assert utils.normalize_category("Engineering") == "engineering"
    assert utils.normalize_category("dev") == "dev"


# ---------------------------------------------------------------------------
# Repo suffix and dir-name builder (AGENTS.md case-conflict policy)
# ---------------------------------------------------------------------------


def test_get_repo_suffix_basic(utils):
    assert utils.get_repo_suffix("owner/repo") == "owner-repo"
    assert utils.get_repo_suffix("https://github.com/Owner/Repo") == "owner-repo"
    assert utils.get_repo_suffix("") == ""
    assert utils.get_repo_suffix("just-owner") == ""


def test_get_repo_suffix_truncates_long_components(utils):
    # AGENTS.md says owner and repo each capped at 20 chars.
    long_owner = "x" * 50
    long_repo = "y" * 50
    suffix = utils.get_repo_suffix(f"{long_owner}/{long_repo}")
    owner_part, repo_part = suffix.split("-", 1)
    assert len(owner_part) <= 20
    assert len(repo_part) <= 20


def test_build_dir_name_uses_repo_suffix(utils):
    assert utils.build_dir_name("My Skill", repo="owner/repo") == "my-skill-owner-repo"
    assert utils.build_dir_name("plain-skill") == "plain-skill"


def test_build_skill_key_priority(utils):
    # Per implementation: repo+path > repo+name > repo+category > repo > category:name > "".
    assert utils.build_skill_key(repo="o/r", path="x/y") == "o/r:x/y"
    assert utils.build_skill_key(repo="o/r") == "o/r"
    assert utils.build_skill_key(repo="o/r", path=".", name="foo") == "o/r:foo"
    assert utils.build_skill_key(repo="o/r", path="SKILL.md", name="foo") == "o/r:foo"
    assert utils.build_skill_key(repo="o/r", path="./SKILL.md", name="foo") == "o/r:foo"
    assert utils.build_skill_key(repo="o/r", category="dev") == "o/r:dev"
    assert utils.build_skill_key(category="dev", name="foo") == "dev:foo"
    assert utils.build_skill_key() == ""
    # path alone is ignored once repo is missing — the category:name fallback wins.
    assert utils.build_skill_key(path="x/y", name="foo") == ":foo"


def test_build_skill_key_coerces_non_string_repo_and_path(utils):
    assert utils.build_skill_key(repo="o/r", path=123) == "o/r:123"
    assert utils.build_skill_key(repo=123, path="x/y") == "123:x/y"
    assert utils.build_skill_key(repo="o/r", path={"bad": "path"}) == "o/r:{'bad': 'path'}"


def test_build_skill_key_treats_boolean_repo_and_path_as_missing(utils):
    assert utils.build_skill_key(repo="o/r", path=False) == "o/r"
    assert utils.build_skill_key(repo="o/r", path=True) == "o/r"
    assert utils.build_skill_key(repo="o/r", path=False, name="foo") == "o/r:foo"
    assert utils.build_skill_key(repo=False, path="x/y", category="dev", name="foo") == "dev:foo"


def test_iter_source_skills_inherits_top_level_repo(utils):
    source = {
        "repo": "anthropics/skills",
        "skills": [{"name": "docx", "path": "skills/docx"}],
    }
    rows = list(utils.iter_source_skills(source))
    assert rows == [{"name": "docx", "path": "skills/docx", "repo": "anthropics/skills"}]


def test_iter_source_skills_keeps_row_repo(utils):
    source = {
        "repo": "anthropics/skills",
        "skills": [{"name": "custom", "repo": "owner/repo", "path": "skills/custom"}],
    }
    rows = list(utils.iter_source_skills(source))
    assert rows[0]["repo"] == "owner/repo"


def test_short_hash_is_deterministic_and_8_hex(utils):
    out = utils.short_hash("hello")
    assert len(out) == 8
    assert all(c in "0123456789abcdef" for c in out)
    assert out == utils.short_hash("hello")
    assert out != utils.short_hash("hello!")


# ---------------------------------------------------------------------------
# ensure_unique_dir: case-insensitive uniqueness rules from AGENTS.md
# ---------------------------------------------------------------------------


def test_ensure_unique_dir_no_conflict(utils, tmp_path):
    target = utils.ensure_unique_dir(tmp_path, "my-skill")
    assert target == tmp_path / "my-skill"


def test_ensure_unique_dir_case_conflict_uses_repo_suffix(utils, tmp_path):
    (tmp_path / "MY-SKILL").mkdir()
    # Force fresh scan since the cached state from a previous test could interfere.
    utils._DIR_CACHE.clear()
    target = utils.ensure_unique_dir(tmp_path, "my-skill", repo="owner/repo")
    assert target.name == "my-skill-owner-repo"


def test_ensure_unique_dir_falls_back_to_short_hash_without_repo(utils, tmp_path):
    (tmp_path / "MY-SKILL").mkdir()
    utils._DIR_CACHE.clear()
    target = utils.ensure_unique_dir(tmp_path, "my-skill", key="key-1")
    assert target.name.startswith("my-skill-")
    suffix = target.name[len("my-skill-") :]
    assert len(suffix) == 8
    assert all(c in "0123456789abcdef" for c in suffix)


def test_ensure_unique_dir_appends_numeric_when_suffix_already_taken(utils, tmp_path):
    (tmp_path / "my-skill").mkdir()
    (tmp_path / "my-skill-owner-repo").mkdir()
    utils._DIR_CACHE.clear()
    target = utils.ensure_unique_dir(tmp_path, "my-skill", repo="owner/repo")
    assert target.name == "my-skill-owner-repo-2"


def test_ensure_unique_dir_reuses_dir_with_matching_metadata_key(utils, tmp_path):
    existing = tmp_path / "my-skill"
    existing.mkdir()
    (existing / "metadata.json").write_text(
        json.dumps({"repo": "owner/repo", "path": "skills/demo"}),
        encoding="utf-8",
    )
    utils._DIR_CACHE.clear()
    target = utils.ensure_unique_dir(
        tmp_path, "completely-different-name", key="owner/repo:skills/demo"
    )
    assert target == existing


def test_ensure_unique_dir_creates_parent_when_missing(utils, tmp_path):
    nested = tmp_path / "does" / "not" / "exist-yet"
    target = utils.ensure_unique_dir(nested, "thing")
    assert target.parent == nested
    assert nested.exists()


# ---------------------------------------------------------------------------
# Frontmatter / description / metadata IO
# ---------------------------------------------------------------------------


def test_extract_frontmatter_valid(utils):
    content = """---
name: demo
description: Some demo skill.
tags:
  - a
  - b
---

# Demo
Body content.
"""
    fm = utils.extract_frontmatter(content)
    assert fm == {"name": "demo", "description": "Some demo skill.", "tags": ["a", "b"]}


def test_extract_frontmatter_returns_empty_for_no_frontmatter(utils):
    assert utils.extract_frontmatter("# Just a heading") == {}
    assert utils.extract_frontmatter("") == {}


def test_extract_frontmatter_returns_empty_for_unterminated(utils):
    assert utils.extract_frontmatter("---\nname: demo\n") == {}


def test_extract_frontmatter_returns_empty_for_invalid_yaml(utils):
    bad = "---\n: : : not yaml\n  -broken\n---\nbody"
    assert utils.extract_frontmatter(bad) == {}


def test_extract_frontmatter_returns_empty_for_non_mapping(utils):
    # A YAML scalar / list at top level is not a mapping and must coerce to {}.
    bad = "---\n- item-1\n- item-2\n---\nbody"
    assert utils.extract_frontmatter(bad) == {}


def test_extract_description_prefers_frontmatter(utils):
    content = "---\ndescription: From frontmatter\n---\n\nFirst body paragraph here."
    assert utils.extract_description(content) == "From frontmatter"


def test_extract_description_falls_back_to_first_paragraph(utils):
    content = (
        "---\nname: demo\n---\n\n# Heading\n\n"
        "This is the first real body paragraph that exceeds twenty characters.\n"
    )
    desc = utils.extract_description(content)
    assert desc.startswith("This is the first real body")


def test_extract_description_strips_markdown_links(utils):
    content = (
        "---\nname: demo\n---\n\n"
        "See [the manual](https://example.com) for more details about this skill.\n"
    )
    desc = utils.extract_description(content)
    assert "https://example.com" not in desc
    assert "the manual" in desc


def test_extract_description_skips_short_lines_and_fence_openers(utils):
    # extract_description only filters lines that *start with* ``` and lines
    # under 20 chars; it does not understand fenced-block scope. The content
    # below verifies that contract: short lines and the fence opener itself
    # are skipped, then the first long body line is picked.
    content = (
        "---\nname: demo\n---\n\n"
        "short\n"
        "```\n"
        "This actually has more than twenty characters in it for sure.\n"
    )
    desc = utils.extract_description(content)
    assert desc.startswith("This actually has more than twenty characters")


def test_extract_description_truncates_at_max_length(utils):
    body = "x" * 500
    content = f"---\ndescription: {body}\n---\n"
    desc = utils.extract_description(content, max_length=100)
    assert len(desc) == 100


def test_skill_semantic_fields_prefer_frontmatter(utils, tmp_path):
    skill_dir = tmp_path / "skill-c"
    skill_dir.mkdir()
    content = (
        "---\n"
        "name: frontmatter-name\n"
        "description: Docker Kubernetes CI CD deploy infrastructure workflow.\n"
        "tags:\n"
        "  - docker\n"
        "  - kubernetes\n"
        "---\n"
    )
    frontmatter = utils.extract_frontmatter(content)
    metadata = {
        "name": "metadata-name",
        "description": "",
        "tags": ["metadata-tag"],
    }

    fields = utils.skill_semantic_fields(
        skill_dir,
        metadata=metadata,
        frontmatter=frontmatter,
        rel=Path("other/skill-c/SKILL.md"),
        content=content,
    )

    assert fields["name"] == "frontmatter-name"
    assert fields["description"].startswith("Docker Kubernetes")
    assert fields["tags"] == ["docker", "kubernetes"]
    assert fields["sources"]["name"] == "frontmatter"
    assert fields["sources"]["description"] == "frontmatter"
    assert fields["sources"]["tags"] == "frontmatter:list"
    assert "metadata-tag" not in fields["text"]


def test_load_metadata_returns_dict_or_empty(utils, tmp_path):
    skill_dir = tmp_path / "skill-a"
    skill_dir.mkdir()
    # Missing metadata.json -> {}.
    assert utils.load_metadata(skill_dir) == {}

    (skill_dir / "metadata.json").write_text('{"name": "a"}', encoding="utf-8")
    assert utils.load_metadata(skill_dir) == {"name": "a"}

    (skill_dir / "metadata.json").write_text("not json", encoding="utf-8")
    # Corrupt files must not crash callers.
    assert utils.load_metadata(skill_dir) == {}


def test_write_metadata_round_trip(utils, tmp_path):
    skill_dir = tmp_path / "skill-b"
    skill_dir.mkdir()
    payload = {"name": "demo", "tags": ["a", "b"], "stars": 7}
    utils.write_metadata(skill_dir, payload)
    assert utils.load_metadata(skill_dir) == payload
    raw = (skill_dir / "metadata.json").read_text(encoding="utf-8")
    # Pretty-printed for human review (indent=2).
    assert "  " in raw


# ---------------------------------------------------------------------------
# Category guessing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "snippet,expected",
    [
        ("React component testing with playwright", "testing"),
        ("Deploy to Kubernetes via Docker and CI/CD", "devops"),
        ("Audit OWASP vulnerabilities", "security"),
        ("Convert PDF and DOCX to markdown", "documents"),
        ("CSS animation in Figma frontend UI", "design"),
        ("Backlog roadmap and PRD for product", "product"),
    ],
)
def test_guess_category_picks_dominant_keyword_family(utils, snippet, expected):
    assert utils.guess_category(snippet) == expected


def test_guess_category_returns_other_when_no_match(utils):
    assert utils.guess_category("entirely-unrelated-mumble-jumble") == "other"
