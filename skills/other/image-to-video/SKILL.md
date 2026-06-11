---
name: image-to-video
description: "FFmpeg-based video creation from image and audio."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - image to video
    - audio visualization
    - static video
    - mp4 from image
    - music video
    - podcast video
    - video from image
    - combine image audio
    - album art video
    - cover art video
  pairs_with:
    - gemini-image-generator
    - workflow
  complexity: simple
  category: video-creation
---

# Image to Video Skill

Combine a static image with an audio file to produce an MP4 video using FFmpeg. Supports resolution presets (1080p, 720p, square, vertical), optional audio visualization overlays (waveform, spectrum, cqt, bars), and batch processing of matched image+audio pairs. For image generation, use `gemini-image-generator` instead.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| building FFmpeg filter graphs for audio visualization; encoding settings | `ffmpeg-filters.md` | Loads detailed guidance from `ffmpeg-filters.md`. |

## Instructions

### Phase 1: VALIDATE

Confirm all prerequisites before attempting video creation.

**Step 1: Check FFmpeg installation**

Always run this check first -- many systems lack FFmpeg or have minimal builds, and skipping it produces confusing subprocess errors instead of clear install guidance.

```bash
ffmpeg -version
```

If FFmpeg is not installed, provide platform-specific install instructions and stop.

**Step 2: Verify input files exist**

Both the image and audio files must be confirmed present before processing. Use absolute paths for all arguments -- relative paths break silently when the script executes from a different working directory.

```bash
ls -la /absolute/path/to/image.png /absolute/path/to/audio.mp3
```

Confirm both files exist and have non-zero size. Supported formats:
- **Images**: PNG, JPG, JPEG, GIF, WEBP, BMP
- **Audio**: MP3, WAV, M4A, OGG, FLAC

**Step 3: Determine parameters**

Re-read the user's request before selecting defaults. Resolve resolution preset and visualization mode from what the user actually asked for. Only apply defaults (1080p, static) when the user did not specify -- defaulting to static when the user requested a visualization is a common mistake.

If the user mentions a target platform, select the matching preset to avoid cropping or black bars on delivery:

| Preset | Dimensions | Platform |
|--------|------------|----------|
| `1080p` | 1920x1080 | YouTube HD (default) |
| `720p` | 1280x720 | Standard HD, smaller files |
| `square` | 1080x1080 | Instagram, social media |
| `vertical` | 1080x1920 | Stories, Reels, TikTok |

Optional visualization modes (off unless the user requests one):
- `--visualization waveform` -- Neon waveform overlay
- `--visualization spectrum` -- Scrolling frequency spectrum
- `--visualization cqt` -- Piano-roll style bars
- `--visualization bars` -- Frequency bar graph

**Gate**: FFmpeg installed, both input files exist, parameters resolved. Proceed only when gate passes.

### Phase 2: PREPARE

Set up output path and confirm no conflicts.

**Step 1: Determine output path**

Use the path provided by the user. If none given, derive from the audio filename:
```
/same/directory/as/audio/filename.mp4
```

**Step 2: Ensure output directory exists**

The script creates parent directories automatically. Verify the target directory is writable.

**Gate**: Output path determined, directory accessible. Proceed only when gate passes.

### Phase 3: ENCODE

Execute FFmpeg to produce the video. Only implement what the user requested -- no extra visualizations or format conversions beyond MP4.

Encoding defaults: libx264 preset medium, CRF 23, yuv420p pixel format, 192k AAC audio.

**Step 1: Run the script**

```bash
python3 $HOME/vexjoy-agent/skills/content/image-to-video/scripts/image_to_video.py \
  --image /absolute/path/to/image.png \
  --audio /absolute/path/to/audio.mp3 \
  --output /absolute/path/to/output.mp4 \
  --resolution 1080p \
  --visualization static
```

For workspace batch mode (processes all matched pairs in `workspace/input/`):

```bash
python3 $HOME/vexjoy-agent/skills/content/image-to-video/scripts/image_to_video.py \
  --process-workspace \
  --visualization waveform
```

**Step 2: Monitor output**

The script prints progress including input paths, resolution, visualization mode, and duration. Watch for ERROR lines in output.

**Gate**: Script exits with code 0. Proceed only when gate passes.

### Phase 4: VERIFY

Confirm the output video is valid. Do not report success based on exit code alone -- FFmpeg can exit 0 but produce a corrupt or zero-duration file.

**Step 1: Check file exists and has reasonable size**

```bash
ls -la /absolute/path/to/output.mp4
```

**Step 2: Probe video metadata**

File size alone does not prove video integrity. Always probe with ffprobe to confirm the output is a valid video with correct duration.

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height \
  -of default=noprint_wrappers=1 /absolute/path/to/output.mp4
```

Confirm video duration matches audio duration (within 1 second tolerance).

**Step 3: Report to user**

Provide: output file path, file size, duration, resolution, and visualization mode used.

**Gate**: Output file exists, duration matches audio, metadata is valid. Task complete.

## Error Handling

### Error: "FFmpeg is not installed or not in PATH"
Cause: FFmpeg binary not found on system
Solution:
1. Install via package manager: `brew install ffmpeg` (macOS), `sudo apt install ffmpeg` (Ubuntu)
2. Verify with `ffmpeg -version` after install
3. Ensure FFmpeg is in system PATH

### Error: "Image file not found" or "Audio file not found"
Cause: Path is incorrect, relative, or file does not exist
Solution:
1. Verify the path is absolute, not relative
2. Check file permissions with `ls -la`
3. Confirm the file extension matches a supported format

### Error: "FFmpeg failed" with filter errors
Cause: FFmpeg build lacks filter support (showwaves, showspectrum, showcqt)
Solution:
1. Install the full FFmpeg build, not a minimal variant
2. On Ubuntu: `sudo apt install ffmpeg` (full package)
3. Fall back to `--visualization static` which requires no special filters

### Error: "Could not determine audio duration"
Cause: Audio file is corrupted or uses an unsupported container format
Solution:
1. Test the audio independently: `ffprobe /path/to/audio.mp3`
2. Convert to a known format: `ffmpeg -i input.audio -acodec pcm_s16le output.wav`
3. Re-run with the converted file

## References

- `${CLAUDE_SKILL_DIR}/references/ffmpeg-filters.md`: FFmpeg filter documentation for visualization modes
- `${CLAUDE_SKILL_DIR}/scripts/image_to_video.py`: Python CLI script (exit codes: 0=success, 1=no FFmpeg, 2=encode failed, 3=missing args)
