import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_registry_summary  # noqa: E402


def test_build_registry_summary_uses_registry_total_and_plugin_source(tmp_path):
    registry_path = tmp_path / "registry.json"
    plugins_path = tmp_path / "plugins.json"

    registry_path.write_text(
        json.dumps(
            {
                "updated_at": "2026-03-31T00:00:00Z",
                "total_count": 107802,
            }
        ),
        encoding="utf-8",
    )
    plugins_path.write_text(
        json.dumps(
            {
                "plugins": [
                    {"name": "a"},
                    {"name": "b"},
                    {"name": "c"},
                ]
            }
        ),
        encoding="utf-8",
    )

    summary = build_registry_summary.build_registry_summary(registry_path, plugins_path)

    assert summary == {
        "schema_version": 1,
        "registry_updated_at": "2026-03-31T00:00:00Z",
        "total_count": 107802,
        "plugin_count": 3,
    }


def test_write_summary_writes_expected_json(tmp_path):
    output_path = tmp_path / "registry_summary.json"
    summary = {
        "schema_version": 1,
        "registry_updated_at": "2026-03-31T00:00:00Z",
        "total_count": 107802,
        "plugin_count": 3,
    }

    build_registry_summary.write_summary(output_path, summary)

    assert json.loads(output_path.read_text(encoding="utf-8")) == summary
