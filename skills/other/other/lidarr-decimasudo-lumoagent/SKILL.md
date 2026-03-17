---
name: lidarr
version: 1.0.0
description: Search and add music to Lidarr. Supports artists, albums, and quality profiles (FLAC preferred).
metadata: {"openclaw":{"emoji":"🎵","requires":{"bins":["curl","jq"]}}}
---

# Lidarr

Add music (artists and albums) to your Lidarr library.

## Setup

Create `~/.clawdbot/credentials/lidarr/config.json`:
```json
{
  "url": "http://192.168.1.50:8686",
  "apiKey": "efbd6c29db184911a7b0f4707ae8f10f",
  "defaultQualityProfile": 2,
  "defaultMetadataProfile": 7
}
```

- `defaultQualityProfile`: Quality profile ID (FLAC, MP3, etc. — run `config` to see options)
- `defaultMetadataProfile`: Metadata profile ID (albums only, discography, etc. — run `config` to see options)

## Quality Profiles
Typically you'll want FLAC:
- Lossless (FLAC)
- Lossless 24bit (FLAC 24-bit)

## Metadata Profiles
- **Albums only** (recommended) — just studio albums
- Standard — albums + some extras
- Discography / Everything — all releases

## Workflow

### 1. Search for an artist
```bash
bash scripts/lidarr.sh search "Artist Name"
```
Returns numbered list with MusicBrainz links.

### 2. Check if artist exists
```bash
bash scripts/lidarr.sh exists <foreignArtistId>
```

### 3. Add artist
```bash
bash scripts/lidarr.sh add <foreignArtistId>
```
If artist already exists, this will monitor them instead of failing.

**Options:**
- `--discography` — add full discography instead of albums only
- `--no-search` — don't search immediately

### 4. List albums for an artist
```bash
bash scripts/lidarr.sh list-artist-albums <artistId>
```
Shows all albums with their IDs and monitored status.

### 5. Monitor specific albums
```bash
bash scripts/lidarr.sh monitor-album <albumId>
```
Monitor and optionally search for a specific album.

**Options:**
- `--no-search` — monitor but don't search yet

## Commands

### Search for artists
```bash
bash scripts/lidarr.sh search "KMFDM"
```

### Check if artist exists
```bash
bash scripts/lidarr.sh exists 45074d7c-5307-44a8-854f-ae072e1622ae
```

### Add an artist (FLAC + albums only by default)
```bash
bash scripts/lidarr.sh add 45074d7c-5307-44a8-854f-ae072e1622ae
```

### Add with full discography
```bash
bash scripts/lidarr.sh add 45074d7c-5307-44a8-854f-ae072e1622ae --discography
```

### List albums for an artist
```bash
bash scripts/lidarr.sh list-artist-albums 382
```

### Monitor a specific album
```bash
bash scripts/lidarr.sh monitor-album 11116
```

### List your library
```bash
bash scripts/lidarr.sh list
```

### Refresh artist metadata
```bash
bash scripts/lidarr.sh refresh <artistId>
```

### Remove an artist
```bash
bash scripts/lidarr.sh remove <artistId>              # keep files
bash scripts/lidarr.sh remove <artistId> --delete-files  # delete files too
```

### Get configuration
```bash
bash scripts/lidarr.sh config
```
