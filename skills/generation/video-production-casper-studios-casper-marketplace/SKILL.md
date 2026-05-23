---
name: video-production
description: Video downloading, stitching, title slides, and YouTube descriptions. Use this skill when downloading videos from Google Drive, creating title slides, stitching multiple videos together, or generating YouTube descriptions with timestamps. Triggers on video course creation, video editing, video compilation, or YouTube upload preparation.
---

# Video Production

## Overview

Assemble course videos from individual lesson files with title slides and auto-generated timestamps for YouTube.

## Quick Decision Tree

```
What do you need?
│
├── Full course assembly (end-to-end)
│   └── references/workflow.md
│   └── Combines all scripts below
│
├── Download videos from Drive
│   └── Script: scripts/gdrive_video_download.py
│
├── Create title slides
│   └── Script: scripts/create_title_slides.py
│
├── Stitch videos together
│   └── Script: scripts/stitch_videos.py
│
└── Generate YouTube description
    └── Script: scripts/generate_youtube_description.py
```

## Environment Setup

Google Drive OAuth (same as google-workspace skill).

### System Requirements
- **FFmpeg** installed and in PATH
- Python 3.9+

## Complete Workflow

```bash
# Full course assembly from Drive folder
python scripts/stitch_videos.py \
  --folder "https://drive.google.com/drive/folders/xxx" \
  --output "Complete Course.mp4" \
  --slide-duration 3
```

## Pipeline Steps

1. **Download** - Get all videos from Drive folder
2. **Parse Titles** - Extract clean names from `[e1] Intro` format
3. **Get Metadata** - FFprobe for duration/resolution
4. **Generate Slides** - Title card for each lesson
5. **Build Concat List** - video1 → slide2 → video2 → ...
6. **Stitch with FFmpeg** - Concatenate all segments
7. **Calculate Timestamps** - Track cumulative duration
8. **Generate Description** - YouTube-ready markdown

## Outputs

| File | Description |
|------|-------------|
| `{output_name}.mp4` | Final stitched video |
| `youtube_description.md` | Timestamped description |
| `metadata.json` | Processing info |

## Performance

| Input | Time | Output Size |
|-------|------|-------------|
| 5 videos (30 min) | ~5 min | ~1.5 GB |
| 10 videos (1 hr) | ~10 min | ~3 GB |
| 20 videos (2 hr) | ~20 min | ~6 GB |

## Security Notes

### Credential Handling
- Google OAuth credentials for Drive access (see google-workspace skill)
- `mycreds.txt` and `client_secrets.json` never committed to git
- No additional API keys required for local video processing

### Data Privacy
- All video processing happens locally using FFmpeg
- No video content is uploaded to external cloud services
- Source videos downloaded from Google Drive to local `.tmp/`
- Final videos stored locally until manually uploaded
- Metadata JSON contains file names and timestamps only

### Access Scopes
- Google Drive: `drive.readonly` sufficient for downloading
- Google Drive: `drive` required for uploading final videos
- No external video processing APIs used

### Compliance Considerations
- **Local Processing**: All encoding/stitching done locally (privacy-preserving)
- **No Cloud Upload**: Videos never leave your machine during processing
- **Content Rights**: Ensure you have rights to source video content
- **Course Content**: Verify licensing for educational content distribution
- **YouTube ToS**: Generated descriptions comply with YouTube guidelines
- **Storage**: Large video files require adequate local disk space
- **Cleanup**: Remove temporary files from `.tmp/` after processing

## Troubleshooting

### Common Issues

#### Issue: FFmpeg not found
**Symptoms:** "FFmpeg not found" or "command not found: ffmpeg"
**Cause:** FFmpeg not installed or not in system PATH
**Solution:**
- Install FFmpeg: `brew install ffmpeg` (macOS) or download from ffmpeg.org
- Verify installation: `ffmpeg -version`
- Add FFmpeg to PATH if installed in non-standard location
- Restart terminal after installation

#### Issue: Codec mismatch / incompatible videos
**Symptoms:** "Non-monotonous DTS" or codec errors during stitching
**Cause:** Source videos have different codecs, resolutions, or frame rates
**Solution:**
- Re-encode all source videos to the same format before stitching
- Use FFmpeg to normalize: `ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4`
- Ensure consistent resolution (e.g., all 1920x1080)
- Match frame rates across all videos (e.g., all 30fps)

#### Issue: Audio out of sync
**Symptoms:** Audio drifts from video over time
**Cause:** Inconsistent frame rates or variable frame rate sources
**Solution:**
- Use constant frame rate for all source videos
- Re-encode with `-vsync cfr` flag
- Avoid mixing video from different sources/devices
- Check audio sample rates match across files

#### Issue: Insufficient disk space
**Symptoms:** "No space left on device" or incomplete output
**Cause:** Not enough free space for video processing
**Solution:**
- Check available disk space: `df -h`
- Clear `.tmp/` directory of old files
- Move large source videos to external drive
- Process fewer videos at once

#### Issue: Google Drive download fails
**Symptoms:** Videos fail to download from Drive folder
**Cause:** OAuth issue, permissions, or network timeout
**Solution:**
- Verify Google OAuth credentials (see google-workspace skill)
- Check folder sharing permissions
- Try downloading single file first to test
- Check for network connectivity issues

#### Issue: Title slides not generating
**Symptoms:** Missing title cards in final video
**Cause:** Font or image generation issue
**Solution:**
- Verify ImageMagick or Pillow is installed
- Check font files exist if custom fonts specified
- Review title text for special characters
- Try with default font settings first

## Resources

- **references/workflow.md** - Complete video course workflow

## Integration Patterns

### Full Course Pipeline
**Skills:** google-workspace → video-production → google-workspace
**Use case:** End-to-end course video assembly
**Flow:**
1. Download lesson videos from Google Drive folder
2. Generate title slides and stitch all videos together
3. Upload final video back to Drive and generate YouTube description

### Transcript to Timestamps
**Skills:** transcript-search → video-production
**Use case:** Generate YouTube descriptions from meeting recordings
**Flow:**
1. Search transcripts for relevant meetings
2. Extract topic timestamps from transcript
3. Generate formatted YouTube description with chapter markers

### Content to Title Slides
**Skills:** content-generation → video-production
**Use case:** Create branded title cards for videos
**Flow:**
1. Generate title slide images with content-generation
2. Export slides in video-compatible format
3. Insert title slides between video segments
