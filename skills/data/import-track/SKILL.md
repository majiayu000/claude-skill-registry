---
name: import-track
description: Move track markdown files to the correct album location
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

## Step 2: Read Config (REQUIRED)

**ALWAYS read the config file first. Never skip this step.**

```bash
cat ~/.bitwize-music/config.yaml
```

Extract:
- `paths.content_root` → The base content directory
- `artist.name` → The artist name (e.g., "bitwize")

## Step 3: Find Album and Determine Genre

Search for the album directory to find its genre:

```bash
find {content_root}/artists/{artist}/albums -type d -name "{album-name}" 2>/dev/null
```

If album not found:
```
Error: Album "{album-name}" not found.

Available albums:
[list albums found in artists/{artist}/albums/]

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

### ❌ Don't: Skip reading config

**Wrong:**
```bash
# Assuming content_root path
mv track.md ~/music-projects/artists/bitwize/albums/...
```

**Right:**
```bash
# Always read config first
cat ~/.bitwize-music/config.yaml
# Use paths.content_root and artist.name from config
```

### ❌ Don't: Search from wrong location

**Wrong:**
```bash
# Searching from current directory
find . -name "README.md" -path "*albums/$album_name*"
```

**Right:**
```bash
# Search from content_root
content_root=$(yq '.paths.content_root' ~/.bitwize-music/config.yaml)
find "$content_root" -name "README.md" -path "*albums/$album_name*"
```

**Why it matters:** Album might not be in current working directory.

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

### ❌ Don't: Use hardcoded artist name

**Wrong:**
```bash
# Assuming artist is bitwize
find ~/music-projects/artists/bitwize/albums -name "README.md"
```

**Right:**
```bash
# Read artist.name from config
artist=$(yq '.artist.name' ~/.bitwize-music/config.yaml)
find "$content_root/artists/$artist/albums" -name "README.md"
```

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
```bash
# Search for album across all genres
find "$content_root/artists/$artist/albums" -type d -name "$album_name"
# Album might be in hip-hop, electronic, folk, etc.
```

**Why it matters:** Albums are organized by genre. You need to find the album first, not assume its genre.
