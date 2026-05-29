---
name: portrait-resizer
description: Convert videos to 9:16 portrait format (1080x1920) for TikTok, YouTube Shorts, Instagram Reels, and Facebook Reels. Supports smart cropping (focus on faces/subjects), center cropping, and letterboxing. Maintains aspect ratio and quality.
allowed-tools: Bash(ffmpeg:*)
compatibility: Requires FFmpeg and OpenCV
metadata:
  version: "1.0"
  formats: "9:16 portrait"
---

# Portrait Resizer

This skill converts horizontal videos to vertical 9:16 portrait format suitable for short-form content platforms.

## When to Use

- User wants to create TikTok videos from horizontal content
- Converting YouTube videos to YouTube Shorts format
- Creating Instagram Reels from widescreen video
- Preparing content for Facebook Reels
- Converting any 16:9 video to 9:16 format

## Supported Platforms

- **TikTok**: 1080x1920, 9:16, 15-60s
- **YouTube Shorts**: 1080x1920, 9:16, 15-60s
- **Instagram Reels**: 1080x1920, 9:16, 15-90s
- **Facebook Reels**: 1080x1920, 9:16, 15-90s

## Available Scripts

### `scripts/resize_to_portrait.py`

Convert video to 9:16 portrait format.

**Usage:**
```bash
python skills/portrait-resizer/scripts/resize_to_portrait.py <video_path> [options]
```

**Options:**
- `--width`: Target width (default: 1080)
- `--height`: Target height (default: 1920)
- `--mode`: Resize mode (smart, center, letterbox) - default: smart
- `--focus-x`: Focus point X coordinate (0-1, smart mode)
- `--focus-y`: Focus point Y coordinate (0-1, smart mode)
- `--output, -o`: Output video path (default: `<video_path>_portrait.mp4`)
- `--quality`: Quality preset (fast, medium, slow) - default: fast

**Examples:**

Basic resize to portrait:
```bash
python skills/portrait-resizer/scripts/resize_to_portrait.py video.mp4
```

Resize with smart cropping:
```bash
python skills/portrait-resizer/scripts/resize_to_portrait.py video.mp4 --mode smart
```

Resize with specific focus point:
```bash
python skills/portrait-resizer/scripts/resize_to_portrait.py video.mp4 --mode smart --focus-x 0.7 --focus-y 0.5
```

Center crop:
```bash
python skills/portrait-resizer/scripts/resize_to_portrait.py video.mp4 --mode center
```

Letterbox (padding on top/bottom):
```bash
python skills/portrait-resizer/scripts/resize_to_portrait.py video.mp4 --mode letterbox
```

### `scripts/batch_resize.py`

Resize multiple videos to portrait format.

**Usage:**
```bash
python skills/portrait-resizer/scripts/batch_resize.py --input-dir <dir> [options]
```

**Options:**
- `--input-dir`: Directory with videos to resize
- `--output-dir`: Output directory (default: `./portrait/`)
- All other options from `resize_to_portrait.py`

**Example:**
```bash
python skills/portrait-resizer/scripts/batch_resize.py --input-dir ./clips/ --output-dir ./portrait_clips/
```

## Resize Modes

### Smart Crop (Default)

Intelligently crops to focus on subjects:
- Detects faces and main subjects
- Analyzes motion and activity
- Centers on the most important area
- Best for talking-head, interviews, tutorials

### Center Crop

Simple center crop:
- Crops from the center of the video
- May cut off subjects on edges
- Fast and predictable
- Best when subject is always centered

### Letterbox

Pillarbox/black bars:
- Maintains full width of video
- Adds padding on top and bottom
- No content loss
- Best for showing full context

## Output Specifications

**Default Output:**
- Resolution: 1080x1920
- Aspect Ratio: 9:16
- Video Codec: H.264 (libx264)
- Audio Codec: AAC
- Container: MP4

**Platform-Specific Presets:**

```python
presets = {
    'tiktok': {
        'width': 1080,
        'height': 1920,
        'bitrate': '4000k',
        'fps': 30
    },
    'youtube_shorts': {
        'width': 1080,
        'height': 1920,
        'bitrate': '4000k',
        'fps': 30
    },
    'instagram_reels': {
        'width': 1080,
        'height': 1920,
        'bitrate': '4000k',
        'fps': 30
    }
}
```

## Output Format

```json
{
  "success": true,
  "input_path": "video.mp4",
  "output_path": "video_portrait.mp4",
  "input_resolution": {
    "width": 1920,
    "height": 1080
  },
  "output_resolution": {
    "width": 1080,
    "height": 1920
  },
  "mode": "smart",
  "focus_point": {
    "x": 0.65,
    "y": 0.50
  },
  "quality_settings": {
    "preset": "fast",
    "crf": 23
  }
}
```

## Smart Crop Algorithm

1. **Face Detection**: Uses OpenCV Haar Cascades to detect faces
2. **Motion Analysis**: Identifies areas with highest motion activity
3. **Center Weighting**: Gives slight preference to center (0.5, 0.5)
4. **Subject Tracking**: Maintains focus on moving subjects
5. **Fallback**: Uses center crop if no faces/motion detected

## Integration with Other Skills

After resizing, you can use these skills:

- `subtitle-overlay`: Add captions to portrait video
- `autocut-shorts`: Full workflow with all steps

## Common Workflow

1. User provides video file
2. Find highlights using `highlight-scanner`
3. Trim segments using `video-trimmer`
4. Resize to portrait using this skill
5. Add subtitles using `subtitle-overlay`
6. Export final clips

## Tips

- Resize AFTER trimming (more efficient)
- Use smart crop for talking-head content
- Use center crop for action/sports content
- Use letterbox for cinematic/wide shots
- Test different focus points for best results
- Face detection works best with clear frontal faces

## Performance

- **Simple crop/resize**: ~2-5 seconds per minute
- **Smart crop with face detection**: ~5-10 seconds per minute
- **Batch processing**: Parallel processing available

## Error Handling

- **Small videos**: Minimum resolution checks
- **Already portrait**: Returns as-is or error
- **Face detection failure**: Falls back to center crop
- **Codec issues**: Re-encodes with standard codecs

## References

- FFmpeg crop filter: https://ffmpeg.org/ffmpeg-filters.html#crop
- FFmpeg scale filter: https://ffmpeg.org/ffmpeg-filters.html#scale
- OpenCV face detection: https://docs.opencv.org/
