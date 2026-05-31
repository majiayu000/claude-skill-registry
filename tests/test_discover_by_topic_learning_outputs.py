import importlib.util
import sys
from pathlib import Path


def load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "discover_by_topic.py"
    scripts_dir = str(module_path.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("discover_by_topic_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text


class FakeSession:
    def __init__(self, response):
        self.response = response
        self.headers = {}
        self.calls = 0

    def get(self, url, timeout=None):
        self.calls += 1
        return self.response


def test_write_candidates_jsonl_emits_repo_and_path_rows(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)

    discovery.repo_candidates = {
        "acme/demo": {
            "candidate_level": "repo",
            "repo": "acme/demo",
            "topics": ["claude-skills"],
            "code_queries": ["filename:SKILL.md"],
            "topic_hits": 1,
            "code_hits": 1,
            "max_stars": 42,
            "selected_for_scan": False,
            "downloaded_skills": 2,
        }
    }
    discovery.path_candidates = {
        "acme/demo:skills/demo/SKILL.md": {
            "candidate_level": "path",
            "repo": "acme/demo",
            "path": "skills/demo/SKILL.md",
            "code_queries": ["filename:SKILL.md"],
            "discovered_via_code_search": True,
            "discovered_via_repo_scan": True,
            "downloaded": True,
        }
    }

    output = tmp_path / "discovery_candidates.jsonl"
    written = discovery._write_candidates_jsonl(
        str(output),
        "2026-04-12T00:00:00Z",
        ["acme/demo"],
    )

    lines = output.read_text(encoding="utf-8").strip().splitlines()
    assert written == 2
    assert len(lines) == 2
    assert '"candidate_key": "repo:acme/demo"' in lines[0]
    assert '"selected_for_scan": true' in lines[0]
    assert '"candidate_key": "path:acme/demo:skills/demo/SKILL.md"' in lines[1]


def test_update_priors_accumulates_stats_across_runs(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)

    discovery.repo_candidates = {
        "acme/demo": {
            "candidate_level": "repo",
            "repo": "acme/demo",
            "topics": ["claude-skills"],
            "code_queries": ["filename:SKILL.md"],
            "topic_hits": 2,
            "code_hits": 1,
            "max_stars": 10,
            "selected_for_scan": True,
            "downloaded_skills": 1,
        }
    }
    discovery.topic_stats["claude-skills"]["repo_hits"] = 1
    discovery.topic_stats["claude-skills"]["repo_selected"] = 1
    discovery.topic_stats["claude-skills"]["downloaded_skills"] = 1
    discovery.code_query_stats["filename:SKILL.md"]["repo_hits"] = 1
    discovery.code_query_stats["filename:SKILL.md"]["path_hits"] = 1
    discovery.code_query_stats["filename:SKILL.md"]["downloaded_skills"] = 1

    priors_path = tmp_path / "discovery_priors.json"
    discovery._update_priors(
        str(priors_path),
        "2026-04-12T00:00:00Z",
        ["acme/demo"],
    )
    discovery._update_priors(
        str(priors_path),
        "2026-04-13T00:00:00Z",
        ["acme/demo"],
    )

    priors = module.json.loads(priors_path.read_text(encoding="utf-8"))
    repo = priors["repo_priors"]["acme/demo"]
    assert priors["runs"] == 2
    assert repo["seen_runs"] == 2
    assert repo["selected_runs"] == 2
    assert repo["downloaded_skills"] == 2
    assert priors["topic_yield"]["claude-skills"]["downloaded_skills"] == 2


def test_download_skill_rejects_security_listed_path(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)
    discovery.session = FakeSession(FakeResponse(200, "---\nname: demo\n---\n# Demo\n"))

    downloaded = discovery.download_skill(
        "nowork-studio/toprank",
        "openclaw/skills/toprank/SKILL.md",
        tmp_path / "skills",
    )

    assert downloaded is False
    assert not list(tmp_path.rglob("SKILL.md"))


def test_download_skill_removes_security_scan_failure(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)
    discovery.session = FakeSession(
        FakeResponse(
            200,
            (
                "---\nname: unsafe-demo\n"
                "description: Demo skill with unsafe shell execution.\n---\n"
                "# Unsafe Demo\n"
                "```python\n"
                "import subprocess\n"
                "subprocess.run('echo unsafe', shell=True)\n"
                "```\n"
            ),
        )
    )

    downloaded = discovery.download_skill(
        "acme/unsafe-demo",
        "skills/unsafe-demo/SKILL.md",
        tmp_path / "skills",
    )

    assert downloaded is False
    assert not list(tmp_path.rglob("SKILL.md"))


def test_download_skill_preserves_existing_archive_on_security_scan_failure(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)
    discovery.session = FakeSession(
        FakeResponse(
            200,
            (
                "---\nname: unsafe-demo\n"
                "description: Demo skill with unsafe shell execution.\n---\n"
                "# Unsafe Demo\n"
                "```python\n"
                "import subprocess\n"
                "subprocess.run('echo unsafe', shell=True)\n"
                "```\n"
            ),
        )
    )

    existing_dir = tmp_path / "skills" / "other" / "unsafe-demo"
    existing_dir.mkdir(parents=True)
    existing_skill = (
        "---\nname: unsafe-demo\n"
        "description: Previously archived safe version.\n---\n"
        "# Existing Demo\n"
    )
    existing_metadata = module.json.dumps(
        {
            "name": "unsafe-demo",
            "repo": "acme/unsafe-demo",
            "path": "skills/unsafe-demo/SKILL.md",
            "category": "other",
            "source": "github.com/acme/unsafe-demo",
            "dir_name": "unsafe-demo",
        },
        indent=2,
    )
    (existing_dir / "SKILL.md").write_text(existing_skill, encoding="utf-8")
    (existing_dir / "metadata.json").write_text(existing_metadata, encoding="utf-8")

    downloaded = discovery.download_skill(
        "acme/unsafe-demo",
        "skills/unsafe-demo/SKILL.md",
        tmp_path / "skills",
    )

    assert downloaded is False
    assert (existing_dir / "SKILL.md").read_text(encoding="utf-8") == existing_skill
    assert (existing_dir / "metadata.json").read_text(encoding="utf-8") == existing_metadata


def test_download_skill_classifies_from_skill_md_first(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)
    discovery.session = FakeSession(
        FakeResponse(
            200,
            (
                "---\n"
                "name: docker-deployer\n"
                "description: Deploy Docker Kubernetes CI CD infrastructure automation.\n"
                "tags: [docker, kubernetes, ci]\n"
                "---\n"
                "# Docker Deployer\n\n"
                "Builds release images and deploys services to Kubernetes clusters.\n"
            ),
        )
    )

    downloaded = discovery.download_skill(
        "acme/docker-deployer",
        "skills/docker-deployer/SKILL.md",
        tmp_path / "skills",
    )

    assert downloaded is True
    skill_dir = tmp_path / "skills" / "devops" / "docker-deployer"
    metadata = module.json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert (skill_dir / "SKILL.md").exists()
    assert not (tmp_path / "skills" / "other" / "docker-deployer").exists()
    assert metadata["category"] == "devops"
    assert metadata["description"] == "Deploy Docker Kubernetes CI CD infrastructure automation."
    assert metadata["classification"]["status"] == "classified"
    assert metadata["classification"]["confidence"] == "high"
    assert metadata["classification"]["method"] == "taxonomy_keyword_v1"
    assert metadata["classification"]["semantic_sources"]["description"] == "frontmatter"


def test_download_skill_skips_source_already_archived_in_another_category(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)
    discovery.session = FakeSession(
        FakeResponse(
            200,
            (
                "---\n"
                "name: docker-deployer\n"
                "description: Deploy Docker Kubernetes CI CD infrastructure automation.\n"
                "---\n"
                "# Docker Deployer\n"
            ),
        )
    )

    existing_dir = tmp_path / "skills" / "development" / "docker-deployer"
    existing_dir.mkdir(parents=True)
    existing_skill = "---\nname: docker-deployer\n---\n# Existing Docker Deployer\n"
    existing_metadata = module.json.dumps(
        {
            "name": "docker-deployer",
            "repo": "acme/docker-deployer",
            "path": "skills/docker-deployer",
            "category": "development",
            "source": "github.com/acme/docker-deployer",
            "dir_name": "docker-deployer",
        },
        indent=2,
    )
    (existing_dir / "SKILL.md").write_text(existing_skill, encoding="utf-8")
    (existing_dir / "metadata.json").write_text(existing_metadata, encoding="utf-8")

    downloaded = discovery.download_skill(
        "acme/docker-deployer",
        "skills/docker-deployer/SKILL.md",
        tmp_path / "skills",
    )

    assert downloaded is False
    assert discovery.session.calls == 0
    assert (existing_dir / "SKILL.md").read_text(encoding="utf-8") == existing_skill
    assert not (tmp_path / "skills" / "other" / "docker-deployer").exists()
    assert not (tmp_path / "skills" / "devops" / "docker-deployer").exists()


def test_download_skill_falls_back_to_other_with_audit_reason(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)
    discovery.session = FakeSession(
        FakeResponse(
            200,
            "---\nname: quiet-helper\n---\n# Quiet Helper\n\nShort note.\n",
        )
    )

    downloaded = discovery.download_skill(
        "acme/quiet-helper",
        "skills/quiet-helper/SKILL.md",
        tmp_path / "skills",
    )

    assert downloaded is True
    skill_dir = tmp_path / "skills" / "other" / "quiet-helper"
    metadata = module.json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert (skill_dir / "SKILL.md").exists()
    assert metadata["category"] == "other"
    assert metadata["classification"]["status"] == "unclassified"
    assert metadata["classification"]["confidence"] == "low"
    assert metadata["classification"]["reason"] == (
        "no taxonomy keywords matched SKILL.md semantic text"
    )


def test_download_skill_scans_existing_bundled_files_before_refresh(tmp_path):
    module = load_module()
    discovery = module.GitHubTopicDiscovery(request_delay=0.0)
    discovery.session = FakeSession(
        FakeResponse(
            200,
            (
                "---\nname: bundled-demo\n"
                "description: Safe refreshed skill content.\n---\n"
                "# Refreshed Demo\n"
            ),
        )
    )

    existing_dir = tmp_path / "skills" / "other" / "bundled-demo"
    existing_dir.mkdir(parents=True)
    (existing_dir / "scripts").mkdir()
    existing_skill = (
        "---\nname: bundled-demo\n"
        "description: Previously archived version.\n---\n"
        "# Existing Demo\n"
    )
    existing_metadata = module.json.dumps(
        {
            "name": "bundled-demo",
            "repo": "acme/bundled-demo",
            "path": "skills/bundled-demo/SKILL.md",
            "category": "other",
            "source": "github.com/acme/bundled-demo",
            "dir_name": "bundled-demo",
        },
        indent=2,
    )
    (existing_dir / "SKILL.md").write_text(existing_skill, encoding="utf-8")
    (existing_dir / "metadata.json").write_text(existing_metadata, encoding="utf-8")
    (existing_dir / "scripts" / "tool.py").write_text("eval('unsafe')\n", encoding="utf-8")

    downloaded = discovery.download_skill(
        "acme/bundled-demo",
        "skills/bundled-demo/SKILL.md",
        tmp_path / "skills",
    )

    assert downloaded is False
    assert (existing_dir / "SKILL.md").read_text(encoding="utf-8") == existing_skill
    assert (existing_dir / "metadata.json").read_text(encoding="utf-8") == existing_metadata
    assert (existing_dir / "scripts" / "tool.py").exists()
