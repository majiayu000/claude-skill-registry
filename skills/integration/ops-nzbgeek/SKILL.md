---
name: ops-nzbgeek
description: General-purpose NZBGeek search and SABnzbd download management with interview and task-monitor integration
triggers:
  - "nzbgeek search"
  - "download from nzbgeek"
  - "sabnzbd queue"
  - "sabnzbd status"
  - "usenet search"
  - "download nzb"
  - "search binaries"

provides:
  - ops-nzbgeek
composes: [, task-monitor]
---

# ops-nzbgeek - General-Purpose NZBGeek/SABnzbd Integration

Provides NZBGeek API search and SABnzbd API download operations for ANY content type (movies, TV, music, apps, books, etc.). Integrates with `/interview` for ambiguous searches and `/task-monitor` for download progress tracking.

## When to Use

**Use this skill when:**
- Searching NZBGeek for any content type
- Downloading content via SABnzbd
- Checking SABnzbd queue/download status
- Managing SABnzbd downloads (pause, resume, cancel)
- Content is ambiguous or unavailable (uses `/interview` to clarify)

**Triggers:**
- "Search NZBGeek for X"
- "Download Y from NZBGeek"
- "Check SABnzbd queue"
- "What's downloading in SABnzbd?"
- "Pause/resume/cancel download"

## Quick Start

```bash
# Search for content
~/.pi/skills/ops-nzbgeek/run.sh search "ubuntu iso" --category apps --limit 10

# Download via SABnzbd (with monitoring)
~/.pi/skills/ops-nzbgeek/run.sh download "<nzb_url>" --monitor

# Check queue status
~/.pi/skills/ops-nzbgeek/run.sh status

# Control downloads
~/.pi/skills/ops-nzbgeek/run.sh pause <nzb_id>
~/.pi/skills/ops-nzbgeek/run.sh resume <nzb_id>
~/.pi/skills/ops-nzbgeek/run.sh cancel <nzb_id>
```

## Commands

### Search

Search NZBGeek for content:

```bash
# Basic search
./run.sh search "query string"

# Search with category filter
./run.sh search "ubuntu" --category apps
./run.sh search "python book" --category books
./run.sh search "documentary" --category movies

# Limit results
./run.sh search "music" --limit 20

# JSON output
./run.sh search "query" --json
```

**Categories:**
- `movies` (2000) - Movies
- `tv` (5000) - TV shows
- `music` (3000) - Music
- `apps` (4000) - Applications
- `books` (7000) - Ebooks/Audiobooks
- `all` - Search all categories (default)

### Download

Download content via SABnzbd:

```bash
# Download NZB (basic)
./run.sh download "<nzb_url>"

# Download with monitoring (updates every 5 seconds)
./run.sh download "<nzb_url>" --monitor

# Dry-run (show API call without executing)
./run.sh download "<nzb_url>" --dry-run

# Download with custom category/priority
./run.sh download "<nzb_url>" --category software --priority 1
```

### Status

Check SABnzbd queue/download status:

```bash
# Check entire queue
./run.sh status

# Check specific download
./run.sh status --nzb-id <id>

# JSON output
./run.sh status --json
```

### Control

Manage active downloads:

```bash
# Pause download
./run.sh pause <nzb_id>

# Resume download
./run.sh resume <nzb_id>

# Cancel download
./run.sh cancel <nzb_id>
```

## Environment Variables

Required environment variables (set in `.env`):

```bash
# NZBGeek API credentials
NZBD_GEEK_API_KEY="your_api_key"
NZBD_GEEK_USER="your_username"
NZBD_GEEK_BASE_URL="https://api.nzbgeek.info/"

# SABnzbd API credentials
SABNZBD_API_KEY="your_api_key"
SABNZBD_BASE_URL="http://localhost:8090"
```

## Interview Integration

When search returns multiple results or content is unavailable, the skill automatically invokes `/interview` to ask clarifying questions:

```json
{
  "title": "Multiple results for 'ubuntu'",
  "questions": [{
    "id": "selection",
    "header": "Select",
    "text": "Which release?",
    "type": "select",
    "options": [
      {"label": "Ubuntu 24.04 LTS (5.2GB)", "description": "2024-04-25"},
      {"label": "Ubuntu 23.10 (4.8GB)", "description": "2023-10-12"}
    ]
  }]
}
```

The user selects an option, and the skill proceeds with the download.

## Task-Monitor Integration

When using `--monitor` flag, downloads are automatically registered with `/task-monitor`:

- **Registration**: Creates task entry in `~/.pi/task-monitor/registry.json`
- **Progress updates**: Every 5 seconds with % complete, speed, ETA
- **Completion notification**: Shows final size and time when done
- **Error tracking**: Failed downloads logged with error details

Monitor downloads via:
```bash
# TUI interface
~/.pi/skills/task-monitor/run.sh tui --filter nzbgeek

# Check specific download
cat ~/.pi/task-monitor/state/<nzb_id>.json
```

## File Organization

```
~/.pi/skills/ops-nzbgeek/
├── SKILL.md                # This file
├── run.sh                  # Dispatcher script
├── sanity.sh               # Sanity tests
├── pyproject.toml          # Dependencies
├── ops_nzbgeek/
│   ├── __init__.py
│   ├── cli.py              # Typer CLI
│   ├── search.py           # NZBGeek search
│   ├── download.py         # SABnzbd download
│   ├── status.py           # SABnzbd status/queue
│   ├── interview_helper.py # /interview integration
│   └── monitor_helper.py   # /task-monitor integration
└── sanity/
    ├── nzbgeek-api.sh      # NZBGeek API sanity check
    └── sabnzbd-api.sh      # SABnzbd API sanity check
```

## Sanity Checks

Run sanity tests to verify API connectivity:

```bash
# Run all sanity checks
./run.sh sanity

# Individual checks
./sanity/nzbgeek-api.sh
./sanity/sabnzbd-api.sh
```

**Sanity checks verify:**
- Environment variables are set
- NZBGeek API is accessible (200 status, valid JSON)
- SABnzbd API is accessible (200 status, queue data)

## Download Storage

Downloads are stored according to SABnzbd configuration:
- **Default**: Configured download directory (check SABnzbd settings)
- **User's setup**: 12TB drive at `/mnt/storage12tb/downloads/` (per SABnzbd config)

SABnzbd handles:
- Binary assembly from NZB segments
- PAR2 verification and repair
- RAR extraction
- File organization by category

## Examples

### Search and download workflow

```bash
# 1. Search for content
./run.sh search "python tutorial" --category books --limit 5

# 2. If multiple results, /interview is invoked automatically
# User selects option from TUI/HTML interface

# 3. Download selected item (with monitoring)
./run.sh download "<nzb_url_from_search>" --monitor

# 4. Check progress
./run.sh status --nzb-id <id>
```

### Batch downloads

```bash
# Search returns multiple URLs
URLS=$(./run.sh search "documentary series" --json | jq -r '.[].link')

# Download all with monitoring
for url in $URLS; do
  ./run.sh download "$url" --monitor &
done

# Monitor all via task-monitor TUI
~/.pi/skills/task-monitor/run.sh tui
```

## Integration with Other Skills

### ingest-movie

After ops-nzbgeek is complete, `ingest-movie` will delegate NZBGeek search to this skill:

```python
# Before (ingest-movie/search.py)
results = search_nzb(term, cat="2000")

# After (delegating to ops-nzbgeek)
results = subprocess.run(
    ["bash", "~/.pi/skills/ops-nzbgeek/run.sh", "search", term, "--category", "movies", "--json"],
    capture_output=True, text=True
).json()
```

### ingest-samples

Music sample library acquisition will use ops-nzbgeek for downloads:

```bash
# Search for Kontakt library
./run.sh search "Kontakt Factory Library" --category apps

# Download via SABnzbd
./run.sh download "<nzb_url>" --category audio --monitor
```

## API Reference

### NZBGeek API

**Search endpoint:**
```
GET https://api.nzbgeek.info/api?t=search&q=<query>&cat=<category>&apikey=<key>&o=json
```

**Response:**
```json
{
  "channel": {
    "item": [
      {
        "title": "Release Name",
        "size": "5242880000",
        "pubDate": "2024-01-15",
        "link": "https://api.nzbgeek.info/api?t=get&id=...",
        "category": "2000"
      }
    ]
  }
}
```

### SABnzbd API

**Queue endpoint:**
```
GET http://localhost:8090/api?mode=queue&apikey=<key>&output=json
```

**Add NZB:**
```
POST http://localhost:8090/api?mode=addurl&name=<nzb_url>&apikey=<key>
```

**Control:**
```
GET http://localhost:8090/api?mode=pause&value=<nzb_id>&apikey=<key>
GET http://localhost:8090/api?mode=resume&value=<nzb_id>&apikey=<key>
GET http://localhost:8090/api?mode=queue&name=delete&value=<nzb_id>&apikey=<key>
```

## Notes

- **General purpose**: Works with ANY content type on NZBGeek (not just movies)
- **Full binary downloads**: SABnzbd handles complete binary reconstruction from NZB segments
- **Storage**: Files stored on 12TB drive per SABnzbd configuration
- **Interview required**: Ambiguous searches MUST use `/interview` (per CONVENTIONS.md)
- **Task-monitor required**: All downloads SHOULD register with `/task-monitor` for progress tracking
- **Error handling**: Failed searches/downloads trigger interview for user clarification

## Skills Used

- `/interview` - Clarifying questions for ambiguous searches
- `/task-monitor` - Download progress tracking
