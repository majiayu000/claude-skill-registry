---
name: review-music
description: >
  Analyze audio files to extract musical features (BPM, key, chords, timbre, dynamics)
  and generate structured reviews with HMT taxonomy mapping for Horus persona.
  Uses MIR tools (madmom, essentia, librosa) + LLM chain-of-thought reasoning.
triggers:
  - review music
  - analyze song
  - music analysis
  - extract audio features
  - what key is this
  - chord progression
  - music theory analysis
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Audio analysis with MIR tools + LLM music theory reasoning
---

# Review Music Skill

Analyze audio files to extract musical features and generate structured reviews with Horus Music Taxonomy (HMT) mapping.

## Quick Start

```bash
cd .pi/skills/review-music

# Analyze a local audio file
./run.sh analyze path/to/song.mp3

# Analyze from YouTube URL
./run.sh analyze --youtube "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Extract specific features only
./run.sh features path/to/song.mp3 --bpm --key --chords

# Generate full review with HMT taxonomy
./run.sh review path/to/song.mp3 --sync-memory

# Batch analyze directory
./run.sh batch ./music_folder --output reviews.jsonl
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      review-music Pipeline                       │
├─────────────────────────────────────────────────────────────────┤
│  Input: Audio file (mp3/wav/flac) or YouTube URL                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Stage 1: Feature Extraction (MIR Tools)                        │
│  ├── madmom → beat positions, tempo/BPM, downbeats              │
│  ├── essentia → key, mode, loudness, dynamics                   │
│  ├── librosa → MFCC (timbre), chromagram, spectral features     │
│  ├── Chordino/autochord → chord progression, changes            │
│  └── Whisper → lyrics transcription                             │
│                                                                  │
│  Stage 2: Embeddings (Optional - Foundation Models)             │
│  ├── MERT → acoustic music understanding embeddings             │
│  └── CLAP → audio-text joint embeddings for semantic search     │
│                                                                  │
│  Stage 3: LLM Analysis (Chain-of-Thought)                       │
│  ├── Structured prompt with extracted features                  │
│  ├── Music theory reasoning (chord function, harmony)           │
│  └── Multi-aspect review generation                             │
│                                                                  │
│  Stage 4: HMT Taxonomy Mapping                                   │
│  ├── Map features → Bridge Attributes                           │
│  ├── Extract collection_tags (domain, thematic_weight)          │
│  └── Identify episodic associations (lore connections)          │
│                                                                  │
│  Stage 5: Memory Sync                                            │
│  └── /memory learn with full taxonomy + review                  │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  Output: Structured review JSON with HMT taxonomy                │
└─────────────────────────────────────────────────────────────────┘
```

## Commands

### Analyze

```bash
./run.sh analyze <audio_file> [options]
```

Extract all features and generate analysis report.

**Options:**
| Option | Description |
|--------|-------------|
| `--youtube <url>` | Download and analyze from YouTube |
| `--output <file>` | Output JSON file (default: stdout) |
| `--no-lyrics` | Skip lyrics transcription |
| `--no-llm` | Skip LLM analysis, features only |

### Features

```bash
./run.sh features <audio_file> [--bpm] [--key] [--chords] [--timbre] [--dynamics]
```

Extract specific audio features only.

### Review

```bash
./run.sh review <audio_file> [options]
```

Generate full multi-aspect review with HMT taxonomy.

**Options:**
| Option | Description |
|--------|-------------|
| `--sync-memory` | Sync to /memory after review |
| `--artist <name>` | Override artist name |
| `--title <name>` | Override track title |

### Batch

```bash
./run.sh batch <directory> --output <file.jsonl>
```

Batch analyze all audio files in directory.

## Feature Extraction

### Rhythm & Tempo (madmom)
- `bpm`: Beats per minute
- `tempo_variance`: Stability of tempo
- `beat_positions`: Array of beat timestamps
- `downbeats`: Measure boundaries
- `time_signature`: Detected meter (4/4, 3/4, etc.)

### Harmony (essentia + Chordino)
- `key`: Musical key (C, F#m, etc.)
- `mode`: Major/minor
- `chords`: Array of {chord, start, end}
- `chord_changes_per_minute`: Harmonic rhythm
- `harmonic_complexity`: Variety of chord types

### Timbre (librosa)
- `mfcc`: Mel-frequency cepstral coefficients
- `spectral_centroid`: Brightness
- `spectral_bandwidth`: Frequency spread
- `spectral_rolloff`: High-frequency content
- `zero_crossing_rate`: Noisiness

### Dynamics (essentia)
- `loudness_integrated`: Overall loudness (LUFS)
- `dynamic_range`: Peak-to-average ratio
- `loudness_range`: Variation in loudness

### Lyrics (Whisper)
- `lyrics`: Transcribed text
- `language`: Detected language
- `word_timestamps`: Word-level timing

## HMT Bridge Mapping

Audio features are mapped to Bridge Attributes:

| Bridge | Audio Indicators |
|--------|------------------|
| **Precision** | High tempo variance, polyrhythmic, odd time signatures, technical passages |
| **Resilience** | Building dynamics, triumphant key progressions, crescendos, major keys |
| **Fragility** | Sparse instrumentation, minor keys, soft dynamics, acoustic timbre |
| **Corruption** | Distorted timbre, dissonance, harsh frequencies, industrial textures |
| **Loyalty** | Ceremonial rhythm, drone elements, choral textures, modal harmony |
| **Stealth** | Ambient textures, minimal beats, low spectral centroid, drone |

## Output Format

```json
{
  "metadata": {
    "artist": "Chelsea Wolfe",
    "title": "Carrion Flowers",
    "duration_seconds": 245,
    "file_path": "/path/to/file.mp3"
  },
  "features": {
    "rhythm": {
      "bpm": 72,
      "tempo_variance": 0.05,
      "time_signature": "4/4"
    },
    "harmony": {
      "key": "D minor",
      "mode": "minor",
      "chords": [
        {"chord": "Dm", "start": 0.0, "end": 4.2},
        {"chord": "Am", "start": 4.2, "end": 8.1}
      ],
      "harmonic_complexity": 0.65
    },
    "timbre": {
      "spectral_centroid_mean": 1850.5,
      "brightness": "dark",
      "texture": "layered"
    },
    "dynamics": {
      "loudness_integrated": -14.2,
      "dynamic_range": 12.5
    },
    "lyrics": {
      "text": "...",
      "language": "en",
      "themes": ["mortality", "nature", "darkness"]
    }
  },
  "review": {
    "summary": "A haunting doom-folk track with sparse instrumentation...",
    "music_theory": "The song employs a D minor tonality with...",
    "production": "Heavy reverb on vocals creates ethereal atmosphere...",
    "emotional_arc": "Builds from intimate verses to powerful chorus..."
  },
  "hmt_taxonomy": {
    "bridge_attributes": ["Fragility", "Corruption"],
    "collection_tags": {
      "domain": "Dark_Folk",
      "thematic_weight": "Melancholic",
      "function": "Contemplation"
    },
    "tactical_tags": ["Score", "Immerse"],
    "episodic_associations": ["Webway_Collapse", "Sanguinius_Fall"],
    "confidence": 0.85
  }
}
```

## Integration with Horus Persona

After analysis, reviews are synced to `/memory` for Horus recall:

```bash
# Review syncs automatically with --sync-memory
./run.sh review song.mp3 --sync-memory

# Later, Horus can recall:
/memory recall --bridge Fragility --collection music
/memory recall --scene "mourning scene" --collection music
```

## Crucial Dependencies

| Library | Purpose | Sanity Script |
|---------|---------|---------------|
| madmom | Beat/tempo detection | `sanity/madmom.py` |
| essentia | Key/dynamics extraction | `sanity/essentia.py` |
| librosa | Timbre/spectral features | `sanity/librosa.py` |
| openai-whisper | Lyrics transcription | `sanity/whisper.py` |
| yt-dlp | YouTube download | N/A (well-known) |

## Data Storage

| Data | Location |
|------|----------|
| Reviews cache | `~/.pi/review-music/reviews/` |
| Feature cache | `~/.pi/review-music/features/` |
| Downloaded audio | `~/.pi/review-music/audio/` |
