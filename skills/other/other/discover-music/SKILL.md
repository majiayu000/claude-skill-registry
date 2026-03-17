---
name: discover-music
description: >
  Discover new music using MusicBrainz and ListenBrainz APIs.
  Recommends music based on Horus taste profile and HMT bridge attributes.
  Can also be invoked via /dogpile music.
triggers:
  - discover music
  - find new music
  - music recommendations
  - similar to
  - music like
  - dogpile music
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Discover music via MusicBrainz + ListenBrainz

provides:
  - discover-music
composes:
  - learn-artist
  - ingest-yt-history
  - discover-books
  - discover-movies
  - dogpile
  - task-monitor
---

# Discover Music Skill

Find new music for Horus based on taste profile and external discovery services.

## Quick Start

```bash
cd .pi/skills/discover-music

# Find similar artists
./run.sh similar "Chelsea Wolfe"

# Get trending artists
./run.sh trending --range week

# Search by genre/style tag
./run.sh search-tag "doom metal"

# Search by bridge attribute
./run.sh bridge Corruption

# Get fresh releases
./run.sh fresh

# Check API connectivity
./run.sh check
```

## Discovery Services

| Service | API | Use For |
|---------|-----|---------|
| **MusicBrainz** | Free (User-Agent only) | Artist search, metadata, genre tags, relationships |
| **ListenBrainz** | Free (token optional) | Similar artists, trending, user stats, recommendations |

No API keys required for basic functionality. ListenBrainz token enables personalized recommendations.

## Commands

### Similar Artists

```bash
./run.sh similar "<artist>" [--limit 10] [--json]
```

Find artists similar to a given artist via ListenBrainz + MusicBrainz tags fallback.

### Trending Artists

```bash
./run.sh trending [--range week|month|year|all_time] [--limit 10] [--json]
```

Get site-wide trending artists from ListenBrainz.

### Search by Tag

```bash
./run.sh search-tag "<tag>" [--limit 10] [--json]
```

Search MusicBrainz for artists by genre/style tag (e.g., "doom metal", "dark folk").

### Search by Bridge

```bash
./run.sh bridge <attribute> [--limit 10] [--json]
```

Search for music matching an HMT bridge attribute:

| Bridge | MusicBrainz Tags |
|--------|------------------|
| Precision | progressive metal, math rock, technical death metal, djent |
| Resilience | epic metal, power metal, post-rock, cinematic, symphonic metal |
| Fragility | dark folk, acoustic, slowcore, sadcore, singer-songwriter |
| Corruption | industrial, doom metal, sludge metal, dark ambient, noise |
| Loyalty | neofolk, neoclassical, world, ritual ambient, medieval |
| Stealth | drone, dark ambient, ambient, minimalist, atmospheric |

### Fresh Releases

```bash
./run.sh fresh [--limit 10] [--json]
```

Get fresh/new releases from ListenBrainz explore API.

### User Top Artists

```bash
./run.sh user-top <username> [--range all_time] [--limit 10] [--json]
```

Get a ListenBrainz user's top artists.

### Check APIs

```bash
./run.sh check
```

Test connectivity to MusicBrainz and ListenBrainz APIs.

## Integration with /dogpile

This skill can be invoked via `/dogpile music`:

```bash
# Via dogpile
/dogpile music "dark atmospheric metal similar to Chelsea Wolfe"

# Equivalent to
./run.sh similar "Chelsea Wolfe"
./run.sh search-tag "dark atmospheric metal"
```

## Configuration

Environment variables (optional, in `.env`):

```bash
LISTENBRAINZ_TOKEN=xxx      # Optional: enables personalized recommendations
LISTENBRAINZ_USERNAME=xxx   # Optional: for user-specific queries
```

MusicBrainz requires no API key - only a User-Agent string (preconfigured as `HorusAgent/1.0`).

## Crucial Dependencies

| Library | API/Method | Sanity Script | Status |
|---------|------------|---------------|--------|
| musicbrainzngs | MusicBrainz API | `sanity/musicbrainz.py` | [x] PASS |
| pylistenbrainz | ListenBrainz API | `sanity/listenbrainz.py` | [x] PASS |
| requests | HTTP client | N/A (well-known) | - |

## Rate Limits

| Service | Limit | Implementation |
|---------|-------|----------------|
| MusicBrainz | 1 req/sec | Enforced in client |
| ListenBrainz | ~2 req/sec | 0.5s minimum interval |

## Example Horus Queries

```bash
# "What's similar to Chelsea Wolfe?"
./run.sh similar "Chelsea Wolfe" --limit 10

# "Find doom metal artists"
./run.sh search-tag "doom metal"

# "Music for a battle scene" (Resilience bridge)
./run.sh bridge Resilience

# "Dark ambient for corruption scene"
./run.sh bridge Corruption

# "What's trending this week?"
./run.sh trending --range week

# "New releases for discovery"
./run.sh fresh --json
```

## Output Formats

All commands support `--json` for agent-parseable output:

```json
[
  {"name": "Emma Ruth Rundle", "mbid": "abc123...", "similarity": 0.85},
  {"name": "Lingua Ignota", "mbid": "def456...", "similarity": 0.78}
]
```
