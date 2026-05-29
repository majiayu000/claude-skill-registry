---
name: learn-movie
description: Analyze movies to extract cinematographic techniques and store them in memory.
triggers:
  - learn movie
  - analyze film
  - cinematography extraction
  - movie analysis
provides:
  - learn-movie
composes:
  - task-monitor
---

# learn-movie

TEACH Horus by analyzing actual movies.
Extracts lighting, composition, emotional cues, and director style from video files.

## Features

- **Scene Detection**: Automatically detects scene cuts using ffmpeg.
- **VLM Analysis**: Uses Vision-Language Models (via `scillm`) to analyze keyframes.
- **Memory Integration**: Stores learned patterns into the `horus-movies` collection.

## Usage

```bash
# Analyze a video file
/learn-movie analyze path/to/movie.mp4

# Analyze with specific director context
/learn-movie analyze path/to/movie.mp4 --director "Ridley Scott"
```

## Setup

Requires `ffmpeg` installed.
Uses `scillm` skill for VLM inference (e.g., `pixtral-12b`).

## Memory + Taxonomy Integration

Follows the canonical `create-context/memory_integration.py` pattern with graceful degradation.

### Pre-hook: `recall_prior_analyses(movie_name, k=5)`
- Recalls prior cinematographic analyses for the same movie before analysis begins
- Surfaces previously learned techniques to avoid redundant storage
- Enables cumulative learning across sessions

### Post-hook: `learn_analysis(movie_name, techniques, scenes, insights)`
- Stores analysis snapshot (movie, date, technique counts, bridge tags)
- Stores individual techniques (shot type, lighting, composition)
- Stores scene-level insights for cross-movie pattern matching
- Tags: `["learn_movie", movie_name] + bridges`

### Bridge Keywords (keyword fallback)
| Bridge | Keywords |
|--------|----------|
| Precision | technique, frame, composition, symmetry, geometric, calculated |
| Resilience | adaptation, creative, enduring, triumphant, recovery |
| Fragility | inconsistency, discontinuity, fragile, delicate, breaking |
| Corruption | distortion, decay, grotesque, horror, darkness |
| Loyalty | devotion, sacrifice, bond, duty, honor |
| Stealth | shadow, silhouette, hidden, subtle, muted |

### Graceful Degradation
- Uses `try/except ImportError` at every hook callsite
- Falls back to keyword-based bridge extraction when taxonomy module unavailable
- All hooks are no-ops when `common.memory_client` is not importable

## File Structure

| File | Purpose |
|------|---------|
| `SKILL.md` | This file |
| `run.sh` | Execution entry point |
| `sanity.sh` | Health check |
| `orchestrator.py` | Main orchestrator (scene detect, VLM analyze, memorize) |
| `memory_integration.py` | Memory + Taxonomy hooks (pre/post) |
