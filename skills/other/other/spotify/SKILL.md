---
name: spotify
description: Use when the user asks to play music, control playback, search for songs/albums/artists, manage queue, or adjust volume via Spotify.
---

# Spotify

Control Spotify playback via `spotify-ctl`.

## Setup

The script lives alongside this skill at `spotify-ctl`. Ensure it's on PATH (e.g. symlink to `~/.local/bin/spotify-ctl`).

Requires `~/.config/spotify-api/credentials.json` and `~/.config/spotify-api/tokens.json`.

## Commands

| Command | Description |
|---------|-------------|
| `spotify-ctl devices` | List available devices |
| `spotify-ctl play [uri] [--device id]` | Play (optionally: track/album/playlist URI) |
| `spotify-ctl queue <uri> [--device id]` | Add to queue (supports track, album, playlist URIs) |
| `spotify-ctl pause` | Pause playback |
| `spotify-ctl next` | Skip to next track |
| `spotify-ctl prev` | Previous track |
| `spotify-ctl status` | Current track info |
| `spotify-ctl search <query> [--type TYPE] [--limit N]` | Search (type: track, album, artist, playlist) |
| `spotify-ctl transfer <device_id>` | Transfer playback to device |
| `spotify-ctl clear-queue` | Clear the playback queue |
| `spotify-ctl volume <0-100>` | Set volume |

## Workflow

1. `spotify-ctl search <query>` to find a URI
2. `spotify-ctl play <uri>` or `spotify-ctl queue <uri>` to play/queue it
3. Use `spotify-ctl status` to confirm what's playing
