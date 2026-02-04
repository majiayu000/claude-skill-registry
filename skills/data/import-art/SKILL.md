---
name: import-art
description: Place album art in correct audio and content locations
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

## Step 2: Read Config (REQUIRED)

**ALWAYS read the config file first. Never skip this step.**

```bash
cat ~/.bitwize-music/config.yaml
```

Extract:
- `paths.content_root` → The base content directory
- `paths.audio_root` → The base audio directory
- `artist.name` → The artist name (e.g., "bitwize")

## Step 3: Find Album Genre

Search for the album to determine its genre:

```bash
find {content_root}/artists/{artist}/albums -type d -name "{album-name}" 2>/dev/null
```

Extract genre from path (the folder between `albums/` and `{album-name}/`).

If album not found:
```
Error: Album "{album-name}" not found in content directory.
Create it first with: /new-album {album-name} <genre>
```

## Step 4: Construct Target Paths

**TWO destinations required:**

1. **Audio folder** (for platforms/mastering):
   ```
   {audio_root}/{artist}/{album}/album.png
   ```

2. **Content folder** (for documentation):
   ```
   {content_root}/artists/{artist}/albums/{genre}/{album}/album-art.{ext}
   ```

Example with:
- `content_root: ~/bitwize-music`
- `audio_root: ~/bitwize-music/audio`
- `artist: bitwize`
- `genre: electronic`
- `album: sample-album`

Results:
```
Audio:   ~/bitwize-music/audio/bitwize/sample-album/album.png
Content: ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/album-art.jpg
```

**CRITICAL**: Audio path includes artist folder: `{audio_root}/{artist}/{album}/`

## Step 5: Create Directories and Copy Files

```bash
# Create audio directory (includes artist folder!)
mkdir -p {audio_root}/{artist}/{album}

# Copy to audio folder as album.png
cp "{source_file}" "{audio_root}/{artist}/{album}/album.png"

# Copy to content folder preserving extension
cp "{source_file}" "{content_root}/artists/{artist}/albums/{genre}/{album}/album-art.{ext}"
```

## Step 6: Confirm

Report:
```
Album art imported for: {album-name}

Copied to:
1. {audio_root}/{artist}/{album}/album.png (for platforms)
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
1. ~/bitwize-music/audio/bitwize/sample-album/album.png (for platforms)
2. ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/album-art.jpg (for docs)
```

---

## Common Mistakes

### ❌ Don't: Skip reading config

**Wrong:**
```bash
# Assuming paths
cp art.png ~/music-projects/audio/sample-album/
```

**Right:**
```bash
# Always read config first
cat ~/.bitwize-music/config.yaml
# Use paths.audio_root, paths.content_root, and artist.name from config
```

### ❌ Don't: Forget to include artist in audio path

**Wrong audio destination:**
```
{audio_root}/{album}/album.png
# Example: ~/music-projects/audio/sample-album/album.png
```

**Correct audio destination:**
```
{audio_root}/{artist}/{album}/album.png
# Example: ~/music-projects/audio/bitwize/sample-album/album.png
```

**Why it matters:** This is the most common mistake - audio_root includes artist folder.

### ❌ Don't: Place art in only one location

**Wrong:**
```bash
# Only copying to audio folder
cp art.png {audio_root}/{artist}/{album}/album.png
# Missing: content folder copy
```

**Right:**
```bash
# Copy to BOTH locations
# 1. Audio location (for streaming platforms)
cp art.png {audio_root}/{artist}/{album}/album.png
# 2. Content location (for documentation)
cp art.jpg {album_path}/album-art.jpg
```

**Why it matters:** Album art needs to be in both locations - audio folder for release, content folder for documentation.

### ❌ Don't: Mix up the filenames

**Wrong:**
```bash
# Using same filename in both locations
cp art.png {audio_root}/{artist}/{album}/album-art.png
cp art.png {album_path}/album.png
```

**Correct naming:**
```
Audio location: album.png (or album.jpg)
Content location: album-art.jpg (or album-art.png)
```

**Why it matters:** Different locations use different naming conventions to avoid confusion.

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

### ❌ Don't: Forget to create directories

**Wrong:**
```bash
# Copying without ensuring directory exists
cp art.png {audio_root}/{artist}/{album}/album.png
# Fails if directory doesn't exist
```

**Right:**
```bash
# Create directory first
mkdir -p {audio_root}/{artist}/{album}/
cp art.png {audio_root}/{artist}/{album}/album.png
```

**Why it matters:** Audio directory might not exist yet, especially for new albums.
