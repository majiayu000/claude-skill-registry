---
name: rename
description: Renames an album or track, updating slugs, titles, and all mirrored paths. Use when the user wants to rename an album or track.
argument-hint: <album|track> <current-name> <new-name>
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - Bash
---

## Your Task

**Input**: $ARGUMENTS

Rename an album or track using the MCP rename tools.

---

# Rename Skill

You rename albums or tracks, updating slugs, display titles, and all mirrored directory paths (content, audio, documents).

## Step 1: Parse Arguments

Expected format: `<type> <current-name> <new-name>`

Examples:
- `album old-album-name new-album-name`
- `track my-album 01-old-track 01-new-track`

If arguments are missing or unclear, show usage:
```
Usage:
  /rename album <current-slug> <new-slug>
  /rename track <album-slug> <current-track-slug> <new-track-slug>

Examples:
  /rename album my-old-album my-new-album
  /rename track my-album 01-old-name 01-new-name
```

## Step 2: Verify Config via MCP

Call `get_config()` to verify configuration is loaded. The MCP rename tools resolve paths internally, but config must be valid.

## Step 3: Confirm with User

Before renaming, confirm the action:

**For albums:**
```
Rename album 'old-name' -> 'new-name'?

This will:
- Move content directory
- Move audio directory (if exists)
- Move documents directory (if exists)
- Update README.md title
- Update state cache
```

**For tracks:**
```
Rename track 'old-name' -> 'new-name' in album 'album-name'?

This will:
- Rename track file
- Update title in metadata table
- Update state cache

Note: Audio files are NOT renamed (they have Suno-generated names).
```

Wait for user confirmation before proceeding.

## Step 4: Invoke MCP Tool

**For albums:** Use the `rename_album` MCP tool with:
- `old_slug`: Current album slug
- `new_slug`: New album slug
- `new_title`: (optional) Custom display title

**For tracks:** Use the `rename_track` MCP tool with:
- `album_slug`: Album containing the track
- `old_track_slug`: Current track slug
- `new_track_slug`: New track slug
- `new_title`: (optional) Custom display title

## Step 5: Report Results

**Success:**
```
Renamed album 'old-name' -> 'new-name'
  Content directory: moved
  Audio directory: moved (or: no audio directory found)
  Documents directory: moved (or: no documents directory found)
  Tracks updated: N
```

**For tracks:**
```
Renamed track 'old-name' -> 'new-name' in album 'album-name'
  Old path: /path/to/old-file.md
  New path: /path/to/new-file.md
  Title updated to: "New Name"
```

## Error Handling

**Album/track not found:**
```
Error: Album 'name' not found.
Available albums: album-1, album-2, album-3
```

**New name already exists:**
```
Error: Album 'new-name' already exists.
Choose a different name.
```

**Partial failure (album rename):**
```
Warning: Content directory renamed successfully, but:
  - Audio directory rename failed: [error]
  - Documents directory rename failed: [error]

The content directory has been moved. Use rebuild_state to refresh the cache,
then manually move any remaining directories.
```
