import importlib.util
from pathlib import Path

import pytest


def load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "security_blocklist.py"
    spec = importlib.util.spec_from_file_location("security_blocklist_module", module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_load_security_blocklist_fails_when_file_missing(tmp_path):
    module = load_module()

    with pytest.raises(FileNotFoundError):
        module.load_security_blocklist(tmp_path / "missing.json")


def test_blocked_repo_entry_normalizes_urls(tmp_path):
    module = load_module()
    blocklist_path = tmp_path / "security_blocklist.json"
    blocklist_path.write_text(
        """
{
  "blocked_repos": [
    {
      "repo": "Owner/Repo",
      "reason": "test",
      "action": "reject"
    }
  ]
}
""",
        encoding="utf-8",
    )

    blocklist = module.load_security_blocklist(blocklist_path)
    entry = module.blocked_repo_entry(
        "https://github.com/owner/repo/blob/main/SKILL.md",
        blocklist,
    )

    assert entry is not None
    assert entry["repo"] == "owner/repo"


@pytest.mark.parametrize(
    "repo",
    [
        "git@github.com:Owner/Repo.git",
        "ssh://git@github.com/Owner/Repo.git",
        "https://github.com/Owner/Repo.git",
        "https://github.com/Owner/Repo.git/blob/main/SKILL.md",
        "https://raw.githubusercontent.com/Owner/Repo/main/SKILL.md",
    ],
)
def test_normalize_repo_id_handles_common_git_forms(repo):
    module = load_module()

    assert module.normalize_repo_id(repo) == "owner/repo"


def test_blocked_metadata_source_matches_github_path_prefix():
    module = load_module()
    blocklist = {
        "openclaw/skills": {
            "repo": "openclaw/skills",
            "reason": "test",
            "action": "reject",
        }
    }

    result = module.blocked_metadata_source(
        {
            "repo": "blisspixel/primr",
            "github_path": "openclaw/skills/primr-strategy",
        },
        blocklist,
    )

    assert result is not None
    entry, field = result
    assert entry["repo"] == "openclaw/skills"
    assert field == "github_path"


def test_blocked_metadata_source_matches_github_path_url():
    module = load_module()
    blocklist = {
        "openclaw/skills": {
            "repo": "openclaw/skills",
            "reason": "test",
            "action": "reject",
        }
    }

    result = module.blocked_metadata_source(
        {
            "repo": "blisspixel/primr",
            "github_path": "https://github.com/openclaw/skills/tree/main/primr-strategy",
        },
        blocklist,
    )

    assert result is not None
    entry, field = result
    assert entry["repo"] == "openclaw/skills"
    assert field == "github_path"
