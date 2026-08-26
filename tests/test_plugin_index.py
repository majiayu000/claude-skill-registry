from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import plugin_index  # noqa: E402


def _plugin(**overrides):
    value = {"name": "demo", "repo": "owner/demo", "description": "demo"}
    value.update(overrides)
    return value


@pytest.mark.parametrize(
    ("loader", "path_factory", "source"),
    [
        (
            plugin_index.load_plugins_from_source,
            lambda root: root / "sources",
            "plugin_source",
        ),
        (
            plugin_index.load_plugins_from_registry,
            lambda root: root / "registry.json",
            "registry_index",
        ),
    ],
)
def test_optional_loaders_distinguish_missing(loader, path_factory, source, tmp_path):
    result = loader(path_factory(tmp_path))

    assert result.present is False
    assert result.plugins == []
    assert result.source == source


def test_source_loader_preserves_present_empty(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "plugins.json").write_text('{"plugins": []}', encoding="utf-8")

    result = plugin_index.load_plugins_from_source(sources)

    assert result.present is True
    assert result.plugins == []


def test_registry_loader_reads_valid_plugins(tmp_path):
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps({"plugins": [_plugin()]}), encoding="utf-8")

    result = plugin_index.load_plugins_from_registry(registry)

    assert result.present is True
    assert result.plugins == [_plugin()]


def test_registry_loader_accepts_http_homepage(tmp_path):
    registry = tmp_path / "registry.json"
    expected = _plugin(homepage="https://example.com/plugin")
    registry.write_text(json.dumps({"plugins": [expected]}), encoding="utf-8")

    result = plugin_index.load_plugins_from_registry(registry)

    assert result.plugins == [expected]


def test_fallback_uses_registry_only_when_source_is_missing(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    registry = tmp_path / "registry.json"
    registry.write_text(json.dumps({"plugins": [_plugin()]}), encoding="utf-8")

    assert plugin_index.load_plugins_with_fallback(sources, registry) == [_plugin()]

    (sources / "plugins.json").write_text('{"plugins": []}', encoding="utf-8")
    assert plugin_index.load_plugins_with_fallback(sources, registry) == []

    registry.unlink()
    (sources / "plugins.json").unlink()
    assert plugin_index.load_plugins_with_fallback(sources, registry) == []


@pytest.mark.parametrize(
    ("payload", "kind"),
    [
        ("{", "malformed_json"),
        ("[]", "invalid_shape"),
        ('{"other": []}', "invalid_shape"),
        ('{"plugins": {}}', "invalid_shape"),
        ('{"plugins": [null]}', "invalid_shape"),
        ('{"plugins": [{"name": "demo"}]}', "invalid_shape"),
        ('{"plugins": [{"name": "", "repo": "owner/repo"}]}', "invalid_shape"),
        ('{"plugins": [{"name": "demo", "repo": "owner/repo", "homepage": "javascript:alert(1)"}]}', "invalid_shape"),
        ('{"plugins": [{"name": "demo", "repo": "owner/repo", "homepage": 42}]}', "invalid_shape"),
        ('{"plugins": [{"name": "demo", "repo": "owner/repo", "homepage": "https:"}]}', "invalid_shape"),
        ('{"plugins": [{"name": "demo", "repo": "owner/repo", "homepage": "https://["}]}', "invalid_shape"),
    ],
)
def test_present_malformed_source_fails_closed(tmp_path, payload, kind):
    sources = tmp_path / "sources"
    sources.mkdir()
    path = sources / "plugins.json"
    path.write_text(payload, encoding="utf-8")

    with pytest.raises(plugin_index.PluginIndexError) as caught:
        plugin_index.load_plugins_from_source(sources)

    assert caught.value.source == "plugin_source"
    assert caught.value.kind == kind
    assert caught.value.path == path


def test_read_failure_is_typed(monkeypatch, tmp_path):
    path = tmp_path / "registry.json"
    path.write_text('{"plugins": []}', encoding="utf-8")
    original = Path.read_text

    def fail_read(self, *args, **kwargs):
        if self == path:
            raise OSError("private detail")
        return original(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", fail_read)

    with pytest.raises(plugin_index.PluginIndexError) as caught:
        plugin_index.load_plugins_from_registry(path)

    assert caught.value.kind == "read_error"


def test_non_utf8_source_is_malformed(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "plugins.json").write_bytes(b"\xff")
    with pytest.raises(plugin_index.PluginIndexError) as caught:
        plugin_index.load_plugins_from_source(sources)
    assert caught.value.kind == "malformed_json"


def test_build_plugins_index_atomically_writes_empty_and_nonempty(tmp_path):
    plugin_index.build_plugins_index([_plugin()], tmp_path, updated_at="now")
    first = json.loads((tmp_path / "plugins.json").read_text(encoding="utf-8"))
    assert first == {"updated_at": "now", "count": 1, "plugins": [_plugin()]}

    plugin_index.build_plugins_index([], tmp_path, updated_at="later")
    second = json.loads((tmp_path / "plugins.json").read_text(encoding="utf-8"))
    assert second == {"updated_at": "later", "count": 0, "plugins": []}
    assert list(tmp_path.glob(".plugins.json.*.tmp")) == []


def test_build_plugins_index_serialization_failure_preserves_existing(tmp_path):
    output = tmp_path / "plugins.json"
    output.write_bytes(b"trusted\n")
    invalid = _plugin(extra={"not-json"})

    with pytest.raises(plugin_index.PluginIndexError) as caught:
        plugin_index.build_plugins_index([invalid], tmp_path)

    assert caught.value.kind == "write_error"
    assert output.read_bytes() == b"trusted\n"
    assert list(tmp_path.glob(".plugins.json.*.tmp")) == []


def test_build_plugins_index_replace_failure_cleans_temp(monkeypatch, tmp_path):
    output = tmp_path / "plugins.json"
    output.write_bytes(b"trusted\n")
    original_replace = Path.replace

    def fail_replace(self, target):
        if Path(target) == output:
            raise OSError("replace failed")
        return original_replace(self, target)

    monkeypatch.setattr(Path, "replace", fail_replace)

    with pytest.raises(plugin_index.PluginIndexError) as caught:
        plugin_index.build_plugins_index([_plugin()], tmp_path)

    assert caught.value.kind == "write_error"
    assert output.read_bytes() == b"trusted\n"
    assert list(tmp_path.glob(".plugins.json.*.tmp")) == []


def test_build_plugins_index_temp_creation_failure_is_typed(monkeypatch, tmp_path):
    output = tmp_path / "plugins.json"
    output.write_bytes(b"trusted\n")

    def fail_temp(*args, **kwargs):
        raise OSError("failure")

    monkeypatch.setattr(plugin_index.tempfile, "NamedTemporaryFile", fail_temp)
    with pytest.raises(plugin_index.PluginIndexError) as caught:
        plugin_index.build_plugins_index([_plugin()], tmp_path)
    assert caught.value.kind == "write_error"
    assert output.read_bytes() == b"trusted\n"
