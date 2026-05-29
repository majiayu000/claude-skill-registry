---
name: video-trimmer
description: Trim and cut videos by timestamp with precision. Supports both stream copy (fast) and re-encoding (quality) modes. Use when you need to extract specific segments from videos, create clips from highlights, or cut unwanted portions.
allowed-tools: Bash(ffmpeg:*)
compatibility: Requires FFmpeg
metadata:
  version: "1.0"
---

# Video Trimmer

This skill enables AI agents to trim and cut videos with precision using FFmpeg.

## When to Use

- User wants to extract a specific segment from a video
- Creating clips from highlight timestamps
- Removing unwanted portions from videos
- Cutting videos for short-form content
- Trimming based on detected highlights

## Available Scripts

### `scripts/trim.py`

Trim video to specified time range.

**Usage:**
```bash
python skills/video-trimmer/scripts/trim.py <video_path> [options]
```

**Options:**
- `--start, -s`: Start time (seconds or HH:MM:SS) - required
- `--end, -e`: End time (seconds or HH:MM:SS) - required
- `--output, -o`: Output video path (default: `<video_path>_trimmed.mp4`)
- `--reencode`: Re-encode video (higher quality, slower)
- `--codec`: Video codec for re-encoding (default: libx264)
- `--quality`: Quality preset (fast, medium, slow) - default: fast
- `--copy`: Use stream copy (faster, no quality loss)

**Examples:**

Trim 10-second segment:
```bash
python skills/video-trimmer/scripts/trim.py video.mp4 --start 30 --end 40
```

Trim with timestamp format:
```bash
python skills/video-trimmer/scripts/trim.py video.mp4 --start 00:01:30 --end 00:01:45
```

Re-encode for better quality:
```bash
python skills/video-trimmer/scripts/trim.py video.mp4 --start 30 --end 40 --reencode --quality medium
```

Fast stream copy:
```bash
python skills/video-trimmer/scripts/trim.py video.mp4 --start 30 --end 40 --copy
```

### `scripts/trim_multiple.py`

Trim multiple segments from one video.

**Usage:**
```bash
python skills/video-trimmer/scripts/trim_multiple.py <video_path> --segments <json_file> [options]
```

**Options:**
- `--segments`: JSON file with segment list
- `--output-dir`: Output directory (default: `./clips/`)
- `--copy`: Use stream copy
- `--prefix`: Filename prefix for clips

**Segments JSON Format:**
```json
[
  {"start": 30, "end": 45},
  {"start": 120, "end": 135},
  {"start": 200, "end": 220}
]
```

**Example:**
```bash
python skills/video-trimmer/scripts/trim_multiple.py video.mp4 --segments segments.json --prefix highlight
```

## Output

### Single Trim

Returns trimmed video file:
```
video_trimmed.mp4
```

### Multiple Trims

Returns multiple clip files:
```
clips/
  highlight_001.mp4
  highlight_002.mp4
  highlight_003.mp4
```

## Modes Explained

### Stream Copy (Default, Fast)

- **Speed**: Very fast (seconds)
- **Quality**: No quality loss (exact copy)
- **Use when**: Quick cuts, same codec segments
- **Limitations**: Cut points may not be frame-perfect

### Re-encode (High Quality)

- **Speed**: Slower (depends on length)
- **Quality**: Frame-perfect, configurable quality
- **Use when**: Frame-accurate cuts, codec conversion
- **Options**: Adjust CRF for quality vs file size

## Time Formats

Supported time formats:

- **Seconds**: `30`, `45.5`, `120`
- **MM:SS**: `1:30`, `2:45`
- **HH:MM:SS**: `00:01:30`, `01:15:30`

## Integration with Other Skills

After trimming, you can use these skills:

- `portrait-resizer`: Convert to 9:16 portrait format
- `subtitle-overlay`: Add captions to clips
- `autocut-shorts`: Full workflow with all steps

## Common Workflow

1. User provides video file
2. Find highlights using `highlight-scanner`
3. Trim segments using this skill
4. Resize to portrait using `portrait-resizer`
5. Add subtitles using `subtitle-overlay`

## Tips

- Use `--copy` for fast processing when quality isn't critical
- Use `--reencode` for frame-perfect cuts
- Trimming before resizing is more efficient
- Keep 2-3 second buffers around highlights for context
- Use JSON input for batch trimming

## Error Handling

- **Invalid timestamps**: Returns error with valid range
- **Out of bounds**: Clamps to video duration
- **File not found**: Clear error message
- **Codec issues**: Falls back to re-encoding

## Performance

- **Stream copy**: ~1 second per minute of video
- **Re-encode**: ~5-30 seconds per minute (depends on quality)
- **Batch processing**: Processes sequentially

## References

- FFmpeg documentation: https://ffmpeg.org/documentation.html
- FFmpeg trim filter: https://ffmpeg.org/ffmpeg-filters.html#trim
