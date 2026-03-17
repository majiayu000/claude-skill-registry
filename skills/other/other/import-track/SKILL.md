---
name: import-track
description: Moves track markdown files to the correct album location. Use when the user has track files in Downloads or other locations that need to be placed in an album.
argument-hint: <file-path> <album-name> [track-number]
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - Bash
  - Glob
---

## Your Task

**Input**: $ARGUMENTS

Import a track markdown file (.md) to the correct album location based on config.

---

# Import Track Skill

You move track markdown files to the correct location in the user's content directory.

## Step 1: Parse Arguments

Expected format: `<file-path> <album-name> [track-number]`

Examples:
- `~/Downloads/track.md sample-album 03`
- `~/Downloads/t-day-beach.md sample-album 03`
- `~/Downloads/03-t-day-beach.md sample-album` (number already in filename)

If arguments are missing, ask:
```
Usage: /import-track <file-path> <album-name> [track-number]

Example: /import-track ~/Downloads/track.md sample-album 03
```

## Step 2: Find Album and Resolve Path via MCP

1. Call `find_album(album_name)` — fuzzy match by name, slug, or partial. Returns album metadata including genre.
2. Call `resolve_path("tracks", album_slug)` — returns the full tracks directory path

If album not found, MCP returns available albums:
```
Error: Album "{album-name}" not found.

Available albums:
[list from MCP response]

Create album first with: /new-album {album-name} <genre>
```

## Step 4: Construct Target Path

The target path is **ALWAYS**:

```
{content_root}/artists/{artist}/albums/{genre}/{album}/tracks/{XX}-{track-name}.md
```

Example with:
- `content_root: ~/bitwize-music`
- `artist: bitwize`
- `genre: electronic` (found from album location)
- `album: sample-album`
- `track-number: 03`
- `track-name: t-day-beach`

Result:
```
~/bitwize-music/artists/bitwize/albums/electronic/sample-album/tracks/03-t-day-beach.md
```

**Track numbering**:
- If track number provided, use it (zero-padded: `03`)
- If filename already has number prefix (e.g., `03-name.md`), preserve it
- If neither, ask user for track number

## Step 5: Move File

```bash
mv "{source_file}" "{target_path}"
```

## Step 6: Confirm

Report:
```
Moved: {source_file}
   To: {target_path}
```

## Error Handling

**Source file doesn't exist:**
```
Error: File not found: {source_file}
```

**Config file missing:**
```
Error: Config not found at ~/.bitwize-music/config.yaml
Run /configure to set up.
```

**Album not found:**
```
Error: Album "{album-name}" not found.
Create it first with: /new-album {album-name} <genre>
```

**Track already exists:**
```
Warning: Track already exists at destination.
Overwrite? (The original was not moved)
```

---

## Examples

```
/import-track ~/Downloads/t-day-beach.md sample-album 03
```

Config has:
```yaml
paths:
  content_root: ~/bitwize-music
artist:
  name: bitwize
```

Album found at: `~/bitwize-music/artists/bitwize/albums/electronic/sample-album/`

Result:
```
Moved: ~/Downloads/t-day-beach.md
   To: ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/tracks/03-t-day-beach.md
```

---

## Common Mistakes

### ❌ Don't: Manually read config and search for albums

**Wrong:**
```bash
cat ~/.bitwize-music/config.yaml
find . -name "README.md" -path "*albums/$album_name*"
```

**Right:**
```
# Use MCP to find album and resolve path
find_album(album_name) → returns album metadata with genre
resolve_path("tracks", album_slug) → returns full tracks directory path
```

**Why it matters:** MCP handles config reading, fuzzy matching, and path resolution in single calls.

### ❌ Don't: Forget the tracks/ subdirectory

**Wrong destination:**
```
{album_path}/01-track.md
# Example: ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/01-track.md
```

**Correct destination:**
```
{album_path}/tracks/01-track.md
# Example: ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/tracks/01-track.md
```

**Why it matters:** Tracks always go in the `tracks/` subdirectory within the album folder.

### ❌ Don't: Skip track number validation

**Wrong:**
```bash
# Not validating track number format
mv track.md {album_path}/tracks/$track_num-track.md
# Could result in: 3-track.md instead of 03-track.md
```

**Right:**
```bash
# Ensure zero-padding
track_num=$(printf "%02d" $track_num)
mv track.md {album_path}/tracks/$track_num-track.md
# Results in: 03-track.md
```

**Why it matters:** Track numbers must be zero-padded (01, 02, 03...) for proper sorting.

### ❌ Don't: Assume album location without searching

**Wrong:**
```bash
# Guessing album is in electronic genre
mv track.md ~/music-projects/artists/bitwize/albums/electronic/sample-album/tracks/
```

**Right:**
```
# Use MCP to find the album (handles genre resolution)
find_album(album_name) → returns album metadata including genre and path
```

**Why it matters:** Albums are organized by genre. `find_album` resolves the genre automatically.
