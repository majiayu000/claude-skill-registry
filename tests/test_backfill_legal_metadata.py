import importlib.util
import json
import sys
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def load_module():
    module_path = ROOT / "scripts" / "backfill_legal_metadata.py"
    spec = importlib.util.spec_from_file_location("backfill_legal_metadata", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_metadata(path: Path) -> None:
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "name": "demo",
                "description": "Demo skill",
                "repo": "owner/repo",
                "category": "development",
                "dir_name": "demo",
                "github_path": ".github/skills/demo",
                "github_branch": "main",
            }
        ),
        encoding="utf-8",
    )


def test_backfill_metadata_uses_repo_license_cache():
    module = load_module()
    metadata = {
        "name": "demo",
        "repo": "owner/repo",
        "category": "development",
        "dir_name": "demo",
        "github_path": ".github/skills/demo",
    }

    updated = module.backfill_metadata(
        metadata,
        {"license": "MIT", "copyright": "Copyright (c) 2026 Owner"},
    )

    assert updated["author"] == "owner"
    assert (
        updated["source_url"]
        == "https://github.com/owner/repo/blob/main/.github/skills/demo/SKILL.md"
    )
    assert updated["license"] == "MIT"
    assert updated["copyright"] == "Copyright (c) 2026 Owner"
    assert updated["distribution"] == "compatible"
    assert updated["license_class"] == "compatible"


def test_extract_copyright_notice_ignores_apache_definition_lines():
    module = load_module()
    license_text = """
      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      Copyright (c) 2026 Real Owner
    """

    assert module.extract_copyright_notice(license_text) == "Copyright (c) 2026 Real Owner"


def test_fetch_repo_license_degrades_after_url_errors(monkeypatch):
    module = load_module()

    def fail_request(*args, **kwargs):
        raise urllib.error.URLError("tls eof")

    monkeypatch.setattr(module, "github_request", fail_request)
    monkeypatch.setattr(module.time, "sleep", lambda _seconds: None)

    result = module.fetch_repo_license("owner/repo", token="", timeout=1)

    assert result["license"] == "NOASSERTION"
    assert result["error"] == "fetch_error:tls eof"


def test_fetch_repo_license_degrades_after_timeout(monkeypatch):
    module = load_module()

    def fail_request(*args, **kwargs):
        raise TimeoutError("read timed out")

    monkeypatch.setattr(module, "github_request", fail_request)
    monkeypatch.setattr(module.time, "sleep", lambda _seconds: None)

    result = module.fetch_repo_license("owner/repo", token="", timeout=1)

    assert result["license"] == "NOASSERTION"
    assert result["error"] == "fetch_error:read timed out"


def test_license_classification_covers_backfill_spdx_values():
    module = load_module()

    assert module.build_legal_metadata(license_name="MIT-0")["distribution"] == "compatible"
    assert module.build_legal_metadata(license_name="WTFPL")["distribution"] == "compatible"
    assert module.build_legal_metadata(license_name="EUPL-1.2")["distribution"] == "restricted"


def test_main_dry_run_does_not_modify_metadata(tmp_path, monkeypatch):
    module = load_module()
    metadata_path = tmp_path / "skills" / "development" / "demo" / "metadata.json"
    write_metadata(metadata_path)
    cache_path = tmp_path / "cache.json"
    cache_path.write_text(
        json.dumps({"owner/repo": {"license": "MIT", "copyright": "Copyright (c) 2026 Owner"}}),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "backfill_legal_metadata.py",
            "--skills-dir",
            "skills",
            "--cache",
            "cache.json",
        ],
    )

    assert module.main() == 0

    current = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert "license" not in current


def test_main_apply_writes_missing_legal_fields(tmp_path, monkeypatch):
    module = load_module()
    metadata_path = tmp_path / "skills" / "development" / "demo" / "metadata.json"
    write_metadata(metadata_path)
    cache_path = tmp_path / "cache.json"
    cache_path.write_text(
        json.dumps({"owner/repo": {"license": "MIT", "copyright": "Copyright (c) 2026 Owner"}}),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "backfill_legal_metadata.py",
            "--skills-dir",
            "skills",
            "--cache",
            "cache.json",
            "--apply",
        ],
    )

    assert module.main() == 0

    current = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert current["license"] == "MIT"
    assert current["copyright"] == "Copyright (c) 2026 Owner"
