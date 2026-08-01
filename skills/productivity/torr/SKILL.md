---
name: torr
description: 'Search and download torrents using ArcTorrent API and WebTorrent. Use
  when users request to: (1) Search for torrents across multiple sources, (2) Download
  content via magnet links, (3) Find torrents f'
---

---
name: torr
description: Search and download torrents using ArcTorrent API and WebTorrent. Use when users request to: (1) Search for torrents across multiple sources, (2) Download content via magnet links, (3) Find torrents filtered by seeder counts, or any torrent-related tasks
---

# Torrent Search & Download

## Prerequisites

- ArcTorrent API at `http://localhost:3000`
  ```bash
  # Clone to /tmp and start
  cd /tmp && git clone https://github.com/theriturajps/ArcTorrent
  cd ArcTorrent && npm install && npm start &
  ```
- `jq` for JSON parsing

## Search

```bash
scripts/search.sh <source> "<query>" [page]
scripts/search.sh piratebay "ubuntu iso" 1
scripts/search.sh yts "big buck bunny" 1
```

### Sources

List available sources:
```bash
scripts/search.sh --list-sources
```

### Get Magnet Link

```bash
# First result
scripts/search.sh piratebay "ubuntu" 1 | head -1 | cut -f4

# Filter by seeders (>10), get first magnet
scripts/search.sh piratebay "ubuntu" 1 | awk -F'\t' '$3+0 > 10 {print $4; exit}'
```

## Download

```bash
# Basic download
node scripts/download.js "magnet:?xt=urn:btih:..." /tmp/downloads

# With custom timeout (default: 10800s)
node scripts/download.js "magnet:?xt=urn:btih:..." /tmp/downloads --timeout 3600

# JSON output for automation
node scripts/download.js "magnet:?xt=urn:btih:..." /tmp/downloads --json
```

## Complete Workflow

```bash
MAGNET=$(scripts/search.sh piratebay "ubuntu iso" 1 | head -1 | cut -f4)
node scripts/download.js "$MAGNET" /tmp/downloads
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| API not responding | `cd /tmp/ArcTorrent && npm start &` |
| Download slow/hangs | Filter for seeders > 20; try different source |
