---
name: audio-video
description: Audio and video processing with FFmpeg, transcoding, and streaming. Process media files, generate thumbnails, and build streaming solutions. Use when working with audio/video processing, FFmpeg, media transcoding, or streaming applications. Triggers on ffmpeg, video processing, audio processing, transcoding, streaming, media conversion, HLS, thumbnail generation.
---

# Audio & Video Processing

Complete guide for audio and video processing.

## Quick Reference

### FFmpeg Commands

| Task | Command |
|------|---------|
| **Convert** | `ffmpeg -i input.mp4 output.webm` |
| **Extract Audio** | `ffmpeg -i video.mp4 -vn audio.mp3` |
| **Thumbnail** | `ffmpeg -i video.mp4 -ss 5 -frames:v 1 thumb.jpg` |
| **Resize** | `ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4` |
| **Compress** | `ffmpeg -i input.mp4 -crf 28 output.mp4` |

### Common Formats

```
Video: MP4, WebM, MKV, AVI, MOV
Audio: MP3, AAC, WAV, FLAC, OGG
Codecs: H.264, H.265/HEVC, VP9, AV1
```

## Installation

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg
```

## Video Processing

### Basic Conversion

```bash
# Video format conversion
ffmpeg -i input.avi output.mp4

# With codec specification
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

### Quality Control

```bash
# CRF (Constant Rate Factor) - 0-51, lower = better quality
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# Bitrate control
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M output.mp4

# Two-pass encoding for better quality
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output.mp4
```

### Resize and Scale

```bash
# Scale to specific resolution
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4

# Scale maintaining aspect ratio
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4  # Auto height

# Scale with padding (letterbox)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

### Trim and Cut

```bash
# Cut from timestamp to timestamp
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy output.mp4

# Cut with duration
ffmpeg -i input.mp4 -ss 00:01:00 -t 30 -c copy output.mp4

# Fast seek (put -ss before input)
ffmpeg -ss 00:01:00 -i input.mp4 -t 30 -c copy output.mp4
```

### Add Watermark

```bash
# Image watermark
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4

# Bottom right corner
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# Text watermark
ffmpeg -i input.mp4 -vf "drawtext=text='Copyright':fontsize=24:fontcolor=white:x=10:y=10" output.mp4
```

## Audio Processing

### Extract Audio

```bash
# Extract audio track
ffmpeg -i video.mp4 -vn -c:a copy audio.aac

# Convert to MP3
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3
```

### Audio Conversion

```bash
# WAV to MP3
ffmpeg -i input.wav -c:a libmp3lame -b:a 320k output.mp3

# FLAC to MP3
ffmpeg -i input.flac -c:a libmp3lame -q:a 0 output.mp3
```

### Audio Normalization

```bash
# Loudnorm filter (EBU R128)
ffmpeg -i input.mp3 -af loudnorm=I=-16:LRA=11:TP=-1.5 output.mp3

# Volume adjustment
ffmpeg -i input.mp3 -af "volume=2.0" output.mp3  # 2x louder
```

### Merge Audio/Video

```bash
# Replace audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v -map 1:a output.mp4
```

## Thumbnails and Screenshots

### Single Thumbnail

```bash
# At specific time
ffmpeg -i video.mp4 -ss 00:00:05 -frames:v 1 thumbnail.jpg

# Specific size
ffmpeg -i video.mp4 -ss 00:00:05 -frames:v 1 -vf "scale=320:180" thumbnail.jpg
```

### Multiple Thumbnails

```bash
# Every N seconds
ffmpeg -i video.mp4 -vf "fps=1/10" thumbnails_%03d.jpg  # Every 10 seconds

# Thumbnail sprite/grid
ffmpeg -i video.mp4 -vf "fps=1/10,scale=160:90,tile=10x10" sprite.jpg
```

### GIF Creation

```bash
# Simple GIF
ffmpeg -i video.mp4 -ss 0 -t 5 -vf "fps=10,scale=320:-1" output.gif

# High quality GIF with palette
ffmpeg -i video.mp4 -ss 0 -t 5 -vf "fps=10,scale=320:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i video.mp4 -i palette.png -ss 0 -t 5 -filter_complex "[0:v]fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
```

## Streaming Formats

### HLS (HTTP Live Streaming)

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -hls_time 10 \
  -hls_list_size 0 \
  -hls_segment_filename "segment_%03d.ts" \
  output.m3u8
```

### DASH

```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -f dash \
  output.mpd
```

## Live Streaming

### Stream to RTMP

```bash
# Stream file to RTMP
ffmpeg -re -i input.mp4 -c copy -f flv rtmp://server/live/stream

# Stream to YouTube
ffmpeg -i input.mp4 \
  -c:v libx264 -preset medium -b:v 4M \
  -c:a aac -b:a 128k \
  -f flv rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY
```

## Python Integration

### FFmpeg Subprocess

```python
import subprocess
import json

def get_video_info(video_path):
    """Get video metadata using ffprobe"""
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def transcode_video(input_path, output_path, crf=23):
    """Transcode video with FFmpeg"""
    cmd = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264', '-crf', str(crf),
        '-c:a', 'aac',
        '-y', output_path
    ]
    subprocess.run(cmd, check=True)
```

### MoviePy

```python
from moviepy.editor import VideoFileClip

def process_video(input_path, output_path):
    clip = VideoFileClip(input_path)
    trimmed = clip.subclip(10, 60)
    resized = trimmed.resize(height=720)
    resized.write_videofile(output_path, codec='libx264')
    clip.close()
```

## Encoding Presets

```bash
# Web-optimized MP4
ffmpeg -i input.mp4 \
  -c:v libx264 -preset slow -crf 22 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output.mp4

# Archive quality
ffmpeg -i input.mp4 \
  -c:v libx264 -preset veryslow -crf 18 \
  -c:a flac \
  archive.mkv

# Mobile-optimized
ffmpeg -i input.mp4 \
  -c:v libx264 -preset fast -crf 28 \
  -vf "scale='min(720,iw)':-2" \
  -c:a aac -b:a 96k \
  mobile.mp4
```

## Best Practices

1. **Use hardware acceleration** - NVENC, VAAPI, VideoToolbox
2. **Optimize for web** - faststart flag for streaming
3. **Choose right codec** - H.264 for compatibility, VP9/AV1 for quality
4. **Appropriate CRF** - 18-23 for quality, 28+ for size
5. **Two-pass for size** - When file size matters
6. **Process async** - Queue long operations
7. **Generate previews** - Thumbnails and sprites
8. **Validate input** - Check format before processing
9. **Clean temp files** - Remove intermediate files
10. **Monitor resources** - CPU/memory limits

## When to Use This Skill

- Video format conversion
- Audio extraction and processing
- Thumbnail generation
- Streaming setup (HLS/DASH)
- Video compression and optimization
- Batch media processing
- Live streaming configuration
