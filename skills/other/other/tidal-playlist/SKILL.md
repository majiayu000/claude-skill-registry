---
name: tidal-playlist
description: Manage Tidal playlists — list, create, rename, delete, add or remove albums and tracks. Use when the user wants to work with playlists.
allowed-tools: Bash, Read, Grep
argument-hint: "<list|create|rename|delete|add-album|add-track|remove-track> [options]"
---

# Tidal Playlist

Manage Tidal playlists: list, create, rename, delete, and add or remove content.

## Commands

### playlist list
- **Usage**: `tidal-cli --json playlist list`
- **Arguments**: none
- **Output**: `[{id, name, num_tracks}]`

### playlist create
- **Usage**: `tidal-cli --json playlist create --name "<name>" [--desc "<description>"]`
- **Arguments**: `--name` (required), `--desc` (optional)
- **Output**: `{id, name, description}`

### playlist rename
- **Usage**: `tidal-cli --json playlist rename --playlist-id <id> --name "<new_name>"`
- **Arguments**: `--playlist-id` (required), `--name` (required)
- **Output**: `{status, id, old_name, new_name}`

### playlist delete
- **Usage**: `tidal-cli --json playlist delete --playlist-id <id>`
- **Arguments**: `--playlist-id` (required)
- **Output**: `{status, id, name}`

### playlist add-album
- **Usage**: `tidal-cli --json playlist add-album --playlist-id <id> --album-id <id>`
- **Arguments**: `--playlist-id` (required), `--album-id` (required)
- **Output**: `{status, tracks_added, album, playlist}`

### playlist add-track
- **Usage**: `tidal-cli --json playlist add-track --playlist-id <id> --track-id <id>`
- **Arguments**: `--playlist-id` (required), `--track-id` (required)
- **Output**: `{status, track, playlist}`

### playlist remove-track
- **Usage**: `tidal-cli --json playlist remove-track --playlist-id <id> --track-id <id>`
- **Arguments**: `--playlist-id` (required), `--track-id` (required)
- **Output**: `{status, track, playlist}`

## Instructions

1. Parse `$ARGUMENTS` to determine the operation (first word) and its parameters:
   - `list` — no additional arguments needed
   - `create` — extract `--name` and optionally `--desc` from arguments
   - `rename` — extract `--playlist-id` and `--name`
   - `delete` — extract `--playlist-id`
   - `add-album` — extract `--playlist-id` and `--album-id`
   - `add-track` — extract `--playlist-id` and `--track-id`
   - `remove-track` — extract `--playlist-id` and `--track-id`
   - If no operation given, show usage: `/tidal-playlist <list|create|rename|delete|add-album|add-track|remove-track> [options]`

2. Run the appropriate command and parse JSON output:
   - **list** → format as table with columns `ID`, `Name`, `Tracks`
   - **create** → confirm: "Playlist created: **<name>** (ID: `<id>`)"
   - **rename** → confirm: "Playlist renamed: **<old_name>** → **<new_name>**"
   - **delete** → confirm: "Playlist **<name>** (ID: `<id>`) deleted."
   - **add-album** → confirm: "<tracks_added> track(s) from album **<album>** added to playlist **<playlist>**."
   - **add-track** → confirm: "Track **<track>** added to playlist **<playlist>**."
   - **remove-track** → confirm: "Track **<track>** removed from playlist **<playlist>**."

3. If required arguments are missing for an operation, show a usage hint specific to that operation.

## Error Handling

- If exit code is non-zero, read stderr:
  - `"Error: Not authenticated"` → "You need to authenticate first. Run `/tidal-auth` to log in."
  - `"Error: Playlist not found"` → "Playlist not found (ID: `<id>`). Use `/tidal-playlist list` to see your playlists."
  - `"Error: Track not found in playlist"` → "Track (ID: `<id>`) is not in this playlist."
  - `"Error: Playlist name cannot be empty"` → "Please provide a non-empty playlist name."
  - `"Error: Unable to connect to Tidal"` → "Network error: unable to reach Tidal. Check your internet connection."
  - Any other error → display the raw error message with label "Error:"
