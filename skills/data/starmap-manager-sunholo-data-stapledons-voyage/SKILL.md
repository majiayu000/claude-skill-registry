---
name: Starmap Manager
description: Manage starmap data assets for Stapledons Voyage. Use when downloading star catalogs, galactic backgrounds, or processing astronomical data. (project)
---

# Starmap Manager

Download, process, and manage astronomical data for the game's 3D starmap. Handles real star catalogs (Gaia), exoplanet data (NASA), and galactic background imagery (ESA/ESO).

## Quick Start

**Most common usage:**
```bash
# Download quick dataset (~2MB total, fastest start)
.claude/skills/starmap-manager/scripts/download_stars.sh quick

# Download medium dataset (~15MB, richer local bubble)
.claude/skills/starmap-manager/scripts/download_stars.sh medium

# Download galactic background
.claude/skills/starmap-manager/scripts/download_background.sh

# Check what's installed
.claude/skills/starmap-manager/scripts/status.sh
```

## When to Use This Skill

Invoke this skill when:
- User wants to download real star data for the game
- User asks about Gaia, exoplanet, or astronomical data sources
- User wants galactic background images/textures
- Setting up starmap assets for the first time
- Upgrading from quick to medium/large dataset

## Data Tiers

| Tier | Stars | Exoplanets | Size | Use Case |
|------|-------|------------|------|----------|
| **Quick** | 5,930 (CNS5) | ~6,000 | ~2 MB | Rapid prototyping |
| **Medium** | ~50,000 (filtered GCNS) | ~6,000 | ~15 MB | Release candidate |
| **Large** | 331,312 (full GCNS) | ~6,000 | ~75 MB | HD/DLC option |

## Available Scripts

### `scripts/download_stars.sh <tier>`
Download star catalog for specified tier (quick/medium/large).

```bash
# Quick: CNS5 nearby stars (~1.2MB)
.claude/skills/starmap-manager/scripts/download_stars.sh quick

# Medium: Filtered GCNS G/K/M dwarfs (~10MB)
.claude/skills/starmap-manager/scripts/download_stars.sh medium

# Large: Full GCNS 100pc catalog (~72MB compressed)
.claude/skills/starmap-manager/scripts/download_stars.sh large
```

### `scripts/download_exoplanets.sh`
Download NASA Exoplanet Archive confirmed planets (~3MB).

```bash
.claude/skills/starmap-manager/scripts/download_exoplanets.sh
```

### `scripts/download_background.sh [resolution]`
Download ESA Gaia all-sky map for galactic background.

```bash
# 4K version (4096x2048, ~5MB) - default
.claude/skills/starmap-manager/scripts/download_background.sh 4k

# 8K version (8192x4096, ~20MB)
.claude/skills/starmap-manager/scripts/download_background.sh 8k
```

### `scripts/process_stars.sh`
Convert downloaded star catalogs to game-ready format.

```bash
# Process all downloaded catalogs
.claude/skills/starmap-manager/scripts/process_stars.sh
```

### `scripts/status.sh`
Show current starmap asset status.

```bash
.claude/skills/starmap-manager/scripts/status.sh
```

## Workflow

### 1. Initial Setup (Quick Start)

```bash
# Download minimal dataset for development
.claude/skills/starmap-manager/scripts/download_stars.sh quick
.claude/skills/starmap-manager/scripts/download_exoplanets.sh
.claude/skills/starmap-manager/scripts/download_background.sh
.claude/skills/starmap-manager/scripts/process_stars.sh
```

### 2. Upgrade to Medium (Pre-Release)

```bash
# Get richer dataset for release
.claude/skills/starmap-manager/scripts/download_stars.sh medium
.claude/skills/starmap-manager/scripts/process_stars.sh
```

### 3. HD Assets (Optional DLC)

```bash
# Full catalog + high-res background
.claude/skills/starmap-manager/scripts/download_stars.sh large
.claude/skills/starmap-manager/scripts/download_background.sh 8k
.claude/skills/starmap-manager/scripts/process_stars.sh
```

## Output Files

All processed data goes to `assets/data/starmap/`:

```
assets/data/starmap/
├── stars.json          # Combined star catalog (positions, types, etc.)
├── exoplanets.json     # Confirmed exoplanets with orbital data
├── habitable.json      # Pre-filtered habitable zone candidates
└── background/
    └── galaxy_4k.png   # All-sky galactic panorama
```

## Resources

### Data Sources
See [`resources/data_sources.md`](resources/data_sources.md) for:
- Complete data source documentation
- API endpoints and download URLs
- Data schemas and column descriptions
- Licensing information (all CC BY-SA 3.0 compatible)

### Processing Pipeline
See [`resources/processing.md`](resources/processing.md) for:
- Coordinate conversion (RA/Dec to galactic XYZ)
- Filtering criteria for each tier
- JSON schema for game integration
- Habitable zone calculations

## Notes

- **Licensing**: All data is CC BY-SA 3.0 or public domain
- **Updates**: Star positions don't change; exoplanets update quarterly
- **Determinism**: Same processing produces identical output
- **Dependencies**: Requires `curl`, `jq`, `python3` (for coordinate conversion)
