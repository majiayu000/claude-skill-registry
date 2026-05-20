import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_search_index  # noqa: E402
import rebuild_registry  # noqa: E402


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
    lite_data = json.loads((output_dir / "search-index-lite.json").read_text(encoding="utf-8"))
    search_pointer = json.loads((output_dir / "search-index.json").read_text(encoding="utf-8"))
    search_manifest = json.loads(
        (output_dir / "search-index-manifest.json").read_text(encoding="utf-8")
    )
    category_index = json.loads((output_dir / "categories" / "index.json").read_text(encoding="utf-8"))
    category_pointer = json.loads(
        (output_dir / "categories" / "development.json").read_text(encoding="utf-8")
    )
    category_manifest = json.loads(
        (output_dir / "categories" / "development" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    quality_pointer = json.loads((output_dir / "quality-index.json").read_text(encoding="utf-8"))
    quality_manifest = json.loads(
        (output_dir / "quality-index-manifest.json").read_text(encoding="utf-8")
    )
    quality_shard = json.loads(
        (output_dir / quality_manifest["shards"][0]["path"]).read_text(encoding="utf-8")
    )
    security_pointer = json.loads((output_dir / "security-index.json").read_text(encoding="utf-8"))
    security_manifest = json.loads(
        (output_dir / "security-index-manifest.json").read_text(encoding="utf-8")
    )
    security_shard = json.loads(
        (output_dir / security_manifest["shards"][0]["path"]).read_text(encoding="utf-8")
    )
    ranking_pointer = json.loads((output_dir / "ranking-index.json").read_text(encoding="utf-8"))
    ranking_manifest = json.loads(
        (output_dir / "ranking-index-manifest.json").read_text(encoding="utf-8")
    )
    ranking_shard = json.loads(
        (output_dir / ranking_manifest["shards"][0]["path"]).read_text(encoding="utf-8")
    )

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
    assert stats_data["lite_index_count"] == 1
    assert stats_data["lite_index_included_count"] == 1
    assert stats_data["search_shard_count"] == 1
    assert stats_data["category_shard_count"] == 1
    assert stats_data["quality_shard_count"] == 1
    assert stats_data["security_shard_count"] == 1
    assert stats_data["ranking_shard_count"] == 1
    assert stats_data["quality_largest_shard_bytes"] > 0
    assert stats_data["security_largest_shard_bytes"] > 0
    assert stats_data["ranking_largest_shard_bytes"] > 0
    assert stats_data["category_counts"] == [
        {"name": "development", "code": "dev", "count": 1}
    ]
    assert stats_data["unique_repo_count"] == 1
    assert stats_data["official_skill_count"] == 0
    assert stats_data["top_repositories"] == [{"repo": "owner/repo", "count": 1}]
    assert stats_data["largest_generated_file_bytes"] > 0
    assert search_pointer["deprecated_full_payload"] is True
    assert search_pointer["manifest"] == "search-index-manifest.json"
    assert "s" not in search_pointer
    assert search_manifest["shard_count"] == 1
    assert sum(shard["count"] for shard in search_manifest["shards"]) == 1
    assert category_index["categories"][0]["manifest"] == "categories/development/manifest.json"
    assert category_pointer["deprecated_full_payload"] is True
    assert category_pointer["manifest"] == "categories/development/manifest.json"
    assert "skills" not in category_pointer
    assert category_manifest["part_count"] == 1
    assert sum(part["count"] for part in category_manifest["parts"]) == 1
    assert lite_data["dedupe_key"] == "install|branch"
    assert lite_data["total_count"] == 1
    assert lite_data["included_count"] == 1
    assert lite_data["skills"][0]["id"]
    assert lite_data["skills"][0]["quality_grade"] in {"S", "A", "B", "C", "unknown", "blocked"}
    assert lite_data["skills"][0]["security_status"] == "unknown"
    assert quality_pointer["deprecated_full_payload"] is True
    assert quality_pointer["manifest"] == "quality-index-manifest.json"
    assert "records" not in quality_pointer
    assert quality_manifest["record_schema"] == "quality-v1"
    assert quality_manifest["shard_count"] == 1
    assert sum(shard["count"] for shard in quality_manifest["shards"]) == 1
    assert quality_shard["records"][0]["id"]
    assert security_pointer["deprecated_full_payload"] is True
    assert security_pointer["manifest"] == "security-index-manifest.json"
    assert "records" not in security_pointer
    assert security_manifest["record_schema"] == "security-v1"
    assert security_manifest["shard_count"] == 1
    assert sum(shard["count"] for shard in security_manifest["shards"]) == 1
    assert security_shard["records"][0]["security_status"] == "unknown"
    assert ranking_pointer["deprecated_full_payload"] is True
    assert ranking_pointer["manifest"] == "ranking-index-manifest.json"
    assert "records" not in ranking_pointer
    assert ranking_manifest["record_schema"] == "ranking-v1"
    assert ranking_manifest["shard_strategy"] == "bounded-sequential-score-desc"
    assert ranking_manifest["shard_count"] == 1
    assert sum(shard["count"] for shard in ranking_manifest["shards"]) == 1
    assert ranking_shard["records"][0]["recommended_score"] >= 0


def test_build_search_index_lite_dedupes_install_and_branch(tmp_path):
    output_dir = tmp_path / "docs"
    skills = [
        {
            "name": "demo-weak",
            "description": "short",
            "repo": "owner/repo",
            "path": "skills/demo/SKILL.md",
            "branch": "main",
            "category": "development",
            "tags": [],
            "stars": 1,
            "install": "owner/repo/skills/demo/SKILL.md",
            "source": "test",
        },
        {
            "name": "demo-strong",
            "description": "A much clearer description for the same install target with richer metadata.",
            "repo": "owner/repo",
            "path": "skills/demo/SKILL.md",
            "branch": "main",
            "category": "development",
            "tags": ["demo", "quality", "search"],
            "stars": 10,
            "install": "owner/repo/skills/demo/SKILL.md",
            "source": "test",
        },
    ]

    build_search_index.build_search_index(skills, output_dir, source_name="test-skills")

    lite_data = json.loads((output_dir / "search-index-lite.json").read_text(encoding="utf-8"))
    assert lite_data["raw_count"] == 2
    assert lite_data["total_count"] == 1
    assert lite_data["included_count"] == 1
    assert lite_data["skills"][0]["name"] == "demo-strong"


def test_build_search_index_removes_stale_category_and_search_parts(tmp_path):
    output_dir = tmp_path / "docs"
    stale_category_part = output_dir / "categories" / "other" / "part-999.json"
    stale_search_part = output_dir / "search-shards" / "part-999.json"
    stale_category_part.parent.mkdir(parents=True)
    stale_search_part.parent.mkdir(parents=True)
    stale_category_part.write_text("{}", encoding="utf-8")
    stale_search_part.write_text("{}", encoding="utf-8")

    build_search_index.build_search_index(
        [
            {
                "name": "demo",
                "description": "Demo skill with enough description for the index.",
                "repo": "owner/repo",
                "path": "skills/demo/SKILL.md",
                "branch": "main",
                "category": "development",
                "tags": ["demo"],
                "stars": 1,
                "install": "owner/repo/skills/demo/SKILL.md",
                "source": "test",
            }
        ],
        output_dir,
        source_name="test-skills",
    )

    assert not stale_category_part.exists()
    assert not stale_search_part.exists()
    assert (output_dir / "categories" / "development" / "part-000.json").exists()
    assert (output_dir / "search-shards" / "part-000.json").exists()


def test_build_search_index_lite_dedupe_uses_untruncated_description_length(tmp_path):
    output_dir = tmp_path / "docs"
    install = "owner/repo/skills/demo/SKILL.md"
    long_description = "a" * 240
    shorter_but_over_truncation = "b" * 181
    skills = [
        {
            "name": "demo-long",
            "description": long_description,
            "repo": "owner/repo",
            "path": "skills/demo/SKILL.md",
            "branch": "main",
            "category": "development",
            "tags": ["demo", "quality", "search"],
            "stars": 10,
            "install": install,
            "source": "test",
        },
        {
            "name": "demo-shorter",
            "description": shorter_but_over_truncation,
            "repo": "owner/repo",
            "path": "skills/demo/SKILL.md",
            "branch": "main",
            "category": "development",
            "tags": ["demo", "quality", "search"],
            "stars": 10,
            "install": install,
            "source": "test",
        },
    ]

    build_search_index.build_search_index(skills, output_dir, source_name="test-skills")

    lite_data = json.loads((output_dir / "search-index-lite.json").read_text(encoding="utf-8"))
    assert lite_data["total_count"] == 1
    assert lite_data["skills"][0]["name"] == "demo-long"
    assert "_description_length" not in lite_data["skills"][0]


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


def test_registry_shard_id_is_stable_for_install_and_branch():
    skill = {
        "name": "demo",
        "repo": "owner/repo",
        "path": "skills/demo/SKILL.md",
        "branch": "main",
    }

    assert rebuild_registry.registry_shard_id(skill) == rebuild_registry.registry_shard_id(skill)


def test_write_registry_shards_writes_manifest_entries_and_removes_stale(tmp_path):
    shards_dir = tmp_path / "registry-shards"
    shards_dir.mkdir()
    stale = shards_dir / "stale.json"
    stale.write_text("{}", encoding="utf-8")

    skills = [
        {
            "name": "alpha",
            "repo": "owner/repo",
            "path": "skills/alpha/SKILL.md",
            "branch": "main",
        },
        {
            "name": "beta",
            "repo": "owner/repo",
            "path": "skills/beta/SKILL.md",
            "branch": "main",
        },
    ]

    entries = rebuild_registry.write_registry_shards(
        skills,
        shards_dir,
        "2026-05-14T00:00:00Z",
    )

    assert not stale.exists()
    assert len(entries) == 256
    assert sum(entry["count"] for entry in entries) == 2
    assert all((tmp_path / entry["path"]).exists() for entry in entries)
    assert all((tmp_path / entry["gzip_path"]).exists() for entry in entries)
    assert all(entry["sha256"] for entry in entries)


def test_write_registry_shards_references_paths_from_manifest_location(tmp_path):
    manifest_dir = tmp_path / "published"
    shards_dir = manifest_dir / "registry-shards"
    skills = [
        {
            "name": "alpha",
            "repo": "owner/repo",
            "path": "skills/alpha/SKILL.md",
            "branch": "main",
        },
    ]

    entries = rebuild_registry.write_registry_shards(
        skills,
        shards_dir,
        "2026-05-14T00:00:00Z",
        reference_base=manifest_dir,
    )

    assert all(entry["path"].startswith("registry-shards/") for entry in entries)
    assert all(entry["gzip_path"].startswith("registry-shards/") for entry in entries)


def test_build_compatibility_registry_can_omit_manifest_pointer():
    registry = rebuild_registry.build_compatibility_registry(
        generated_at="2026-05-14T00:00:00Z",
        total_count=2,
        plugin_count=1,
        archive_skill_md_count_raw=3,
        archive_metadata_count_raw=3,
    )

    assert registry["total_count"] == 2
    assert registry["registry_skill_count_dedup"] == 2
    assert "manifest" not in registry
    assert registry["deprecated_full_payload"] is True
    assert "merged claude-skill-registry artifact" in registry["message"]
    assert "skills" not in registry


def test_build_compatibility_registry_points_to_manifest_without_skills():
    registry = rebuild_registry.build_compatibility_registry(
        generated_at="2026-05-14T00:00:00Z",
        total_count=2,
        plugin_count=1,
        archive_skill_md_count_raw=3,
        archive_metadata_count_raw=3,
        manifest_path="registry-manifest.json",
    )

    assert registry["total_count"] == 2
    assert registry["registry_skill_count_dedup"] == 2
    assert registry["manifest"] == "registry-manifest.json"
    assert registry["deprecated_full_payload"] is True
    assert "skills" not in registry


def test_rebuild_registry_accepts_absolute_manifest_output(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "development" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# demo\n\nDemo skill.", encoding="utf-8")
    (skill_dir / "metadata.json").write_text(
        json.dumps(
            {
                "name": "demo",
                "repo": "owner/repo",
                "github_path": "skills/demo",
                "github_branch": "main",
                "category": "development",
                "tags": ["demo"],
                "stars": 1,
                "source": "test",
            }
        ),
        encoding="utf-8",
    )
    registry_path = tmp_path / "registry.json"
    manifest_path = tmp_path / "artifacts" / "registry-manifest.json"
    shards_dir = tmp_path / "artifacts" / "registry-shards"

    subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "rebuild_registry.py"),
            "--skills-dir",
            str(skills_dir),
            "--registry",
            str(registry_path),
            "--manifest",
            str(manifest_path),
            "--shards-dir",
            str(shards_dir),
            "--skip-categories",
            "--compat-manifest-pointer",
        ],
        check=True,
        cwd=ROOT,
    )

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert registry["manifest"] == "artifacts/registry-manifest.json"
    assert manifest["shard_count"] == 256
    assert all(entry["path"].startswith("registry-shards/") for entry in manifest["shards"])


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
