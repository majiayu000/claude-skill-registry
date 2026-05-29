---
name: scene-detector
description: Detect scene changes and shot boundaries in videos. Use when you need to identify where scenes change, find natural cut points, or segment video into scenes. Supports adaptive detection for both fast cuts and gradual fades.
allowed-tools: Bash(ffmpeg:*) Bash(python:*)
compatibility: Requires PySceneDetect, FFmpeg, and OpenCV
metadata:
  version: "1.0"
  method: "Adaptive Content-Aware Detection"
---

# Scene Detector

This skill enables AI agents to detect scene changes and shot boundaries in videos using PySceneDetect.

## When to Use

- User wants to find scene changes in a video
- Need natural cut points for video editing
- Want to segment long video into scenes
- Detecting transitions for autocut workflow

## Available Scripts

### `scripts/detect_scenes.py`

Detect scene changes in video.

**Usage:**
```bash
python skills/scene-detector/scripts/detect_scenes.py <video_path> [options]
```

**Options:**
- `--threshold`: Detection threshold (0.1-0.5) - default: 0.3 (lower = more scenes)
- `--min-scene-len`: Minimum scene length in seconds - default: 0.5
- `--output, -o`: Output JSON path (default: `<video_path>_scenes.json`)
- `--split`: Split video into clips
- `--output-dir`: Directory for split clips (default: `./clips/`)

**Examples:**

Detect scenes with default settings:
```bash
python skills/scene-detector/scripts/detect_scenes.py video.mp4
```

Detect with more sensitivity (more scenes):
```bash
python skills/scene-detector/scripts/detect_scenes.py video.mp4 --threshold 0.2
```

Detect and split video into clips:
```bash
python skills/scene-detector/scripts/detect_scenes.py video.mp4 --split --output-dir ./scene_clips/
```

## Detection Methods

### Adaptive Detection (Default)

Adapts to video content, works well for:
- Fast cuts (music videos, action)
- Gradual fades (narrative content)
- Mixed content

### Threshold-Based Detection

Fixed threshold comparison:
- `--threshold 0.1`: Very sensitive (many scenes)
- `--threshold 0.3`: Balanced (default)
- `--threshold 0.5`: Less sensitive (fewer scenes)

## Output Format

### JSON Output

```json
{
  "video_path": "video.mp4",
  "duration": 123.45,
  "total_scenes": 15,
  "scenes": [
    {
      "scene_number": 1,
      "start_time": 0.0,
      "end_time": 8.5,
      "duration": 8.5,
      "content_type": "fast_cut"
    },
    {
      "scene_number": 2,
      "start_time": 8.5,
      "end_time": 23.2,
      "duration": 14.7,
      "content_type": "fade"
    }
  ]
}
```

### Split Clips

When `--split` is used, creates:
```
clips/
  scene_001.mp4
  scene_002.mp4
  scene_003.mp4
  ...
```

## Integration with Other Skills

After scene detection, you can use these skills:

- `video-trimmer`: Trim specific scenes
- `highlight-scanner`: Use scene changes as cut points
- `autocut-shorts`: Full workflow for creating short clips

## Common Workflow

1. User provides video file
2. Detect scenes using this skill
3. Identify interesting scenes based on timing
4. Create short clips from selected scenes

## Tips

- Lower threshold = more scenes detected
- Use `--min-scene-len` to filter out very short scenes
- Scene boundaries are excellent cut points for short-form content
- Consider scene changes when creating clips (15-60s each)

## References

- PySceneDetect documentation: https://www.scenedetect.com/
- OpenCV documentation: https://docs.opencv.org/
