---
name: sfx-catalog
description: >
  Sound effects management for Horus's filmmaking pipeline. Catalogs audio files
  with acoustic analysis, provides semantic search via memory integration, tracks
  usage patterns, and generates missing SFX. Makes sound effects discoverable,
  reusable, and learnable through the Memory First pattern.
allowed-tools: [Bash, Read, Write]
triggers:
  - catalog sfx
  - search sound effects
  - find sfx
  - sound effect library
  - audio library catalog
  - sfx search
  - record sfx usage
  - generate sound effect
metadata:
  short-description: Sound effects cataloging, search, and learning system
  version: "0.1.0"
  author: "Horus"
---

# sfx-catalog

Professional sound effects cataloging and management system for Horus's filmmaking pipeline.

> **Mission**: Make the right sound effect available at the right time, learning from every use.

## Quick Start

```bash
cd .pi/skills/sfx-catalog

# Catalog your SFX library
./run.sh catalog /mnt/storage12tb/media/sfx/ --output library.json

# Ingest into memory
./run.sh ingest library.json

# Search for sound effects
./run.sh search "door creak"

# Check system status
./run.sh status
```

## Problem Statement

Horus has a professional library of 166 studio-quality 3D sound effects, but they're numbered generically:

- `01-pro_studio_library-3d_sound_effect_1.mp3`
- `02-pro_studio_library-3d_sound_effect_2.mp3`
- ...

**Challenges:**

1. **Not searchable** - Generic filenames, no metadata
2. **Not reusable** - Can't remember which sounds work for which scenes
3. **Not learnable** - No pattern recognition across projects

**Solution**: The sfx-catalog system makes sound effects **discoverable, reusable, and learnable**.

## Core Features

### 1. Audio Analysis

Extracts technical characteristics from MP3 files:

- Duration, frequency profile, envelope (ADSR)
- Loudness metrics, harmonic content
- Automatic categorization (impact, ambient, foley, etc.)

### 2. Semantic Search

Natural language queries powered by memory integration:

```bash
./run.sh search "deep ominous thunder"
# Returns ranked results with similarity scores
```

### 3. Memory First

Learns from prior usage to improve recommendations:

```bash
./run.sh recall-usage "tense apartment entrance"
# Returns SFX successfully used in similar scenes before
```

### 4. Usage Tracking

Records context for every SFX selection:

```bash
./run.sh record-usage \
    --sfx-id abc123 \
    --project "Dark Horizon" \
    --scene "INT. APARTMENT - Sarah enters cautiously" \
    --rationale "Adds tension to entrance"
```

### 5. On-Demand Generation

Creates missing sound effects via AI when library lacks options:

```bash
./run.sh generate "metallic door slam" --duration 2.5 --ingest
```

## Integration Points

### [`create-movie`](../create-movie/SKILL.md)

Automatically selects and applies SFX during movie generation:

```python
# In create-movie workflow
from sfx_catalog.query_engine import SFXQueryEngine

engine = SFXQueryEngine(scope="horus_lore")

# Memory First: Check for prior usage
sfx = engine.recall_usage(scene_description)

# Fallback: Semantic search
if not sfx:
    sfx = engine.search(query, categories, duration_range)

# Record for future learning
engine.record_usage(sfx_id, project, scene, timestamp, rationale)
```

### [`create-storyboard`](../create-storyboard/SKILL.md)

Suggests sound effects during storyboard planning:

```python
# During storyboard phase
suggestions = suggest_sfx_for_shot(shot)
# Returns natural language recommendations with alternatives
```

## Architecture

High-level system design:

```
┌─────────────────┐
│ 166 MP3 Files   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│ Audio Analyzer  │────►│ Content Class.   │
│ (librosa)       │     │ (rule-based)     │
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ Metadata Gen.    │
                        │ (LLM-assisted)   │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ JSON Manifest    │
                        └────────┬─────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────┐
│          ArangoDB Memory                │
│  ┌────────────┐  ┌────────────────┐    │
│  │sfx_library │  │  sfx_usage     │    │
│  │(catalog)   │  │  (tracking)    │    │
│  └────────────┘  └────────────────┘    │
│  ┌────────────┐                         │
│  │sfx_generated                         │
│  │(cache)     │                         │
│  └────────────┘                         │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│ Query Engine    │ ◄──── create-movie, create-storyboard
│ (multi-strategy)│
└─────────────────┘
```

**Deep Dive**: See [`ARCHITECTURE.md`](ARCHITECTURE.md) for detailed component specifications.

## Memory Schema

SFX data is stored in ArangoDB with three main collections:

### `sfx_library` - Sound Effect Catalog

```json
{
  "_key": "sfx_abc123",
  "file_path": "/mnt/storage12tb/media/sfx/...",
  "description": "Deep, punchy impact with quick attack",
  "categories": ["impact", "low_frequency"],
  "audio_features": {
    "duration_seconds": 2.34,
    "envelope": {...},
    "frequency_profile": {...}
  },
  "embedding": [...],
  "usage_count": 5
}
```

### `sfx_usage` - Usage History

```json
{
  "sfx_id": "sfx_library/sfx_abc123",
  "project_name": "Dark Horizon",
  "scene_description": "INT. APARTMENT - Tense entrance",
  "timestamp_in_scene": 2.5,
  "rationale": "Adds atmosphere and tension"
}
```

### `sfx_generated` - Generation Cache

```json
{
  "prompt": "metallic door creak",
  "file_path": "/mnt/.../generated/door_creak.mp3",
  "reuse_count": 3,
  "user_approved": true
}
```

**Deep Dive**: See [`MEMORY_SCHEMA.md`](MEMORY_SCHEMA.md) for complete schema, indices, and query patterns.

## CLI Commands

### Core Workflow

```bash
# 1. Catalog audio files
./run.sh catalog <directory> --output manifest.json

# 2. Ingest into memory
./run.sh ingest manifest.json

# 3. Search catalog
./run.sh search "explosion boom" --categories impact --duration 2-5

# 4. Check system status
./run.sh status
```

### Advanced Operations

```bash
# Record usage after selection
./run.sh record-usage \
    --sfx-id abc123 \
    --project "Dark Horizon" \
    --scene "INT. WAREHOUSE - Explosion" \
    --timestamp 5.2

# Recall prior usage (Memory First)
./run.sh recall-usage "warehouse explosion scene"

# Find similar sounds
./run.sh similar sfx_abc123 --threshold 0.80

# Generate missing SFX
./run.sh generate "deep rumbling thunder" --duration 4.0 --ingest

# View usage statistics
./run.sh stats --type categories
```

**Full Reference**: See [`API.md`](API.md) for complete command documentation and Python API.

## Python API

For programmatic integration:

```python
from sfx_catalog import SFXQueryEngine

engine = SFXQueryEngine(scope="horus_lore")

# Memory First pattern
prior_usage = engine.recall_usage(
    scene_description="tense entrance scene",
    threshold=0.7
)

# Semantic search with filters
results = engine.search(
    query="door creak",
    categories=["foley"],
    duration_range=(1.0, 3.0),
    k=5
)

# Record usage for learning
engine.record_usage(
    sfx_id="sfx_abc123",
    project_name="Dark Horizon",
    scene_description="INT. APARTMENT - Sarah enters",
    timestamp_in_scene=2.5,
    rationale="Perfect tension builder"
)

# Generate if needed
generated = engine.generate_sfx(
    prompt="metallic door slam",
    duration=2.0,
    check_cache=True,  # Avoid duplicate generation
    ingest=True        # Add to catalog
)
```

## Data Flow

### 1. Cataloging Workflow

```
User SFX files
    ↓
Audio Analysis (librosa)
    ↓
Content Classification (rule-based)
    ↓
Description Generation (LLM optional)
    ↓
JSON Manifest
    ↓
Memory Ingestion (ArangoDB)
    ↓
Searchable Catalog
```

### 2. Query Workflow

```
User/Agent Query
    ↓
Query Engine
    ├─► Strategy 1: Check memory (prior usage)
    ├─► Strategy 2: Semantic search (embeddings)
    └─► Strategy 3: Generate (if missing)
    ↓
Ranked Results
    ↓
User Selection
    ↓
Usage Recording (for learning)
```

### 3. Learning Workflow

```
Every SFX Use
    ↓
Record: project, scene, rationale
    ↓
Store in sfx_usage collection
    ↓
Build patterns over time
    ↓
Improve future recommendations
```

## Technology Stack

### Audio Processing

- **librosa** - Audio feature extraction
- **soundfile** - Audio I/O
- **scipy** - Signal processing
- **numpy** - Numerical operations

### Memory & Search

- **ArangoDB** - Graph database (via memory skill)
- **python-arango** - Database client
- **Embeddings** - Via [`embedding`](../embedding) skill

### Generation (Optional)

- **Stable Audio Open** - Text-to-audio generation
- **PyTorch** - ML framework

### CLI & UX

- **typer** - CLI framework
- **rich** - Terminal formatting
- **task-monitor** - Progress reporting

## Performance

### Cataloging

- **Single file**: 2-3 seconds (audio analysis + description)
- **166 files**: 5-10 minutes (parallel processing, 4 workers)

### Queries

- **Memory search**: <100ms (indexed ArangoDB)
- **Semantic search**: <200ms (pre-computed embeddings)
- **Total query time**: <500ms end-to-end

### Generation

- **Text-to-audio**: 30-60 seconds per 3-second clip
- **Cache lookup**: <50ms (check before generating)

## Storage Requirements

- **Library files**: ~166MB (existing MP3 files)
- **Metadata**: ~50MB (JSON + ArangoDB)
- **Embeddings**: ~2MB (166 × 384 dimensions)
- **Generated SFX**: ~1GB over time
- **Total**: ~1.2GB

## Dependencies

### Required

- Python 3.11+
- ArangoDB (existing memory system)
- librosa, soundfile, scipy, numpy
- [`memory`](../memory) skill
- [`embedding`](../embedding) skill

### Optional

- [`scillm`](../scillm) skill (for LLM descriptions)
- Stable Audio Open (for generation)
- GPU with 8GB+ VRAM (accelerates generation)

## Configuration

Environment variables (optional, has defaults):

```bash
# Memory system
export MEMORY_ROOT="$HOME/workspace/experiments/memory"
export ARANGO_HOST="127.0.0.1"
export ARANGO_PORT="8529"

# SFX catalog data
export SFX_DATA_DIR="$HOME/.pi/sfx-catalog"

# LLM for descriptions (optional)
export SFX_LLM_MODEL="qwen2.5-coder:7b"
export SFX_LLM_PROVIDER="ollama"

# Audio generation (optional)
export STABLE_AUDIO_DEVICE="cuda:0"  # or "cpu"
```

## Installation

```bash
cd .pi/skills/sfx-catalog

# Install dependencies
uv sync

# Run sanity checks
./sanity/run_all.sh

# Verify memory connection
./run.sh status
```

## Usage Examples

### Example 1: Initial Library Cataloging

```bash
# Catalog the entire library
./run.sh catalog /mnt/storage12tb/media/sfx/ \
    --output library_manifest.json \
    --parallel 4

# Review manifest
cat library_manifest.json | jq '.items[0]'

# Ingest into memory
./run.sh ingest library_manifest.json

# Test search
./run.sh search "impact" --limit 3
```

### Example 2: Finding SFX for a Scene

```bash
# Search for thunder sounds
./run.sh search "deep rumbling thunder" \
    --categories ambient \
    --duration 3-8

# Preview top result (if ffplay/mpv installed)
./run.sh search "thunder" --play-top
```

### Example 3: Recording Usage

```bash
# After selecting SFX for a scene
./run.sh record-usage \
    --sfx-id sfx_abc123 \
    --project "Storm Chaser" \
    --scene "EXT. FIELD - Dark clouds gather, distant thunder" \
    --timestamp 12.5 \
    --rationale "Sets ominous mood, foreshadows the storm"
```

### Example 4: Memory First Pattern

```bash
# Working on a new tense scene
./run.sh recall-usage "tense interior entrance quiet footsteps"

# Returns SFX used successfully in similar scenes:
# Result 1: footsteps_hardwood_slow.mp3 (used in "Dark Horizon" INT. APARTMENT)
#   Rationale: "Built tension perfectly during cautious entrance"
#   Score: 0.87
```

### Example 5: Generating Missing SFX

```bash
# Library doesn't have "sci-fi computer beep"
./run.sh generate "futuristic computer beep, clean, short" \
    --duration 0.5 \
    --ingest

# Generated SFX is now searchable:
./run.sh search "computer beep"
```

## Testing

```bash
# Run all sanity checks
./sanity/run_all.sh

# Individual checks
./sanity/test_audio_analysis.sh   # Verify librosa
./sanity/test_memory.sh           # Verify ArangoDB
./sanity/test_search.sh           # Verify queries work

# Unit tests
uv run pytest tests/

# Integration tests
uv run pytest tests/integration/
```

## Troubleshooting

### "ArangoDB connection failed"

```bash
# Check if ArangoDB is running
systemctl status arangodb3

# Verify memory skill works
cd ../memory
./run.sh status
```

### "No module named 'librosa'"

```bash
# Reinstall dependencies
uv sync --reinstall
```

### "Search returns no results"

```bash
# Check if catalog was ingested
./run.sh status

# Re-ingest if needed
./run.sh ingest library_manifest.json
```

### "Generation is too slow"

```bash
# Check if using GPU
./run.sh status --verbose

# Use shorter duration or lower quality
./run.sh generate "thunder" --duration 2.0 --steps 50
```

## Roadmap

### Phase 1: Foundation (MVP) - Weeks 1-3

- ✅ Audio analysis with librosa
- ✅ Rule-based classification
- ✅ Memory integration
- ✅ CLI interface

### Phase 2: Integration - Weeks 4-5

- ⏳ Usage tracking
- ⏳ Query engine (multi-strategy)
- ⏳ create-movie integration
- ⏳ create-storyboard integration

### Phase 3: Generation - Weeks 6-7

- ⏳ Stable Audio integration
- ⏳ Generation caching
- ⏳ Similarity graph

### Phase 4: Enhancement - Weeks 8-9

- ⏳ Advanced classification (ML-based)
- ⏳ Usage analytics
- ⏳ Performance optimization

**Full Plan**: See [`ROADMAP.md`](ROADMAP.md) for detailed implementation timeline.

## Contributing

This skill follows the conventions in [`../CONVENTIONS.md`](../CONVENTIONS.md):

- **Code**: Stored in `.pi/skills/sfx-catalog/`
- **Data**: Stored in `~/.pi/sfx-catalog/` (persistent across syncs)
- **Progress**: Reported to [`task-monitor`](../task-monitor) for long operations
- **Memory**: Uses `horus_lore` scope via [`memory`](../memory) skill

## Documentation

- [`ARCHITECTURE.md`](ARCHITECTURE.md) - System design and component specs
- [`MEMORY_SCHEMA.md`](MEMORY_SCHEMA.md) - ArangoDB collections and queries
- [`API.md`](API.md) - Complete CLI and Python API reference
- [`ROADMAP.md`](ROADMAP.md) - Implementation plan and timeline

## License

Part of Horus's filmmaking toolkit. For private use.

---

**Status**: Design phase complete, ready for implementation.

**Next Step**: Begin Phase 1 implementation (audio analysis + cataloging).
