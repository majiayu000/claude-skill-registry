---
name: consume-movie
description: >
  Search and extract clips from ingested movies. Query SRT subtitles,
  extract video clips at timestamps, and track Horus notes on scenes.
  Use after /ingest-movie has processed content.
triggers:
  - consume movie
  - search subtitles
  - extract clip
  - movie notes
  - srt search
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Consume ingested movies - search SRT, extract clips, take notes
---

# Consume Movie Skill

Search and extract content from ingested movies. This skill works with content already processed by `/ingest-movie`.

**Key Feature:** Integrates with `/consume-book` to provide book context while watching movie adaptations, and with `/dogpile` for external reviews.

## Quick Start

```bash
cd .pi/skills/consume-movie

# Watch a movie with book context and external reviews
./run.sh watch --movie "abc123" --with-book-context --with-reviews

# Search subtitles with book annotations
./run.sh search "rage" --movie "tywin_tyrion" --with-book-context

# Extract a clip
./run.sh clip --query "You are a Lannister" --output ~/clips/

# Add a note at a timestamp
./run.sh note --movie "movie_id" --timestamp 125.5 --note "Manipulation pattern"

# List available movies (shows which have book context)
./run.sh list
```

## Book-Before-Movie Workflow

The recommended workflow reads the source material before watching:

```bash
# 1. Read the book first
cd .pi/skills/consume-book
./run.sh sync --books-dir ~/library/books
./run.sh search "Paul Atreides" --book dune-id
./run.sh note --book dune-id --char-position 50000 --note "Character motivation"

# 2. Watch the movie with book context
cd .pi/skills/consume-movie
./run.sh watch --movie dune-2021-id --with-book-context --with-reviews

# Book notes are displayed alongside movie scenes
# External reviews from dogpile provide critical analysis
```

## Automatic Book Acquisition

When watching a movie, the skill automatically:

1. **Searches for related books** using the book-movie mapping (e.g., "There Will Be Blood" → "Oil!")
2. **Checks local registry** for existing book content
3. **Searches Readarr** for missing books via `/ingest-book`
4. **Falls back to movie reviews** via `/dogpile` if books unavailable

```bash
# Auto-acquire missing books before watching
./run.sh watch --movie dune-2021-id --acquire-books

# This will:
# 1. Search Readarr for "Dune" by Frank Herbert
# 2. If found: retrieve and extract via /ingest-book + /extractor
# 3. If not found: fetch movie reviews via /dogpile as fallback
```

### Acquisition Pipeline

```
Movie Title → find_related_books() → search Readarr
                                          ↓
                              Found? → /ingest-book retrieve
                                          ↓
                                     /extractor → consume-book registry
                                          ↓
                              Not found? → /dogpile movie reviews (fallback)
```

## Commands

### Search Subtitles

```bash
./run.sh search <query> [--movie <movie_id>] [--context <seconds>]
```

Search for text in movie subtitles. Returns matches with timestamps and context.

**Options:**

- `--movie`: Specific movie ID (omit to search all)
- `--context`: Seconds of context before/after (default: 5)

**Output:**

```json
{
  "results": [
    {
      "movie_id": "uuid",
      "movie_title": "Game of Thrones S03E10",
      "start": 125.5,
      "end": 128.0,
      "text": "You are a Lannister",
      "context_before": "...",
      "context_after": "..."
    }
  ]
}
```

### Extract Clip

```bash
./run.sh clip --query <text> --output <dir> [--duration <seconds>]
```

Extract a video clip matching the search query.

**Options:**

- `--query`: Text to search for
- `--output`: Output directory for clip
- `--duration`: Clip duration in seconds (default: 10)

### Add Note

```bash
./run.sh note --movie <movie_id> --timestamp <seconds> --note <text> [--agent <agent_id>]
```

Add Horus note at a specific timestamp.

**Options:**

- `--movie`: Movie ID
- `--timestamp`: Time in seconds
- `--note`: Note text
- `--agent`: Agent ID (default: horus_lupercal)

### List Movies

```bash
./run.sh list [--json]
```

List all ingested movies available for consumption.

### Import from Ingest

```bash
./run.sh sync
```

Sync with `/ingest-movie` to import new transcripts.

## Data Storage

- **Registry**: `~/.pi/consume-movie/registry.json`
- **Notes**: `~/.pi/consume-movie/notes/<agent_id>/notes.jsonl`
- **Clip Cache**: `~/.pi/consume-movie/clips/`

## Integration with /memory

Consumption events and notes are automatically stored in `/memory`:

```bash
# After adding a note, the skill calls:
./memory/run.sh learn \
  --problem "Watched Game of Thrones S03E10" \
  --solution "Observed manipulation pattern: authority denies approval" \
  --category emotional_learning \
  --tags manipulation,authority,family_dynamics
```
