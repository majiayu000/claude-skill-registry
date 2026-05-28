---
name: markdown-video
description: Convert Deckset-format markdown slides with speaker notes to presentation video with TTS narration. Use when user requests to create video from slides, generate presentation video, or convert slides to MP4 format.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
license: MIT
---

# Markdown Video Skill

Convert markdown slides to presentation video with AI-generated visuals and TTS audio narration.

## When to Use This Skill

Activate this skill when the user:
- Asks to create video from markdown slides
- Requests to convert presentation to MP4 format
- Wants to generate narrated video from slides
- Needs automated slide-to-video conversion

## Key Features

- **Gemini AI-generated visuals**: High-quality slide images with full emoji and Korean support
- **OpenAI TTS narration**: Natural voice from speaker notes
- **Delta updates**: Only regenerates changed slides (saves time and API costs)
- **Multiple visual styles**: technical-diagram, professional, vibrant-cartoon, watercolor

## Input Requirements

- **Markdown file** with speaker notes marked with `^` prefix
- **GEMINI_API_KEY** environment variable for image generation
- **OPENAI_API_KEY** environment variable for TTS audio

## Output Specifications

- **MP4 video**: 1920x1080 (Full HD)
- **Duration**: Each slide displays for duration of its audio narration
- **File naming**: `{input_filename}.mp4`

---

## Workflow

### Step 1: Generate Audio Files

```bash
cd "{slides_directory}"
python /Users/lifidea/.claude/skills/markdown-video/generate_audio.py "{slides_filename}" --output-dir "audio"
```

**Delta update**: Only regenerates audio for slides with changed speaker notes.
- Use `--force` to regenerate all audio files

**Output**:
- `audio/slide_0.mp3`, `slide_1.mp3`, ... (0-indexed)
- Cache file: `audio/.audio_cache.json`

### Step 2: Generate Slide Images with Gemini

```bash
cd "{slides_directory}"
python /Users/lifidea/.claude/skills/markdown-video/create_slides_gemini.py "{slides_filename}" \
  --output-dir "slides-gemini" \
  --style "technical-diagram" \
  --auto-approve
```

**Delta update**: Only regenerates images for slides with changed content.
- Use `--force` to regenerate all slide images

**Style Options**:

| Style | Description | Best For |
|-------|-------------|----------|
| `technical-diagram` | Clean lines, infographic icons, muted blue/gray | Technical, education |
| `professional` | Minimalist, geometric shapes | Corporate, formal |
| `vibrant-cartoon` | Bright gradients, flat design | Marketing, startups |
| `watercolor` | Soft pastels, organic shapes | Creative, personal |

**Other Parameters**:
- `--model`: Gemini model (default: gemini-3-pro-image-preview)
- `--aspect-ratio`: 16:9 (default), 1:1, 9:16, 4:3, 3:4
- `--start-from N`: Resume from slide N
- `--dry-run`: Preview prompts without generating

**Output**:
- `slides-gemini/1.jpeg`, `2.jpeg`, ... (1-indexed)
- Cache file: `slides-gemini/.slides_cache.json`

### Step 3: Create Final Video

```bash
cd "{slides_directory}"
python /Users/lifidea/.claude/skills/markdown-video/slides_to_video.py \
  --slides-dir "slides-gemini" \
  --audio-dir "audio" \
  --output "{output_filename}.mp4"
```

---

## Delta Updates

Both audio and image generation support **delta updates** - only regenerating what changed.

### How It Works

1. **Content hashing**: Each slide's content is hashed (MD5)
2. **Cache storage**: Hashes stored in `.audio_cache.json` / `.slides_cache.json`
3. **Change detection**: On subsequent runs, only changed slides are regenerated
4. **File verification**: Also checks if output file exists

### Example Output

```
✅ Found 20 slides
   20 slides with speaker notes

✨ Delta update: 17 slides unchanged, 3 to regenerate

🎵 Generating 3 audio files...
Progress |████████████████████████████████████████| 3/3 (100.0%)

✅ Audio generation complete!
   Generated: 3/3 files
   Unchanged: 17 files (skipped)
```

### Force Regeneration

To ignore cache and regenerate everything:

```bash
# Force regenerate all audio
python generate_audio.py "slides.md" --output-dir "audio" --force

# Force regenerate all images
python create_slides_gemini.py "slides.md" --output-dir "slides-gemini" --force
```

---

## Quick Reference

### Full Workflow (First Run)

```bash
cd "{slides_directory}"

# Step 1: Generate audio
python /Users/lifidea/.claude/skills/markdown-video/generate_audio.py "slides.md" --output-dir "audio"

# Step 2: Generate slide images
python /Users/lifidea/.claude/skills/markdown-video/create_slides_gemini.py "slides.md" \
  --output-dir "slides-gemini" \
  --style "technical-diagram" \
  --auto-approve

# Step 3: Create video
python /Users/lifidea/.claude/skills/markdown-video/slides_to_video.py \
  --slides-dir "slides-gemini" \
  --audio-dir "audio" \
  --output "presentation.mp4"
```

### Update Workflow (After Changes)

Same commands - delta updates are automatic:

```bash
# Only regenerates changed slides
python generate_audio.py "slides.md" --output-dir "audio"
python create_slides_gemini.py "slides.md" --output-dir "slides-gemini" --auto-approve
python slides_to_video.py --slides-dir "slides-gemini" --audio-dir "audio" --output "presentation.mp4"
```

---

## Requirements

### System Dependencies
- **Python 3.7+**
- **ffmpeg**: `brew install ffmpeg`

### Python Packages
```bash
pip install Pillow requests google-genai
```

### Environment Variables
```bash
export OPENAI_API_KEY="sk-..."
export GEMINI_API_KEY="..."
```

---

## Cost Estimation

| Component | Cost | Example (20 slides) |
|-----------|------|---------------------|
| Gemini images | ~$0.04/slide | ~$0.80 |
| OpenAI TTS | ~$0.015/1K chars | ~$0.50 |
| **Total** | | ~$1.30 |

With delta updates, subsequent runs only cost for changed slides.

---

## Error Handling

### No speaker notes found
- Slides need `^` prefixed speaker notes for narration
- Example: `^ This is the speaker note for this slide.`

### Pronunciation problems
- Replace technical terms with phonetic equivalents in speaker notes
- Test with `--dry-run` first

### API errors
- Check API key environment variables
- Gemini rate limits: script includes 1-second delay between generations

---

## Quality Checklist

Before marking complete:

- [ ] OpenAI and Gemini API keys configured
- [ ] Markdown file has speaker notes with `^` prefix
- [ ] Audio files generated successfully
- [ ] Slide images generated successfully
- [ ] Video plays correctly with synced audio
- [ ] Resolution is 1920x1080
