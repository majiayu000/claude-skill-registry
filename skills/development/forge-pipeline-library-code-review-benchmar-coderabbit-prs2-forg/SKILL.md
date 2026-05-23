---
name: forge-pipeline-library
description: Use the forge-gpu asset pipeline library — a pip-installable Python package for scanning, fingerprinting, processing, and bundling game assets with a plugin architecture. Use when working with pipeline code, writing plugins, processing textures/meshes/animations, bundling assets, or extending the pipeline CLI.
---

# forge-pipeline-library

The forge asset pipeline is a pip-installable Python package at the repo root
(`pipeline/`). It processes raw game assets (textures, meshes, animations)
into GPU-ready formats with incremental builds driven by content hashing.

## When to use this skill

- Writing or modifying pipeline code in `pipeline/`
- Creating a new asset plugin (texture, mesh, animation, or custom)
- Processing assets with the `forge-pipeline` CLI
- Bundling processed assets into `.forgepak` archives
- Debugging pipeline configuration or plugin discovery
- Extending the pipeline with new file types or processing steps
- Loading pipeline-processed assets in C/GPU code
- Writing tests for pipeline modules

## Installation

```bash
# Install in development mode (editable) from the repo root
pip install -e ".[dev]"

# Verify
forge-pipeline --help
```

The package is defined in `pyproject.toml` at the repo root. The CLI entry
point is `forge-pipeline`, which maps to `pipeline.__main__:main`.

## Package structure

```text
pipeline/
├── __init__.py          # Package version (__version__ = "0.1.0")
├── __main__.py          # CLI entry point — argparse, scan, process, bundle
├── config.py            # TOML config loader → PipelineConfig dataclass
├── plugin.py            # AssetPlugin base class, PluginRegistry, discovery
├── scanner.py           # File scanning, SHA-256 fingerprinting, cache
├── bundler.py           # .forgepak bundle writer/reader, dependency graph
└── plugins/
    ├── __init__.py
    ├── texture.py       # TexturePlugin — resize, mipmaps, GPU compression
    ├── mesh.py          # MeshPlugin — deduplicate, optimize, tangents, LOD
    └── animation.py     # AnimationPlugin — glTF animation → .fanim binary
```

## Core modules

### config.py — Configuration

```python
from pipeline.config import load_config, default_config, PipelineConfig, ConfigError

# Load from TOML file
config = load_config(Path("pipeline.toml"))

# Use defaults if no file exists
config = default_config()

# Access typed fields
config.source_dir   # Path — where raw assets live
config.output_dir   # Path — where processed files go
config.cache_dir    # Path — fingerprint cache location
config.plugin_settings  # dict[str, dict] — per-plugin config sections
config.raw          # dict — full parsed TOML for forward-compatibility
```

**TOML structure:**

```toml
[pipeline]
source_dir = "assets/raw"
output_dir = "assets/processed"
cache_dir  = ".forge-cache"

[texture]
max_size = 2048
generate_mipmaps = true
output_format = "png"
compression = "none"        # none, basisu, or astc

[mesh]
deduplicate = true
optimize = true
generate_tangents = true
lod_levels = [1.0, 0.5, 0.25]

[animation]
tool_path = ""              # override forge-anim-tool location
```

Per-plugin sections (everything except `[pipeline]`) are passed to plugins
as the `settings` dict in their `process()` method.

### plugin.py — Plugin system

```python
from pipeline.plugin import AssetPlugin, AssetResult, PluginRegistry

# Base class — subclass this to create a new plugin
class MyPlugin(AssetPlugin):
    name = "my-type"
    extensions = [".xyz", ".abc"]

    def process(self, source: Path, output_dir: Path, settings: dict) -> AssetResult:
        output = output_dir / f"{source.stem}.processed"
        # ... do work ...
        return AssetResult(source=source, output=output, metadata={"key": "val"})

# Registry — discovers and stores plugins
registry = PluginRegistry()
registry.register(MyPlugin())                # manual registration
count = registry.discover(Path("plugins/"))  # file-based discovery

# Lookup
plugins = registry.get_by_extension(".xyz")  # returns list[AssetPlugin]
plugin = registry.get_by_name("my-type")     # returns AssetPlugin | None
all_exts = registry.supported_extensions     # set[str]
all_plugins = registry.plugins               # list[AssetPlugin]
```

**Discovery rules:**

- Scans `*.py` files in a directory (skips `_`-prefixed files)
- Imports each module, finds `AssetPlugin` subclasses with a non-empty `name`
- Only registers classes defined in that module (not imported base classes)
- Multiple plugins can handle the same extension (all are invoked)

### scanner.py — Fingerprinting and change detection

```python
from pipeline.scanner import scan, fingerprint_file, FingerprintCache, FileStatus, ScannedFile

# Fingerprint a single file
digest = fingerprint_file(Path("texture.png"))  # SHA-256 hex string

# Load or create a cache
cache = FingerprintCache(Path(".forge-cache/fingerprints.json"))
cached_hash = cache.get(Path("textures/brick.png"))  # str | None
cache.set(Path("textures/brick.png"), digest)
cache.save()  # persist to disk

# Scan a directory
files: list[ScannedFile] = scan(
    source_dir=Path("assets/raw"),
    supported_extensions={".png", ".jpg", ".obj", ".gltf"},
    cache=cache,
)

# Each ScannedFile has:
for f in files:
    f.path         # Path — absolute path
    f.relative     # Path — relative to source_dir
    f.extension    # str — lowercase with dot
    f.fingerprint  # str — SHA-256 hex
    f.status       # FileStatus.NEW | CHANGED | UNCHANGED
```

**Why content hashes, not timestamps:**

- Deterministic — same bytes always produce the same hash
- Portable — survives git clone, file copies, CI
- Correct — touching a file without changing content skips reprocessing

### bundler.py — Asset bundles

```python
from pipeline.bundler import (
    BundleWriter, BundleReader, BundleManifest, BundleEntry,
    DependencyGraph, create_bundle, BundleError, BundleFormatError,
)

# Write a bundle
writer = BundleWriter(Path("game.forgepak"), compression_level=3)
writer.add("textures/brick.png", png_bytes)
writer.add_file(Path("hero.fmesh"), "meshes/hero.fmesh",
                dependencies=["textures/brick.png"])
manifest = writer.finalize()

# Read a bundle (random access)
with BundleReader(Path("game.forgepak")) as reader:
    data = reader.read("textures/brick.png")
    paths = reader.manifest.paths
    entry = reader.manifest.get("meshes/hero.fmesh")

# Bundle an entire directory
manifest = create_bundle(
    output_dir=Path("assets/processed"),
    bundle_path=Path("game.forgepak"),
    compress=True,
    compression_level=3,
    patterns=["*.png", "*.fmesh"],  # optional glob filters
)

# Dependency graph (from .meta.json sidecars)
graph = DependencyGraph.from_meta_files(Path("assets/processed"))
deps = graph.dependencies_of("meshes/hero.fmesh")
dependents = graph.dependents_of("textures/brick.png")
order = graph.topological_order()
```

**Bundle format (`.forgepak`):**

- Header (24 bytes): magic `FPAK`, version, entry count, TOC offset/size
- Entry data: each entry compressed independently with zstd
- TOC at end: zstd-compressed JSON array of entry metadata
- O(1) random access — seek to offset, decompress one entry

## Built-in plugins

### TexturePlugin (`plugins/texture.py`)

Handles: `.png`, `.jpg`, `.jpeg`, `.tga`, `.bmp`

Processing steps:

1. Load with Pillow, convert to RGB/RGBA
2. Resize to fit `max_size` (preserves aspect ratio)
3. Save in `output_format` (png, jpg, bmp)
4. Generate mipmap chain (halved sizes down to 1x1)
5. Optional GPU compression via `basisu` (KTX2) or `astcenc` (ASTC)
6. Write `.meta.json` sidecar

Settings (`[texture]` in pipeline.toml):

| Setting | Default | Description |
|---|---|---|
| `max_size` | 2048 | Clamp width/height |
| `generate_mipmaps` | true | Create mip chain |
| `output_format` | "png" | Output format |
| `jpg_quality` | 90 | JPEG quality (1-100) |
| `compression` | "none" | none, basisu, astc |
| `basisu_format` | "uastc" | etc1s or uastc |
| `basisu_quality` | 128 | 1-255 |
| `astc_block_size` | "6x6" | 4x4, 5x5, 6x6, 8x8 |
| `astc_quality` | "medium" | fastest..exhaustive |
| `normal_map` | false | BC5/linear encoding |

### MeshPlugin (`plugins/mesh.py`)

Handles: `.obj`, `.gltf`, `.glb`

Invokes `forge-mesh-tool` (compiled C binary) as a subprocess for:

1. Vertex deduplication
2. Index/vertex cache optimization (meshoptimizer)
3. MikkTSpace tangent generation
4. LOD simplification at configurable ratios

Output: `.fmesh` binary + `.meta.json` + optional `.fmat` material sidecar

Settings (`[mesh]` in pipeline.toml):

| Setting | Default | Description |
|---|---|---|
| `deduplicate` | true | Remove duplicate vertices |
| `optimize` | true | Cache-friendly index reorder |
| `generate_tangents` | true | MikkTSpace tangent frames |
| `lod_levels` | [1.0] | Target triangle ratios |
| `tool_path` | "" | Override tool location |

Falls back gracefully if the C tool is not installed.

### AnimationPlugin (`plugins/animation.py`)

Handles: `.gltf`, `.glb`

Invokes `forge-anim-tool` (compiled C binary) to extract glTF animation clips
into `.fanim` binary files with channels, samplers, and keyframe data.

Settings (`[animation]` in pipeline.toml):

| Setting | Default | Description |
|---|---|---|
| `tool_path` | "" | Override tool location |

Multiple plugins can handle the same extension — both `MeshPlugin` and
`AnimationPlugin` register `.gltf`/`.glb`, so a single glTF file produces
both a `.fmesh` and a `.fanim`.

## CLI usage

```bash
# Scan and process all assets (uses pipeline.toml or defaults)
forge-pipeline

# Dry run — scan and report without processing
forge-pipeline --dry-run

# Verbose output
forge-pipeline -v

# Custom config file
forge-pipeline -c my-config.toml

# Override source directory
forge-pipeline --source-dir path/to/assets

# Process only one plugin type
forge-pipeline --plugin texture

# Bundle processed assets
forge-pipeline bundle
forge-pipeline bundle -o game.forgepak --level 9
forge-pipeline bundle --pattern "*.png" --pattern "*.fmesh"

# Inspect a bundle
forge-pipeline info game.forgepak
```

## Writing a new plugin

1. Create `pipeline/plugins/my_type.py`
2. Subclass `AssetPlugin`, set `name` and `extensions`
3. Implement `process()` returning an `AssetResult`
4. Add a `[my_type]` section to `pipeline.toml` for settings
5. Add tests in `tests/pipeline/test_my_type.py`

```python
"""My custom asset type plugin."""
from pathlib import Path
from pipeline.plugin import AssetPlugin, AssetResult

class MyTypePlugin(AssetPlugin):
    name = "my_type"
    extensions = [".xyz"]

    def process(self, source: Path, output_dir: Path, settings: dict) -> AssetResult:
        threshold = int(settings.get("threshold", 100))
        output = output_dir / f"{source.stem}.processed"
        # ... transform source into output ...
        return AssetResult(
            source=source,
            output=output,
            metadata={"threshold": threshold, "processed": True},
        )
```

The plugin is auto-discovered — no registration code needed.

## Settings-aware caching

The pipeline combines each file's content hash with a digest of its plugin
settings. Changing a setting (e.g. `max_size` from 2048 to 1024) invalidates
previously processed assets even if the source file hasn't changed.

```python
# From __main__.py — the combined fingerprint
combined = sha256(f"{content_hash}:{json.dumps(settings, sort_keys=True)}")
```

## Metadata sidecars

Every plugin writes a `.meta.json` file alongside its output. Sidecars
record the source file, output dimensions, processing settings, and
dependency information. The bundler reads these to build the dependency
graph for correct processing order and invalidation.

## Testing

```bash
# Run all pipeline tests
pytest tests/pipeline/ -v

# Run a specific test module
pytest tests/pipeline/test_scanner.py -v

# Lint
ruff check pipeline/ tests/pipeline/
ruff format --check pipeline/ tests/pipeline/
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Using timestamps for change detection | Use SHA-256 content hashes — timestamps break on git clone |
| Hardcoding plugin list in core code | Use file-based discovery — drop a `.py` file to add a type |
| Storing absolute paths in the cache | Use POSIX-style relative paths for portability |
| Not validating plugin registration | Check for duplicate names — silent conflicts cause confusion |
| Forgetting `tomllib` fallback for Python < 3.11 | Guard with `sys.version_info`, fall back to `tomli` |
| Skipping `_`-prefixed plugin files | Convention: `_`-prefixed files are internal helpers |
| Not writing `.meta.json` sidecars | Bundler needs them for dependency graph construction |
| Single Write call for large files | Use chunked-write pattern for files over 800 lines |

## Cross-references

| Lesson | What it covers |
|---|---|
| [Asset 01 — Pipeline Scaffold](../../../lessons/assets/01-pipeline-scaffold/) | CLI, config, scanner, plugin system |
| [Asset 02 — Texture Processing](../../../lessons/assets/02-texture-processing/) | TexturePlugin, mipmaps, GPU compression |
| [Asset 03 — Mesh Processing](../../../lessons/assets/03-mesh-processing/) | MeshPlugin, meshoptimizer, MikkTSpace |
| [Asset 04 — Procedural Geometry](../../../lessons/assets/04-procedural-geometry/) | forge_shapes.h C library |
| [Asset 05 — Asset Bundles](../../../lessons/assets/05-asset-bundles/) | BundleWriter/Reader, .forgepak format |
| [Asset 06 — Loading Processed Assets](../../../lessons/assets/06-loading-processed-assets/) | C-side .fmesh/.meta.json loading |
| [Asset 07 — Materials](../../../lessons/assets/07-materials/) | .fmat material sidecars, PBR pipeline |
| [Asset 08 — Animations](../../../lessons/assets/08-animations/) | AnimationPlugin, .fanim binary format |
| [GPU Lesson 05 — Mipmaps](../../../lessons/gpu/05-mipmaps/) | How GPU uses mip chains |
| [GPU Lesson 17 — Normal Maps](../../../lessons/gpu/17-normal-maps/) | Tangent space in shaders |
| [GPU Lesson 39 — Pipeline Assets](../../../lessons/gpu/39-pipeline-processed-assets/) | Loading .fmesh in GPU code |
