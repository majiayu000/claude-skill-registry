---
name: arr-media-stack
description: Radarr, Sonarr, Prowlarr, Bazarr, and qBittorrent APIs for automated media management — search, add, monitor, and troubleshoot downloads
---

# Arr Media Stack

Manage your automated media stack: Radarr (movies), Sonarr (TV), Prowlarr (indexers), Bazarr (subtitles), and qBittorrent (downloads).

All APIs use `X-Api-Key` header for auth. Base URLs default to `http://localhost:<port>/api/v3` (Radarr/Sonarr/Prowlarr) or `http://localhost:<port>/api/v2` (Bazarr).

## Radarr (Movies) — port 7878

### Search and add a movie

```bash
# Search by name
curl -s -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/movie/lookup?term=inception" | jq '.[0] | {title, year, tmdbId}'

# Add movie (use tmdbId from lookup)
curl -s -X POST -H "X-Api-Key: YOUR_RADARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tmdbId": 27205,
    "title": "Inception",
    "qualityProfileId": 1,
    "rootFolderPath": "/movies",
    "monitored": true,
    "addOptions": {"searchForMovie": true}
  }' "http://localhost:7878/api/v3/movie"
```

### List and manage movies

```bash
# List all movies
curl -s -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/movie" | jq '.[] | {id, title, year, monitored, hasFile}'

# Get specific movie
curl -s -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/movie/1"

# Delete movie (with files)
curl -s -X DELETE -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/movie/1?deleteFiles=true"

# Trigger search for missing movies
curl -s -X POST -H "X-Api-Key: YOUR_RADARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "MissingMoviesSearch"}' \
  "http://localhost:7878/api/v3/command"
```

### Queue and downloads

```bash
# View download queue
curl -s -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/queue" | jq '.records[] | {title, status, sizeleft, timeleft}'

# System health
curl -s -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/health" | jq '.[] | {type, message}'

# Root folders
curl -s -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/rootfolder" | jq '.[] | {path, freeSpace}'

# Quality profiles
curl -s -H "X-Api-Key: YOUR_RADARR_KEY" \
  "http://localhost:7878/api/v3/qualityprofile" | jq '.[] | {id, name}'
```

## Sonarr (TV Shows) — port 8989

### Search and add a series

```bash
# Search by name
curl -s -H "X-Api-Key: YOUR_SONARR_KEY" \
  "http://localhost:8989/api/v3/series/lookup?term=breaking+bad" | jq '.[0] | {title, year, tvdbId}'

# Add series
curl -s -X POST -H "X-Api-Key: YOUR_SONARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tvdbId": 81189,
    "title": "Breaking Bad",
    "qualityProfileId": 1,
    "rootFolderPath": "/tv",
    "monitored": true,
    "addOptions": {"searchForMissingEpisodes": true}
  }' "http://localhost:8989/api/v3/series"
```

### List and manage series

```bash
# List all series
curl -s -H "X-Api-Key: YOUR_SONARR_KEY" \
  "http://localhost:8989/api/v3/series" | jq '.[] | {id, title, year, monitored, episodeFileCount, episodeCount}'

# Upcoming episodes
curl -s -H "X-Api-Key: YOUR_SONARR_KEY" \
  "http://localhost:8989/api/v3/calendar?start=$(date +%F)&end=$(date -d '+7 days' +%F)" | \
  jq '.[] | {series: .series.title, episode: .title, airDate: .airDate}'

# Missing episodes
curl -s -H "X-Api-Key: YOUR_SONARR_KEY" \
  "http://localhost:8989/api/v3/wanted/missing?pageSize=20" | jq '.records[] | {series: .series.title, episode: .title, airDate: .airDate}'

# Trigger search for missing episodes
curl -s -X POST -H "X-Api-Key: YOUR_SONARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "MissingEpisodeSearch"}' \
  "http://localhost:8989/api/v3/command"

# Queue
curl -s -H "X-Api-Key: YOUR_SONARR_KEY" \
  "http://localhost:8989/api/v3/queue" | jq '.records[] | {title, status, sizeleft, timeleft}'
```

## Prowlarr (Indexers) — port 9696

### Manage indexers

```bash
# List indexers
curl -s -H "X-Api-Key: YOUR_PROWLARR_KEY" \
  "http://localhost:9696/api/v1/indexer" | jq '.[] | {id, name, enable, protocol}'

# Test indexer
curl -s -X POST -H "X-Api-Key: YOUR_PROWLARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": 1}' \
  "http://localhost:9696/api/v1/indexer/test"

# Sync indexers to Radarr/Sonarr
curl -s -X POST -H "X-Api-Key: YOUR_PROWLARR_KEY" \
  "http://localhost:9696/api/v1/application/action/sync"

# List linked applications
curl -s -H "X-Api-Key: YOUR_PROWLARR_KEY" \
  "http://localhost:9696/api/v1/application" | jq '.[] | {id, name, syncLevel}'

# Search across all indexers
curl -s -H "X-Api-Key: YOUR_PROWLARR_KEY" \
  "http://localhost:9696/api/v1/search?query=inception&type=movie" | \
  jq '.[] | {title, indexer, size, seeders}'
```

### FlareSolverr (Cloudflare bypass)

FlareSolverr runs alongside Prowlarr to bypass Cloudflare-protected indexers.

```bash
# Health check
curl -s http://localhost:8191/v1 -d '{"cmd": "sessions.list"}' -H "Content-Type: application/json"
```

Configure in Prowlarr: Settings → Indexer Proxies → Add → FlareSolverr → `http://flaresolverr:8191`

## Bazarr (Subtitles) — port 6767

```bash
# List wanted subtitles (movies)
curl -s -H "X-Api-Key: YOUR_BAZARR_KEY" \
  "http://localhost:6767/api/movies/wanted" | jq '.data[] | {title, missing_subtitles}'

# List wanted subtitles (series)
curl -s -H "X-Api-Key: YOUR_BAZARR_KEY" \
  "http://localhost:6767/api/episodes/wanted" | jq '.data[] | {seriesTitle, episodeTitle, missing_subtitles}'

# Trigger search for wanted subtitles
curl -s -X POST -H "X-Api-Key: YOUR_BAZARR_KEY" \
  "http://localhost:6767/api/subtitles/wanted/movies"

# System health
curl -s -H "X-Api-Key: YOUR_BAZARR_KEY" \
  "http://localhost:6767/api/system/health"
```

## qBittorrent — port 8080

qBittorrent uses cookie-based auth. Login first, then use the cookie.

```bash
# Login (save cookie)
curl -s -c /tmp/qbt-cookies.txt \
  -d "username=admin&password=YOUR_PASSWORD" \
  "http://localhost:8080/api/v2/auth/login"

# List all torrents
curl -s -b /tmp/qbt-cookies.txt \
  "http://localhost:8080/api/v2/torrents/info" | \
  jq '.[] | {name, state, progress, dlspeed, size}'

# List active downloads
curl -s -b /tmp/qbt-cookies.txt \
  "http://localhost:8080/api/v2/torrents/info?filter=downloading" | \
  jq '.[] | {name, progress: (.progress * 100 | round), dlspeed, eta}'

# Pause/resume torrent
curl -s -b /tmp/qbt-cookies.txt -d "hashes=TORRENT_HASH" \
  "http://localhost:8080/api/v2/torrents/pause"
curl -s -b /tmp/qbt-cookies.txt -d "hashes=TORRENT_HASH" \
  "http://localhost:8080/api/v2/torrents/resume"

# Delete torrent (with files)
curl -s -b /tmp/qbt-cookies.txt -d "hashes=TORRENT_HASH&deleteFiles=true" \
  "http://localhost:8080/api/v2/torrents/delete"

# Transfer info (global speeds)
curl -s -b /tmp/qbt-cookies.txt \
  "http://localhost:8080/api/v2/transfer/info" | jq '{dl_info_speed, up_info_speed}'
```

### VPN container networking

qBittorrent commonly runs through a VPN container (nordvpn, gluetun, etc.):

```yaml
services:
  vpn:
    image: bubuntux/nordlynx  # or qmcgaw/gluetun
    cap_add: [NET_ADMIN]
    ports:
      - "8080:8080"  # qBittorrent WebUI exposed through VPN
    environment:
      - PRIVATE_KEY=your-wireguard-key

  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent
    network_mode: "service:vpn"  # Route all traffic through VPN
    depends_on: [vpn]
```

## Overseerr (Media Requests) — port 5055

```bash
# Search
curl -s -H "X-Api-Key: YOUR_OVERSEERR_KEY" \
  "http://localhost:5055/api/v1/search?query=inception" | jq '.results[] | {title, mediaType, year}'

# Request a movie
curl -s -X POST -H "X-Api-Key: YOUR_OVERSEERR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mediaType": "movie", "mediaId": 27205}' \
  "http://localhost:5055/api/v1/request"

# List pending requests
curl -s -H "X-Api-Key: YOUR_OVERSEERR_KEY" \
  "http://localhost:5055/api/v1/request?filter=pending" | jq '.results[] | {id, type: .type, status: .status, media: .media.tmdbId}'
```

## Common storage layout

```
/opt/media/
├── downloads/      # qBittorrent download directory
├── movies/         # Radarr movie library
├── tv/             # Sonarr TV library
├── radarr/         # Radarr config
├── sonarr/         # Sonarr config
├── prowlarr/       # Prowlarr config
└── qbittorrent/    # qBittorrent config
```

## Troubleshooting

| Problem | Service | Fix |
|---------|---------|-----|
| Download stuck at 100% | Radarr/Sonarr | Check import errors in Activity → Queue. Usually permissions or path mapping |
| No results from search | Prowlarr | Check indexer health. Test individual indexers. Try FlareSolverr for Cloudflare sites |
| "Path does not exist" | Radarr/Sonarr | Docker volume mounts don't match. Ensure paths inside container match config |
| Torrent stalled | qBittorrent | Check VPN connection. Restart VPN container. Verify port forwarding |
| Subtitle not found | Bazarr | Check provider API limits. Add more subtitle providers in Settings |
| Can't reach qBittorrent UI | qBittorrent | It's behind VPN container. Check VPN container ports, not qBittorrent's |
| Import failed | Radarr/Sonarr | Check PUID/PGID match between containers. Verify write permissions on library folder |

### Health check all services

```bash
for svc in "radarr:7878" "sonarr:8989" "prowlarr:9696"; do
  name="${svc%%:*}"; port="${svc##*:}"
  status=$(curl -s -o /dev/null -w "%{http_code}" -H "X-Api-Key: YOUR_KEY" \
    "http://localhost:$port/api/v3/system/status")
  echo "$name: $status"
done
```
