---
name: plex-media-server
description: Plex Media Server API — library management, media search, playback sessions, server status, and automation
---

# Plex Media Server

Manage your Plex Media Server: scan libraries, search media, monitor playback sessions, and automate maintenance.

## Authentication

All Plex API calls require an `X-Plex-Token`. Find yours:

1. Open Plex Web → any media item → Get Info → View XML → check URL for `X-Plex-Token=`
2. Or from the Plex claim: `curl -s "https://plex.tv/api/v2/user" -H "X-Plex-Token: YOUR_TOKEN" | jq .`

```bash
export PLEX_URL="http://localhost:32400"
export PLEX_TOKEN="YOUR_PLEX_TOKEN"
```

## Server status

```bash
# Server identity
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/identity" | jq .

# Server capabilities
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/" | jq '.MediaContainer | {friendlyName, version, platform, updatedAt}'

# Server preferences
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/:/prefs" | jq '.MediaContainer.Setting[] | {id, value}'
```

## Libraries

### List libraries

```bash
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/sections" | \
  jq '.MediaContainer.Directory[] | {key, title, type, agent, scanner}'
```

### Scan library

```bash
# Scan specific library (use key from list)
curl -s -X POST -H "X-Plex-Token: $PLEX_TOKEN" \
  "$PLEX_URL/library/sections/SECTION_KEY/refresh"

# Scan all libraries
curl -s -X POST -H "X-Plex-Token: $PLEX_TOKEN" \
  "$PLEX_URL/library/sections/all/refresh"

# Force full metadata refresh
curl -s -X POST -H "X-Plex-Token: $PLEX_TOKEN" \
  "$PLEX_URL/library/sections/SECTION_KEY/refresh?force=1"
```

### Browse library contents

```bash
# List all items in a library section
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/sections/SECTION_KEY/all" | \
  jq '.MediaContainer.Metadata[] | {title, year, rating, addedAt}'

# Recently added
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/recentlyAdded" | \
  jq '.MediaContainer.Metadata[] | {title, type, year, addedAt}'

# On deck (continue watching)
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/onDeck" | \
  jq '.MediaContainer.Metadata[] | {title, grandparentTitle, viewOffset, duration}'
```

## Search

```bash
# Search across all libraries
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/hubs/search?query=inception" | \
  jq '.MediaContainer.Hub[] | {type, size, Metadata: [.Metadata[]? | {title, year, type}]}'

# Search specific library
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/sections/SECTION_KEY/search?query=inception" | \
  jq '.MediaContainer.Metadata[] | {title, year, summary}'
```

## Playback sessions

### Currently playing

```bash
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/status/sessions" | \
  jq '.MediaContainer.Metadata[]? | {
    title,
    user: .User.title,
    player: .Player.title,
    state: .Player.state,
    progress: ((.viewOffset / .duration * 100) | round),
    transcoding: (.TranscodeSession != null)
  }'
```

### Playback history

```bash
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/status/sessions/history/all" | \
  jq '.MediaContainer.Metadata[] | {title, viewedAt, accountID}'
```

## Media info

### Get item details

```bash
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/metadata/RATING_KEY" | \
  jq '.MediaContainer.Metadata[0] | {title, year, summary, rating, Media: [.Media[] | {videoResolution, bitrate, container}]}'
```

### Get TV show seasons and episodes

```bash
# Seasons of a show
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/metadata/SHOW_RATING_KEY/children" | \
  jq '.MediaContainer.Metadata[] | {title, index, leafCount}'

# Episodes of a season
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/library/metadata/SEASON_RATING_KEY/children" | \
  jq '.MediaContainer.Metadata[] | {title, index, duration}'
```

## Maintenance

### Optimize database

```bash
curl -s -X PUT -H "X-Plex-Token: $PLEX_TOKEN" \
  "$PLEX_URL/library/optimize"
```

### Clean bundles (remove orphaned data)

```bash
curl -s -X PUT -H "X-Plex-Token: $PLEX_TOKEN" \
  "$PLEX_URL/library/clean/bundles"
```

### Empty trash for a library

```bash
curl -s -X PUT -H "X-Plex-Token: $PLEX_TOKEN" \
  "$PLEX_URL/library/sections/SECTION_KEY/emptyTrash"
```

### Analyze media (detect intros, credits)

```bash
# Analyze all items in a library
curl -s -X POST -H "X-Plex-Token: $PLEX_TOKEN" \
  "$PLEX_URL/library/sections/SECTION_KEY/analyze"
```

## Playback control

```bash
# Get list of available players
curl -s -H "X-Plex-Token: $PLEX_TOKEN" \
  -H "Accept: application/json" \
  "$PLEX_URL/clients" | \
  jq '.MediaContainer.Server[] | {name, address, port, machineIdentifier}'
```

## Docker deployment

```yaml
services:
  plex:
    image: lscr.io/linuxserver/plex:latest
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Amsterdam
      - VERSION=docker
      - PLEX_CLAIM=claim-XXXXX  # From https://plex.tv/claim
    ports:
      - "32400:32400"
    volumes:
      - ./plex-config:/config
      - /path/to/movies:/movies
      - /path/to/tv:/tv
    restart: unless-stopped
```

## Webhooks

Plex can send webhooks on playback events (requires Plex Pass):

Events: `media.play`, `media.pause`, `media.resume`, `media.stop`, `media.scrobble`, `library.new`, `library.on.deck`

Configure in Settings → Webhooks → Add Webhook URL.

### Example: ntfy notification on new media

```bash
# Receive webhook and forward to ntfy (simple Flask/Node server)
# Plex sends POST with JSON payload containing event type and metadata
# Parse and forward:
curl -H "Authorization: Bearer $NTFY_TOKEN" \
     -H "Tags: movie_camera" \
     -d "New on Plex: $TITLE ($YEAR)" \
     "https://ntfy.example.com/plex"
```

## Integration with Radarr/Sonarr

Trigger Plex library scan after Radarr/Sonarr imports:

- Radarr: Settings → Connect → Add → Plex Media Server → enter host, port, token
- Sonarr: Settings → Connect → Add → Plex Media Server → same config

This automatically scans the relevant library section after new media is imported.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Library not showing new files | Trigger manual scan: `POST /library/sections/KEY/refresh` |
| Remote access not working | Check port 32400 forwarded, or use reverse proxy. Check Settings → Remote Access |
| Transcoding issues | Check hardware transcoding enabled. Verify `/dev/dri` mapped for Intel QSV |
| Slow library scan | Run `optimize` and `clean/bundles`. Check disk I/O |
| Metadata wrong | Force refresh: `PUT /library/metadata/KEY/refresh?force=1` |
| "Not authorized" | Token expired or wrong. Re-fetch from Plex Web UI |
| Database locked | Stop Plex, check for `com.plexapp.plugins.library.db-wal`, restart |
