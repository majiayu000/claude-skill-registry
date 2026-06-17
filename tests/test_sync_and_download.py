import asyncio
import importlib.util
import json
import subprocess
import sys
import types
from datetime import timedelta
from pathlib import Path

import pytest


def load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "sync_and_download.py"
    spec = importlib.util.spec_from_file_location("sync_and_download_module", module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_support_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    module_path = scripts_dir / "sync_pipeline_support.py"
    spec = importlib.util.spec_from_file_location("sync_pipeline_support_module", module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, status, *, text="", json_payload=None, body=b""):
        self.status = status
        self._text = text
        self._json_payload = json_payload
        self._body = body

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def text(self):
        return self._text

    async def json(self):
        return self._json_payload

    async def read(self):
        return self._body


def install_fake_aiohttp(monkeypatch, routes):
    class FakeClientSession:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        def get(self, url, timeout=None):
            response = routes.get(url)
            if isinstance(response, Exception):
                raise response
            if response is None:
                return FakeResponse(404)
            return response

    fake_aiohttp = types.SimpleNamespace(
        TCPConnector=lambda *args, **kwargs: object(),
        ClientTimeout=lambda *args, **kwargs: object(),
        ClientSession=FakeClientSession,
    )
    monkeypatch.setitem(sys.modules, "aiohttp", fake_aiohttp)


def test_should_fail_on_empty_download_only_when_all_attempts_fail():
    module = load_module()

    assert module.should_fail_on_empty_download({"downloaded": 0, "failed": 3}) is True
    assert module.should_fail_on_empty_download({"downloaded": 2, "failed": 3}) is False
    assert module.should_fail_on_empty_download({"downloaded": 0, "failed": 0}) is False
    assert (
        module.should_fail_on_empty_download({"downloaded": 0, "failed": 3, "skipped": 10}) is False
    )


def test_build_unified_registry_inherits_top_level_repo(tmp_path):
    module = load_module()
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    output_path = tmp_path / "registry.json"
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
                        "category": "documents",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    assert module.build_unified_registry(sources_dir, output_path) == 1
    registry = json.loads(output_path.read_text(encoding="utf-8"))
    assert registry["skills"][0]["repo"] == "anthropics/skills"


def test_build_unified_registry_preserves_legal_metadata(tmp_path):
    module = load_module()
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    output_path = tmp_path / "registry.json"
    (sources_dir / "community.json").write_text(
        json.dumps(
            {
                "name": "Community",
                "skills": [
                    {
                        "name": "product-manager-skills",
                        "repo": "Digidai/product-manager-skills",
                        "description": "Product management skill.",
                        "category": "product",
                        "author": "Gene Dai",
                        "source_url": "https://github.com/Digidai/product-manager-skills/blob/main/SKILL.md",
                        "license": "CC-BY-NC-SA-4.0",
                        "distribution": "restricted",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    assert module.build_unified_registry(sources_dir, output_path) == 1
    skill = json.loads(output_path.read_text(encoding="utf-8"))["skills"][0]
    assert skill["author"] == "Gene Dai"
    assert skill["source_url"].endswith("/Digidai/product-manager-skills/blob/main/SKILL.md")
    assert skill["license"] == "CC-BY-NC-SA-4.0"
    assert skill["distribution"] == "restricted"


def test_build_unified_registry_stringifies_legal_metadata(tmp_path):
    module = load_module()
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    output_path = tmp_path / "registry.json"
    (sources_dir / "community.json").write_text(
        json.dumps(
            {
                "name": "Community",
                "skills": [
                    {
                        "name": "typed-legal-metadata",
                        "repo": "owner/repo",
                        "description": "Skill with non-string metadata.",
                        "category": "development",
                        "author": 123,
                        "license": 456,
                        "permission_note": ["verify upstream"],
                        "distribution": " restricted ",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    assert module.build_unified_registry(sources_dir, output_path) == 1
    skill = json.loads(output_path.read_text(encoding="utf-8"))["skills"][0]
    assert skill["author"] == "123"
    assert skill["license"] == "456"
    assert skill["permission_note"] == "['verify upstream']"
    assert skill["distribution"] == "restricted"


def test_build_unified_registry_dedupes_root_path_spellings(tmp_path):
    module = load_module()
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    output_path = tmp_path / "registry.json"
    root_skill = {
        "name": "root-skill",
        "repo": "owner/root-skill",
        "description": "Repo-root skill.",
        "category": "productivity",
    }
    (sources_dir / "community.json").write_text(
        json.dumps({"name": "Community", "skills": [root_skill]}),
        encoding="utf-8",
    )
    (sources_dir / "custom.json").write_text(
        json.dumps(
            {
                "name": "Custom",
                "skills": [{**root_skill, "path": "."}],
            }
        ),
        encoding="utf-8",
    )

    assert module.build_unified_registry(sources_dir, output_path) == 1
    registry = json.loads(output_path.read_text(encoding="utf-8"))
    assert registry["skills"][0]["path"] == ""


def test_build_unified_registry_accepts_non_string_path_values(tmp_path):
    module = load_module()
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    output_path = tmp_path / "registry.json"
    (sources_dir / "community.json").write_text(
        json.dumps(
            {
                "name": "Community",
                "skills": [
                    {"name": "numeric-path", "repo": "owner/repo", "path": 123},
                    {
                        "name": "object-path",
                        "repo": "owner/repo",
                        "path": {"bad": "path"},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    assert module.build_unified_registry(sources_dir, output_path) == 2


def test_build_unified_registry_dedupes_boolean_root_path(tmp_path):
    module = load_module()
    sources_dir = tmp_path / "sources"
    sources_dir.mkdir()
    output_path = tmp_path / "registry.json"
    root_skill = {
        "name": "root-skill",
        "repo": "owner/root-skill",
        "description": "Repo-root skill.",
        "category": "productivity",
    }
    (sources_dir / "community.json").write_text(
        json.dumps(
            {
                "name": "Community",
                "skills": [
                    root_skill,
                    {**root_skill, "path": False},
                ],
            }
        ),
        encoding="utf-8",
    )

    assert module.build_unified_registry(sources_dir, output_path) == 1


def test_download_blocks_security_listed_source_repo(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "php-code-injection",
                        "repo": "blacklanternsecurity/red-run",
                        "path": "skills/web/php-code-injection/SKILL.md",
                        "category": "other",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(monkeypatch, {})

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 0
    assert stats["failed"] == 1
    assert not list(output_dir.rglob("SKILL.md"))
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert failure_report["failure_reasons"]["blocked_source"] == 1


def test_download_blocks_security_listed_source_path_alias(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "toprank",
                        "repo": "nowork-studio/toprank",
                        "path": "openclaw/skills/toprank/SKILL.md",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(monkeypatch, {})

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 0
    assert stats["failed"] == 1
    assert not list(output_dir.rglob("SKILL.md"))
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert failure_report["failure_reasons"]["blocked_source"] == 1


def test_download_removes_skill_that_fails_security_scan(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "unsafe-demo",
                        "repo": "acme/unsafe-demo",
                        "path": "SKILL.md",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/unsafe-demo/main/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: unsafe-demo\n"
                    "description: Demo skill with unsafe shell execution.\n---\n"
                    "# Unsafe Demo\n"
                    "```python\n"
                    "import subprocess\n"
                    "subprocess.run('echo unsafe', shell=True)\n"
                    "```\n"
                ),
            ),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 0
    assert stats["failed"] == 1
    assert not list(output_dir.rglob("SKILL.md"))
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert failure_report["failure_reasons"]["security_scan_failed"] == 1


def test_download_removes_existing_blocked_archive_before_existing_skip(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    skill_dir = output_dir / "other" / "php-code-injection"
    failure_report_path = tmp_path / "failure_report.json"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: php-code-injection
description: Existing blocked archive.
---

# Demo
""",
        encoding="utf-8",
    )
    (skill_dir / "metadata.json").write_text(
        json.dumps({"repo": "blacklanternsecurity/red-run"}),
        encoding="utf-8",
    )
    registry_path.write_text(json.dumps({"skills": []}), encoding="utf-8")
    install_fake_aiohttp(monkeypatch, {})

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["blocked_archives_removed"] == 1
    assert stats["downloaded"] == 0
    assert not skill_dir.exists()


def test_download_removes_ci_untracked_archive_leftovers(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    stale_dir = output_dir / "other" / "old-core-leftover"
    stale_dir.mkdir(parents=True)
    (stale_dir / "SKILL.md").write_text(
        """---
name: old-core-leftover
description: Stale file left by the core checkout.
---

# Demo
""",
        encoding="utf-8",
    )
    (stale_dir / "metadata.json").write_text("{}", encoding="utf-8")
    registry_path.write_text(json.dumps({"skills": []}), encoding="utf-8")
    install_fake_aiohttp(monkeypatch, {})
    monkeypatch.setenv("GITHUB_ACTIONS", "true")

    subprocess_result = subprocess.run(
        ["git", "init"],
        cwd=output_dir,
        check=True,
        capture_output=True,
    )
    assert subprocess_result.returncode == 0

    stats = asyncio.run(module.download_skills(registry_path, output_dir))

    assert stats["ci_untracked_files_removed"] == 2
    assert not stale_dir.exists()


def test_download_can_skip_ci_untracked_archive_cleanup(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    discovered_dir = output_dir / "other" / "new-discovery"
    discovered_dir.mkdir(parents=True)
    (discovered_dir / "SKILL.md").write_text(
        """---
name: new-discovery
description: Newly discovered in this workflow run.
---

# Demo
""",
        encoding="utf-8",
    )
    (discovered_dir / "metadata.json").write_text("{}", encoding="utf-8")
    registry_path.write_text(json.dumps({"skills": []}), encoding="utf-8")
    install_fake_aiohttp(monkeypatch, {})
    monkeypatch.setenv("GITHUB_ACTIONS", "true")

    subprocess_result = subprocess.run(
        ["git", "init"],
        cwd=output_dir,
        check=True,
        capture_output=True,
    )
    assert subprocess_result.returncode == 0

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            cleanup_ci_untracked=False,
        )
    )

    assert stats["ci_untracked_files_removed"] == 0
    assert (discovered_dir / "SKILL.md").exists()


def test_existing_archive_blocks_security_listed_github_path(tmp_path):
    module = load_module()
    output_dir = tmp_path / "skills"
    skill_dir = output_dir / "other" / "primr-strategy"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        """---
name: primr-strategy
description: Existing archive with blocked github_path.
---

# Demo
""",
        encoding="utf-8",
    )
    (skill_dir / "metadata.json").write_text(
        json.dumps(
            {
                "repo": "blisspixel/primr",
                "github_path": "openclaw/skills/primr-strategy",
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(RuntimeError, match="Existing archive contains blocked source repos"):
        module.validate_existing_archive_sources(
            output_dir,
            module.load_security_blocklist(),
        )


def test_manifest_round_trip(tmp_path):
    module = load_module()
    manifest_path = tmp_path / "acquisition_manifest.json"
    entries = {
        "development:demo-skill": {
            "repo": "acme/demo",
            "branch": "main",
            "relative_path": "skills/demo/SKILL.md",
            "updated_at": "2026-04-10T00:00:00Z",
        }
    }

    module.save_acquisition_manifest(manifest_path, entries)
    loaded = module.load_acquisition_manifest(manifest_path)
    assert loaded == entries


def test_manifest_loader_tolerates_legacy_and_invalid_entries(tmp_path):
    module = load_module()
    manifest_path = tmp_path / "acquisition_manifest.json"
    manifest_path.write_text(
        """
        {
          "legacy_key": {"repo": "acme/demo", "branch": "main", "relative_path": "SKILL.md"},
          "bad_key": {"repo": "acme/demo", "branch": "", "relative_path": ""},
          "bad_type": "oops"
        }
        """,
        encoding="utf-8",
    )

    loaded = module.load_acquisition_manifest(manifest_path)
    assert loaded == {
        "legacy_key": {
            "repo": "acme/demo",
            "branch": "main",
            "relative_path": "SKILL.md",
            "updated_at": "",
        }
    }


def test_probe_order_prefers_manifest_hints():
    module = load_module()
    manifest_entry = {"branch": "release", "relative_path": "custom/path/SKILL.md"}
    preferred = {"acme/demo": "main"}

    branch_order = module.build_branch_probe_order(
        "acme/demo", preferred, manifest_entry, ("main", "master")
    )
    path_order = module.build_relative_probe_order(
        ["skills/demo/SKILL.md", "SKILL.md"], manifest_entry
    )

    assert branch_order == ["release", "main", "master"]
    assert path_order == ["custom/path/SKILL.md", "skills/demo/SKILL.md", "SKILL.md"]


def test_probe_order_removes_duplicates():
    module = load_module()
    manifest_entry = {"branch": "main", "relative_path": "skills/demo/SKILL.md"}
    preferred = {"acme/demo": "main"}

    branch_order = module.build_branch_probe_order(
        "acme/demo", preferred, manifest_entry, ("main", "master")
    )
    path_order = module.build_relative_probe_order(
        ["skills/demo/SKILL.md", "SKILL.md", "SKILL.md"], manifest_entry
    )

    assert branch_order == ["main", "master"]
    assert path_order == ["skills/demo/SKILL.md", "SKILL.md"]


def test_download_skills_can_disable_acquisition_manifest(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    default_manifest = tmp_path / "default_manifest.json"
    stale_manifest = {
        "entries": {
            "acme/demo:skills/demo": {
                "repo": "acme/demo",
                "branch": "release",
                "relative_path": "stale/SKILL.md",
                "updated_at": "2026-04-10T00:00:00Z",
            }
        }
    }
    default_manifest.write_text(json.dumps(stale_manifest), encoding="utf-8")
    monkeypatch.setitem(
        module.download_skills.__globals__,
        "DEFAULT_MANIFEST_PATH",
        default_manifest,
    )
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "demo",
                        "repo": "acme/demo",
                        "path": "skills/demo",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/demo/main/skills/demo/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: demo\n"
                    "description: Demo skill without manifest help.\n---\n"
                    "# Demo\nUse this skill directly.\n"
                ),
            ),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=None,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["manifest_hits"] == 0
    assert stats["manifest_misses"] == 0
    assert json.loads(default_manifest.read_text(encoding="utf-8")) == stale_manifest


def test_skill_source_dir_resolves_skill_parent():
    module = load_module()

    assert module.skill_source_dir("skills/demo/SKILL.md") == "skills/demo"
    assert module.skill_source_dir(".claude/skills/demo/SKILL.md") == ".claude/skills/demo"
    assert module.skill_source_dir("SKILL.md") == ""
    assert module.skill_source_dir("") == ""


def test_bundled_file_allowlist_is_scoped_and_size_limited():
    module = load_module()
    support = load_support_module()

    assert module.bundled_relative_path("", "package.json") == "package.json"
    assert (
        module.bundled_relative_path("skills/demo", "skills/demo/scripts/run.sh")
        == "scripts/run.sh"
    )
    assert module.bundled_relative_path("skills/demo", "other/scripts/run.sh") == ""
    assert module.should_recurse_bundled_dir("scripts") is True
    assert module.should_recurse_bundled_dir("bin") is True
    assert module.should_recurse_bundled_dir("bin/nested") is False
    assert module.should_recurse_bundled_dir("references/nested") is True
    assert module.should_recurse_bundled_dir("reference") is True
    assert module.should_recurse_bundled_dir("connectors") is True
    assert module.should_recurse_bundled_dir("knowledge") is True
    assert module.should_recurse_bundled_dir("prompts") is True
    assert module.should_recurse_bundled_dir("docs") is False
    assert module.is_safe_bundled_file("references/helper.py", 1024) is True
    assert module.is_safe_bundled_file("reference/environment.md", 1024) is True
    assert module.is_safe_bundled_file("connectors/slack.md", 1024) is True
    assert module.is_safe_bundled_file("knowledge/finance-metrics.md", 1024) is True
    assert module.is_safe_bundled_file("prompts/audit-system-prompt.md", 1024) is True
    assert module.is_safe_bundled_file("scripts/listen.mjs", 1024) is True
    assert module.is_safe_bundled_file("bin/jq-linux-amd64", 2_319_424) is True
    assert module.is_safe_bundled_file("bin/jq-windows-amd64.exe", 985_088) is True
    assert module.is_safe_bundled_file("bin/jq.LICENSE", 6_026) is True
    assert module.is_safe_bundled_file("bin/random-tool", 1024) is False
    assert module.is_safe_bundled_file("bin/nested/jq-linux-amd64", 1024) is False
    assert module.is_safe_bundled_file("package.json", 1024) is True
    assert module.is_safe_bundled_file("setup.md", 1024) is True
    assert module.is_safe_bundled_file("audit.md", 1024) is True
    assert module.is_safe_bundled_file("references/SKILL.md", 1024) is False
    assert module.is_safe_bundled_file("examples/SKILL.md", 1024) is False
    assert module.is_safe_bundled_file("docs/helper.py", 1024) is False
    assert module.is_safe_bundled_file("references/.env", 10) is False
    assert (
        module.is_safe_bundled_file(
            "references/huge.py",
            module.MAX_BUNDLED_FILE_BYTES + 1,
        )
        is False
    )
    assert (
        module.is_safe_bundled_file(
            "bin/jq-linux-amd64",
            support.MAX_BUNDLED_BIN_FILE_BYTES + 1,
        )
        is False
    )
    assert support.requires_complete_bundled_archive("See references/guide.md") is True
    assert support.requires_complete_bundled_archive("Set user preference/theme.md") is False


def test_bundled_download_failure_does_not_publish_partial_archive(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    manifest_path = tmp_path / "manifest.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "demo",
                        "repo": "acme/demo",
                        "path": "skills/demo",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/demo/main/skills/demo/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: demo\n"
                    "description: Demo skill with a helper script.\n---\n# Demo\n"
                    "Run scripts/run.sh before using this skill.\n"
                ),
            ),
            "https://api.github.com/repos/acme/demo/contents/skills/demo?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "dir",
                        "path": "skills/demo/scripts",
                        "size": 0,
                    }
                ],
            ),
            "https://api.github.com/repos/acme/demo/contents/skills/demo/scripts?ref=main": (
                FakeResponse(
                    200,
                    json_payload=[
                        {
                            "type": "file",
                            "path": "skills/demo/scripts/run.sh",
                            "download_url": "https://download.example/run.sh",
                            "size": 10,
                        }
                    ],
                )
            ),
            "https://download.example/run.sh": FakeResponse(503),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=manifest_path,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 0
    assert stats["failed"] == 1
    assert stats["bundled_files"] == 0
    assert not list(output_dir.rglob("SKILL.md"))
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert failure_report["failure_reasons"]["bundled_download_failed"] == 1


def test_bundled_listing_failure_does_not_publish_skill_md_only(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    manifest_path = tmp_path / "manifest.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "demo",
                        "repo": "acme/demo",
                        "path": "skills/demo",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/demo/main/skills/demo/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: demo\n"
                    "description: Demo skill with references.\n---\n# Demo\n"
                    "Read references/guide.md before using this skill.\n"
                ),
            ),
            "https://api.github.com/repos/acme/demo/contents/skills/demo?ref=main": FakeResponse(
                403
            ),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=manifest_path,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 0
    assert stats["failed"] == 1
    assert stats["bundled_files"] == 0
    assert not list(output_dir.rglob("SKILL.md"))
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert failure_report["failure_reasons"]["bundled_listing_failed"] == 1
    assert "status 403" in failure_report["failures"]["bundled_listing_failed"][0]


def test_bundled_listing_failure_degrades_when_skill_has_no_support_refs(
    tmp_path,
    monkeypatch,
):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    manifest_path = tmp_path / "manifest.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "demo",
                        "repo": "acme/demo",
                        "path": "skills/demo",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/demo/main/skills/demo/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: demo\n"
                    "description: Demo skill without support files.\n---\n"
                    "# Demo\nUse this skill directly from the markdown instructions.\n"
                ),
            ),
            "https://api.github.com/repos/acme/demo/contents/skills/demo?ref=main": FakeResponse(
                403
            ),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=manifest_path,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    assert stats["bundled_files"] == 0
    skill_dir = next(output_dir.glob("development/*"))
    metadata = json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["archive_mode"] == "skill-md"
    assert metadata["bundled_files"] == []
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert "bundled_listing_failed" not in failure_report["failure_reasons"]


def test_optional_bundled_download_failure_degrades_to_skill_md(
    tmp_path,
    monkeypatch,
):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    manifest_path = tmp_path / "manifest.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "demo",
                        "repo": "acme/demo",
                        "path": "SKILL.md",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/demo/main/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: demo\n"
                    "description: Demo skill with optional repo files.\n---\n"
                    "# Demo\nUse this skill directly from the markdown instructions.\n"
                ),
            ),
            "https://api.github.com/repos/acme/demo/contents?ref=main": FakeResponse(
                200,
                json_payload=[
                    {"type": "file", "path": "SKILL.md", "size": 80},
                    {"type": "dir", "path": "scripts", "size": 0},
                ],
            ),
            "https://api.github.com/repos/acme/demo/contents/scripts?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "scripts/optional.py",
                        "download_url": "https://download.example/optional.py",
                        "size": 12,
                    }
                ],
            ),
            "https://download.example/optional.py": FakeResponse(503),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=manifest_path,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    assert stats["bundled_files"] == 0
    skill_dir = next(output_dir.glob("development/*"))
    metadata = json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["archive_mode"] == "skill-md"
    assert metadata["bundled_files"] == []
    assert not (skill_dir / "scripts" / "optional.py").exists()
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert "bundled_download_failed" not in failure_report["failure_reasons"]


def test_bundled_references_rules_and_knowledge_are_archived_with_directory_mode(
    tmp_path, monkeypatch
):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    manifest_path = tmp_path / "manifest.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "demo",
                        "repo": "acme/demo",
                        "path": "SKILL.md",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/demo/main/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: demo\n"
                    "description: Demo skill with references.\n---\n"
                    "# Demo\nSee references/guide.md, rules/rule.md, and knowledge/framework.md.\n"
                ),
            ),
            "https://api.github.com/repos/acme/demo/contents?ref=main": FakeResponse(
                200,
                json_payload=[
                    {"type": "file", "path": "SKILL.md", "size": 80},
                    {"type": "dir", "path": "references", "size": 0},
                    {"type": "dir", "path": "rules", "size": 0},
                    {"type": "dir", "path": "knowledge", "size": 0},
                ],
            ),
            "https://api.github.com/repos/acme/demo/contents/references?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "references/guide.md",
                        "download_url": "https://download.example/guide.md",
                        "size": 12,
                    }
                ],
            ),
            "https://download.example/guide.md": FakeResponse(200, body=b"# Guide\n"),
            "https://api.github.com/repos/acme/demo/contents/rules?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "rules/rule.md",
                        "download_url": "https://download.example/rule.md",
                        "size": 12,
                    }
                ],
            ),
            "https://download.example/rule.md": FakeResponse(200, body=b"# Rule\n"),
            "https://api.github.com/repos/acme/demo/contents/knowledge?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "knowledge/framework.md",
                        "download_url": "https://download.example/framework.md",
                        "size": 12,
                    }
                ],
            ),
            "https://download.example/framework.md": FakeResponse(200, body=b"# Framework\n"),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=manifest_path,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    assert stats["bundled_files"] == 3
    skill_dir = next(output_dir.glob("development/*"))
    metadata = json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["archive_mode"] == "directory"
    assert metadata["bundled_files"] == [
        "knowledge/framework.md",
        "references/guide.md",
        "rules/rule.md",
    ]
    assert (skill_dir / "knowledge" / "framework.md").read_text(
        encoding="utf-8"
    ) == "# Framework\n"
    assert (skill_dir / "references" / "guide.md").read_text(encoding="utf-8") == "# Guide\n"
    assert (skill_dir / "rules" / "rule.md").read_text(encoding="utf-8") == "# Rule\n"


def test_bundled_collection_skips_github_submodule_entries(tmp_path, monkeypatch):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    manifest_path = tmp_path / "manifest.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "demo",
                        "repo": "acme/demo",
                        "path": "SKILL.md",
                        "category": "development",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/acme/demo/main/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: demo\n"
                    "description: Demo skill with a submodule path.\n---\n# Demo\n"
                ),
            ),
            "https://api.github.com/repos/acme/demo/contents?ref=main": FakeResponse(
                200,
                json_payload=[
                    {"type": "file", "path": "SKILL.md", "size": 80},
                    {"type": "dir", "path": "scripts", "size": 0},
                ],
            ),
            "https://api.github.com/repos/acme/demo/contents/scripts?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "scripts/tool.py",
                        "size": 0,
                        "download_url": None,
                        "submodule_git_url": "https://github.com/acme/tool.git",
                    }
                ],
            ),
        },
    )

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=manifest_path,
            failure_report_path=failure_report_path,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    skill_dir = next(output_dir.glob("development/*"))
    metadata = json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["archive_mode"] == "skill-md"
    assert metadata["bundled_files"] == []
    assert not (skill_dir / "scripts" / "tool.py").exists()


def test_select_shard_skills_is_deterministic():
    module = load_module()
    skills = [
        {"repo": "acme/repo1", "path": "skills/a", "name": "a", "category": "dev"},
        {"repo": "acme/repo2", "path": "skills/b", "name": "b", "category": "dev"},
        {"repo": "acme/repo3", "path": "skills/c", "name": "c", "category": "dev"},
        {"repo": "acme/repo4", "path": "skills/d", "name": "d", "category": "dev"},
    ]
    first = module.select_shard_skills(skills, shard_count=3, shard_index=1)
    second = module.select_shard_skills(skills, shard_count=3, shard_index=1)
    assert first == second


def test_select_shard_skills_partition_has_no_overlap():
    module = load_module()
    skills = [
        {"repo": f"acme/repo{i}", "path": f"skills/{i}", "name": f"s{i}", "category": "dev"}
        for i in range(15)
    ]
    shard_count = 4
    buckets = []
    for idx in range(shard_count):
        bucket = module.select_shard_skills(skills, shard_count=shard_count, shard_index=idx)
        keys = {module.skill_key(item) for item in bucket}
        buckets.append(keys)

    combined = set().union(*buckets)
    original = {module.skill_key(item) for item in skills}

    assert combined == original
    for i in range(shard_count):
        for j in range(i + 1, shard_count):
            assert buckets[i].isdisjoint(buckets[j])


def test_filter_pending_skills_prefilters_no_repo_and_cooldown():
    module = load_module()
    now = module.utc_now()
    valid = {"repo": "acme/ok", "path": "skills/ok", "name": "ok", "category": "dev"}
    missing_repo = {"repo": "", "path": "skills/missing", "name": "missing", "category": "dev"}
    cooldown = {"repo": "acme/cool", "path": "skills/cool", "name": "cool", "category": "dev"}

    negative_cache = {
        module.skill_key(cooldown): {
            "reason": "not_found",
            "cooldown_until": module.to_utc_iso(now + timedelta(hours=24)),
        }
    }

    filtered, skipped, skipped_rows = module.filter_pending_skills(
        [valid, missing_repo, cooldown],
        existing=set(),
        negative_cache=negative_cache,
        now_utc=now,
    )

    assert filtered == [valid]
    assert skipped["no_repo"] == 1
    assert skipped["cooldown_not_found"] == 1
    reasons = [reason for _, reason in skipped_rows]
    assert "no_repo_prefilter" in reasons
    assert "cooldown_not_found" in reasons


def test_sync_pipeline_category_sanitization_does_not_use_legacy_aliases():
    module = load_support_module()
    assert module.sanitize_category("dev") == "dev"
    assert module.sanitize_category("Engineering") == "engineering"
    assert module.skill_key({"name": "demo", "category": "dev"}) == "dev:demo"


def test_negative_cache_helpers_prune_and_cooldown():
    module = load_module()
    now = module.utc_now()
    stale = module.to_utc_iso(now - timedelta(days=40))
    future = module.to_utc_iso(now + timedelta(days=1))
    cache = {
        "bad": "x",
        "stale": {"reason": "not_found", "cooldown_until": stale},
        "active": {"reason": "not_found", "cooldown_until": future},
    }

    removed = module.prune_negative_cache(cache, now)
    assert removed == 2
    assert "active" in cache
    assert module.is_negative_cache_active(cache["active"], now) is True
    assert module.not_found_cooldown_hours(1) == 24
    assert module.not_found_cooldown_hours(2) == 72
    assert module.not_found_cooldown_hours(5) == 168


def test_main_exits_when_fail_on_empty_download_is_enabled(monkeypatch):
    module = load_module()

    async def fake_download_skills(*args, **kwargs):
        return {"downloaded": 0, "failed": 2, "skipped": 0, "total": 0}

    monkeypatch.setattr(module, "download_skills", fake_download_skills)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--download-only", "--fail-on-empty-download"],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert exc.value.code == 1


def test_main_allows_partial_success_with_fail_on_empty_download(monkeypatch):
    module = load_module()

    async def fake_download_skills(*args, **kwargs):
        return {"downloaded": 1, "failed": 2, "total": 1}

    monkeypatch.setattr(module, "download_skills", fake_download_skills)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--download-only", "--fail-on-empty-download"],
    )

    module.main()


def test_main_allows_existing_archive_when_all_pending_fail(monkeypatch):
    module = load_module()

    async def fake_download_skills(*args, **kwargs):
        return {"downloaded": 0, "failed": 2, "skipped": 100, "total": 100}

    monkeypatch.setattr(module, "download_skills", fake_download_skills)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--download-only", "--fail-on-empty-download"],
    )

    module.main()


def test_main_passes_skip_ci_untracked_cleanup(monkeypatch):
    module = load_module()
    captured = {}

    async def fake_download_skills(*args, **kwargs):
        captured.update(kwargs)
        return {"downloaded": 0, "failed": 0, "skipped": 0, "total": 0}

    monkeypatch.setattr(module, "download_skills", fake_download_skills)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--download-only", "--skip-ci-untracked-cleanup"],
    )

    module.main()

    assert captured["cleanup_ci_untracked"] is False


def test_main_cleanup_only_runs_ci_archive_cleanup(monkeypatch):
    module = load_module()
    captured = {}

    def fake_cleanup(output_dir):
        captured["output_dir"] = output_dir
        return 2

    monkeypatch.setattr(module, "remove_ci_untracked_archive_files", fake_cleanup)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--cleanup-ci-untracked-archive-files-only"],
    )

    module.main()

    assert captured["output_dir"].name == "skills"
