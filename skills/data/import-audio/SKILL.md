---
name: import-audio
description: Move audio files to the correct album location
argument-hint: <file-path> <album-name>
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - Bash
---

## Your Task

**Input**: $ARGUMENTS

Import an audio file (WAV, MP3, etc.) to the correct album location based on config.

---

# Import Audio Skill

You move audio files to the correct location in the user's audio directory.

## Step 1: Parse Arguments

Expected format: `<file-path> <album-name>`

Examples:
- `~/Downloads/track.wav sample-album`
- `~/Downloads/03-t-day-beach.wav sample-album`

If arguments are missing, ask:
```
Usage: /import-audio <file-path> <album-name>

Example: /import-audio ~/Downloads/track.wav sample-album
```

## Step 2: Read Config (REQUIRED)

**ALWAYS read the config file first. Never skip this step.**

```bash
cat ~/.bitwize-music/config.yaml
```

Extract:
- `paths.audio_root` → The base audio directory
- `artist.name` → The artist name (e.g., "bitwize")

## Step 3: Construct Target Path

The target path is **ALWAYS**:

```
{audio_root}/{artist}/{album}/{filename}
```

Example with:
- `audio_root: ~/bitwize-music/audio`
- `artist: bitwize`
- `album: sample-album`
- `file: 03-t-day-beach.wav`

Result:
```
~/bitwize-music/audio/bitwize/sample-album/03-t-day-beach.wav
```

**CRITICAL**: The path MUST include the artist folder. Never put files directly at `{audio_root}/{album}/`.

## Step 4: Create Directory and Move File

```bash
mkdir -p {audio_root}/{artist}/{album}
mv "{source_file}" "{audio_root}/{artist}/{album}/{filename}"
```

## Step 5: Confirm

Report:
```
Moved: {source_file}
   To: {audio_root}/{artist}/{album}/{filename}
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

**File already exists at destination:**
```
Warning: File already exists at destination.
Overwrite? (The original was not moved)
```

---

## Examples

```
/import-audio ~/Downloads/03-t-day-beach.wav sample-album
```

Config has:
```yaml
paths:
  audio_root: ~/bitwize-music/audio
artist:
  name: bitwize
```

Result:
```
Moved: ~/Downloads/03-t-day-beach.wav
   To: ~/bitwize-music/audio/bitwize/sample-album/03-t-day-beach.wav
```

---

## Common Mistakes

### ❌ Don't: Skip reading config

**Wrong:**
```bash
# Assuming audio_root path
mv file.wav ~/music-projects/audio/sample-album/
```

**Right:**
```bash
# Always read config first
cat ~/.bitwize-music/config.yaml
# Use paths.audio_root from config
```

**Why it matters:** If audio_root is different from what you assume, files end up in the wrong place.

### ❌ Don't: Forget to include artist in path

**Wrong destination:**
```
{audio_root}/{album}/file.wav
# Example: ~/music-projects/audio/sample-album/file.wav
```

**Correct destination:**
```
{audio_root}/{artist}/{album}/file.wav
# Example: ~/music-projects/audio/bitwize/sample-album/file.wav
```

**Why it matters:** Audio path structure includes artist name. This is the most common mistake with import-audio.

### ❌ Don't: Use hardcoded artist name

**Wrong:**
```bash
# Hardcoding artist
mv file.wav ~/audio/bitwize/sample-album/
```

**Right:**
```bash
# Read artist.name from config
artist=$(yq '.artist.name' ~/.bitwize-music/config.yaml)
audio_root=$(yq '.paths.audio_root' ~/.bitwize-music/config.yaml)
mv file.wav "$audio_root/$artist/sample-album/"
```

### ❌ Don't: Assume current working directory

**Wrong:**
```bash
# Moving relative to current directory
mv ~/Downloads/file.wav ./audio/sample-album/
```

**Right:**
```bash
# Use absolute path from config
audio_root=$(yq '.paths.audio_root' ~/.bitwize-music/config.yaml)
# Then use $audio_root for absolute path
```

### ❌ Don't: Mix up content_root and audio_root

**Wrong:**
```bash
# Using content_root for audio files
mv file.wav {content_root}/artists/bitwize/albums/electronic/sample-album/
```

**Right:**
```bash
# Audio files go to audio_root, not content_root
mv file.wav {audio_root}/{artist}/{album}/
```

**Path comparison:**
- Content: `{content_root}/artists/{artist}/albums/{genre}/{album}/` (markdown, lyrics)
- Audio: `{audio_root}/{artist}/{album}/` (WAV files, flattened structure)
- Documents: `{documents_root}/{artist}/{album}/` (PDFs, research)
