---
name: discover-books
description: >
  Discover new books using OpenLibrary API with Federated Taxonomy integration.
  Recommends books based on subjects, authors, and HMT bridge attributes.
  Can be invoked via /dogpile books.
triggers:
  - discover books
  - find new books
  - book recommendations
  - similar books
  - books like
  - dogpile books
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Discover books via OpenLibrary + Taxonomy

provides:
  - discover-books
composes:
  - dogpile
  - discover-movies
  - discover-music
  - memory
  - doc2qra
  - task-monitor
---

# Discover Books Skill

Find new books for Horus based on preferences, taxonomy bridge attributes, and OpenLibrary.

## Quick Start

```bash
cd .pi/skills/discover-books

# Find similar books
./run.sh similar "Dune"

# Get books by author
./run.sh by-author "Frank Herbert"

# Search by subject/genre
./run.sh search-subject "science fiction"

# Search by bridge attribute
./run.sh bridge Resilience

# Trending/popular books
./run.sh trending

# New releases
./run.sh fresh

# Check API connectivity
./run.sh check
```

## Discovery Services

| Service | API | Use For |
|---------|-----|---------|
| **OpenLibrary** | Free (no key) | Book search, authors, subjects, trending |

No API key required. Just respect rate limits (100 req/5 min).

## Commands

### Similar Books

```bash
./run.sh similar "<book>" [--limit 10] [--json]
```

Find books similar to a given book via shared subjects.

### Books by Author

```bash
./run.sh by-author "<name>" [--limit 10] [--json]
```

Get all books by a specific author.

### Search by Subject

```bash
./run.sh search-subject "<subject>" [--limit 10] [--json]
```

Search books by subject or genre (e.g., "science fiction", "horror", "philosophy").

### Search by Bridge

```bash
./run.sh bridge <attribute> [--limit 10] [--json]
```

Search for books matching an HMT bridge attribute:

| Bridge | Book Subjects |
|--------|---------------|
| Precision | hard science fiction, technical thriller, mathematics, philosophy |
| Resilience | epic fantasy, military fiction, adventure, survival, heroic |
| Fragility | literary fiction, poetry, memoir, psychological, coming of age |
| Corruption | dark fantasy, horror, grimdark, cosmic horror, dystopian |
| Loyalty | historical fiction, saga, mythology, family saga, war |
| Stealth | mystery, espionage, thriller, detective, conspiracy |

### Trending Books

```bash
./run.sh trending [--limit 10] [--json]
```

Get popular/trending books (by edition count).

### Fresh Releases

```bash
./run.sh fresh [--limit 10] [--json]
```

Get recently published books.

### Recommendations

```bash
./run.sh recommendations [--limit 10] [--json]
```

Get personalized recommendations based on consume-book history.

### Check API

```bash
./run.sh check
```

Test connectivity to OpenLibrary API.

## Integration with /dogpile

This skill can be invoked via `/dogpile books`:

```bash
# Via dogpile
/dogpile books "epic fantasy similar to Dune"

# Equivalent to
./run.sh similar "Dune"
./run.sh bridge Resilience
```

## Taxonomy Integration

All JSON output includes taxonomy metadata for cross-collection graph traversal:

```json
{
  "results": [...],
  "taxonomy": {
    "bridge_tags": ["Resilience", "Precision"],
    "collection_tags": {
      "domain": "Imperium",
      "function": "Revelation"
    },
    "confidence": 0.75,
    "worth_remembering": true
  }
}
```

This enables queries like:
- "Find books with same bridge as Siege of Terra lore"
- "Books matching Fragility theme"

## Configuration

No environment variables required. OpenLibrary is free and open.

## Rate Limits

| Service | Limit | Implementation |
|---------|-------|----------------|
| OpenLibrary | ~100 req/5 min | 0.5s minimum interval |

## Example Horus Queries

```bash
# "What's similar to Dune?"
./run.sh similar "Dune" --limit 10

# "Books by Frank Herbert"
./run.sh by-author "Frank Herbert"

# "Find cosmic horror books"
./run.sh search-subject "cosmic horror"

# "Books for a resilience scene" (Resilience bridge)
./run.sh bridge Resilience

# "Dark fantasy for corruption scene"
./run.sh bridge Corruption

# "What's popular right now?"
./run.sh trending

# "New releases for discovery"
./run.sh fresh --json
```

## Output Formats

All commands support `--json` for agent-parseable output with taxonomy:

```json
{
  "results": [
    {"key": "/works/OL45804W", "title": "Dune", "authors": "Frank Herbert", "year": "1965", "subjects": ["science fiction", "space opera"]},
    {"key": "/works/OL45810W", "title": "Children of Dune", "authors": "Frank Herbert", "year": "1976", "subjects": ["science fiction"]}
  ],
  "count": 2,
  "taxonomy": {
    "bridge_tags": ["Resilience", "Precision"],
    "collection_tags": {"domain": "Imperium", "function": "Revelation"},
    "confidence": 0.75,
    "worth_remembering": true
  }
}
```

## Pipeline Integration

```
discover-books → ingest-book → consume-book → review-story
      ↓               ↓             ↓              ↓
  Find books    Download via    Read with       Analyze
                Readarr         context         themes
```
