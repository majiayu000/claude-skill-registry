---
name: validate-album
description: Validates album directory structure, file locations, and content integrity. Use before release or whenever the user wants to check an album's structural health.
argument-hint: <album-name>
model: claude-haiku-4-5-20251001
context: fork
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Album Validator Agent

## Your Task

**Input**: $ARGUMENTS (album name, e.g., `sample-album`)

Validate that an album has all required files in the correct locations, catching path issues and missing content before they become problems.

---

## Step 1: Load Config & Find Album

1. Call `get_config()` — returns paths (`content_root`, `audio_root`, `documents_root`) and `artist.name`
   - If config missing, STOP and report:
     ```
     [FAIL] Config file missing: ~/.bitwize-music/config.yaml
            Run /configure to set up the plugin.
     ```

2. Call `find_album(album_name)` — fuzzy match by name, slug, or partial
   - If not found, STOP and report (MCP returns available albums):
     ```
     [FAIL] Album not found: {album-name}
     ```

3. Optionally call `validate_album_structure(album_slug)` — runs structural validation checks and returns `{passed, failed, warnings, skipped, issues[], checks[]}`. This MCP tool handles directory structure, required files, audio placement, and track content checks in one call.

**Note**: The MCP `validate_album_structure` tool performs many of the checks below automatically. You can use its results directly or run the manual checks for more detailed reporting.

---

## Step 3: Run Validations

### Initialize Counters
- `passed = 0`
- `failed = 0`
- `warnings = 0`
- `skipped = 0`
- `issues = []` (list of fix commands)

### Output Header
```
═══════════════════════════════════════════════════════════
ALBUM VALIDATION: {album-name}
═══════════════════════════════════════════════════════════
```

---

## Validation Categories

### CONFIG
```
CONFIG
──────
```

| Check | Pass | Fail |
|-------|------|------|
| Config file exists | `[PASS] Config file exists` | `[FAIL] Config file missing` |
| content_root defined | `[PASS] content_root: {value}` | `[FAIL] content_root not defined` |
| audio_root defined | `[PASS] audio_root: {value}` | `[FAIL] audio_root not defined` |
| artist defined | `[PASS] artist: {value}` | `[FAIL] artist.name not defined` |

### ALBUM STRUCTURE
```
ALBUM STRUCTURE
───────────────
```

| Check | How | Pass | Fail |
|-------|-----|------|------|
| Album dir exists | `test -d {album_path}` | `[PASS] Album directory: {path}` | `[FAIL] Album directory missing` |
| README.md exists | `test -f {album_path}/README.md` | `[PASS] README.md exists` | `[FAIL] README.md missing` |
| tracks/ dir exists | `test -d {album_path}/tracks` | `[PASS] tracks/ directory exists` | `[FAIL] tracks/ directory missing` |
| Track files exist | `ls {album_path}/tracks/*.md` | `[PASS] {N} track files found` | `[WARN] No track files found` |

**For documentary albums** (check README.md for type):
| Check | How | Pass | Fail |
|-------|-----|------|------|
| RESEARCH.md exists | `test -f {album_path}/RESEARCH.md` | `[PASS] RESEARCH.md exists` | `[WARN] RESEARCH.md missing (documentary album)` |
| SOURCES.md exists | `test -f {album_path}/SOURCES.md` | `[PASS] SOURCES.md exists` | `[WARN] SOURCES.md missing (documentary album)` |

### AUDIO FILES
```
AUDIO FILES
───────────
```

Expected path: `{audio_root}/artists/{artist}/albums/{genre}/{album}/`

| Check | How | Pass | Fail |
|-------|-----|------|------|
| Audio dir exists (correct path) | `test -d {audio_root}/artists/{artist}/albums/{genre}/{album}` | `[PASS] Audio directory: {path}` | See below |
| Audio dir in wrong location | `test -d {audio_root}/{album}` | N/A | `[FAIL] Audio in wrong location (missing artist folder)` |

**If audio in wrong location**, add to issues:
```
→ Expected: {audio_root}/artists/{artist}/albums/{genre}/{album}/
→ Found at: {audio_root}/{album}/ (WRONG - missing artist folder)
→ Fix: mv {audio_root}/{album}/ {audio_root}/artists/{artist}/albums/{genre}/{album}/
```

| Check | How | Pass | Skip |
|-------|-----|------|------|
| WAV files present | `ls {audio_path}/*.wav` | `[PASS] {N} WAV files found` | `[SKIP] No audio files yet` |
| mastered/ exists | `test -d {audio_path}/mastered` | `[PASS] mastered/ directory exists` | `[SKIP] Not mastered yet` |

### ALBUM ART
```
ALBUM ART
─────────
```

| Check | How | Pass | Skip |
|-------|-----|------|------|
| Art in audio folder | `test -f {audio_path}/album.png` | `[PASS] album.png in audio folder` | `[SKIP] No album art yet` |
| Art in content folder | `test -f {album_path}/album-art.*` | `[PASS] album-art in content folder` | `[SKIP] No album art yet` |

### TRACKS
```
TRACKS
──────
```

For each track file in `{album_path}/tracks/*.md`:

1. Read the file
2. Check for required fields:
   - Status field exists
   - Suno Style Box exists (has `## Suno Inputs` section)
   - Suno Lyrics Box exists
   - If Status is `Generated` or `Final`: Suno Link present
   - If documentary: Sources Verified status

Output per track:
- `[PASS] {filename} - Status: {status}, Suno Link: {present/missing}`
- `[WARN] {filename} - Status: {status}, missing {what}`
- `[FAIL] {filename} - No Status field`

---

## Step 4: Summary

```
═══════════════════════════════════════════════════════════
SUMMARY: {passed} passed, {failed} failed, {warnings} warning(s), {skipped} skipped
═══════════════════════════════════════════════════════════
```

If any issues:
```
ISSUES TO FIX:
1. {issue description}
   {fix command}
2. ...
```

---

## Example Output

```
═══════════════════════════════════════════════════════════
ALBUM VALIDATION: sample-album
═══════════════════════════════════════════════════════════

CONFIG
──────
[PASS] Config file exists
[PASS] content_root: ~/bitwize-music
[PASS] audio_root: ~/bitwize-music/audio
[PASS] artist: bitwize

ALBUM STRUCTURE
───────────────
[PASS] Album directory: ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/
[PASS] README.md exists
[PASS] tracks/ directory exists
[PASS] 5 track files found

AUDIO FILES
───────────
[FAIL] Audio directory in wrong location
       → Expected: ~/bitwize-music/audio/artists/bitwize/albums/electronic/sample-album/
       → Found at: ~/bitwize-music/audio/sample-album/
       → Fix: mv ~/bitwize-music/audio/sample-album/ ~/bitwize-music/audio/artists/bitwize/albums/electronic/sample-album/

ALBUM ART
─────────
[SKIP] No album art yet

TRACKS
──────
[PASS] 01-intro.md - Status: Final, Suno Link: present
[PASS] 02-track.md - Status: Final, Suno Link: present
[WARN] 03-t-day-beach.md - Status: Generated, Suno Link: missing

═══════════════════════════════════════════════════════════
SUMMARY: 8 passed, 1 failed, 1 warning, 1 skipped
═══════════════════════════════════════════════════════════

ISSUES TO FIX:
1. Move audio folder to include artist:
   mv ~/bitwize-music/audio/sample-album/ ~/bitwize-music/audio/artists/bitwize/albums/electronic/sample-album/
```

---

## Important Notes

1. **Use MCP tools first** - `get_config()`, `find_album()`, `validate_album_structure()` before manual checks
2. **Check both correct AND wrong locations** - Catch misplaced files
3. **Provide actionable fixes** - Include exact commands to fix issues
4. **Use appropriate status** - PASS/FAIL/WARN/SKIP based on severity
5. **Count everything** - Report totals in summary
