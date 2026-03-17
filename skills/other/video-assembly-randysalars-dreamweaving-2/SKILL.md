---
name: Video Assembly
tier: 3
load_policy: task-specific
description: Assemble final video from audio, images, and subtitles
version: 1.0.0
parent_skill: production-operations
---

# Video Assembly Skill

> **The Visual Wrapper for the Audio Journey**

This skill handles assembling the final video from mastered audio, scene images, and VTT subtitles.

---

## Purpose

Create YouTube-ready video files that complement the hypnotic audio experience.

---

## Video Standards

| Parameter | Standard |
|-----------|----------|
| Resolution | 1920x1080 (Full HD) |
| Aspect Ratio | 16:9 |
| Codec | H.264 |
| Frame Rate | 24 fps (cinematic) |
| Audio Codec | AAC 320kbps |
| Container | MP4 |

---

## Input Requirements

| Input | File | Required |
|-------|------|----------|
| Master Audio | `{session}_MASTER.mp3` | Yes |
| Scene Images | `images/uploaded/*.png` | Yes |
| Subtitles | `output/subtitles.vtt` | Yes |

---

## Scene Image Generation

### Primary Method: Stable Diffusion (Default)

```bash
python3 scripts/core/generate_scene_images.py sessions/{session}/
```

### Alternative: Midjourney Prompts

```bash
python3 scripts/core/generate_scene_images.py sessions/{session}/ --midjourney-only
```

### Alternative: Stock Images

```bash
python3 scripts/core/generate_scene_images.py sessions/{session}/ --method stock
```

### Image Specifications

| Property | Requirement |
|----------|-------------|
| Resolution | 1920x1080 minimum |
| Format | PNG or JPEG |
| Aspect Ratio | 16:9 |
| Naming | `scene_01.png`, `scene_02.png`, etc. |

---

## VTT Subtitle Generation

```bash
python3 scripts/ai/vtt_generator.py sessions/{session}
```

### VTT Format

```vtt
WEBVTT
Kind: captions
Language: en

1
00:00:00.000 --> 00:00:05.500
Welcome to this healing journey.

2
00:00:06.000 --> 00:00:12.000
Find a comfortable position and
allow your eyes to close.
```

### Subtitle Guidelines

| Guideline | Value |
|-----------|-------|
| Max lines per caption | 2 |
| Max characters per line | ~80 |
| Min duration | 1.5 seconds |
| Max duration | 7 seconds |

---

## Video Assembly Command

```bash
python3 scripts/core/assemble_session_video.py sessions/{session}/
```

This automatically:
- Sequences images based on script sections
- Adds cross-fade transitions
- Syncs subtitles to audio
- Outputs to `output/video/session_final.mp4`

---

## Manual FFmpeg Assembly

For custom control:

```bash
# Create video from images with audio
ffmpeg -y \
  -framerate 1/10 \
  -pattern_type glob -i 'images/uploaded/*.png' \
  -i output/{session}_MASTER.mp3 \
  -c:v libx264 -r 24 -pix_fmt yuv420p \
  -c:a aac -b:a 320k \
  -shortest \
  output/video/session_final.mp4
```

---

## Image-to-Section Mapping

Images should correspond to script sections:

| Image | Section | Timing |
|-------|---------|--------|
| `scene_01.png` | Pre-Talk | 0:00-3:00 |
| `scene_02.png` | Induction | 3:00-8:00 |
| `scene_03.png` | Deepening | 8:00-12:00 |
| `scene_04.png` | Journey Start | 12:00-17:00 |
| `scene_05.png` | Journey Core | 17:00-22:00 |
| `scene_06.png` | Helm/Deepest | 22:00-25:00 |
| `scene_07.png` | Integration | 25:00-28:00 |
| `scene_08.png` | Emergence | 28:00-30:00 |

---

## Transition Effects

| Transition | Duration | Use For |
|------------|----------|---------|
| Cross-dissolve | 2-3 seconds | Section transitions |
| Fade from black | 3 seconds | Opening |
| Fade to black | 3 seconds | Closing |

---

## Output Files

| File | Location | Purpose |
|------|----------|---------|
| Final video | `output/video/session_final.mp4` | Direct use |
| YouTube copy | `output/youtube_package/final_video.mp4` | Upload ready |

---

## Video Overlay Generation

Generate supporting graphics:

```bash
python3 scripts/core/generate_video_images.py sessions/{session}/ --all
```

Creates:
- `title_card.png` - Video intro screen
- `sections/section_*.png` - Chapter transitions
- `outro.png` - End screen
- `social_preview.png` - Social sharing

---

## Quality Verification

After assembly:

```bash
# Check video properties
ffprobe -v error -show_format -show_streams output/video/session_final.mp4

# Play with VLC to verify sync
vlc output/video/session_final.mp4
```

### Quality Checklist

- [ ] Resolution is 1920x1080
- [ ] Frame rate is 24 fps
- [ ] Audio syncs with subtitles
- [ ] Transitions are smooth
- [ ] No visible artifacts
- [ ] Duration matches audio
- [ ] File size reasonable (<2GB for 30 min)

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Audio/video desync | Different durations | Use `-shortest` flag |
| Pixelated video | Wrong pixel format | Use `-pix_fmt yuv420p` |
| Green frames | Image format issue | Convert images to PNG |
| Subtitle timing off | VTT not scaled | Regenerate VTT with actual audio duration |
| File too large | Bitrate too high | Use `-crf 23` for smaller file |

---

## Integration with Pipeline

**Before** (dependencies):
- Audio mastered (`{session}_MASTER.mp3`)
- Scene images ready (`images/uploaded/`)
- VTT subtitles generated (`output/subtitles.vtt`)

**After** (next steps):
- YouTube packaging

---

## Related Resources

- **Skill**: `tier3-production/audio-mixing/` (input)
- **Skill**: `tier3-production/youtube-packaging/` (next step)
- **Doc**: `docs/STOCK_IMAGE_SOP.md`
- **Script**: `scripts/core/assemble_session_video.py`
