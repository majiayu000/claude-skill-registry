---
name: image-well
description: "Multi-source image search and download aggregator. Searches 12 image APIs in parallel (Openverse, Pexels, Pixabay, Met Museum, NASA, Rijksmuseum, Wikimedia Commons, Unsplash, Smithsonian, Europeana, Iconify, Pollinations AI). This skill should be used when searching for images, downloading stock photos, finding public domain artwork, sourcing museum images, searching for CC-licensed images, downloading NASA photos, finding icons, or when any project needs images from multiple sources at once. Supports license filtering, presets (military, museum, stock), cached results, and bulk download with metadata sidecars."
---

# Image Well

Search and download images from 12 sources through a single CLI. Four sources work with zero API keys (Openverse, Wikimedia, Met Museum, NASA). Additional sources activate when keys are set.

## Quick Start

```bash
# Search across all no-key sources
uv run ~/.claude/skills/image-well/scripts/well.py search "ancient Minoan fresco"

# Use a preset for domain-specific searches
uv run ~/.claude/skills/image-well/scripts/well.py search "F-35 fighter jet" --preset military

# Download results with metadata sidecars
uv run ~/.claude/skills/image-well/scripts/well.py search "sunset" --format download --output ./images/

# Check which sources are available
uv run ~/.claude/skills/image-well/scripts/well.py sources

# Visual HTML preview — opens in browser, no context pollution
uv run ~/.claude/skills/image-well/scripts/well.py search "bronze statue" --format html

# Output as JSON for piping
uv run ~/.claude/skills/image-well/scripts/well.py search "cat" --format json
```

## Sources

| Tier | Source | Key Required | License |
|------|--------|-------------|---------|
| 1 | Openverse (800M+) | No | CC variants |
| 1 | Wikimedia Commons | No | CC variants |
| 1 | Met Museum (375k) | No | CC0 |
| 1 | NASA (140k) | No | Public Domain |
| 2 | Pexels | `PEXELS_API_KEY` | Pexels License |
| 2 | Pixabay | `PIXABAY_API_KEY` | Pixabay License |
| 2 | Rijksmuseum (700k) | `RIJKSMUSEUM_API_KEY` | CC0 |
| 2 | Unsplash | `UNSPLASH_ACCESS_KEY` | Unsplash License |
| 3 | Smithsonian | No | CC0 |
| 3 | Europeana (50M+) | `EUROPEANA_API_KEY` | Mixed |
| 3 | Iconify (275k icons) | No | Various |
| 3 | Pollinations AI | No | Free Use (AI gen) |

Add Tier 2 keys to `~/.config/env/secrets.env` for expanded coverage.

## Presets

| Preset | Sources | Use Case |
|--------|---------|----------|
| `military` | nasa, wikimedia, smithsonian | Defense/military imagery |
| `museum` | met, rijksmuseum, smithsonian | Art, antiquities, historical |
| `texture` | wikimedia, pollinations | Game dev, 3D materials |
| `stock` | pexels, pixabay, unsplash | Editorial photography |
| `all-free` | openverse, wikimedia, met, nasa, smithsonian | All no-key sources |

## Options

```
--sources NAME [...]    Specific sources to search
--preset NAME           Use a preset group
--limit N               Max results per source (default: 10)
--license LICENSE       Filter: cc0, cc-by, cc-by-sa, any
--format FORMAT         table, json, download, urls
--output DIR            Download directory (default: ./well-images/)
--no-cache              Skip result cache
--timeout N             Per-source timeout in seconds (default: 15)
--quiet                 Suppress progress output
```

## Workflows

### Source images for a project
```bash
# Search, review in table, then download the good ones
uv run well.py search "Mediterranean landscape" --preset stock --format json > results.json
# Review results.json, then download specific URLs
```

### Build an image corpus
```bash
# Download CC0 images for a research project
uv run well.py search "Bronze Age pottery" --preset museum --license cc0 --format download --output ./corpus/
```

### Pipe to image-forge for processing
```bash
# Search, download, then resize with image-forge
uv run well.py search "sunset" --format download --output ./raw/
# Then use image-forge skill to process downloaded images
```

## Cache

Results are cached for 24 hours at `~/.cache/image-well/`.

```bash
uv run well.py cache stats    # Show cache size
uv run well.py cache clear    # Clear all cached results
```
