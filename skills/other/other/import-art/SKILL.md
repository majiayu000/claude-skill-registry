---
name: import-art
description: Places album art files in the correct audio and content directory locations. Use when the user has generated or downloaded album artwork that needs to be saved.
argument-hint: <file-path> <album-name>
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - Bash
  - Glob
---

## Your Task

**Input**: $ARGUMENTS

Import album art to both the audio folder and album content folder.

---

# Import Art Skill

You copy album art to both required locations based on config.

## Step 1: Parse Arguments

Expected format: `<file-path> <album-name>`

Examples:
- `~/Downloads/album-art.jpg sample-album`
- `~/Downloads/cover.png sample-album`

If arguments are missing, ask:
```
Usage: /import-art <file-path> <album-name>

Example: /import-art ~/Downloads/album-art.jpg sample-album
```

## Step 2: Find Album and Resolve Paths via MCP

1. Call `find_album(album_name)` — fuzzy match, returns album metadata including genre
2. Call `resolve_path("audio", album_slug)` — returns audio directory path
3. Call `resolve_path("content", album_slug)` — returns content directory path

If album not found:
```
Error: Album "{album-name}" not found.
Create it first with: /new-album {album-name} <genre>
```

## Step 3: Construct Target Paths

**TWO destinations required** (paths from MCP `resolve_path` calls):

1. **Audio folder** (for platforms/mastering): `{audio_path}/album.png`
2. **Content folder** (for documentation): `{content_path}/album-art.{ext}`

**CRITICAL**: `resolve_path` includes the artist folder automatically.

## Step 4: Create Directories and Copy Files

```bash
# Create audio directory (includes artist folder!)
mkdir -p {audio_root}/artists/{artist}/albums/{genre}/{album}

# Copy to audio folder as album.png
cp "{source_file}" "{audio_root}/artists/{artist}/albums/{genre}/{album}/album.png"

# Copy to content folder preserving extension
cp "{source_file}" "{content_root}/artists/{artist}/albums/{genre}/{album}/album-art.{ext}"
```

## Step 5: Confirm

Report:
```
Album art imported for: {album-name}

Copied to:
1. {audio_root}/artists/{artist}/albums/{genre}/{album}/album.png (for platforms)
2. {content_root}/artists/{artist}/albums/{genre}/{album}/album-art.{ext} (for docs)
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

**Not an image file:**
```
Warning: File doesn't appear to be an image: {source_file}
Expected: .jpg, .jpeg, .png, .webp

Continue anyway? (y/n)
```

---

## Examples

```
/import-art ~/Downloads/sample-album-cover.jpg sample-album
```

Config has:
```yaml
paths:
  content_root: ~/bitwize-music
  audio_root: ~/bitwize-music/audio
artist:
  name: bitwize
```

Album found at: `~/bitwize-music/artists/bitwize/albums/electronic/sample-album/`

Result:
```
Album art imported for: sample-album

Copied to:
1. ~/bitwize-music/audio/artists/bitwize/albums/electronic/sample-album/album.png (for platforms)
2. ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/album-art.jpg (for docs)
```

---

## Common Mistakes

### ❌ Don't: Manually read config and construct paths

**Wrong:**
```bash
cat ~/.bitwize-music/config.yaml
cp art.png ~/music-projects/audio/sample-album/
```

**Right:**
```
# Use MCP to find album and resolve both paths
find_album(album_name) → returns album metadata
resolve_path("audio", album_slug) → audio path with artist folder
resolve_path("content", album_slug) → content path with genre
```

**Why it matters:** `resolve_path` handles config reading, artist folder, and genre resolution automatically.

### ❌ Don't: Place art in only one location

**Wrong:**
```bash
# Only copying to audio folder
cp art.png {audio_root}/artists/{artist}/albums/{genre}/{album}/album.png
# Missing: content folder copy
```

**Right:**
```bash
# Copy to BOTH locations
# 1. Audio location (for streaming platforms)
cp art.png {audio_root}/artists/{artist}/albums/{genre}/{album}/album.png
# 2. Content location (for documentation)
cp art.jpg {album_path}/album-art.jpg
```

**Why it matters:** Album art needs to be in both locations - audio folder for release, content folder for documentation.

### ❌ Don't: Mix up the filenames

**Wrong:**
```bash
# Using same filename in both locations
cp art.png {audio_root}/artists/{artist}/albums/{genre}/{album}/album-art.png
cp art.png {album_path}/album.png
```

**Correct naming:**
```
Audio location: album.png (or album.jpg)
Content location: album-art.jpg (or album-art.png)
```

**Why it matters:** Different locations use different naming conventions to avoid confusion.

### ❌ Don't: Search for albums manually

**Wrong:**
```bash
find . -name "README.md" -path "*albums/$album_name*"
```

**Right:**
```
find_album(album_name) → returns album data including path and genre
```

### ❌ Don't: Forget to create directories

**Wrong:**
```bash
# Copying without ensuring directory exists
cp art.png {audio_root}/artists/{artist}/albums/{genre}/{album}/album.png
# Fails if directory doesn't exist
```

**Right:**
```bash
# Create directory first
mkdir -p {audio_root}/artists/{artist}/albums/{genre}/{album}/
cp art.png {audio_root}/artists/{artist}/albums/{genre}/{album}/album.png
```

**Why it matters:** Audio directory might not exist yet, especially for new albums.
