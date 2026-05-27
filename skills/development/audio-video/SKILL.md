---
name: audio-video
description: "Audio and video processing with FFmpeg, WebRTC, and streaming. Covers transcoding, format conversion, real-time communication, and media pipelines. Use for video processing, live streaming, or audio manipulation."
---

# Audio & Video Processing Skill

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

---

## 1. FFmpeg Basics

### Installation
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (Chocolatey)
choco install ffmpeg
```

### Basic Conversion
```bash
# Video format conversion
ffmpeg -i input.avi output.mp4

# Audio format conversion
ffmpeg -i input.wav output.mp3

# With codec specification
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

### Video Quality Control
```bash
# CRF (Constant Rate Factor) - 0-51, lower = better quality
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# Bitrate control
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M output.mp4

# Two-pass encoding for better quality
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output.mp4
```

---

## 2. Video Processing

### Resize and Scale
```bash
# Scale to specific resolution
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4

# Scale maintaining aspect ratio
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4  # Auto height
ffmpeg -i input.mp4 -vf "scale=-1:720" output.mp4   # Auto width

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

### Concatenate Videos
```bash
# Create file list
echo "file 'video1.mp4'" > list.txt
echo "file 'video2.mp4'" >> list.txt
echo "file 'video3.mp4'" >> list.txt

# Concatenate
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
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

### Speed Adjustment
```bash
# Speed up 2x
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" output.mp4

# Slow down 0.5x
ffmpeg -i input.mp4 -filter:v "setpts=2*PTS" -filter:a "atempo=0.5" output.mp4
```

---

## 3. Audio Processing

### Extract Audio
```bash
# Extract audio track
ffmpeg -i video.mp4 -vn -c:a copy audio.aac

# Convert to MP3
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3

# Extract specific audio stream
ffmpeg -i video.mp4 -map 0:a:0 -c copy audio.m4a
```

### Audio Conversion
```bash
# WAV to MP3
ffmpeg -i input.wav -c:a libmp3lame -b:a 320k output.mp3

# FLAC to MP3
ffmpeg -i input.flac -c:a libmp3lame -q:a 0 output.mp3

# MP3 to AAC
ffmpeg -i input.mp3 -c:a aac -b:a 256k output.m4a
```

### Audio Normalization
```bash
# Loudnorm filter (EBU R128)
ffmpeg -i input.mp3 -af loudnorm=I=-16:LRA=11:TP=-1.5 output.mp3

# Volume adjustment
ffmpeg -i input.mp3 -af "volume=2.0" output.mp3  # 2x louder
ffmpeg -i input.mp3 -af "volume=0.5" output.mp3  # Half volume

# Peak normalization
ffmpeg -i input.mp3 -af "acompressor" output.mp3
```

### Merge Audio/Video
```bash
# Replace audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v -map 1:a output.mp4

# Add audio to video (mix)
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -filter_complex "[0:a][1:a]amix=inputs=2:duration=first" output.mp4
```

---

## 4. Thumbnails and Screenshots

### Single Thumbnail
```bash
# At specific time
ffmpeg -i video.mp4 -ss 00:00:05 -frames:v 1 thumbnail.jpg

# Best quality
ffmpeg -i video.mp4 -ss 00:00:05 -frames:v 1 -q:v 2 thumbnail.jpg

# Specific size
ffmpeg -i video.mp4 -ss 00:00:05 -frames:v 1 -vf "scale=320:180" thumbnail.jpg
```

### Multiple Thumbnails
```bash
# Every N seconds
ffmpeg -i video.mp4 -vf "fps=1/10" thumbnails_%03d.jpg  # Every 10 seconds

# Specific number of thumbnails
ffmpeg -i video.mp4 -vf "select='not(mod(n,300))'" -vsync vfr thumb_%03d.jpg

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

---

## 5. Streaming Formats

### HLS (HTTP Live Streaming)
```bash
# Generate HLS
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -hls_time 10 \
  -hls_list_size 0 \
  -hls_segment_filename "segment_%03d.ts" \
  output.m3u8

# Adaptive bitrate HLS
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split=3[v1][v2][v3];[v1]scale=1920:1080[v1out];[v2]scale=1280:720[v2out];[v3]scale=854:480[v3out]" \
  -map "[v1out]" -c:v:0 libx264 -b:v:0 5M \
  -map "[v2out]" -c:v:1 libx264 -b:v:1 2M \
  -map "[v3out]" -c:v:2 libx264 -b:v:2 1M \
  -map 0:a -c:a aac -b:a 128k \
  -var_stream_map "v:0,a:0 v:1,a:0 v:2,a:0" \
  -master_pl_name master.m3u8 \
  -hls_time 6 \
  -hls_segment_filename "v%v/segment_%03d.ts" \
  v%v/index.m3u8
```

### DASH (Dynamic Adaptive Streaming)
```bash
ffmpeg -i input.mp4 \
  -c:v libx264 -c:a aac \
  -f dash \
  -init_seg_name "init-\$RepresentationID\$.m4s" \
  -media_seg_name "chunk-\$RepresentationID\$-\$Number%05d\$.m4s" \
  output.mpd
```

---

## 6. Python Integration

### PyAV (FFmpeg bindings)
```python
import av

def transcode_video(input_path, output_path, target_codec='libx264'):
    input_container = av.open(input_path)
    output_container = av.open(output_path, 'w')

    # Get input streams
    video_stream = input_container.streams.video[0]
    audio_stream = input_container.streams.audio[0] if input_container.streams.audio else None

    # Create output streams
    output_video = output_container.add_stream(target_codec, rate=video_stream.average_rate)
    output_video.width = video_stream.width
    output_video.height = video_stream.height
    output_video.pix_fmt = 'yuv420p'

    if audio_stream:
        output_audio = output_container.add_stream('aac', rate=audio_stream.rate)

    for packet in input_container.demux():
        if packet.stream.type == 'video':
            for frame in packet.decode():
                for out_packet in output_video.encode(frame):
                    output_container.mux(out_packet)
        elif packet.stream.type == 'audio' and audio_stream:
            for frame in packet.decode():
                for out_packet in output_audio.encode(frame):
                    output_container.mux(out_packet)

    # Flush encoders
    for packet in output_video.encode():
        output_container.mux(packet)

    output_container.close()
    input_container.close()
```

### MoviePy
```python
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

def process_video(input_path, output_path):
    # Load video
    clip = VideoFileClip(input_path)

    # Trim
    trimmed = clip.subclip(10, 60)  # 10s to 60s

    # Resize
    resized = trimmed.resize(height=720)

    # Add text overlay
    txt_clip = TextClip("Hello World", fontsize=50, color='white')
    txt_clip = txt_clip.set_position('center').set_duration(5)

    # Composite
    final = CompositeVideoClip([resized, txt_clip])

    # Export
    final.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac'
    )

    clip.close()

def create_thumbnail(video_path, output_path, time=5):
    clip = VideoFileClip(video_path)
    frame = clip.get_frame(time)
    clip.save_frame(output_path, t=time)
    clip.close()

def concatenate_videos(video_paths, output_path):
    clips = [VideoFileClip(path) for path in video_paths]
    final = concatenate_videoclips(clips)
    final.write_videofile(output_path)
    for clip in clips:
        clip.close()
```

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

def transcode_video(input_path, output_path, options=None):
    """Transcode video with FFmpeg"""
    cmd = ['ffmpeg', '-i', input_path]

    if options:
        if 'video_codec' in options:
            cmd.extend(['-c:v', options['video_codec']])
        if 'audio_codec' in options:
            cmd.extend(['-c:a', options['audio_codec']])
        if 'crf' in options:
            cmd.extend(['-crf', str(options['crf'])])
        if 'resolution' in options:
            cmd.extend(['-vf', f"scale={options['resolution']}"])

    cmd.extend(['-y', output_path])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"FFmpeg error: {result.stderr}")

    return True

def generate_hls(input_path, output_dir):
    """Generate HLS stream"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    cmd = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-hls_time', '10',
        '-hls_list_size', '0',
        '-hls_segment_filename', f'{output_dir}/segment_%03d.ts',
        f'{output_dir}/index.m3u8'
    ]

    subprocess.run(cmd, check=True)
```

---

## 7. Live Streaming

### RTMP Server (nginx-rtmp)
```nginx
# nginx.conf
rtmp {
    server {
        listen 1935;

        application live {
            live on;
            record off;

            # HLS output
            hls on;
            hls_path /var/www/hls;
            hls_fragment 3;
            hls_playlist_length 60;
        }
    }
}
```

### Stream to RTMP
```bash
# Stream file to RTMP
ffmpeg -re -i input.mp4 -c copy -f flv rtmp://server/live/stream

# Stream webcam
ffmpeg -f v4l2 -i /dev/video0 -f alsa -i hw:0 \
  -c:v libx264 -preset veryfast -b:v 2M \
  -c:a aac -b:a 128k \
  -f flv rtmp://server/live/stream

# Stream to YouTube
ffmpeg -i input.mp4 \
  -c:v libx264 -preset medium -b:v 4M \
  -c:a aac -b:a 128k \
  -f flv rtmp://a.rtmp.youtube.com/live2/YOUR_STREAM_KEY
```

---

## 8. Video Processing Pipeline

### Async Processing with Celery
```python
from celery import Celery
import os

celery = Celery('video_tasks')

@celery.task
def process_upload(video_id, input_path):
    """Complete video processing pipeline"""
    output_dir = f'/videos/{video_id}'
    os.makedirs(output_dir, exist_ok=True)

    # Generate thumbnail
    generate_thumbnail.delay(video_id, input_path, f'{output_dir}/thumb.jpg')

    # Transcode to multiple resolutions
    resolutions = [
        ('1080p', '1920:1080', '5M'),
        ('720p', '1280:720', '2.5M'),
        ('480p', '854:480', '1M'),
    ]

    for name, scale, bitrate in resolutions:
        transcode_resolution.delay(
            video_id, input_path,
            f'{output_dir}/{name}.mp4',
            scale, bitrate
        )

    # Generate HLS
    generate_hls.delay(video_id, input_path, f'{output_dir}/hls')

@celery.task
def generate_thumbnail(video_id, input_path, output_path):
    cmd = [
        'ffmpeg', '-i', input_path,
        '-ss', '5', '-frames:v', '1',
        '-vf', 'scale=320:-1',
        output_path
    ]
    subprocess.run(cmd, check=True)

@celery.task
def transcode_resolution(video_id, input_path, output_path, scale, bitrate):
    cmd = [
        'ffmpeg', '-i', input_path,
        '-c:v', 'libx264', '-b:v', bitrate,
        '-vf', f'scale={scale}',
        '-c:a', 'aac', '-b:a', '128k',
        output_path
    ]
    subprocess.run(cmd, check=True)
```

---

## 9. Audio Analysis

### Waveform Generation
```python
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def generate_waveform(audio_path, output_path):
    """Generate waveform image"""
    y, sr = librosa.load(audio_path)

    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(y, sr=sr)
    plt.title('Waveform')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

def generate_spectrogram(audio_path, output_path):
    """Generate spectrogram image"""
    y, sr = librosa.load(audio_path)
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    plt.figure(figsize=(14, 5))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

---

## 10. Best Practices

### Encoding Presets
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

---

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
