---
name: upload-prepare
description: Prepare YouTube upload for bilingual audiobook video. Runs youtube-metadata skill, builds upload command, validates all files, checks languages by reading translations from middle of book, verifies wordcards play, shows thumbnail/background/output. Does NOT upload - only preparation and checklist. Use when user wants to prepare upload, check before upload, or validate video for YouTube.
allowed-tools: Read, Bash, Glob, Skill
---

# Upload Prepare - YouTube Upload Preparation & Validation

## Overview

Prepare and validate everything for YouTube upload without actually uploading. Creates comprehensive checklist for user verification.

## Activation Triggers

- "prepare upload"
- "check before upload"
- "validate for youtube"
- "upload checklist"
- "готовь к загрузке"
- "проверь перед аплоадом"

## Workflow

### Step 1: Identify Project

1. Get project name from user or detect from context
2. Verify project exists in `projects/` directory
3. Load project metadata from SQLite database

```bash
# Check project exists
ls projects/{project_name}/

# Get meta from DB
sqlite3 projects/{project_name}/project.db "SELECT key, value FROM meta;"
```

### Step 2: Validate Languages

1. Read source and target language from project meta
2. Read 2-3 translations from MIDDLE of the book (not beginning!)
3. Display translations for user to verify correct language

```bash
# Get total sentences
sqlite3 projects/{project_name}/project.db "SELECT value FROM meta WHERE key='total_sentences';"

# Read translations from middle (e.g., sentences 100-102)
sqlite3 projects/{project_name}/project.db "SELECT sentence_idx, text FROM sentences WHERE lang='{target_lang}' LIMIT 3 OFFSET 100;"
```

### Step 3: Validate Files

Check all required files exist:

```bash
# Video output
ls -lh projects/{project_name}/video/output.mp4

# Background image
ls -la projects/{project_name}/video/background.*

# Timeline with wordcards
head -30 projects/{project_name}/audio/timeline.json | grep -E "(wordcard_start|wordcard_duration)"

# Wordcard audio files
ls projects/{project_name}/audio/wordcards/ | head -5
```

### Step 4: Verify Wordcards

1. Check timeline.json contains wordcard_start and wordcard_duration fields
2. Play one wordcard audio from middle of book for verification

```bash
# Check timeline has wordcard data
grep -c "wordcard_start" projects/{project_name}/audio/timeline.json

# Play wordcard from middle (user listens)
afplay projects/{project_name}/audio/wordcards/0000100_combined.mp3
```

### Step 5: Find Thumbnail

1. Determine language pair from project (e.g., ru_en, ru_es-latam)
2. Check `thumbnails/{lang_pair}/` directory for matching thumbnail
3. If not found, generate using thumbnail generator

```bash
# Find thumbnail in language-specific folder
# Structure: thumbnails/ru_en/, thumbnails/ru_es-latam/
ls -la thumbnails/{source}_{target}/ | grep -i {project_base_name}
```

**If thumbnail NOT found, generate it:**

```python
# Quick one-liner to generate single thumbnail
python3 -c "
from pathlib import Path
from video.thumbnail_variants import prepare_background, variant_13, load_fonts
from PIL import ImageDraw

fonts = load_fonts()
img = prepare_background(Path('txt_source/{book_name}.png'))
draw = ImageDraw.Draw(img)

# For RU→EN use tgt_lang='ENGLISH'
# For RU→ES-LATAM use tgt_lang='LATAM SPANISH'
img = variant_13(img, draw, fonts,
    author_en='{Author English}',
    title_en='{Title English}',
    src_lang='RUSSIAN',
    tgt_lang='ENGLISH',  # or 'LATAM SPANISH'
    title_ru='{Название}',
    author_ru='{Автор}'
)
img = img.convert('RGB')
img.save('thumbnails/ru_en/{book_name}.png', quality=95)
"
```

**Batch generation (all books):**
```bash
# Generate all thumbnails for specific language pair
python3 scripts/generate_thumbnails.py thumbnails/ru_es-latam  # default LATAM SPANISH
```

To add target language option to batch script, edit `generate_thumbnails.py`.

### Step 6: Generate Metadata

Invoke youtube-metadata skill to generate title, description, tags:

```
Skill(skill: "youtube-metadata")
```

Follow youtube-metadata workflow to generate proper metadata.

### Step 7: Build Upload Command

Construct the upload command (do NOT execute):

```bash
python3 scripts/youtube_upload.py upload {project_name} {thumbnail_path} --playlist "{playlist_name}"
```

Playlist selection:
- RU → EN: `--playlist "RU - EN"`
- RU → ES-LATAM: `--playlist "RU - ES (LATAM)"`
- Other: ask user

### Step 8: Display Checklist

Output comprehensive checklist for user:

```
============================================================
UPLOAD PREPARATION CHECKLIST
============================================================

PROJECT: {project_name}
LANGUAGES: {SOURCE} → {TARGET}

------------------------------------------------------------
FILES (clickable paths)
------------------------------------------------------------
[✓/✗] Video:      file://{full_video_path} ({size})
[✓/✗] Background: file://{full_background_path}
[✓/✗] Thumbnail:  file://{full_thumbnail_path}
[✓/✗] Timeline: {has wordcard data}
[✓/✗] Wordcards: {count} files

------------------------------------------------------------
LANGUAGE VERIFICATION (from middle of book)
------------------------------------------------------------
Sentence 100: "{source_text}"
Translation:  "{target_text}"

Sentence 101: "{source_text}"
Translation:  "{target_text}"

>>> Verify translations are in {target_lang}! <<<

------------------------------------------------------------
WORDCARD AUDIO
------------------------------------------------------------
[✓/✗] Timeline has wordcard timing
[✓/✗] Wordcard files exist
[PLAYED] Wordcard sample from sentence 100

------------------------------------------------------------
METADATA (use youtube-metadata skill format!)
------------------------------------------------------------
Title: [Bilingual][{SOURCE}→{TARGET}] {Author} - {Title}

Description:
🎧 AI-generated bilingual audio for passive language learning.
Each sentence: first {source_language}, then {target_language}.

⚠️ Neural TTS - minor errors possible. Premium voices coming soon.

📩 Want other languages or texts? Drop a comment!

#{hashtag1} #Bilingual #LanguageLearning #{hashtag2}

Tags: (from youtube-metadata skill, NO # symbols)
Playlist: {playlist}

------------------------------------------------------------
UPLOAD COMMAND (copy & run when ready)
------------------------------------------------------------
python3 scripts/youtube_upload.py upload {project_name} {thumbnail_path} \
  --title "[Bilingual][{SOURCE}→{TARGET}] {Author} - {Title}" \
  --playlist "{playlist}" \
  --privacy public

============================================================
```

**Upload command flags:**
- `--title` — REQUIRED! Title in youtube-metadata format
- `--thumbnail` — path to thumbnail image (positional arg)
- `--playlist` — playlist name (RU - EN, RU - ES (LATAM), etc.)
- `--privacy` — private/unlisted/public (use public for immediate publish)
- `--schedule` — optional: "tomorrow", "tomorrow 14:00", "18:00", "+2h", or ISO datetime
- `--dry-run` — preview without uploading
- `-y` — skip confirmation

**Optimal premiere times for language learning content:**
- Best days: Wednesday, Thursday, Friday
- Best time: 10:00-14:00 (target audience timezone)
- For RU→EN: 14:00 MSK (11:00 UTC) — catches both Russian and European learners
- For RU→ES LATAM: 18:00 MSK (15:00 UTC, 12:00 Argentina) — catches LATAM afternoon

**CRITICAL:** Metadata MUST follow youtube-metadata skill format exactly:
- Title: `[Bilingual][{SOURCE}→{TARGET}] {Author} - {Title}`
- Author and Title MUST be in ENGLISH
- Description: standard template from youtube-metadata skill
- Tags: from youtube-metadata skill (NO hashtag symbols)

## Quality Checklist

Before showing final checklist, verify:

- [ ] Video file exists and size > 10MB
- [ ] Background image exists
- [ ] Thumbnail exists
- [ ] Timeline contains wordcard_start fields (if wordcards enabled)
- [ ] Wordcard audio files exist (if wordcards enabled)
- [ ] Translations are in correct target language
- [ ] Metadata generated via youtube-metadata skill
- [ ] Upload command is valid

## Anti-Patterns to Avoid

- **Don't** execute the upload command
- **Don't** skip language verification
- **Don't** use translations from beginning (use middle of book)
- **Don't** skip wordcard audio playback
- **Don't** generate metadata manually (use youtube-metadata skill)

## Example Execution

```
User: prepare upload nabokov_uzhas_ru_en

Claude:
Starting upload preparation for nabokov_uzhas_ru_en...

[Validates project exists]
[Reads meta: ru → en, 209 sentences]
[Reads translations from middle - sentences 100-102]
[Checks video: 192MB ✓] → file:///Users/.../video/output.mp4
[Checks background ✓] → file:///Users/.../video/background.png
[Checks thumbnail ✓] → file:///Users/.../thumbnails/ru_en/nabokov_uzhas.png
[Checks timeline: has wordcard_start ✓]
[Plays wordcard audio from sentence 100]
[Invokes youtube-metadata skill]
[Builds upload command]

============================================================
UPLOAD PREPARATION CHECKLIST
============================================================
[Full checklist output...]
============================================================

All checks passed! Review the checklist and run the upload command when ready.
```

## Summary

This skill prepares everything for YouTube upload:
1. Validates all files exist
2. Verifies languages by checking translations from middle of book
3. Confirms wordcards are included
4. Generates metadata via youtube-metadata skill
5. Builds upload command
6. Displays comprehensive checklist

User makes final decision to upload.
