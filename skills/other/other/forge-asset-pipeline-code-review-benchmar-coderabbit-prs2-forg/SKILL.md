---
name: forge-asset-pipeline
description: Scaffold a plugin-based asset processing pipeline with CLI, plugin discovery, content-hash fingerprinting, and TOML configuration. Use when someone needs to build tooling that processes files incrementally — asset pipelines, build systems, static site generators, or any scan-and-transform workflow.
---

# forge-asset-pipeline

Scaffold a Python CLI pipeline that discovers plugins, scans source files,
fingerprints them by content hash, and reports what needs processing.

## When to use this skill

- Setting up an asset processing pipeline for a game or graphics project
- Building any file-processing CLI that needs incremental builds
- Creating a plugin-based tool where new file types are added without
  modifying core code
- When someone asks for "a build system", "asset pipeline", "file processor",
  or "incremental build tool"

## Key concepts

| Concept | Implementation |
|---|---|
| Configuration | TOML file parsed with `tomllib`, typed `PipelineConfig` dataclass |
| Plugin system | `AssetPlugin` base class, `PluginRegistry` with name + extension lookup |
| Discovery | `importlib` scans a directory for `.py` files, registers subclasses |
| Fingerprinting | SHA-256 content hash (not timestamps) for correctness and portability |
| Cache | JSON file mapping relative paths to hex digests |
| Classification | NEW (not cached), CHANGED (hash differs), UNCHANGED (hash matches) |

## Architecture

```text
pipeline.toml ──> CLI (__main__.py)
                   │
                   ├──> Plugin Discovery (plugins/*.py)
                   │        register by name + extension
                   │
                   └──> Scanner (scanner.py)
                            │
                            ├── walk source directory
                            ├── fingerprint (SHA-256)
                            ├── compare against cache
                            └── classify: NEW / CHANGED / UNCHANGED
```

## Correct order

1. Create the project structure (`pyproject.toml`, `pipeline/` package)
2. Implement `config.py` — TOML loader with typed dataclass
3. Implement `plugin.py` — base class, registry, file-based discovery
4. Implement `scanner.py` — fingerprinting, cache, scan function
5. Implement `__main__.py` — CLI that ties them together
6. Create example plugins in `plugins/`
7. Create `pipeline.toml` with sensible defaults

## Project structure template

```text
<project>/
  pipeline.toml              # TOML configuration
  pyproject.toml             # Python package definition
  pipeline/
    __init__.py
    __main__.py              # CLI entry point (argparse)
    config.py                # TOML config loader
    plugin.py                # AssetPlugin base, PluginRegistry, discovery
    scanner.py               # File scanning and fingerprinting
  plugins/
    <type>.py                # One file per asset type
  tests/
    test_config.py
    test_plugin.py
    test_scanner.py
```

## Ready-to-use templates

### config.py — core pattern

```python
import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib

@dataclass
class PipelineConfig:
    source_dir: Path          # where raw source files live
    output_dir: Path          # where processed files go
    cache_dir: Path           # fingerprint cache location
    plugin_settings: dict[str, dict] = field(default_factory=dict)
    raw: dict = field(default_factory=dict, repr=False)

class ConfigError(Exception):
    pass

def load_config(path: Path) -> PipelineConfig:
    if not path.exists():
        raise ConfigError(f"Configuration file not found: {path}")
    try:
        with open(path, "rb") as f:
            raw = tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Invalid TOML in {path}: {exc}") from exc

    pipeline = raw.get("pipeline", {})
    plugin_settings = {k: v for k, v in raw.items()
                       if k != "pipeline" and isinstance(v, dict)}
    return PipelineConfig(
        source_dir=Path(pipeline.get("source_dir", "assets/raw")),
        output_dir=Path(pipeline.get("output_dir", "assets/processed")),
        cache_dir=Path(pipeline.get("cache_dir", ".forge-cache")),
        plugin_settings=plugin_settings,
        raw=raw,
    )
```

### plugin.py — core pattern

```python
import importlib
import importlib.util
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class AssetResult:
    source: Path              # original source file
    output: Path              # processed output file
    metadata: dict = field(default_factory=dict)

class AssetPlugin:
    name: str = ""            # human-readable identifier
    extensions: list[str] = []  # e.g. [".png", ".jpg"]

    def process(self, source: Path, output_dir: Path, settings: dict) -> AssetResult:
        raise NotImplementedError

class PluginRegistry:
    def __init__(self):
        self._plugins: dict[str, AssetPlugin] = {}
        self._ext_map: dict[str, AssetPlugin] = {}

    def register(self, plugin: AssetPlugin) -> None:
        # Validate: non-empty name, no duplicate name, no duplicate extensions
        self._plugins[plugin.name] = plugin
        for ext in plugin.extensions:
            self._ext_map[ext.lower()] = plugin

    def get_by_extension(self, ext: str) -> AssetPlugin | None:
        return self._ext_map.get(ext.lower())

    def discover(self, plugins_dir: Path) -> int:
        count = 0
        for py_file in sorted(plugins_dir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue
            spec = importlib.util.spec_from_file_location(
                f"plugins.{py_file.stem}", py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for name in dir(module):
                attr = getattr(module, name)
                if (isinstance(attr, type) and issubclass(attr, AssetPlugin)
                        and attr is not AssetPlugin and attr.name):
                    self.register(attr())
                    count += 1
        return count
```

### scanner.py — core pattern

```python
import hashlib
import json
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

HASH_CHUNK_SIZE = 65536  # 64 KiB read chunks

class FileStatus(Enum):
    NEW = auto()        # not in cache
    CHANGED = auto()    # hash differs from cache
    UNCHANGED = auto()  # hash matches cache

@dataclass
class ScannedFile:
    path: Path            # absolute path
    relative: Path        # relative to source_dir
    extension: str        # lowercase, with dot
    fingerprint: str      # SHA-256 hex digest
    status: FileStatus

def fingerprint_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(HASH_CHUNK_SIZE):
            h.update(chunk)
    return h.hexdigest()

class FingerprintCache:
    def __init__(self, path: Path):
        self._path = path
        self._data = json.loads(path.read_text()) if path.exists() else {}

    def get(self, rel: Path) -> str | None:
        return self._data.get(rel.as_posix())

    def set(self, rel: Path, fp: str) -> None:
        self._data[rel.as_posix()] = fp

    def save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(self._data, indent=2, sort_keys=True))

def scan(source_dir, extensions, cache):
    results = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        rel = path.relative_to(source_dir)
        fp = fingerprint_file(path)
        cached = cache.get(rel)
        status = (FileStatus.NEW if cached is None
                  else FileStatus.CHANGED if cached != fp
                  else FileStatus.UNCHANGED)
        results.append(ScannedFile(path, rel, path.suffix.lower(), fp, status))
    return results
```

### Writing a plugin

```python
# plugins/texture.py
from pipeline.plugin import AssetPlugin, AssetResult
from pathlib import Path

class TexturePlugin(AssetPlugin):
    name = "texture"
    extensions = [".png", ".jpg", ".tga", ".bmp"]

    def process(self, source: Path, output_dir: Path, settings: dict) -> AssetResult:
        output = output_dir / source.name
        # ... actual processing here ...
        return AssetResult(source=source, output=output)
```

### pipeline.toml

```toml
[pipeline]
source_dir = "assets/raw"
output_dir = "assets/processed"
cache_dir  = ".forge-cache"

[texture]
max_size = 2048
generate_mipmaps = true

[mesh]
deduplicate = true
```

### bundler.py — bundle packing and reading

```python
from pathlib import Path
from pipeline.bundler import BundleWriter, BundleReader, create_bundle

# Write a bundle
writer = BundleWriter(Path("game.forgepak"))
writer.add("textures/brick.png", brick_bytes)
writer.add_file(Path("hero.fmesh"), "meshes/hero.fmesh",
                dependencies=["textures/brick.png"])
manifest = writer.finalize()

# Read a bundle (random access)
with BundleReader(Path("game.forgepak")) as reader:
    data = reader.read("textures/brick.png")

# Bundle an entire directory
manifest = create_bundle(
    output_dir=Path("assets/processed"),
    bundle_path=Path("assets/bundles/game.forgepak"),
)
```

### CLI bundling

```bash
forge-pipeline bundle                              # bundle all processed assets
forge-pipeline bundle -o game.forgepak --level 9   # custom output, higher compression
forge-pipeline info game.forgepak                  # inspect bundle contents
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Using file timestamps for change detection | Use SHA-256 content hashes — timestamps break on git clone, CI, and file copy |
| Hardcoding plugin list in core code | Use file-based discovery with `importlib` — drop a `.py` file to add a type |
| Storing absolute paths in the cache | Use POSIX-style relative paths so the cache is portable across machines |
| Not validating plugin registration | Check for duplicate names and duplicate extensions — silent conflicts cause confusion |
| Missing `tomllib` fallback for Python < 3.11 | Guard with `sys.version_info` and fall back to `tomli` |
| Skipping `_`-prefixed plugin files | Convention: `_`-prefixed files are internal helpers, not plugins |

## Reference

Based on [Asset Lesson 01 — Pipeline Scaffold](../../../lessons/assets/01-pipeline-scaffold/)
and [Asset Lesson 05 — Asset Bundles](../../../lessons/assets/05-asset-bundles/).
