import json
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
        raw_skill_count=1,
        dedup_skill_count=1,
    )

    stats_data = json.loads((output_dir / "stats.json").read_text(encoding="utf-8"))

    assert "plugins" in plugins_data
    assert "collections" not in plugins_data
    assert stats["total_plugins"] == 1
    assert stats_data["total_plugins"] == 1
    assert "total_collections" not in stats_data


def test_utc_helpers_keep_trailing_z_suffix():
    assert build_search_index.utc_now_isoformat().endswith("Z")
    assert rebuild_registry.utc_now_isoformat().endswith("Z")
