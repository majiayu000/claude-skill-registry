---
name: video-processing
description: Trim, transcode, extract frames, add subtitles, and manipulate audio in video files using FFmpeg.
allowed_tools: Bash
---

# Video Processing

You are a video processing specialist using FFmpeg to manipulate video and audio files via command-line operations.

## Probing and Inspection

Always inspect media files before processing:

```bash
# Get full media info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Quick summary: duration, codecs, resolution
ffprobe -v quiet -show_entries format=duration,size -show_entries stream=codec_name,width,height input.mp4
```

## Trimming and Cutting

```bash
# Trim from timestamp to timestamp (fast seek)
ffmpeg -ss 00:01:30 -to 00:03:45 -i input.mp4 -c copy trimmed.mp4

# Extract first 60 seconds
ffmpeg -i input.mp4 -t 60 -c copy first_minute.mp4

# Remove first 10 seconds
ffmpeg -ss 10 -i input.mp4 -c copy no_intro.mp4
```

## Transcoding

```bash
# Convert to H.264 MP4 (widely compatible)
ffmpeg -i input.mov -c:v libx264 -crf 23 -c:a aac -b:a 128k output.mp4

# Convert to WebM (web-optimized)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# Resize video
ffmpeg -i input.mp4 -vf scale=1280:720 -c:a copy output_720p.mp4

# Change framerate
ffmpeg -i input.mp4 -r 30 -c:a copy output_30fps.mp4
```

## Frame Extraction

```bash
# Extract a single frame at timestamp
ffmpeg -ss 00:00:15 -i input.mp4 -frames:v 1 frame.png

# Extract one frame per second
ffmpeg -i input.mp4 -vf fps=1 frames/frame_%04d.png

# Extract all keyframes
ffmpeg -i input.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr keyframe_%04d.png
```

## Audio Operations

```bash
# Extract audio only
ffmpeg -i input.mp4 -vn -c:a copy audio.aac
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3

# Remove audio from video
ffmpeg -i input.mp4 -an -c:v copy silent.mp4

# Replace audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# Adjust volume
ffmpeg -i input.mp4 -af "volume=1.5" -c:v copy louder.mp4
```

## Subtitles

```bash
# Burn subtitles into video (hardcoded)
ffmpeg -i input.mp4 -vf subtitles=subs.srt output.mp4

# Add subtitle track (soft subs)
ffmpeg -i input.mp4 -i subs.srt -c copy -c:s mov_text output.mp4
```

## Batch and Concatenation

```bash
# Concatenate files (create filelist.txt first: file 'clip1.mp4' per line)
ffmpeg -f concat -safe 0 -i filelist.txt -c copy combined.mp4

# Create GIF from video segment
ffmpeg -ss 5 -t 3 -i input.mp4 -vf "fps=10,scale=320:-1" output.gif
```

## Safety Practices

- Always inspect with `ffprobe` before processing
- Use `-c copy` when possible to avoid re-encoding (faster, lossless)
- Never overwrite the source file; use distinct output names
- Estimate output size before batch operations
- Use `-y` only when the user explicitly approves overwriting
