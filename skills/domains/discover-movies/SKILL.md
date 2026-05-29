---
name: discover-movies
description: >
  Discover new movies using TMDB API with Federated Taxonomy integration.
  Recommends movies based on genres, directors, and HMT bridge attributes.
  Can be invoked via /dogpile movies.
triggers:
  - discover movies
  - find new movies
  - movie recommendations
  - similar movies
  - movies like
  - dogpile movies
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Discover movies via TMDB + Taxonomy
---

# Discover Movies Skill

Find new movies for Horus based on preferences, taxonomy bridge attributes, and external discovery services.

## Quick Start

```bash
cd .pi/skills/discover-movies

# Find similar movies
./run.sh similar "There Will Be Blood"

# Get trending movies
./run.sh trending --range week

# Search by genre
./run.sh search-genre "psychological thriller"

# Search by bridge attribute
./run.sh bridge Corruption

# Movies by director
./run.sh by-director "Paul Thomas Anderson"

# New releases
./run.sh fresh

# Check API connectivity
./run.sh check
```

## Discovery Services

| Service | API | Use For |
|---------|-----|---------|
| **TMDB** | Free API key | Similar movies, trending, genres, recommendations |

TMDB API key required. Get one free at: https://www.themoviedb.org/settings/api

## Commands

### Similar Movies

```bash
./run.sh similar "<movie>" [--limit 10] [--json]
```

Find movies similar to a given movie via TMDB.

### Trending Movies

```bash
./run.sh trending [--range day|week] [--limit 10] [--json]
```

Get trending movies from TMDB.

### Search by Genre

```bash
./run.sh search-genre "<genre>" [--limit 10] [--json]
```

Search movies by genre name (Action, Drama, Horror, Thriller, etc.).

### Movies by Director

```bash
./run.sh by-director "<name>" [--limit 10] [--json]
```

Get movies directed by a specific person.

### Search by Bridge

```bash
./run.sh bridge <attribute> [--limit 10] [--json]
```

Search for movies matching an HMT bridge attribute:

| Bridge | Movie Genres |
|--------|--------------|
| Precision | thriller, heist, procedural, legal, documentary |
| Resilience | war, epic, survival, sports, biography |
| Fragility | drama, romance, indie, arthouse, coming-of-age |
| Corruption | noir, crime, psychological, horror, dystopian |
| Loyalty | family, period drama, historical, western, military |
| Stealth | mystery, espionage, slow burn, neo-noir, conspiracy |

### Fresh Releases

```bash
./run.sh fresh [--limit 10] [--json]
```

Get movies currently in theaters (new releases).

### Recommendations

```bash
./run.sh recommendations [--limit 10] [--json]
```

Get personalized recommendations based on consume-movie history.

### Check API

```bash
./run.sh check
```

Test connectivity to TMDB API.

## Integration with /dogpile

This skill can be invoked via `/dogpile movies`:

```bash
# Via dogpile
/dogpile movies "dark psychological thrillers similar to Blade Runner"

# Equivalent to
./run.sh similar "Blade Runner"
./run.sh bridge Corruption
```

## Taxonomy Integration

All JSON output includes taxonomy metadata for cross-collection graph traversal:

```json
{
  "results": [...],
  "taxonomy": {
    "bridge_tags": ["Corruption", "Stealth"],
    "collection_tags": {
      "domain": "Chaos",
      "function": "Revelation"
    },
    "confidence": 0.75,
    "worth_remembering": true
  }
}
```

This enables queries like:
- "Find movies with same bridge as Siege of Terra lore"
- "Movies matching Resilience theme"

## Configuration

Environment variables:

```bash
TMDB_API_KEY=xxx    # Required: TMDB API key
```

## Rate Limits

| Service | Limit | Implementation |
|---------|-------|----------------|
| TMDB | ~40 req/10s | 0.25s minimum interval |

## Example Horus Queries

```bash
# "What's similar to There Will Be Blood?"
./run.sh similar "There Will Be Blood" --limit 10

# "Find noir films"
./run.sh search-genre "noir"

# "Movies for a corruption scene" (Corruption bridge)
./run.sh bridge Corruption

# "Dark psychological thrillers"
./run.sh bridge Stealth

# "What's trending this week?"
./run.sh trending --range week

# "New releases for discovery"
./run.sh fresh --json
```

## Output Formats

All commands support `--json` for agent-parseable output with taxonomy:

```json
{
  "results": [
    {"id": 345, "title": "No Country for Old Men", "year": "2007", "genres": ["Crime", "Drama", "Thriller"]},
    {"id": 678, "title": "Sicario", "year": "2015", "genres": ["Action", "Crime", "Drama"]}
  ],
  "count": 2,
  "taxonomy": {
    "bridge_tags": ["Corruption", "Stealth"],
    "collection_tags": {"domain": "Chaos", "function": "Revelation"},
    "confidence": 0.75,
    "worth_remembering": true
  }
}
```

## Pipeline Integration

```
discover-movies → ingest-movie → consume-movie → review-story
      ↓                ↓              ↓              ↓
  Find movies    Download via    Watch with      Analyze
                 NZBGeek/Radarr  context         themes
```
