import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"


def load_script(script_name: str):
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))

    module_path = SCRIPTS_DIR / f"{script_name}.py"
    spec = importlib.util.spec_from_file_location(f"{script_name}_module", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_check_case_conflicts_import_and_empty_tree(tmp_path):
    module = load_script("check_case_conflicts")
    (tmp_path / "development").mkdir()

    assert module.find_case_conflicts(tmp_path) == {}


def test_normalize_skill_dirs_apply_plan_renames_and_updates_metadata(tmp_path):
    module = load_script("normalize_skill_dirs")
    source_dir = tmp_path / "legacy-name"
    source_dir.mkdir()
    plan = {
        "development": [
            {
                "dir": source_dir,
                "dir_name": "legacy-name",
                "desired_name": "normalized-name",
                "base_name": "normalized-name",
                "key": "owner/repo:skills/normalized-name",
                "meta": {
                    "name": "normalized-name",
                    "repo": "owner/repo",
                    "path": "skills/normalized-name",
                },
            }
        ]
    }

    module.apply_plan(plan, dry_run=False)

    normalized_dir = tmp_path / "normalized-name"
    assert normalized_dir.is_dir()
    assert not source_dir.exists()
    metadata = json.loads((normalized_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["category"] == "development"
    assert metadata["dir_name"] == "normalized-name"


def test_discovery_script_import_has_no_network_side_effects():
    module = load_script("test_discovery")

    assert callable(module.test_topic_search)
    assert callable(module.test_skill_download)
