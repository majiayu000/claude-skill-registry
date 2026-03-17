---
name: classical-887
description: "This skill should be used when checking what's playing on WRHV 88.7 FM (Classical WMHT) in the Hudson Valley, fetching recent tracks, building playlist reports, searching for pieces, creating/renaming Spotify playlists from radio tracks, auditing/cleaning up Spotify playlists, exporting playlist tracks to JSON, or reviewing playlist operation history."
---

# Classical 887

Check what's playing on WRHV 88.7 FM (Classical WMHT) — the classical music station in the Hudson Valley. Queries the NPR Composer API for real-time playlist data and provides clickable links to listen on YouTube, Spotify, Apple Music, IMSLP, IDAGIO, Internet Archive, and Musopen.

## When to Use

- Checking what's playing right now on 88.7
- Getting recent tracks with links to listen again
- Building a Markdown playlist report
- Finding a specific piece heard on the radio
- Creating Spotify playlists from radio tracks
- Renaming Spotify playlists
- Auditing owned Spotify playlists (list, search, sort)
- Cleaning up accumulated Spotify playlists (safe bulk removal)
- Exporting playlist track data to JSON before cleanup
- Reviewing playlist operation history

## Prerequisites

- `requests` Python package (`uv pip install --system requests`)
- No API key required — uses NPR's public Composer API
- **Spotify integration (optional):** `spotipy` package (`uv pip install --system spotipy`) + Spotify Developer App credentials

## Usage

```bash
# What's playing right now (default)
python3 ~/.claude/skills/classical-887/scripts/classical_887.py

# Last 10 tracks
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --recent 10

# Today's full playlist (pages through all tracks for today)
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --period today

# Last week as Markdown report
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --period week --markdown ~/Desktop/classical-week.md

# Last month as Markdown report
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --period month --markdown ~/Desktop/classical-month.md

# Specific date (Valentine's Day)
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --date 2026-02-14

# Search for a composer across a date range
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --period week --search bach

# Full performer details (album, label, catalog number)
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --recent 5 --verbose

# Raw JSON output
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --now --json

# Create Spotify playlist from today's tracks
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --period today --spotify-playlist

# Add yesterday's tracks to the persistent playlist
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --period yesterday --spotify-playlist

# Custom playlist name from a specific date
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --date 2026-02-14 --spotify-playlist "Valentine's Classical"

# Last week's Bach on Spotify
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --period week --search bach --spotify-playlist "Bach on 88.7"

# Rename the default playlist
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-rename "Hudson Valley Classical"

# Rename a specific playlist with a new description
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-playlist "Bach on 88.7" --spotify-rename "Bach Collection" --spotify-description "Curated Bach from WRHV 88.7 FM"

# View playlist operation log as Markdown
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-log-report

# Audit all owned Spotify playlists
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-audit

# Audit with search filter and sort by track count
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-audit --search "Rediscover*" --sort tracks

# Dry run cleanup (preview only, no deletion)
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-cleanup "Rediscover*"

# Execute cleanup with safety cap
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-cleanup "Rediscover*" --confirm --max 10

# Export playlist tracks to JSON before cleanup
python3 ~/.claude/skills/classical-887/scripts/classical_887.py --spotify-export ~/Desktop/exports --search "Rediscover*"
```

## Parameters

| Flag | Description | Default |
|------|-------------|---------|
| `--now` | Show what's playing now | On (if no other mode) |
| `--recent N` | Show last N tracks (1–100) | Off |
| `--date YYYY-MM-DD` | Fetch all tracks from a specific date | Off |
| `--period PERIOD` | Fetch tracks from: `today`, `yesterday`, `week`, `month` | Off |
| `--search QUERY` | Filter results by composer, piece, or performer | Off |
| `--verbose` | Full details (album, label, catalog, all performers) | Off |
| `--json` | Raw JSON output | Off |
| `--markdown [FILE]` | Write Markdown report with clickable links | `classical-playlist.md` |
| `--sort FIELD` | Sort by: `time` (newest first), `duration` (longest), `composer` (A–Z) | `time` |
| `--spotify-playlist [NAME]` | Create/append to a Spotify playlist | `Classical 88.7 FM` |
| `--spotify-rename NEW_NAME` | Rename an existing Spotify playlist (defaults to renaming `Classical 88.7 FM` unless `--spotify-playlist` specifies the current name) | Off |
| `--spotify-description DESC` | Set new description when renaming (used with `--spotify-rename`) | Off |
| `--spotify-log-report` | View the playlist operation log as a Markdown report | Off |
| `--spotify-audit` | List all owned Spotify playlists (combine with `--search` and `--sort`) | Off |
| `--spotify-cleanup PATTERN` | Remove playlists matching glob pattern (dry run unless `--confirm`) | Off |
| `--spotify-export [DIR]` | Export matching playlist tracks to JSON files | `.` |
| `--confirm` | Execute cleanup (without this, `--spotify-cleanup` is preview only) | Off |
| `--max N` | Safety cap: max playlists to remove per invocation | No limit |
| `--spotify-client-id ID` | Spotify app client ID (or `SPOTIFY_CLIENT_ID` env var) | — |
| `--spotify-client-secret SECRET` | Spotify app client secret (or `SPOTIFY_CLIENT_SECRET` env var) | — |

## Output

Default shows: composer, piece, performers, duration, and listen links (YouTube, Spotify, Apple Music, IMSLP, IDAGIO, Internet Archive, Musopen).

Markdown report includes: now-playing header, recent tracks table with 7 platform links, and a composer index.

## Playlist Log

Every `--spotify-playlist` operation automatically appends a JSONL entry to `~/.claude/skills/classical-887/playlist-log.jsonl`. Each entry records:

- Date and action (created/appended)
- Playlist name and Spotify URL
- Tracks added (composer, piece, performers, duration, Spotify URI)
- Tracks not found on Spotify
- Total counts (matched/unmatched)

View the log as a Markdown report with `--spotify-log-report`. The log file is append-only and can be queried with standard `jq` commands:

```bash
# Count total operations
wc -l ~/.claude/skills/classical-887/playlist-log.jsonl

# Show all playlist names used
cat ~/.claude/skills/classical-887/playlist-log.jsonl | jq -r '.playlist_name' | sort -u

# Total tracks matched across all operations
cat ~/.claude/skills/classical-887/playlist-log.jsonl | jq '.matched_count' | paste -sd+ | bc
```

## Data Source

NPR Composer API (`api.composer.nprstations.org/v1/widget/`), which powers the WMHT playlist widget at `classicalwmht.org/playlist`.

Full API documentation: `references/api-reference.md`

## Station Info

WRHV 88.7 FM (Poughkeepsie, NY), simulcast of WMHT-FM 89.1 (Schenectady). Full station details in `references/api-reference.md`.

- Stream: [wmht.org/classical](https://wmht.org/classical/)
- Playlist: [classicalwmht.org/playlist](https://classicalwmht.org/playlist)

## Fallback

If the NPR Composer API is unavailable:

```bash
# Check the playlist page directly
firecrawl scrape "https://classicalwmht.org/playlist" --only-main-content
```

## Reference Documentation

| File | Contents |
|------|----------|
| `references/api-reference.md` | NPR Composer API: endpoints, request/response schema, field reference |
| `references/spotify-setup.md` | Spotify Developer App setup, OAuth, env vars, Dev Mode notes |
