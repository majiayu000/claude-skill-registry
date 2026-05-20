---
name: learn-voice
description: >
  Train RVC voice models from artist names. Full pipeline: YouTube search,
  download, stem separation, preprocessing, training, and model indexing.
  Builds a library of singing voices organized by category (voice/instrument).
allowed-tools: [Bash, Read, Write, Task]
triggers:
  - learn voice
  - train voice
  - train voice model
  - voice training
  - clone voice
  - rvc training
  - voice library
  - add voice to library
metadata:
  short-description: "Train RVC voice models from artist names"
  author: "Horus"
  version: "0.1.0"

provides:
  - learn-voice
composes:
  - learn-artist
  - discover-music
  - memory
  - create-music
  - task-monitor
---

# learn-voice

Train RVC (Retrieval-based Voice Conversion) models from artist names. Creates a searchable library of singing voices.

## Quick Start - For Agents

The simplest way for an agent to learn a voice:

```bash
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/learn-voice

# Just say who you want to learn
./run.sh learn "Sierra Ferrell"
./run.sh learn "Miles Davis" trumpet
./run.sh learn "Keith Moon" drummer

# That's it! The daemon handles everything.
```

## Agent Workflow

When an agent encounters a singer or instrumentalist they want to learn:

1. **Express interest**: `./run.sh learn "Artist Name"`
2. **Daemon trains automatically** (if running)
3. **Use trained voice later** via `create-music` skill

```bash
# Agent sees a cool vocalist
./run.sh learn "Yasamin Shahhosseini"
# Output: Added to queue: Yasamin Shahhosseini
#         Queue now has 13 artists
#         Daemon running (PID 12345) - will train automatically

# Later, use the trained voice
cd ../create-music
./run.sh rvc-infer --model-name yasamin-shahhosseini --input vocals.wav --output converted.wav
```

## Manual Training (if needed)

```bash
# Train immediately (blocks until done)
./run.sh train "Brennen Leigh" --epochs 200

# Batch training
./run.sh train-batch "Artist 1" "Artist 2" "Artist 3"

# Start daemon for continuous training
./run.sh daemon &
```

## Pipeline

The full pipeline for each artist:

1. **Search** - Find YouTube videos via `discover-music`
2. **Download** - Download audio tracks
3. **Separate** - Extract vocals using Demucs (htdemucs model)
4. **Preprocess** - Slice audio into training segments
5. **Extract F0** - Pitch extraction (RMVPE method)
6. **Extract Features** - Hubert embeddings
7. **Train** - RVC v2 training with pretrained weights
8. **Index** - Build FAISS index for fast inference
9. **Register** - Add to voice library with metadata

## Storage Layout

```
/mnt/storage12tb/media/music/
├── rvc-training/              # Raw training data
│   └── <artist-slug>/
│       ├── vocals_all/        # Consolidated vocal stems
│       └── <video-id>/        # Per-track stems
│
└── rvc-models/                # Trained models
    ├── voice/
    │   ├── brennen-leigh/
    │   │   ├── brennen-leigh.pth
    │   │   ├── brennen-leigh.index
    │   │   └── metadata.json
    │   ├── billie-holiday/
    │   └── ...
    └── instrument/
        ├── pedal-steel/
        └── ...
```

## Commands

### train

Train a voice model from an artist name.

```bash
./run.sh train "Artist Name" [options]

Options:
  --epochs N        Training epochs (default: 200)
  --batch-size N    Batch size (default: 4, reduce if OOM)
  --category CAT    voice or instrument (default: voice)
  --min-tracks N    Minimum tracks to download (default: 10)
  --min-minutes N   Minimum audio duration (default: 30)
  --skip-download   Use existing vocals in rvc-training/
```

### train-batch

Train multiple voices sequentially.

```bash
# From arguments
./run.sh train-batch "Artist 1" "Artist 2" "Artist 3"

# From file (one artist per line)
./run.sh train-batch --file artists.txt

# With options applied to all
./run.sh train-batch --epochs 300 --file artists.txt
```

### list

List all trained voice models.

```bash
./run.sh list              # All models
./run.sh list --voice      # Voice models only
./run.sh list --instrument # Instrument models only
./run.sh list --json       # JSON output
```

### status

Check training status for a model.

```bash
./run.sh status brennen-leigh
```

Output:
```
Model: brennen-leigh
Status: training
Epoch: 45/200
Loss: mel=18.2, kl=1.5
ETA: ~2.5 hours
```

### export

Export a model for use with create-music.

```bash
./run.sh export brennen-leigh --to /path/to/destination
```

## Quality Gates

Models are automatically evaluated after training:

| Metric | Good | Warning | Fail |
|--------|------|---------|------|
| loss_mel | <20 | 20-30 | >30 |
| loss_kl | <2 | 2-4 | >4 |

Failed models are flagged in metadata and excluded from default listings.

## Integration with Other Skills

### discover-music

`learn-voice` calls `discover-music` for:
- YouTube search (`youtube-search`)
- Audio download + stem separation (`youtube-stems`)

### create-music

Once trained, use models with `create-music`:

```bash
# In create-music
./run.sh rvc-infer \
  --model-name brennen-leigh \
  --input vocals.wav \
  --output converted.wav
```

## Docker Container

Training runs inside the RVC Docker container:

```bash
docker run -d --gpus all --name rvc-training \
  --shm-size=8g \
  -p 7865:7865 \
  -v /path/to/logs:/app/logs \
  -v /path/to/datasets:/app/datasets \
  cherrymint/rvc_webui:rvc_boss
```

The skill manages container lifecycle automatically.

## Model Metadata

Each trained model has a `metadata.json`:

```json
{
  "name": "brennen-leigh",
  "artist": "Brennen Leigh",
  "category": "voice",
  "tracks": 12,
  "duration_minutes": 38.5,
  "epochs": 200,
  "batch_size": 4,
  "sample_rate": "40k",
  "version": "v2",
  "trained_at": "2026-02-04T01:15:00Z",
  "training_time_minutes": 180,
  "final_loss": {
    "mel": 18.2,
    "kl": 1.5,
    "gen": 2.1,
    "disc": 3.2
  },
  "quality": "good",
  "source_tracks": [
    "Prairie Funeral",
    "Dumpster Diving",
    "..."
  ]
}
```

## Examples

### Train a Single Artist

```bash
./run.sh train "Elizabeth Fraser" --epochs 200

# Output:
# Searching YouTube for Elizabeth Fraser...
# Found 20 tracks
# Downloading 12 tracks (target: 30+ minutes)...
# Separating stems...
# Preprocessing...
# Training (200 epochs, ~3 hours)...
# Building index...
# Model saved to /mnt/storage12tb/media/music/rvc-models/voice/elizabeth-fraser/
# Quality: good (mel=17.8, kl=1.2)
```

### Batch Training Overnight

```bash
# Create artist list
cat > artists.txt << EOF
Lucinda Williams
Beth Gibbons
Elizabeth Fraser
Billie Marten
Joni Mitchell
EOF

# Start batch training
./run.sh train-batch --file artists.txt --epochs 200

# Check progress
./run.sh status --all
```

## Troubleshooting

### CUDA Out of Memory

Reduce batch size:
```bash
./run.sh train "Artist" --batch-size 2
```

### Not Enough Training Data

Increase track count:
```bash
./run.sh train "Artist" --min-tracks 15 --min-minutes 45
```

### Training Stuck

Check container logs:
```bash
docker logs rvc-training --tail 50
```
