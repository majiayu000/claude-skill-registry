---
name: arr-all
version: 1.0.0
description: Unified command-line interface for Radarr, Sonarr, and Lidarr. Search, add, and manage movies (Radarr), TV shows (Sonarr), and music (Lidarr) with calendar view and health monitoring.
metadata:
  openclaw:
    requires:
      bins: ["curl", "jq"]
    optional:
      bins: ["column"]
---

# Arr-All

Unified interface for Radarr (movies), Sonarr (TV), and Lidarr (music).

## Setup

### Configuration

You can use a unified config file or existing individual configs.

**Unified Config (Preferred):**
Create `~/.openclaw/credentials/arr-all/config.json`:

```json
{
  "radarr": {
    "url": "http://localhost:7878",
    "apiKey": "...",
    "defaultQualityProfile": 1
  },
  "sonarr": {
    "url": "http://localhost:8989",
    "apiKey": "...",
    "defaultQualityProfile": 1,
    "defaultSeriesType": "standard"
  },
  "lidarr": {
    "url": "http://localhost:8686",
    "apiKey": "...",
    "defaultQualityProfile": 2,
    "defaultMetadataProfile": 7
  }
}
```

**Legacy Configs:**
Existing configs at `~/.openclaw/credentials/{radarr,sonarr,lidarr}/config.json` are also supported.

## Usage

Command format: `arr-all <type> <action> [args]`

### Common Commands

All media types support these core commands:

- **Search**: `arr-all [movie|tv|music] search "Query"`
- **Add**: `arr-all [movie|tv|music] add <id>`
- **Check**: `arr-all [movie|tv|music] exists <id>`
- **Remove**: `arr-all [movie|tv|music] remove <id> [--delete-files]`
- **Config**: `arr-all [movie|tv|music] config`

### Cross-Cutting Commands

- **Calendar**: `arr-all calendar [days=7]` (Upcoming releases)
- **Health**: `arr-all health` (Status of all apps)
- **Status**: `arr-all status` (Connection status)
- **Combined Search**: `arr-all search "Query"` (Searches all three)

### Type-Specific Features

**Movies (Radarr):**

- `arr-all movie add-collection <id>`
- `arr-all movie collections`

**TV (Sonarr):**

- `arr-all tv add <id> [--monitor latest|all|none|seasons:1,2]`
- `arr-all tv seasons <id>`
- `arr-all tv monitor-season <id> <season>`

**Music (Lidarr):**

- `arr-all music add <id> [--discography]`
- `arr-all music albums <id>`
- `arr-all music monitor-album <id>`

## Examples

**Add a Movie:**

```bash
arr-all movie search "Dune"
arr-all movie add 438631
```

**Check Calendar:**

```bash
arr-all calendar
```

**Check Health:**

```bash
arr-all health
```
