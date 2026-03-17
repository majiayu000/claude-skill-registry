---
name: archive-reprocessing
description: Flexible, version-tracked reprocessing system for archive transformations using design patterns (Strategy, Template Method, Observer). Activate when working with tools/scripts/lib/, reprocessing scripts, transform versions, archive transformations, metadata transformers, or incremental processing workflows.
---

# Archive Reprocessing System

**Auto-activates when**: Working with `tools/scripts/lib/`, reprocessing scripts, transform versions, or discussing archive transformations.

## Quick Reference

**When to use:**
- New transformations on existing archives (flattening, normalization)
- After version bumps (v1.0 → v1.1)
- Vocabulary/model updates
- Regenerating derived outputs

**When NOT to use:**
- Adding new videos → `ingest_youtube.py`
- Rebuilding Qdrant cache → `reingest_from_archive.py`

**Scripts:**
- `reprocess_qdrant_metadata.py` - Flattening + weights (fast, no LLM)
- `reprocess_normalized_tags.py` - Tag normalization (slow, LLM calls)

**Common commands:**
```bash
# Dry run (test 10 archives)
uv run python tools/scripts/reprocess_qdrant_metadata.py --dry-run --limit 10

# Full run
uv run python tools/scripts/reprocess_qdrant_metadata.py
```

## Design

Strategy + Template Method + Observer patterns for incremental, version-tracked reprocessing:
- Pluggable transformers (Strategy) eliminate copy-paste
- Template Method for consistent workflows
- Observer hooks for progress tracking
- Semantic versioning works during development (not git-dependent)
- Incremental processing skips unchanged archives

## Core Components

### 1. Version Registry (`transform_versions.py`)

```python
VERSIONS = {
    "normalizer": "v1.0",
    "vocabulary": "v1",
    "qdrant_flattener": "v1.0",
    "weight_calculator": "v1.0",
    "llm_model": "claude-3-5-haiku-20241022",
}
```

Bump versions on: logic changes (v1.0 → v1.1), vocabulary updates (v1 → v2), breaking changes (v1.x → v2.0)

### 2. Metadata Transformers (`metadata_transformers.py`)

```python
from tools.scripts.lib.metadata_transformers import (
    QdrantMetadataFlattener,
    RecommendationWeightCalculator,
    create_qdrant_transformer,
)

# Pre-built
transformer = create_qdrant_transformer()
metadata = transformer.transform(archive_data)

# Custom
class MyTransformer(BaseTransformer):
    def get_version(self) -> str:
        return get_version("my_transformer")

    def transform(self, archive_data: dict) -> dict:
        return {"transformed": True}
```

### 3. Reprocessing Pipeline (`reprocessing_pipeline.py`)

```python
from tools.scripts.lib.reprocessing_pipeline import (
    BaseReprocessingPipeline,
    ConsoleHooks,
)

class MyPipeline(BaseReprocessingPipeline):
    def get_output_type(self) -> str:
        return "my_transformation_v1"

    def get_version_keys(self) -> list[str]:
        return ["my_transformer"]

    def process_archive(self, archive: YouTubeArchive) -> str:
        return json.dumps(result)

pipeline = MyPipeline(hooks=ConsoleHooks())
stats = pipeline.run(limit=10)
```

## Common Tasks

```bash
# Dry run (test)
uv run python tools/scripts/reprocess_qdrant_metadata.py --dry-run --limit 10
uv run python tools/scripts/reprocess_normalized_tags.py --dry-run --limit 3

# Full run (~12min Qdrant, ~2hr normalization for 470 videos)
uv run python tools/scripts/reprocess_qdrant_metadata.py
uv run python tools/scripts/reprocess_normalized_tags.py

# After version bump (only processes stale archives)
# Edit: tools/scripts/lib/transform_versions.py → "normalizer": "v1.1"
uv run python tools/scripts/reprocess_normalized_tags.py

# Options
--no-context     # Skip semantic retrieval (faster, lower quality)
--no-vocabulary  # Skip vocabulary normalization
```

## Archive Data Structure

```json
{
  "llm_outputs": [
    {"output_type": "tags", "cost_usd": 0.0012, "model": "claude-3-5-haiku-20241022"}
  ],
  "derived_outputs": [
    {
      "output_type": "normalized_metadata_v1",
      "transformer_version": "v1.0+v1",
      "transform_manifest": {"normalizer": "v1.0", "vocabulary": "v1"},
      "source_outputs": ["tags"]
    }
  ]
}
```

`llm_outputs` cost money (permanent), `derived_outputs` free to regenerate (version-tracked)

## Incremental Processing

Staleness detection: compare stored `transform_manifest` to current `VERSIONS`. Reprocess if changed, skip if match.

**Performance:** First run (all 470): ~12min Qdrant / ~2hr normalization. Subsequent runs: ~5s (skip if current). Version bump: only affected archives.


## Creating New Transformations

**Steps:**
1. Add version to `transform_versions.py`: `"my_transformer": "v1.0"`
2. Create transformer class with `get_version()` and `transform()` methods
3. Create pipeline script extending `BaseReprocessingPipeline`

```python
# Transformer
class MyTransformer(BaseTransformer):
    def get_version(self) -> str:
        return get_version("my_transformer")

    def transform(self, archive_data: dict) -> dict:
        return {"result": "value"}

# Pipeline
class MyReprocessor(BaseReprocessingPipeline):
    def get_output_type(self) -> str:
        return "my_output_v1"

    def get_version_keys(self) -> list[str]:
        return ["my_transformer"]

    def process_archive(self, archive: YouTubeArchive) -> str:
        return json.dumps(MyTransformer().transform(archive.model_dump()))
```

## Archive Service Integration

```python
from tools.services.archive import create_local_archive_writer
from tools.scripts.lib.transform_versions import get_transform_manifest

writer = create_local_archive_writer()

# Add
writer.add_derived_output(
    video_id="abc123",
    output_type="my_transformation_v1",
    output_value=json.dumps(result),
    transformer_version="v1.0",
    transform_manifest=get_transform_manifest(),
    source_outputs=["tags"],
)

# Retrieve
archive = writer.get("abc123")
derived = archive.get_latest_derived_output("my_transformation_v1")
```

## Observer Hooks

```python
class MetricsHooks:
    def on_start(self, total: int):
        print(f"Starting {total} archives")
    def on_archive_success(self, video_id: str, elapsed: float):
        print(f"{video_id}: {elapsed:.2f}s")
    def on_complete(self, stats: dict):
        print(f"Done: {stats}")

pipeline = MyPipeline(hooks=MetricsHooks())
```

## Documentation

- `tools/scripts/lib/README.md` - Complete system docs
- `tools/scripts/lib/QUICKSTART.md` - Quick reference
- `lessons/lesson-010/COMPLETE.md` - Tag normalization lesson
