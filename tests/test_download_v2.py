import importlib.util
import json
import sys
from pathlib import Path


def load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    module_path = scripts_dir / "download_v2.py"
    spec = importlib.util.spec_from_file_location("download_v2_module", module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_load_source_skills_inherits_top_level_repo(tmp_path):
    module = load_module()
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    (sources_dir / "anthropic.json").write_text(
        json.dumps(
            {
                "name": "Anthropic",
                "repo": "anthropics/skills",
                "skills": [
                    {
                        "name": "docx",
                        "path": "skills/docx",
                        "description": "Document editing skill.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    rows = module.load_source_skills(sources_dir)
    assert rows[0]["repo"] == "anthropics/skills"
