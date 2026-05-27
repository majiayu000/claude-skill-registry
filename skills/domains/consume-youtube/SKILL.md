````markdown
---
name: consume-youtube
description: >
  Search and annotate YouTube transcripts already ingested by /ingest-youtube.
  Supports per-channel indexing and Horus notes with /memory integration.
triggers:
  - consume youtube
  - search youtube
  - youtube notes
  - youtube transcript search
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Consume YouTube transcripts - search, index, take notes
---

# Consume YouTube Skill

Search and annotate ingested YouTube transcripts. Works with content already processed by `/ingest-youtube`.

## Quick Start

```bash
cd .pi/skills/consume-youtube

# Import transcripts into registry
./run.sh sync

# Search transcripts
./run.sh search "siege" --channel "luetin09"

# Build a channel index
./run.sh index --channel "luetin09"

# Add a note at a timestamp
./run.sh note --video <video_id> --timestamp 184.5 --note "Key claim"

# List videos
./run.sh list --channel "luetin09"
```

## Commands

### Sync Transcripts

```bash
./run.sh sync [--ingest-root <path>]
```

Imports transcript JSON files from the ingest output directory.

### Search Transcripts

```bash
./run.sh search <query> [--channel <name>] [--video <id>] [--context <n>]
```

Searches transcript segments and returns matches with timestamps and context.

### Build Index

```bash
./run.sh index --channel <name>
```

Builds a lightweight inverted index for faster channel searches.

### Add Note

```bash
./run.sh note --video <id> --timestamp <sec> --note <text> [--agent <id>]
```

Adds a Horus note at a timestamp.

### List Videos

```bash
./run.sh list [--json] [--channel <name>]
```

Lists all indexed videos in the registry.

## Data Storage

- **Registry**: `~/.pi/consume-youtube/registry.json`
- **Notes**: `~/.pi/consume-youtube/notes/<agent_id>/notes.jsonl`
- **Indices**: `~/.pi/consume-youtube/indices/<channel>.json`

## Integration with /memory

Notes are stored in `/memory` using the consume-common memory bridge:

```bash
./memory/run.sh learn \
  --problem "Consumed youtube: <title>" \
  --solution "<note>" \
  --category emotional_learning \
  --tags youtube,horus_lupercal
```

````
