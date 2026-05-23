---
name: dev-asset-lesson
description: Add an asset pipeline lesson — hybrid Python + C track for asset processing, procedural geometry, and web frontend
argument-hint: "[number] [topic-name] [description]"
---

Create a new asset pipeline lesson. This is a **hybrid track** — the pipeline
orchestrator is Python, performance-critical processing uses compiled C tools
(meshoptimizer, MikkTSpace), and procedural geometry lives in a header-only C
library (`common/shapes/forge_shapes.h`).

**The goal is not just pedagogical.** Every library, tool, and pipeline
component built in an asset lesson must be production-quality — well-tested,
documented, and designed for reuse beyond the lesson. The project's own
`PLAN.md` has a "Project Integration" section where forge-gpu's existing
assets (models, textures, skyboxes) are processed through the pipeline we
build. So the pipeline, plugins, and C tools are not toy examples scoped to a
single lesson — they are the actual tooling this project depends on.

Concretely this means:

- **Libraries and tools are shared, not lesson-local.** Python code goes in
  `pipeline/`, C libraries go in `common/`, C tools go in `tools/`. The
  lesson directory contains the walkthrough, not the implementation.
- **Test thoroughly.** Every module gets a test suite (`tests/pipeline/` for
  Python, `tests/test_*.c` for C). Edge cases, error paths, and realistic
  inputs — not just happy-path smoke tests.
- **Design for integration.** The Python pipeline will process forge-gpu's
  own models and textures. The C mesh tool will be invoked by the pipeline
  as a subprocess. The shapes library is already used by GPU and physics
  lessons. Build APIs that work for real projects.
- **Don't cut corners for pedagogy.** If the correct approach requires more
  code, write more code. Simplifying for the lesson at the cost of
  correctness or reusability defeats the purpose.

**When to use this skill:**

- You need to teach asset import, processing, or optimization concepts
- A learner wants to build tooling that transforms raw art into GPU-ready formats
- The lesson involves texture compression, mesh optimization, or asset bundling
- The lesson adds a web UI for browsing, previewing, or configuring assets
- The lesson creates procedural geometry from parametric equations
- The lesson integrates third-party C libraries (meshoptimizer, MikkTSpace)

**Smart behavior:**

- Before creating a lesson, check if an existing asset lesson already covers it
- Asset lessons are tool-building lessons — every concept must produce a working
  CLI command, C tool, library, or web page
- Focus on *why* each processing step matters for GPU performance
- Cross-reference GPU lessons that consume the processed assets
- Determine the lesson type (Python, C tool, or C library) before scaffolding

## Arguments

The user (or you) can provide:

- **Number**: two-digit lesson number (e.g. 01, 02)
- **Topic name**: kebab-case (e.g. pipeline-scaffold, texture-processing)
- **Description**: what this teaches (e.g. "Plugin discovery, CLI entry point, TOML config")

If any are missing, infer from context or ask.

## Lesson Types

The asset pipeline track has three lesson types. Determine which type applies
before scaffolding.

### Type A: Python lessons

Pipeline scaffold, texture processing, asset bundles, web frontend. These add
functionality to the **shared `pipeline/` package** at the repo root (not
lesson-local code). The lesson directory contains only the README, diagrams,
example config, and sample assets.

**Directory structure:**

```text
pipeline/                     # shared library (repo root) — code goes HERE
  __init__.py
  __main__.py
  config.py, plugin.py, scanner.py, ...
  plugins/
    <type>.py                 # built-in plugins grow lesson by lesson
tests/
  pipeline/                   # tests for the shared library
    test_<module>.py
lessons/assets/NN-topic-name/
  README.md                   # lesson walkthrough pointing at pipeline/ code
  pipeline.toml               # example config for hands-on testing
  assets/                     # sample source files, diagrams
```

**Not added to CMakeLists.txt** — Python projects are not C targets.
**`pyproject.toml` is at the repo root** — one package for the whole pipeline.

### Type B: C tool lessons

Mesh processing with third-party C libraries (meshoptimizer, MikkTSpace). The
C tool is a standalone executable that the Python pipeline invokes as a
subprocess.

**Directory structure:**

```text
lessons/assets/NN-topic-name/
  README.md
  main.c                    # standalone C tool
  CMakeLists.txt            # builds the tool, fetches dependencies
  tests/
    test_<tool>.c           # C test suite
```

**Added to CMakeLists.txt** — C tools need a build target. Add under an
"Asset Pipeline Lessons" section (create it if needed, after Physics Lessons
or at the end before Tests).

### Type C: C library lessons

Procedural geometry and other header-only libraries that live in `common/`.
These produce a library, a test suite, and optionally a GPU lesson that
renders the output.

**Directory structure:**

```text
common/<lib>/
  forge_<lib>.h             # header-only library
  README.md                 # API reference
lessons/assets/NN-topic-name/
  README.md                 # lesson walkthrough (may also have a GPU demo)
  PLAN.md                   # main.c decomposition (if GPU demo included)
  main.c                    # GPU showcase program (optional)
  CMakeLists.txt
  shaders/                  # if GPU demo
  assets/
tests/
  test_<lib>.c              # comprehensive test suite
```

**Added to CMakeLists.txt** — register the test target and any GPU demo.

## Steps

### 1. Analyze what's needed

- **Determine lesson type**: Python (A), C tool (B), or C library (C)?
- **Check existing asset lessons**: Is there already a lesson for this topic?
- **Identify the scope**: What specific pipeline concepts does this lesson cover?
- **Find cross-references**: Which GPU/engine/math lessons relate?
- **Check PLAN.md**: Where does this lesson fit in the asset pipeline track?

### 2. Create the lesson directory

Follow the directory structure for the determined lesson type (A, B, or C).

### 3. Create the lesson content

#### For Python lessons (Type A)

**Package conventions:**

- **Python 3.10+** — Use modern Python features (type hints, match statements,
  dataclasses, pathlib)
- **CLI**: Use `argparse` or `click` for command-line interface
- **Config**: TOML for project/asset configuration (`tomllib` in 3.11+, or
  `tomli` as fallback)
- **Testing**: pytest for unit tests
- **Naming**: `snake_case` for modules and functions, `PascalCase` for classes
- **No global state** — Pass configuration explicitly

Create `pyproject.toml`:

```toml
[project]
name = "forge-asset-pipeline"
version = "0.1.0"
description = "Asset processing pipeline for forge-gpu"
requires-python = ">=3.10"
dependencies = [
    # Add per-lesson dependencies here
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.4",
]

[project.scripts]
forge-pipeline = "pipeline.__main__:main"
```

#### For C tool lessons (Type B)

- Follow all forge-gpu C conventions (C99, naming, error handling)
- Use `FetchContent` to pull third-party libraries (meshoptimizer, MikkTSpace)
- Build a standalone CLI tool that reads input files and writes output files
- The Python pipeline invokes the tool as a subprocess
- Test with forge-gpu's existing test harness pattern

#### For C library lessons (Type C)

- Follow the `forge_math.h` pattern: header-only, `static inline`,
  thorough inline documentation
- Use `SDL_malloc`/`SDL_free` (not `malloc`/`free`)
- Use `forge_math.h` types (`vec3`, `vec2`, `mat4`, `quat`)
- Create a comprehensive test suite following `tests/test_math.c` pattern
- Optionally include a GPU demo that renders the library output
- For files over 800 lines, use the chunked-write pattern (mandatory)

### 4. Create `README.md`

Structure varies by lesson type but always includes:

- What you'll learn (bullet list)
- Result (screenshot, CLI output, or demo)
- Main explanation with diagrams
- Code walkthrough
- Key concepts
- Cross-references to other tracks
- Exercises
- Further reading

### 5. Update project files

- **`README.md` (root)**: Add a row to the asset lessons table
- **`lessons/assets/README.md`**: Add a row to the lessons table
- **`PLAN.md`**: Check off the asset lesson entry
- **`CMakeLists.txt` (root)**: Add targets for C tools/libraries (Types B and C
  only — Python lessons are not registered here)

### 6. Cross-reference other lessons

- **Find related GPU lessons**: Which rendering features consume these assets?
- **Find related engine lessons**: Build systems, dependency management
- **Find related math lessons**: Vectors, parametric equations, trigonometry
- **Update those lesson READMEs**: Add cross-reference notes
- **Update asset lesson README**: List related lessons in "Where it connects"

### 7. Test

**Python lessons:**

```bash
cd lessons/assets/NN-topic-name
pip install -e ".[dev]"
pytest
ruff check .
```

**C tool/library lessons:**

```bash
cmake -B build
cmake --build build --config Debug --target <test-target>
ctest --test-dir build -R <test-name>
```

Use a Task agent with `model: "haiku"` for build commands per project
conventions.

### 8. Run markdown linting

```bash
npx markdownlint-cli2 "**/*.md"
```

## Asset Lesson Conventions

### Scope

- **Core pipeline** (Python) — CLI scaffold, plugin discovery, configuration,
  scanning, fingerprinting
- **Texture processing** (Python) — Resize, compress, mipmap generation,
  format conversion
- **Mesh processing** (C tool) — Vertex deduplication, index optimization,
  tangent generation (MikkTSpace), LOD generation (meshoptimizer), binary output
- **Procedural geometry** (C library) — Parametric surface generation, smooth
  and flat normals, struct-of-arrays GPU layout
- **Asset bundles** (Python) — Packing, compression, table of contents,
  dependency tracking
- **Web frontend** (Python) — Asset browser, 3D preview, import settings
  editor, scene editor

### Python style

- Python 3.10+ with type hints
- `snake_case` for functions and variables, `PascalCase` for classes
- Docstrings on public functions and classes
- `pathlib.Path` for file paths (not string concatenation)
- `dataclasses` or `attrs` for structured data
- Lint with Ruff (same config as existing `pyproject.toml` in repo root)

### C style

Follow the same conventions as all forge-gpu code:

- C99, matching SDL's style
- `ForgeShapes` prefix for public types, `forge_shapes_` for functions
  (adjust prefix per library)
- `PascalCase` for typedefs, `lowercase_snake_case` for locals
- `UPPER_SNAKE_CASE` for `#define` constants
- No magic numbers — `#define` or `enum` everything
- `SDL_malloc`/`SDL_free` — not `malloc`/`free`
- Extensive comments explaining *why* and *purpose*

### Plugin architecture

The Python pipeline uses a plugin system where each asset type registers a
processor. C tools are invoked as subprocesses by the Python plugin:

```python
import subprocess
from pathlib import Path

class MeshPlugin(AssetPlugin):
    """Mesh processing plugin — invokes compiled C tool."""
    name = "mesh"
    extensions = [".gltf", ".glb", ".obj"]

    def process(self, source: Path, config: dict) -> AssetResult:
        result = subprocess.run(
            ["forge-mesh-tool", str(source), "--output", str(output)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise ProcessingError(result.stderr)
        return AssetResult(source=source, output=output, metadata={...})
```

### Incremental builds

Every processing step must support incremental builds:

1. **Fingerprint** source files (content hash, not timestamp)
2. **Compare** against cached fingerprints from the last build
3. **Skip** unchanged assets
4. **Track dependencies** — if a texture changes, re-process meshes that
   reference it

### Configuration

Use TOML for pipeline and per-asset configuration:

```toml
# pipeline.toml — project-level config
[pipeline]
source_dir = "assets/raw"
output_dir = "assets/processed"
bundle_dir = "assets/bundles"

[texture]
default_format = "bc7"
max_size = 2048
generate_mipmaps = true

[mesh]
deduplicate = true
generate_tangents = true
lod_levels = [1.0, 0.5, 0.25]
```

### Tone

Asset pipeline lessons should be practical and tool-focused. Pipeline tooling
is infrastructure that enables art and rendering — treat it with the same
rigor as the rendering code it serves. The output of these lessons is not
disposable teaching material; it is production tooling that forge-gpu itself
will use to process its own assets.

- **Name the techniques and formats** — BC7, KTX2, glTF, meshoptimizer,
  MikkTSpace — named tools and formats carry weight and help readers find
  documentation
- **Show the data flow** — Diagrams showing source -> process -> output are
  essential for pipeline lessons
- **Measure improvement** — Show file sizes, load times, or vertex counts
  before and after processing
- **Connect to GPU** — Always explain how the processed output maps to GPU
  concepts (texture formats, vertex layouts, draw calls)
- **Build for real use** — Every API, CLI flag, and config option should work
  for a real project, not just the lesson's sample assets

## Example: Pipeline Scaffold Lesson (Type A — Python)

1. **Scope**: CLI entry point, plugin discovery, asset scanning, fingerprinting,
   TOML configuration
2. **Create**: `lessons/assets/01-pipeline-scaffold/`
3. **Package**: `pipeline/` with `__main__.py`, `config.py`, `scanner.py`,
   `plugin.py`
4. **Program**: CLI that scans a directory for assets, fingerprints them, and
   reports what would be processed. No actual processing yet.
5. **README**: Explain plugin architecture, fingerprinting, TOML config, CLI
   design
6. **Exercises**: Add a new file type to the scanner, implement cache
   invalidation, add `--verbose` output

## Example: Mesh Processing Lesson (Type B — C tool)

1. **Scope**: meshoptimizer for vertex/index optimization, MikkTSpace for
   tangent generation, binary output format, LOD generation
2. **Create**: `lessons/assets/03-mesh-processing/`
3. **Tool**: `main.c` that reads glTF/OBJ, processes with meshoptimizer and
   MikkTSpace, writes optimized binary output
4. **CMake**: FetchContent for meshoptimizer and MikkTSpace
5. **Python plugin**: `plugins/mesh.py` invokes the compiled tool as subprocess
6. **README**: Explain vertex cache optimization, overdraw optimization, tangent
   space, LOD simplification metrics
7. **Exercises**: Add vertex quantization, compare draw call performance before
   and after optimization

## Example: Procedural Geometry Lesson (Type C — C library)

1. **Scope**: `forge_shapes.h` — parametric surface generation (sphere,
   icosphere, cylinder, cone, torus, plane, cube, capsule), struct-of-arrays
   layout, smooth vs flat normals
2. **Create**: `common/shapes/forge_shapes.h`, `common/shapes/README.md`,
   `lessons/assets/04-procedural-geometry/`, `tests/test_shapes.c`
3. **Library**: Header-only with `FORGE_SHAPES_IMPLEMENTATION` guard
4. **GPU demo**: Five-shape showcase with Blinn-Phong lighting
5. **Tests**: 28 tests covering vertex counts, normals, UVs, winding, memory
6. **README**: Parametric surfaces, slices/stacks, seam duplication, smooth vs
   flat normals, struct-of-arrays vs interleaved

## When NOT to Create an Asset Lesson

- The topic is covered by an existing asset lesson
- The concept is about GPU rendering only (belongs in a GPU lesson)
- The concept is about C fundamentals only (belongs in an engine lesson)
- The concept is pure math only (belongs in a math lesson)
- The topic is too narrow for a full lesson (add to an existing lesson instead)

In these cases, update existing documentation or plan for later.

## Tips

- **Start with the CLI** — Get the command-line interface working first, then
  add processing logic. A well-structured CLI with no-op plugins is a solid
  foundation.
- **Test with real assets** — Use assets from existing GPU lessons as test
  inputs. This validates that the pipeline produces output the C code can
  actually consume.
- **Fingerprint, don't timestamp** — Content hashes are deterministic and
  portable. Timestamps break on copy, git clone, and CI.
- **Show before/after** — File size comparisons, vertex count reductions, and
  load time improvements make the value of the pipeline concrete.
- **Keep the web UI simple** — Static HTML/CSS/JS served by Python. No npm,
  no webpack, no framework. The pipeline is the lesson, not the frontend stack.
- **Chunked writes for large C files** — `forge_shapes.h` and GPU demo
  `main.c` will exceed 800 lines. Use the chunked-write pattern per
  `.claude/large-file-strategy.md`.
