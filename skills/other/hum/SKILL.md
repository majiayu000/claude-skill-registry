---
name: hum
description: >
  Persona humming pipeline. Downloads songs, separates vocals, converts to
  persona voice via RVC, and caches for playback during idle conversation.
  Orchestrates: /ingest-youtube, /create-stems, /learn-artist, /create-music.
triggers:
  - hum
  - add hum
  - teach humming
  - hum a song
  - humming pipeline
  - convert vocals
  - persona singing
allowed-tools:
  - Bash
  - Python
  - Read
  - Write
metadata:
  short-description: "Persona humming via vocal stem conversion"
  author: graham
  version: "0.1.0"

provides:
  - hum
composes: [, task-monitor]
---

# /hum

Convert any song into a persona's humming voice. Downloads audio, stems vocals,
converts to the persona's RVC voice model, and caches with Federated Taxonomy
metadata for mood-driven playback during idle conversation.

## Quick Start

```bash
cd .pi/skills/hum

# Train a persona's RVC voice model (one-time per persona, ~2hr)
./run.sh train --persona embry
./run.sh train --persona brandon

# Add a song to any persona's humming library
./run.sh add "https://youtu.be/Dordpe3KX_I" \
  --persona embry \
  --mood playful,curious \
  --bridges Loyalty,Resilience

# Different personas, different songs
./run.sh add "https://youtu.be/xyz" \
  --persona brandon \
  --mood melancholic \
  --bridges Fragility,Resilience

# List cached hums for a persona
./run.sh list --persona embry

# Play a cached hum
./run.sh play hawaiian_war_chant --persona embry

# Sanity check all dependencies and all personas
./run.sh sanity
```

## Multi-Persona

Any persona with TTS samples at `/mnt/storage12tb/media/personas/<name>/tts_output/`
can be trained and used. Each persona gets its own RVC voice model and hum cache.

```
/mnt/storage12tb/media/personas/
  embry/
    tts_output/     ← voice samples (any persona needs these)
    hum-cache/      ← generated humming audio + manifest
  brandon/
    tts_output/
    hum-cache/
```

## Pipeline

```
YouTube URL
    |
    v
[ingest-youtube]  yt-dlp --extract-audio
    |
    v
full_mix.wav
    |
    v
[create-stems]    Demucs htdemucs_6s --two-stems vocals
    |
    v
vocals.wav
    |
    v
[create-music]    RVC inference with persona model
    |
    v
persona_vocals.wav
    |
    v
[hum-cache]       /mnt/storage12tb/media/personas/<name>/hum-cache/
                   + manifest.json with taxonomy metadata
```

## Commands

| Command | Description |
|---------|-------------|
| `add <url>` | Full pipeline: download, stem, convert, cache |
| `train` | Train persona RVC voice model from existing samples |
| `list` | List all cached hums with metadata |
| `play <track>` | Play a cached hum through PipeWire |
| `info <track>` | Show track metadata and taxonomy tags |
| `sanity` | Verify all pipeline dependencies |

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--persona NAME` | Target persona | `embry` |
| `--mood TAGS` | Comma-separated mood tags | auto-detected |
| `--bridges ATTRS` | Comma-separated bridge attributes | auto-detected |
| `--pitch N` | Pitch shift in semitones | `0` |
| `--f0method METHOD` | F0 extraction: rmvpe, harvest, crepe | `rmvpe` |
| `--json` | Output as JSON | false |

## Storage Layout

```
/mnt/storage12tb/media/personas/<persona>/hum-cache/
  manifest.json              # Index of all cached hums
  hawaiian_war_chant.wav     # Converted audio
  hawaiian_war_chant.json    # Per-track metadata
```

### Track Metadata Schema

```json
{
  "id": "hawaiian_war_chant",
  "title": "Hawaiian War Chant",
  "artist": "Lennon Sisters",
  "source_url": "https://youtu.be/Dordpe3KX_I",
  "source_video_id": "Dordpe3KX_I",
  "bridge_attributes": ["Loyalty", "Resilience"],
  "mood": ["playful", "curious"],
  "persona_connection": "Linguistics degree, Hawaiian cultural ties",
  "duration_s": 120,
  "pitch_shift": 0,
  "f0_method": "rmvpe",
  "created": "2026-02-11T12:00:00",
  "forbidden": false
}
```

### Manifest Schema

```json
{
  "persona": "embry",
  "tracks": [
    { "id": "hawaiian_war_chant", "file": "hawaiian_war_chant.wav", ... }
  ],
  "updated": "2026-02-11T12:00:00"
}
```

## Integration

### With /converse

The converse idler reads the hum-cache manifest to select tracks matching
the current emotional state. Playback goes through the AudioMixer "humming"
channel at 60% volume, ducking to 0% when speech starts.

```python
# In converse/idler.py
from hum.src.cache import HumCache

cache = HumCache(persona="embry")
track = cache.select(mood="playful", bridges=["Loyalty"])
mixer.play("humming", track.audio_path, volume=0.6)
```

### With /learn-artist

Training uses the learn-artist skill's Docker-based RVC pipeline:

```bash
# learn-artist handles Docker container lifecycle
cd .pi/skills/learn-artist
./run.sh train "embry" \
  --source-dir /mnt/storage12tb/media/personas/embry/tts_output \
  --category voice --epochs 200
```

### With /create-stems

Vocal separation uses the create-stems skill:

```bash
cd .pi/skills/create-stems
./run.sh separate --mix song.wav --out /tmp/stems --instrument vocals
```

### With /create-music

RVC inference uses the create-music skill:

```bash
cd .pi/skills/create-music
./run.sh rvc-infer \
  --model-name embry \
  --input vocals.wav \
  --output humming.wav \
  --f0method rmvpe
```

## Dependencies

| Skill | Purpose | Required |
|-------|---------|----------|
| /ingest-youtube | Audio download via yt-dlp | Yes |
| /create-stems | Demucs vocal separation | Yes |
| /create-music | RVC inference | Yes |
| /learn-artist | RVC model training | For `train` command |
| /consume-music | Registry integration | Optional |

## Safety

- The Kamakawiwoole guard remains active. Hawaiian music tagged as sentimental
  or grief-triggering is marked `forbidden: true` in track metadata.
- The converse idler checks `forbidden` before playback.
- Bridge attribute `Fragility` above 0.7 triggers extra review before caching.
