---
name: subtitle-overlay
description: Add burned-in subtitles/captions to video clips. Supports SRT/VTT subtitle files, customizable styling (font, size, color, position), and platform-specific presets for TikTok, YouTube Shorts, and Instagram Reels.
allowed-tools: Bash(ffmpeg:*) Bash(python:*)
compatibility: Requires FFmpeg
metadata:
  version: "1.0"
  formats: "SRT, VTT, ASS"
---

# Subtitle Overlay

This skill enables AI agents to add burned-in subtitles to video clips, essential for short-form content.

## When to Use

- User wants to add captions to video clips
- Creating accessible content with subtitles
- Adding stylized captions for TikTok/Shorts/Reels
- Converting transcript SRT to burned-in text
- Making content viewable without sound

## Available Scripts

### `scripts/add_subtitles.py`

Add subtitles to video.

**Usage:**
```bash
python skills/subtitle-overlay/scripts/add_subtitles.py <video_path> --subtitle <subtitle_path> [options]
```

**Options:**
- `--subtitle, -s`: Path to subtitle file (SRT/VTT) - required
- `--output, -o`: Output video path
- `--font`: Font name (default: Plus Jakarta Sans)
- `--font-size`: Font size (default: 24)
- `--font-color`: Font color (default: white)
- `--outline-color`: Outline color (default: black)
- `--outline-width`: Outline width (default: 2)
- `--position`: Text position (bottom, top, center) - default: bottom
- `--style`: Style preset (tiktok, shorts, reels, default)
- `--no-outline`: Disable text outline

**Examples:**

Basic subtitle overlay:
```bash
python skills/subtitle-overlay/scripts/add_subtitles.py video.mp4 --subtitle video.srt
```

Custom styling:
```bash
python skills/subtitle-overlay/scripts/add_subtitles.py video.mp4 --subtitle video.srt \
  --font Helvetica --font-size 28 --font-color yellow --outline-color black
```

Platform-specific style:
```bash
python skills/subtitle-overlay/scripts/add_subtitles.py video.mp4 --subtitle video.srt --style tiktok
```

### `scripts/generate_and_add.py`

Generate subtitles from transcript and add to video.

**Usage:**
```bash
python skills/subtitle-overlay/scripts/generate_and_add.py <video_path> <transcript_path> [options]
```

**Example:**
```bash
python skills/subtitle-overlay/scripts/generate_and_add.py video.mp4 video.txt --style shorts
```

## Style Presets

### TikTok Style
- Font: Plus Jakarta Sans
- Size: 28px
- Color: White
- Outline: Black, 2px
- Position: Bottom
- Margin: 20px

### YouTube Shorts Style
- Font: Plus Jakarta Sans
- Size: 26px
- Color: White
- Outline: Black, 3px
- Position: Bottom
- Margin: 30px

### Instagram Reels Style
- Font: Plus Jakarta Sans
- Size: 24px
- Color: White
- Outline: Black, 2px
- Position: Bottom
- Margin: 25px

### Default Style
- Font: Plus Jakarta Sans
- Size: 24px
- Color: White
- Outline: Black, 2px
- Position: Bottom

## Output Format

```json
{
  "success": true,
  "input_video": "video.mp4",
  "input_subtitle": "video.srt",
  "output_video": "video_subtitled.mp4",
  "style": {
    "font": "Plus Jakarta Sans",
    "font_size": 24,
    "font_color": "white",
    "outline_color": "black",
    "outline_width": 2,
    "position": "bottom"
  },
  "subtitle_count": 45,
  "duration": 60.5
}
```

## Subtitle File Formats

### SRT Format
```
1
00:00:00,000 --> 00:00:05,000
This is the first subtitle.

2
00:00:05,000 --> 00:00:10,000
This is the second subtitle.
```

### VTT Format
```
WEBVTT

00:00:00.000 --> 00:00:05.000
This is the first subtitle.

00:00:05.000 --> 00:00:10.000
This is the second subtitle.
```

## Integration with Other Skills

After adding subtitles, the video is ready for:

- Direct upload to TikTok/Shorts/Reels
- Final output from `autocut-shorts` workflow

## Common Workflow

1. User provides video and transcript/subtitle file
2. Add subtitles using this skill
3. Video is ready for platform upload

## Tips

- Ensure subtitle timing matches video
- Use platform-specific styles for consistency
- White text with black outline works best
- Larger font size (26-28px) for mobile viewing
- Test subtitle visibility on mobile devices
- Keep subtitles within safe margins (20-30px from edges)

## Performance

- **Processing time**: ~5-10 seconds per minute of video
- **File size increase**: Minimal (just video re-encode)
- **Quality**: Maintains original quality

## Error Handling

- **Invalid subtitle format**: Returns error with format guide
- **Timing mismatch**: Warns but continues
- **Font not found**: Falls back to system default
- **Encoding issues**: Uses compatible codecs

## References

- FFmpeg subtitles filter: https://ffmpeg.org/ffmpeg-filters.html#subtitles
- SRT format: https://en.wikipedia.org/wiki/SubRip
- WebVTT format: https://www.w3.org/TR/webvtt1/
