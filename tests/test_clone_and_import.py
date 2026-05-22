from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("clone_and_import")


def test_import_skill_guesses_category_when_frontmatter_category_missing(tmp_path):
    module = _load_module()
    repo_dir = tmp_path / "repo" / "skills" / "roadmap-helper"
    repo_dir.mkdir(parents=True)
    skill_file = repo_dir / "SKILL.md"
    skill_file.write_text(
        "---\n"
        "name: roadmap-helper\n"
        "description: Product roadmap PRD backlog feature metrics helper.\n"
        "---\n\n"
        "Product roadmap PRD backlog feature metrics helper for planning work.",
        encoding="utf-8",
    )
    skills_dir = tmp_path / "skills"
    stats = {"imported": 0, "skipped": 0, "errors": 0}

    assert module.import_skill(skill_file, skills_dir, "acme/roadmap", stats) is True

    metadata = json.loads(
        (skills_dir / "product" / "roadmap-helper" / "metadata.json").read_text(
            encoding="utf-8"
        )
    )
    assert metadata["category"] == "product"
    assert stats["imported"] == 1
