---
name: import-audio
description: Moves audio files to the correct album location with proper path structure. Use when the user has downloaded WAV files from Suno or other sources that need to be organized.
argument-hint: <file-path> <album-name> [track-slug]
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

Expected format: `<file-path> <album-name> [track-slug]`

The `track-slug` is optional — only needed for stems zip imports when the track can't be inferred from the filename.

Examples:
- `~/Downloads/track.wav sample-album`
- `~/Downloads/03-t-day-beach.wav sample-album`
- `~/Downloads/stems.zip sample-album 01-first-taste`

If arguments are missing, ask:
```
Usage: /import-audio <file-path> <album-name> [track-slug]

Examples:
  /import-audio ~/Downloads/track.wav sample-album
  /import-audio ~/Downloads/stems.zip sample-album 01-first-taste
```

## Step 2: Resolve Audio Path via MCP

1. Call `resolve_path("audio", album_slug)` — returns the full audio directory path
2. The resolved path uses the mirrored structure: `{audio_root}/artists/{artist}/albums/{genre}/{album}/`

Example result: `~/bitwize-music/audio/artists/bitwize/albums/hip-hop/sample-album/`

**CRITICAL**: Always use `resolve_path` — never construct paths manually.

## Step 3: Detect File Type

Check the file extension and whether it's a stems zip:

| File Type | Action |
|-----------|--------|
| `.wav`, `.mp3`, `.flac`, `.ogg`, `.m4a` | Move to album audio dir (Step 4) |
| `.zip` (stems) | Extract to per-track stems subfolder (Step 4b) |

**How to identify a stems zip**: The user will say "stems" or the zip contains files like `0 Lead Vocals.wav`, `1 Backing Vocals.wav`, etc.

## Step 4: Create Directory and Move File

```bash
mkdir -p {resolved_path}
mv "{source_file}" "{resolved_path}/{filename}"
```

## Step 4b: Import Stems Zip

Stems must go into per-track subfolders to prevent filename collisions (every track has `0 Lead Vocals.wav`, etc.):

```
{resolved_path}/
  01-first-taste.wav
  02-sugar-high.wav
  stems/
    01-first-taste/
      0 Lead Vocals.wav
      1 Backing Vocals.wav
      2 Drums.wav
      ...
    02-sugar-high/
      0 Lead Vocals.wav
      1 Backing Vocals.wav
      ...
```

**Workflow:**

1. **Determine the track slug** from one of:
   - The zip filename if it matches a track pattern (e.g., `01-first-taste-stems.zip` → `01-first-taste`)
   - The user specifying which track (e.g., `/import-audio stems.zip sample-album 01-first-taste`)
   - **If neither**: Ask the user which track the stems belong to
2. **Extract** into the per-track subfolder:
   ```bash
   mkdir -p {resolved_path}/stems/{track-slug}
   unzip "{source_file}" -d "{resolved_path}/stems/{track-slug}"
   ```
3. **Update track metadata**: Call `update_track_field(album_slug, track_slug, "stems", "Yes")`

**Argument format for stems**: `<zip-path> <album-name> [track-slug]`

## Step 5: Confirm

Report:
```
Moved: {source_file}
   To: {resolved_path}/{filename}
```

For stems:
```
Extracted stems: {source_file}
       To: {resolved_path}/stems/{track-slug}/
    Files: {count} stem files extracted
  Updated: {track-slug} stems → Yes
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

## MP3 Files

Suno allows downloading in both WAV and MP3 formats. **Always prefer WAV** for mastering quality.

**If the user provides an MP3 file:**

1. Accept the MP3 and import it normally (same path logic)
2. Warn the user:
```
Note: This is an MP3 file. For best mastering results, download the WAV
version from Suno instead. MP3 compression removes audio data that can't
be recovered during mastering.

If WAV isn't available, this MP3 will work but mastering quality may be limited.
```

3. Import the file to the same destination path as WAV files

**Supported formats:** WAV (preferred), MP3, FLAC, OGG, M4A

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
   To: ~/bitwize-music/audio/artists/bitwize/albums/hip-hop/sample-album/03-t-day-beach.wav
```

### Stems import example

```
/import-audio ~/Downloads/stems.zip sample-album 01-first-taste
```

Result:
```
Extracted stems: ~/Downloads/stems.zip
       To: ~/bitwize-music/audio/artists/bitwize/albums/hip-hop/sample-album/stems/01-first-taste/
    Files: 5 stem files extracted
  Updated: 01-first-taste stems → Yes
```

---

## Common Mistakes

### ❌ Don't: Manually read config and construct paths

**Wrong:**
```bash
cat ~/.bitwize-music/config.yaml
mv file.wav ~/music-projects/audio/artists/bitwize/albums/electronic/sample-album/
```

**Right:**
```
# Use MCP to resolve the correct path
resolve_path("audio", album_slug) → returns full path with artist folder
```

**Why it matters:** `resolve_path` reads config, resolves variables, and includes the artist folder automatically. No manual config parsing or path construction needed.

### ❌ Don't: Mix up content_root and audio_root

**Path comparison:**
- Content: `{content_root}/artists/{artist}/albums/{genre}/{album}/` (markdown, lyrics)
- Audio: `{audio_root}/artists/{artist}/albums/{genre}/{album}/` (WAV files, stems)
- Documents: `{documents_root}/artists/{artist}/albums/{genre}/{album}/` (PDFs, research)

Use `resolve_path` with the appropriate `path_type` ("content", "audio", "documents") to get the right path.
