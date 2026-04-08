import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_search_index  # noqa: E402
import rebuild_registry  # noqa: E402
import update_data_readme  # noqa: E402


def test_load_plugins_reads_plugins_source(tmp_path):
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    plugins_path = sources_dir / "plugins.json"
    plugins_path.write_text(
        json.dumps(
            {
                "plugins": [
                    {
                        "name": "demo-plugin",
                        "description": "Demo plugin for testing",
                        "repo": "owner/repo",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    plugins = rebuild_registry.load_plugins(sources_dir)

    assert len(plugins) == 1
    assert plugins[0]["name"] == "demo-plugin"


def test_build_plugins_index_and_stats_use_plugin_keys(tmp_path):
    output_dir = tmp_path / "docs"
    plugins = [
        {
            "name": "demo-plugin",
            "description": "Demo plugin for testing",
            "repo": "owner/repo",
            "skills": ["demo-skill"],
            "commands": ["/demo:run"],
            "hooks": ["pre-tool-use"],
        }
    ]
    skills = [
        {
            "name": "demo-skill",
            "description": "Demo skill",
            "repo": "owner/repo",
            "path": "plugins/demo-plugin/skills/demo-skill/SKILL.md",
            "branch": "main",
            "category": "development",
            "tags": ["demo"],
            "stars": 1,
            "install": "owner/repo/plugins/demo-plugin/skills/demo-skill/SKILL.md",
            "source": "test",
        }
    ]

    build_search_index.build_plugins_index(plugins, output_dir)
    plugins_data = json.loads((output_dir / "plugins.json").read_text(encoding="utf-8"))
    stats = build_search_index.build_search_index(
        skills,
        output_dir,
        source_name="test-skills",
        archive_skill_md_count_raw=1,
        archive_metadata_count_raw=1,
        registry_skill_count_dedup=1,
    )

    stats_data = json.loads((output_dir / "stats.json").read_text(encoding="utf-8"))

    assert "plugins" in plugins_data
    assert "collections" not in plugins_data
    assert stats["total_plugins"] == 1
    assert stats_data["total_plugins"] == 1
    assert stats_data["archive_skill_md_count_raw"] == 1
    assert stats_data["archive_metadata_count_raw"] == 1
    assert stats_data["indexed_skill_count_scan_shape"] == 1
    assert stats_data["registry_skill_count_dedup"] == 1
    assert "total_skills" not in stats_data
    assert "raw_skill_count" not in stats_data
    assert "dedup_skill_count" not in stats_data
    assert "total_collections" not in stats_data


def test_utc_helpers_keep_trailing_z_suffix():
    assert build_search_index.utc_now_isoformat().endswith("Z")
    assert rebuild_registry.utc_now_isoformat().endswith("Z")


def test_scan_skills_v2_is_recursive_and_metadata_optional(tmp_path):
    skills_dir = tmp_path / "skills"

    nested_dir = skills_dir / "other" / "deep" / "skill-alpha"
    nested_dir.mkdir(parents=True)
    (nested_dir / "SKILL.md").write_text("# alpha", encoding="utf-8")

    flat_dir = skills_dir / "development" / "skill-beta"
    flat_dir.mkdir(parents=True)
    (flat_dir / "SKILL.md").write_text("# beta", encoding="utf-8")
    (flat_dir / "metadata.json").write_text(
        json.dumps(
            {
                "name": "beta",
                "repo": "owner/repo",
                "github_path": "skills/skill-beta",
                "github_branch": "main",
                "category": "development",
                "tags": ["dev"],
                "stars": 7,
                "source": "test",
            }
        ),
        encoding="utf-8",
    )

    records = build_search_index.scan_skills_v2(skills_dir)

    assert len(records) == 2
    by_dir = {r["dir_name"]: r for r in records}
    assert "skill-alpha" in by_dir
    assert "skill-beta" in by_dir
    assert by_dir["skill-alpha"]["category"] == "other"
    assert by_dir["skill-beta"]["category"] == "development"


def test_rebuild_registry_omits_derived_and_empty_optional_fields(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "development" / "skill-beta"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# beta", encoding="utf-8")
    (skill_dir / "metadata.json").write_text(
        json.dumps(
            {
                "name": "beta",
                "repo": "owner/repo",
                "github_path": "skills/skill-beta",
                "github_branch": "main",
                "category": "development",
                "tags": ["dev"],
                "stars": 7,
                "source": "test",
                "author": "",
                "source_url": "",
                "license": "",
                "distribution": "",
                "permission_note": "",
            }
        ),
        encoding="utf-8",
    )

    [record] = rebuild_registry.scan_skills(skills_dir)

    assert record["name"] == "beta"
    assert record["repo"] == "owner/repo"
    assert record["path"] == "skills/skill-beta"
    assert "install" not in record
    assert "author" not in record
    assert "source_url" not in record
    assert "license" not in record
    assert "distribution" not in record
    assert "permission_note" not in record


def test_load_from_registry_reconstructs_install_without_embedded_install_field(tmp_path):
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {"name": "repo-path", "repo": "owner/repo", "path": "skills/repo-path"},
                    {"name": "repo-only", "repo": "owner/repo"},
                    {"name": "path-only", "path": "skills/path-only"},
                    {"name": "name-only"},
                ]
            }
        ),
        encoding="utf-8",
    )

    skills = build_search_index.load_from_registry(registry_path)

    assert [s["install"] for s in skills] == [
        "owner/repo/skills/repo-path",
        "owner/repo",
        "local/skills/path-only",
        "local/name-only",
    ]


def test_safe_write_registry_writes_compact_json(tmp_path):
    registry_path = tmp_path / "registry.json"

    assert rebuild_registry.safe_write_registry(
        registry_path,
        {"skills": [{"name": "demo", "repo": "owner/repo"}]},
    )

    content = registry_path.read_text(encoding="utf-8")
    assert content == '{"skills":[{"name":"demo","repo":"owner/repo"}]}'


def test_cleanup_orphan_metadata_removes_only_orphans(tmp_path):
    skills_dir = tmp_path / "skills"
    good_dir = skills_dir / "data" / "good-skill"
    orphan_dir = skills_dir / "data" / "orphan-meta"
    good_dir.mkdir(parents=True)
    orphan_dir.mkdir(parents=True)

    (good_dir / "SKILL.md").write_text("# good", encoding="utf-8")
    (good_dir / "metadata.json").write_text("{}", encoding="utf-8")
    orphan_meta = orphan_dir / "metadata.json"
    orphan_meta.write_text("{}", encoding="utf-8")

    removed = rebuild_registry.cleanup_orphan_metadata(skills_dir)

    assert removed == 1
    assert (good_dir / "metadata.json").exists()
    assert not orphan_meta.exists()


def test_update_data_readme_rewrites_archive_count_and_date(tmp_path):
    archive_dir = tmp_path / "archive"
    skill_a = archive_dir / "development" / "skill-a"
    skill_b = archive_dir / "docs" / "skill-b"
    skill_a.mkdir(parents=True)
    skill_b.mkdir(parents=True)
    (skill_a / "SKILL.md").write_text("# a", encoding="utf-8")
    (skill_b / "SKILL.md").write_text("# b", encoding="utf-8")

    readme = tmp_path / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# Claude Skill Registry (Data)",
                "",
                "**Archive size**",
                "- **162,170** `SKILL.md` files (as of 2026-02-05)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    changed = update_data_readme.update_readme(
        readme,
        archive_dir,
        as_of_date="2026-04-08",
    )

    updated = readme.read_text(encoding="utf-8")
    assert changed is True
    assert "- **2** `SKILL.md` files (as of 2026-04-08)" in updated
