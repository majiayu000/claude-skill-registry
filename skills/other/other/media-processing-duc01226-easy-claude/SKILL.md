---
name: media-processing
version: 1.0.0
description: '[AI & Tools] Use when processing multimedia files with FFmpeg (video/audio encoding, conversion, streaming), ImageMagick (image manipulation, batch processing), or RMBG (AI background removal). Covers format conversion, resizing, filtering, thumbnails, and media pipelines.'

allowed-tools: NONE
license: MIT
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

## Quick Summary

**Goal:** Process multimedia files using FFmpeg for video/audio encoding, conversion, streaming, and filtering.

**Workflow:**

1. **Identify** -- Match input to correct FFmpeg operation (convert, trim, merge, compress)
2. **Execute** -- Run FFmpeg command with appropriate codec and quality settings
3. **Verify** -- Check output file integrity and quality

**Key Rules:**

- Use tool selection table to pick correct FFmpeg operation
- Prefer hardware-accelerated encoding when available
- Always verify output file exists and is playable

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Media Processing Skill

Process video, audio, and images using FFmpeg, ImageMagick, and RMBG CLI tools.

## Tool Selection

| Task                        | Tool               | Reason                                   |
| --------------------------- | ------------------ | ---------------------------------------- |
| Video encoding/conversion   | FFmpeg             | Native codec support, streaming          |
| Audio extraction/conversion | FFmpeg             | Direct stream manipulation               |
| Image resize/effects        | ImageMagick        | Optimized for still images               |
| Background removal          | RMBG               | AI-powered, local processing             |
| Batch images                | ImageMagick        | mogrify for in-place edits               |
| Video thumbnails            | FFmpeg             | Frame extraction built-in                |
| GIF creation                | FFmpeg/ImageMagick | FFmpeg for video, ImageMagick for images |

## Installation

```bash
# macOS
brew install ffmpeg imagemagick
npm install -g rmbg-cli

# Ubuntu/Debian
sudo apt-get install ffmpeg imagemagick
npm install -g rmbg-cli

# Verify
ffmpeg -version && magick -version && rmbg --version
```

## Essential Commands

```bash
# Video: Convert/re-encode
ffmpeg -i input.mkv -c copy output.mp4
ffmpeg -i input.avi -c:v libx264 -crf 22 -c:a aac output.mp4

# Video: Extract audio
ffmpeg -i video.mp4 -vn -c:a copy audio.m4a

# Image: Convert/resize
magick input.png output.jpg
magick input.jpg -resize 800x600 output.jpg

# Image: Batch resize
mogrify -resize 800x -quality 85 *.jpg

# Background removal
rmbg input.jpg                          # Basic (modnet)
rmbg input.jpg -m briaai -o output.png  # High quality
rmbg input.jpg -m u2netp -o output.png  # Fast
```

## Key Parameters

**FFmpeg:**

- `-c:v libx264` - H.264 codec
- `-crf 22` - Quality (0-51, lower=better)
- `-preset slow` - Speed/compression balance
- `-c:a aac` - Audio codec

**ImageMagick:**

- `800x600` - Fit within (maintains aspect)
- `800x600^` - Fill (may crop)
- `-quality 85` - JPEG quality
- `-strip` - Remove metadata

**RMBG:**

- `-m briaai` - High quality model
- `-m u2netp` - Fast model
- `-r 4096` - Max resolution

## References

Detailed guides in `references/`:

- `ffmpeg-encoding.md` - Codecs, quality, hardware acceleration
- `ffmpeg-streaming.md` - HLS/DASH, live streaming
- `ffmpeg-filters.md` - Filters, complex filtergraphs
- `imagemagick-editing.md` - Effects, transformations
- `imagemagick-batch.md` - Batch processing, parallel ops
- `rmbg-background-removal.md` - AI models, CLI usage
- `common-workflows.md` - Video optimization, responsive images, GIF creation
- `troubleshooting.md` - Error fixes, performance tips
- `format-compatibility.md` - Format support, codec recommendations

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
