import asyncio
import importlib.util
import json
import sys
import types
from pathlib import Path


def load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    module_path = scripts_dir / "sync_download.py"
    spec = importlib.util.spec_from_file_location("sync_download_module", module_path)
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


def test_flowhunt_style_support_files_are_archived_with_directory_mode(
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
                        "name": "flowhunt",
                        "repo": "heyneuron/flowhunt-skill",
                        "path": "skills/flowhunt",
                        "category": "productivity",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    install_fake_aiohttp(
        monkeypatch,
        {
            "https://raw.githubusercontent.com/heyneuron/flowhunt-skill/main/skills/flowhunt/SKILL.md": FakeResponse(
                200,
                text=(
                    "---\nname: flowhunt\n"
                    "description: Automation discovery audit.\n---\n"
                    "# FlowHunt\nRead setup.md, audit.md, connectors/email-calendar.md, "
                    "prompts/audit-system-prompt.md, and reference/environment.md.\n"
                ),
            ),
            "https://api.github.com/repos/heyneuron/flowhunt-skill/contents/skills/flowhunt?ref=main": FakeResponse(
                200,
                json_payload=[
                    {"type": "file", "path": "skills/flowhunt/SKILL.md", "size": 160},
                    {
                        "type": "file",
                        "path": "skills/flowhunt/setup.md",
                        "download_url": "https://download.example/setup.md",
                        "size": 12,
                    },
                    {
                        "type": "file",
                        "path": "skills/flowhunt/audit.md",
                        "download_url": "https://download.example/audit.md",
                        "size": 12,
                    },
                    {"type": "dir", "path": "skills/flowhunt/connectors", "size": 0},
                    {"type": "dir", "path": "skills/flowhunt/prompts", "size": 0},
                    {"type": "dir", "path": "skills/flowhunt/reference", "size": 0},
                ],
            ),
            "https://api.github.com/repos/heyneuron/flowhunt-skill/contents/skills/flowhunt/connectors?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "skills/flowhunt/connectors/email-calendar.md",
                        "download_url": "https://download.example/email-calendar.md",
                        "size": 12,
                    }
                ],
            ),
            "https://api.github.com/repos/heyneuron/flowhunt-skill/contents/skills/flowhunt/prompts?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "skills/flowhunt/prompts/audit-system-prompt.md",
                        "download_url": "https://download.example/audit-system-prompt.md",
                        "size": 12,
                    }
                ],
            ),
            "https://api.github.com/repos/heyneuron/flowhunt-skill/contents/skills/flowhunt/reference?ref=main": FakeResponse(
                200,
                json_payload=[
                    {
                        "type": "file",
                        "path": "skills/flowhunt/reference/environment.md",
                        "download_url": "https://download.example/environment.md",
                        "size": 12,
                    }
                ],
            ),
            "https://download.example/setup.md": FakeResponse(200, body=b"# Setup\n"),
            "https://download.example/audit.md": FakeResponse(200, body=b"# Audit\n"),
            "https://download.example/email-calendar.md": FakeResponse(200, body=b"# Email\n"),
            "https://download.example/audit-system-prompt.md": FakeResponse(
                200,
                body=b"# Prompt\n",
            ),
            "https://download.example/environment.md": FakeResponse(200, body=b"# Env\n"),
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
    assert stats["bundled_files"] == 5
    skill_dir = next(output_dir.glob("productivity/*"))
    metadata = json.loads((skill_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["archive_mode"] == "directory"
    assert metadata["bundled_files"] == [
        "audit.md",
        "connectors/email-calendar.md",
        "prompts/audit-system-prompt.md",
        "reference/environment.md",
        "setup.md",
    ]
    assert (skill_dir / "setup.md").read_text(encoding="utf-8") == "# Setup\n"
    assert (skill_dir / "connectors" / "email-calendar.md").read_text(
        encoding="utf-8"
    ) == "# Email\n"
