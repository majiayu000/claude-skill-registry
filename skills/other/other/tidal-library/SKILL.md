---
name: tidal-library
description: Add or remove artists, albums, or tracks from your Tidal favorites library. Use when the user wants to save music, like a song, follow an artist, or remove items from their library.
allowed-tools: Bash, Read, Grep
argument-hint: "<add|remove> <--artist-id|--album-id|--track-id> <id>"
---

# Tidal Library

Add or remove artists, albums, and tracks from your Tidal favorites library.

## Commands

### library add
- **Usage**: `tidal-cli --json library add <--artist-id|--album-id|--track-id> <id>`
- **Arguments**: exactly one of `--artist-id`, `--album-id`, or `--track-id` (required)
- **Output**: `{status, type, id, name}`

### library remove
- **Usage**: `tidal-cli --json library remove <--artist-id|--album-id|--track-id> <id>`
- **Arguments**: exactly one of `--artist-id`, `--album-id`, or `--track-id` (required)
- **Output**: `{status, type, id, name}`

## Instructions

1. Parse `$ARGUMENTS`:
   - First word: operation (`add` or `remove`)
   - Remaining: the ID flag and its value (`--artist-id <id>`, `--album-id <id>`, or `--track-id <id>`)
   - If no operation given, show usage: `/tidal-library <add|remove> <--artist-id|--album-id|--track-id> <id>`
   - If operation is provided but no ID flag, show: "Please specify one ID: `--artist-id <id>`, `--album-id <id>`, or `--track-id <id>`"

2. Build and run the command:
   ```bash
   tidal-cli --json library <add|remove> <--artist-id|--album-id|--track-id> <id>
   ```

3. Parse JSON output and display confirmation:
   - **add** → "Added **<name>** (<type>, ID: `<id>`) to your library."
   - **remove** → "Removed **<name>** (<type>, ID: `<id>`) from your library."

## Error Handling

- If exit code is non-zero, read stderr:
  - `"Error: Not authenticated"` → "You need to authenticate first. Run `/tidal-auth` to log in."
  - `"Error: Artist/Album/Track not found"` → "Item not found (ID: `<id>`). Please verify the ID is correct."
  - `"Error: You must provide exactly one of --artist-id, --album-id or --track-id"` → "Please provide exactly one ID type: `--artist-id`, `--album-id`, or `--track-id`."
  - `"Error: Unable to connect to Tidal"` → "Network error: unable to reach Tidal. Check your internet connection."
  - Any other error → display the raw error message with label "Error:"
