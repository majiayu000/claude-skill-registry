---
name: ingest-yt-history
description: >
  Ingest YouTube and YouTube Music watch history from Google Takeout exports.
  Builds music taste profile for Horus persona with /memory integration.
allowed-tools: Bash, Read
triggers:
  - ingest youtube history
  - youtube watch history
  - youtube music history
  - google takeout youtube
  - find music for horus
  - what music do I like
  - music preferences
metadata:
  short-description: YouTube history → Horus music discovery

provides:
  - ingest-yt-history
composes: [, task-monitor]
---

# YouTube History → Horus Music Discovery

**Goal:** Let Horus persona easily find music based on human's listening history.

## Quick Start (Horus Persona)

```bash
cd .pi/skills/ingest-yt-history

# What music does the human like?
./run.sh find-music

# Find music matching a mood
./run.sh find-music --mood melancholic
./run.sh find-music --mood epic

# Get artist recommendations
./run.sh similar-artists "Chelsea Wolfe"

# Search music history
./run.sh search "metal" --service youtube_music
```

## Integration with Horus

The skill stores music preferences in `/memory` so Horus can:

1. **Reference in conversations:** "Ah, you favor the grim cadence of Chelsea Wolfe..."
2. **Inform creative work:** Match story/movie mood to human's taste
3. **Connect via taxonomy:** Dark music → Horus's melancholic aesthetic

### Memory Integration

```bash
# Sync music preferences to /memory
./run.sh sync-memory

# Creates entries like:
# - Category: music_preferences
# - Tags: youtube_music, horus_lupercal, dark_folk, doom
```

## Commands

| Command | Description |
|---------|-------------|
| `find-music` | List music from history (filterable by mood, genre) |
| `similar-artists` | Find artists similar to favorites |
| `search` | Search history by title, channel, service |
| `stats` | Show listening stats and top artists |
| `sync-memory` | Export preferences to /memory |
| `profile` | Generate taste profile JSON |

## One-Time Setup

### 1. Export from Google Takeout

1. Go to [Google Takeout](https://takeout.google.com)
2. Select only **"YouTube and YouTube Music"** → **History**
3. **Set format to JSON** (not HTML!)
4. Download and unzip

### 2. Ingest

```bash
./run.sh ingest ~/Downloads/Takeout/YouTube*/history/watch-history.json
```

### 3. Sync to Memory

```bash
./run.sh sync-memory
```

## Example Horus Queries

```bash
# "What atmospheric music does the human listen to?"
./run.sh find-music --mood atmospheric

# "Find something for a battle scene"
./run.sh find-music --mood epic --genre metal

# "The human mentioned Chelsea Wolfe - what else like that?"
./run.sh similar-artists "Chelsea Wolfe"
```

## Data Locations

| Data | Location |
|------|----------|
| Raw history | `~/.pi/ingest-yt-history/history.jsonl` |
| Music index | `~/.pi/ingest-yt-history/music_index.json` |
| Taste profile | `~/.pi/ingest-yt-history/taste_profile.json` |
| Memory entries | ArangoDB via `/memory` |

## Current Human's Profile

From Takeout analysis (10,000 entries):

**Music (dark/atmospheric):**
- Chelsea Wolfe - dark folk, doom
- Daughter - melancholic indie
- Spiritbox - progressive metal
- Billie Marten - atmospheric folk

**Warhammer 40K (Horus lore):**
- Luetin09, In Deep Geek, Stories by Imperium

**Mood alignment with Horus:** High (dark, melancholic, epic)
