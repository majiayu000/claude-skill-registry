---
name: video-post-process
description: Post-process videos with FFmpeg for final output
allowed-tools:
  - Bash
  - Read
  - Write
---

# Video Post-Processing Skill

Apply finishing touches to rendered videos using FFmpeg.

## Common Post-Processing Tasks

### 1. Add Voiceover to Video

```bash
# Replace audio track
ffmpeg -i output/video.mp4 -i output/voiceover.mp3 \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
  output/video_with_vo.mp4

# Mix voiceover with existing audio
ffmpeg -i output/video.mp4 -i output/voiceover.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=0" \
  -c:v copy \
  output/video_mixed.mp4
```

### 2. Add Background Music

```bash
# Add background music at 15% volume
ffmpeg -i output/video.mp4 -i assets/music/background.mp3 \
  -filter_complex "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first" \
  -c:v copy \
  output/video_with_music.mp4

# Add music with fade out at end
ffmpeg -i output/video.mp4 -i assets/music/background.mp3 \
  -filter_complex "[1:a]volume=0.15,afade=t=out:st=55:d=5[bg];[0:a][bg]amix=inputs=2:duration=first" \
  -c:v copy \
  output/video_with_music_fadeout.mp4
```

### 3. Resize/Crop Video

```bash
# Resize to 1080p
ffmpeg -i output/video.mp4 \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  output/video_1080p.mp4

# Convert horizontal to vertical (9:16)
ffmpeg -i output/video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  output/video_vertical.mp4

# Crop center square (for Instagram)
ffmpeg -i output/video.mp4 \
  -vf "crop=ih:ih:(iw-ih)/2:0" \
  output/video_square.mp4
```

### 4. Trim Video

```bash
# Trim from start to specific time
ffmpeg -i output/video.mp4 \
  -ss 00:00:05 -to 00:01:00 \
  -c copy \
  output/video_trimmed.mp4

# Trim last N seconds
ffmpeg -sseof -10 -i output/video.mp4 \
  -c copy \
  output/last_10_seconds.mp4
```

### 5. Add Fade Effects

```bash
# Fade in first 1 second, fade out last 1 second
ffmpeg -i output/video.mp4 \
  -vf "fade=t=in:st=0:d=1,fade=t=out:st=59:d=1" \
  -af "afade=t=in:st=0:d=1,afade=t=out:st=59:d=1" \
  output/video_faded.mp4
```

### 6. Normalize Audio Levels

```bash
# Loudness normalization (broadcast standard)
ffmpeg -i output/video.mp4 \
  -af loudnorm=I=-16:TP=-1.5:LRA=11 \
  -c:v copy \
  output/video_normalized.mp4
```

## Platform-Specific Export

### YouTube

```bash
ffmpeg -i output/video.mp4 \
  -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p \
  -movflags +faststart \
  output/video_youtube.mp4
```

### TikTok/Reels/Shorts (Vertical)

```bash
ffmpeg -i output/video.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 128k \
  output/video_vertical.mp4
```

### Twitter

```bash
ffmpeg -i output/video.mp4 \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  -t 140 \
  output/video_twitter.mp4
```

### GIF (Preview/Thumbnail)

```bash
ffmpeg -i output/video.mp4 \
  -vf "fps=10,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -t 5 \
  output/preview.gif
```

## Utility Commands

### Get Video Info

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration,r_frame_rate \
  -of csv=p=0 \
  output/video.mp4
```

### Get Duration

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  output/video.mp4
```

### Extract Thumbnail

```bash
# Extract frame at 5 seconds
ffmpeg -i output/video.mp4 -ss 5 -vframes 1 output/thumbnail.jpg

# Extract best quality thumbnail
ffmpeg -i output/video.mp4 -ss 5 -vframes 1 -q:v 2 output/thumbnail.jpg
```

## Output Files

- Final videos: `output/{name}_final.mp4`
- Platform variants: `output/{name}_{platform}.mp4`
- Thumbnails: `output/thumbnails/{name}.jpg`
- Previews: `output/previews/{name}.gif`
