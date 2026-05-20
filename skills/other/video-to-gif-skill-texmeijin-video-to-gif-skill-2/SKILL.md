---
name: video-to-gif
description: |
  Convert multiple video files (MOV/MP4) into a single merged GIF with customizable speed per segment.
  Use this skill when users want to:
  - Merge multiple videos into one GIF
  - Create demo GIFs from screen recordings
  - Combine video clips with different playback speeds
  - Convert videos to optimized GIFs with compression
  Triggers: "create GIF from videos", "merge videos to GIF", "convert MOV to GIF", "combine videos into animated GIF"
---

# Video to GIF Converter

Merge multiple video files into a single optimized GIF with per-segment speed control.

## Quick Start

```bash
.claude/skills/video-to-gif/scripts/merge_videos_to_gif.sh -o output.gif video1.mov:2 video2.mov:4.75 video3.mov:4.75
```

## Script Usage

```
.claude/skills/video-to-gif/scripts/merge_videos_to_gif.sh -o output.gif [options] video1:speed1 video2:speed2 ...
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o FILE` | (required) | Output GIF file path |
| `-w WIDTH` | 800 | Output width in pixels |
| `-h HEIGHT` | 338 | Output height in pixels |
| `-f FPS` | 8 | Frames per second (lower = smaller file) |
| `-c COLORS` | 128 | Max colors (64-256, lower = smaller file) |
| `-l LOSSY` | 80 | Lossy compression 0-200 (higher = smaller file, more artifacts) |

### Video Format

`path/to/video.mov:speed_multiplier`

- `1` = original speed
- `2` = 2x faster (video plays in half the time)
- `4.75` = 4.75x faster
- `0.5` = half speed (slower playback)

## Examples

### Basic: Merge 3 videos with different speeds

First video slower (2x), others fast (4.75x):

```bash
.claude/skills/video-to-gif/scripts/merge_videos_to_gif.sh -o demo.gif \
  ~/Desktop/intro.mov:2 \
  ~/Desktop/action.mov:4.75 \
  ~/Desktop/outro.mov:4.75
```

### Custom resolution and compression

Create a smaller GIF (640x360, 64 colors, high compression):

```bash
.claude/skills/video-to-gif/scripts/merge_videos_to_gif.sh -o small.gif -w 640 -h 360 -c 64 -l 120 \
  video1.mov:3 video2.mov:3
```

### Higher quality GIF

More colors and lower compression:

```bash
.claude/skills/video-to-gif/scripts/merge_videos_to_gif.sh -o hq.gif -f 10 -c 256 -l 40 \
  video.mov:2
```

## Dependencies

Required tools (install via Homebrew on macOS):

```bash
brew install ffmpeg gifsicle
```

## Tips

- **File size too large?** Reduce FPS (`-f 6`), colors (`-c 64`), or increase lossy (`-l 100`)
- **Video looks choppy?** Increase FPS (`-f 12`) or reduce speed multiplier
- **Black bars appearing?** Videos with different aspect ratios get padded to fit target dimensions
- **First segment too fast?** Use a lower speed multiplier (e.g., `:1.5` instead of `:4`)
