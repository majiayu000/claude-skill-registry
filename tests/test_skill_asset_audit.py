import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from skill_asset_audit import (
    classify_files,
    classify_skill_text,
    iter_archived_skills,
    verdict_from_counts,
)
from verify_upstream_assets import resolve_skill_dir


class TestClassifySkillText:
    def test_exec_reference(self):
        assert classify_skill_text("Run scripts/setup.py before use.") == "EXEC"

    def test_relative_exec_reference(self):
        assert classify_skill_text("Execute ./tools/build.sh to compile.") == "EXEC"

    def test_doc_reference_only(self):
        assert classify_skill_text("See references/guide.md for details.") == "REF"

    def test_bare(self):
        assert classify_skill_text("Just follow these markdown steps.") == "BARE"

    def test_url_does_not_count_as_exec(self):
        text = "Docs at https://example.com/raw/setup.py explain more."
        assert classify_skill_text(text) == "BARE"


class TestClassifyFiles:
    def test_counts_and_ignores_skill_md(self):
        counts = classify_files([
            "s/SKILL.md", "s/metadata.json", "s/run.py", "s/notes.md", "s/logo.png",
        ])
        assert counts == {"exec": 1, "doc": 1, "asset": 1}

    def test_verdicts(self):
        assert verdict_from_counts({"exec": 1, "doc": 0, "asset": 0}) == "EXEC"
        assert verdict_from_counts({"exec": 0, "doc": 2, "asset": 0}) == "REF_ASSET"
        assert verdict_from_counts({"exec": 0, "doc": 0, "asset": 0}) == "BARE"


class TestResolveSkillDir:
    DIRS = ["skills/alpha", "skills/beta", ""]

    def test_declared_dir_wins(self):
        assert resolve_skill_dir({"dir": "skills/beta", "name": "alpha"}, self.DIRS) == "skills/beta"

    def test_falls_back_to_name_match(self):
        assert resolve_skill_dir({"dir": "", "name": "alpha"}, self.DIRS) == "skills/alpha"

    def test_unmatched_returns_none(self):
        assert resolve_skill_dir({"dir": "", "name": "missing"}, ["skills/alpha"]) is None


class TestIterArchivedSkills:
    def test_yields_skill_dirs_with_metadata(self, tmp_path):
        skill = tmp_path / "cat" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("body")
        (skill / "metadata.json").write_text(json.dumps({"stars": 5}))
        (tmp_path / "cat" / "not-a-skill").mkdir()

        results = list(iter_archived_skills(str(tmp_path)))
        assert len(results) == 1
        dirpath, meta = results[0]
        assert dirpath.endswith("demo")
        assert meta == {"stars": 5}

    def test_bad_metadata_yields_none(self, tmp_path):
        skill = tmp_path / "demo"
        skill.mkdir()
        (skill / "SKILL.md").write_text("body")
        (skill / "metadata.json").write_text("{broken")
        [(_, meta)] = list(iter_archived_skills(str(tmp_path)))
        assert meta is None
