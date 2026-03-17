---
name: viral-video-platform-specs
description: Complete platform upload specifications for viral video creation across TikTok, YouTube Shorts, Instagram Reels, Facebook Reels, Snapchat Spotlight, and Twitter/X. PROACTIVELY activate for: (1) Platform-specific video encoding, (2) Upload requirements lookup, (3) Multi-platform export, (4) File size optimization, (5) Aspect ratio conversion, (6) Duration limits, (7) Audio requirements, (8) Caption/subtitle specs, (9) Thumbnail requirements, (10) Quality vs compatibility trade-offs. Provides: Comprehensive spec tables, FFmpeg presets per platform, optimal encoding settings, file size calculators, batch export workflows, and 2025-2026 platform-specific algorithm insights.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

# Viral Video Platform Specifications (2025-2026)

Complete reference for all major short-form video platforms with FFmpeg encoding presets.

## Quick Reference Table

| Platform | Aspect | Resolution | Max Duration | Max Size | Codec | Audio |
|----------|--------|------------|--------------|----------|-------|-------|
| **TikTok** | 9:16 | 1080x1920 | 10 min | 287 MB | H.264 | AAC 128k |
| **YouTube Shorts** | 9:16 | 1080x1920 | 60 sec | 256 GB | H.264/VP9 | AAC 192k |
| **Instagram Reels** | 9:16 | 1080x1920 | 90 sec | 4 GB | H.264 | AAC 128k |
| **Facebook Reels** | 9:16 | 1080x1920 | 90 sec | 4 GB | H.264 | AAC 128k |
| **Snapchat Spotlight** | 9:16 | 1080x1920 | 60 sec | 300 MB | H.264 | AAC |
| **Twitter/X** | 9:16 | 1080x1920 | 2 min 20 sec | 512 MB | H.264 | AAC 128k |
| **Pinterest Idea Pins** | 9:16 | 1080x1920 | 60 sec | 2 GB | H.264 | AAC |
| **LinkedIn** | 9:16/1:1 | 1080x1920 | 10 min | 5 GB | H.264 | AAC |

---

## TikTok Specifications

### Technical Requirements (2025-2026)

| Specification | Requirement | Notes |
|---------------|-------------|-------|
| **Aspect Ratio** | 9:16 (vertical) - **REQUIRED** | Fills mobile screen |
| **Resolution** | 1080x1920 (recommended), min 720x1280 | TikTok compresses 4K anyway |
| **Video Codec** | H.264 (required) | HEVC transcoded to H.264 |
| **Audio Codec** | AAC | High-quality audio critical |
| **Audio Bitrate** | 128-192 kbps | Higher = better |
| **Audio Sample Rate** | 44100 Hz (48000 Hz accepted) | 44.1kHz standard |
| **Audio Loudness** | -10 to -12 LUFS | Louder wins on mobile |
| **True Peak** | -1.5 dBTP max | Prevents distortion |
| **Frame Rate** | 24-60 fps (30 fps recommended) | 60fps for sports/action only |
| **Pixel Format** | yuv420p (required) | 8-bit color, Rec.709 |
| **Color Space** | Rec.709 (SDR) | Turn off HDR before upload |
| **Max File Size** | 287 MB (iOS), 72 MB (Android web) | ~500 MB desktop |
| **Max Duration** | 10 minutes | Optimal: 21-34s |
| **Optimal Duration** | 21-34 seconds | Highest completion rate |
| **Min Duration** | 3 seconds | Platform minimum |
| **Keyframe Interval** | 2 seconds (60-90 frames at 30fps) | Every 2-3 seconds |

### Optimal Encoding Parameters (2025-2026)

**Bitrate Recommendations** (VBR):
- **24 fps**: 4-6 Mbps
- **30 fps**: 6-8.5 Mbps (sweet spot: 6-8 Mbps)
- **60 fps**: 8-12 Mbps

**CRF Values**:
- **CRF 21-23**: Optimal quality/size balance
- Below CRF 21: Diminishing returns (TikTok recompresses)
- Above CRF 24: Noticeable quality loss on mobile

**Preset Selection**:
- **fast**: Quick encoding, good quality (recommended for batch)
- **medium**: Better compression (default)
- **slow**: Best quality (use for hero content)

### FFmpeg Preset (Updated 2025-2026)

```bash
# TikTok optimized encoding - 2025-2026 specs
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30" \
  -c:v libx264 -preset medium -crf 22 -profile:v high -level 4.1 \
  -x264-params "keyint=60:min-keyint=30:scenecut=0" \
  -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -af "loudnorm=I=-11:TP=-1.5:LRA=11" \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -max_muxing_queue_size 1024 \
  -t 34 \
  output_tiktok.mp4
```

### Two-Pass Encoding for Precise Bitrate Control

```bash
# Pass 1
ffmpeg -y -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset medium -b:v 7M -maxrate 8M -bufsize 16M \
  -profile:v high -level 4.1 -pass 1 -an -f null /dev/null

# Pass 2
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset medium -b:v 7M -maxrate 8M -bufsize 16M \
  -profile:v high -level 4.1 -pass 2 \
  -c:a aac -b:a 192k -ar 44100 \
  -af "loudnorm=I=-11:TP=-1.5:LRA=11" \
  -pix_fmt yuv420p -movflags +faststart \
  output_tiktok.mp4
```

### Algorithm Insights (2025-2026)

- **Hook Window**: 1.3 seconds to capture attention
- **Optimal Length**: 21-34 seconds for highest completion
- **Captions**: 80% boost in engagement when visible
- **Trending Audio**: 88% say it helps discoverability
- **Post Frequency**: 1-3x daily for growth phase

---

## YouTube Shorts Specifications

### Technical Requirements (2025-2026)

| Specification | Requirement | Notes |
|---------------|-------------|-------|
| **Aspect Ratio** | 9:16 (vertical) - **REQUIRED** | Strictly enforced for Shorts shelf |
| **Resolution** | 1080x1920 (recommended), min 1920px on short side | Limited to 1080p playback |
| **Video Codec** | H.264, VP9, HEVC (VP9 preferred by algorithm) | YouTube transcodes to VP9/AV1 |
| **Audio Codec** | AAC, Opus (Opus for VP9) | AAC-LC most compatible |
| **Audio Bitrate** | 192-384 kbps | YouTube recommends 384k stereo |
| **Audio Sample Rate** | 48000 Hz preferred | Match video production standard |
| **Audio Loudness** | -13 to -15 LUFS | YouTube normalizes to -14 LUFS |
| **True Peak** | -1 to -3 dB | Recommended: -1.5 dBTP |
| **Frame Rate** | 24-60 fps (30 fps recommended) | Upload at source frame rate |
| **Pixel Format** | yuv420p (SDR), yuv420p10le (HDR) | Rec.709 color space for SDR |
| **Max File Size** | 256 GB (practical: 20-100 MB for Shorts) | Higher bitrate = better post-compression quality |
| **Max Duration** | 60 seconds (HARD LIMIT) | Strict enforcement |
| **Optimal Duration** | 50-60 seconds | Maximizes watch time metric |
| **Min Duration** | ~15 seconds recommended | Shorter = harder to rank |
| **Color Space** | Rec.709 (SDR), Rec.2100 (HDR only) | Consistent colors across devices |

### Optimal Encoding Parameters (2025-2026)

**Bitrate Recommendations** (VBR):
- **1080p30**: 8 Mbps (YouTube official recommendation)
- **1080p60**: 12 Mbps

**CRF Values**:
- **CRF 18-20**: High quality (hero content, archival)
- **CRF 20-22**: Optimal quality/size (recommended)
- **CRF 23+**: Acceptable for less critical content

**Preset Selection**:
- **slow**: Best quality, longer encode (recommended for uploads)
- **medium**: Good balance for batch processing
- **fast**: Quick turnaround, slightly larger files

### FFmpeg Preset - H.264 (Updated 2025-2026)

```bash
# YouTube Shorts H.264 encoding - maximum compatibility
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30" \
  -c:v libx264 -preset slow -crf 20 -profile:v high -level 4.2 \
  -x264-params "keyint=60:min-keyint=30:scenecut=40" \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -pix_fmt yuv420p \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 \
  -movflags +faststart \
  -max_muxing_queue_size 1024 \
  -t 59 \
  -metadata title="Your Shorts Title" \
  -metadata comment="#Shorts" \
  output_shorts.mp4
```

### Two-Pass Encoding for Optimal Quality

```bash
# Pass 1 - Analysis
ffmpeg -y -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset slow -b:v 8M -profile:v high -level 4.2 \
  -pass 1 -an -f null /dev/null

# Pass 2 - Encode
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset slow -b:v 8M -profile:v high -level 4.2 \
  -pass 2 \
  -c:a aac -b:a 192k -ar 48000 \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -pix_fmt yuv420p -movflags +faststart \
  -metadata comment="#Shorts" \
  output_shorts.mp4
```

### FFmpeg Preset (VP9 - Higher Quality)

```bash
# YouTube Shorts VP9 encoding (preferred by YouTube)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1" \
  -c:v libvpx-vp9 -crf 25 -b:v 0 -deadline good -cpu-used 2 \
  -c:a libopus -b:a 192k -ar 48000 \
  -row-mt 1 \
  -t 59 \
  output_shorts.webm
```

### Algorithm Insights (2025-2026)

- **Completion Rate**: 80-90% = algorithm boost
- **Optimal Length**: 50-60 seconds maximizes watch time
- **First 3 Seconds**: Critical for retention
- **Consistency**: Daily posting recommended for growth
- **Thumbnail**: Custom thumbnails increase CTR 30%+

---

## Instagram Reels Specifications

### Technical Requirements (2025-2026)

| Specification | Requirement | Notes |
|---------------|-------------|-------|
| **Aspect Ratio** | 9:16 (preferred), 4:5, 1:1 accepted | 9:16 fills screen, recommended |
| **Resolution** | 1080x1920 (recommended), min 720p | No 4K support |
| **Video Codec** | H.264 | Instagram transcodes all uploads |
| **Audio Codec** | AAC (AAC-LC preferred) | Superior to MP3 |
| **Audio Bitrate** | 128-192 kbps | Higher quality recommended |
| **Audio Sample Rate** | 44100-48000 Hz | 44.1kHz or 48kHz |
| **Audio Loudness** | -10 to -12 LUFS | Louder = better mobile experience |
| **True Peak** | -1 dBTP recommended | Prevents clipping |
| **Frame Rate** | 30 fps recommended (max 60) | 30fps optimal for compatibility |
| **Pixel Format** | yuv420p | Square pixels, fixed frame rate |
| **Max File Size** | 650 MB (<10 min), 4 GB (longer) | Practical: 50-200 MB |
| **Max Duration** | 15 minutes (uploaded), 3 min (in-app 2025) | In-app recording: 90s before Jan 2025 |
| **Optimal Duration** | 7-15 seconds (casual), 15-30s (tutorial) | First 3 seconds critical |
| **Min Duration** | 3 seconds | Platform minimum |
| **Cover Image** | 1080x1920, JPEG | Custom thumbnail increases engagement |

### Optimal Encoding Parameters (2025-2026)

**Bitrate Recommendations** (VBR):
- **Standard Quality**: 3,500-5,000 kbps
- **High Quality**: 5,000-10,000 kbps (recommended for best results)

**CRF Values**:
- **CRF 21-23**: Optimal balance
- **CRF 20**: High quality for hero content
- **CRF 24+**: Avoid (visible compression on mobile)

**Preset Selection**:
- **fast**: Quick batch encoding
- **medium**: Recommended balance
- **slow**: Best quality (diminishing returns after Instagram recompression)

### Safe Zones (2025-2026)

- **Top safe zone**: Keep text/graphics below top 14%
- **Bottom safe zone**: Avoid bottom 35% (UI overlays)
- **Side safe zones**: 6% margin on each side
- **Text placement**: Upper middle 2/3 of frame safest

### FFmpeg Preset (Updated 2025-2026)

```bash
# Instagram Reels optimized encoding - high quality
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30" \
  -c:v libx264 -preset medium -crf 22 -profile:v high -level 4.1 \
  -x264-params "keyint=60:min-keyint=30:scenecut=40" \
  -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -af "loudnorm=I=-11:TP=-1.5:LRA=11" \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -t 30 \
  output_reels.mp4
```

### Bitrate-Controlled Encoding

```bash
# Instagram Reels with precise bitrate (5-10 Mbps range)
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset medium -b:v 8M -maxrate 10M -bufsize 20M \
  -profile:v high -level 4.1 \
  -c:a aac -b:a 192k -ar 44100 \
  -af "loudnorm=I=-11:TP=-1.5:LRA=11" \
  -pix_fmt yuv420p -movflags +faststart \
  output_reels_bitrate.mp4
```

### Algorithm Insights (2025-2026)

- **Optimal Length**: 7-15 seconds for casual, 15-30 for tutorial
- **First 3 Seconds**: Must hook immediately
- **Trending Audio**: Significant boost in reach
- **Hashtags**: 3-5 relevant hashtags optimal
- **Post Time**: When followers most active

---

## Facebook Reels Specifications

### Technical Requirements (2025-2026)

| Specification | Requirement | Notes |
|---------------|-------------|-------|
| **Aspect Ratio** | 9:16 (recommended), any supported | All videos = Reels as of June 2025 |
| **Resolution** | 1440x2560 (official), 1080x1920 (practical) | Facebook recommends higher res |
| **Video Codec** | H.264, H.265, VP9, AV1 | H.264 most compatible |
| **Compression** | H.264, Closed GOP (2-5s) | Progressive scan, 4:2:0 chroma |
| **Audio Codec** | AAC (stereo) | AAC Low Complexity preferred |
| **Audio Bitrate** | 128 kbps minimum, 192k recommended | Facebook supports up to 384k |
| **Audio Sample Rate** | 48000 Hz | 48kHz official recommendation |
| **Audio Loudness** | -13 LUFS | Facebook normalizes to -13 LUFS |
| **True Peak** | -1 dBTP | Prevent distortion |
| **Frame Rate** | 30 fps or higher recommended | Match source frame rate |
| **Pixel Format** | yuv420p | 8-bit color |
| **Max File Size** | 4 GB | Practical: 50-300 MB |
| **Max Duration** | No limit (as of June 2025) | Reels: 3-90 seconds optimal |
| **Optimal Duration** | 15-30 seconds | Engagement sweet spot |
| **Min Duration** | 3 seconds | Reel minimum |

### Optimal Encoding Parameters (2025-2026)

**Bitrate Recommendations**:
- **1080p H.264**: 5-8 Mbps
- **4K H.264**: 35-45 Mbps (up to 45 Mbps supported)
- **Recommended for Reels**: 6-10 Mbps at 1080p

**CRF Values**:
- **CRF 20-22**: High quality
- **CRF 23**: Good balance (recommended)
- **CRF 24+**: Acceptable for casual content

**Safe Zones**:
- **Top**: Leave 14% clear
- **Bottom**: Avoid 35% (UI elements)
- **Sides**: 6% margin each side

### FFmpeg Preset (Updated 2025-2026)

```bash
# Facebook Reels optimized encoding - 2025-2026
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30" \
  -c:v libx264 -preset medium -crf 22 -profile:v high -level 4.1 \
  -x264-params "keyint=60:min-keyint=30:scenecut=40" \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -af "loudnorm=I=-13:TP=-1:LRA=11" \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -t 30 \
  output_fb_reels.mp4
```

### High-Quality Preset (Bitrate-Controlled)

```bash
# Facebook Reels - high quality with bitrate control
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset medium -b:v 8M -maxrate 10M -bufsize 20M \
  -profile:v high -level 4.1 \
  -c:a aac -b:a 192k -ar 48000 -ac 2 \
  -af "loudnorm=I=-13:TP=-1:LRA=11" \
  -pix_fmt yuv420p -movflags +faststart \
  output_fb_reels_hq.mp4
```

### Algorithm Insights (2025-2026)

- **Cross-Post**: Instagram Reels can be shared to Facebook
- **Original Content**: Watermark-free content preferred
- **Engagement**: Comments boost reach significantly
- **Optimal Length**: 15-30 seconds

---

## Snapchat Spotlight Specifications

### Technical Requirements

| Specification | Requirement |
|---------------|-------------|
| **Aspect Ratio** | 9:16 (required) |
| **Resolution** | 1080x1920 |
| **Video Codec** | H.264 |
| **Audio Codec** | AAC |
| **Frame Rate** | 24-30 fps |
| **Pixel Format** | yuv420p |
| **Max File Size** | 300 MB |
| **Max Duration** | 60 seconds |
| **Min Duration** | 5 seconds |

### FFmpeg Preset

```bash
# Snapchat Spotlight optimized encoding
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30" \
  -c:v libx264 -preset fast -crf 24 -profile:v main -level 4.0 \
  -c:a aac -b:a 128k -ar 44100 -ac 2 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -fs 300M \
  -t 60 \
  output_spotlight.mp4
```

---

## Twitter/X Video Specifications

### Technical Requirements

| Specification | Requirement |
|---------------|-------------|
| **Aspect Ratio** | 9:16, 16:9, 1:1 |
| **Resolution** | 1080x1920 (9:16), 1920x1080 (16:9) |
| **Video Codec** | H.264 |
| **Audio Codec** | AAC |
| **Audio Bitrate** | 128 kbps |
| **Audio Sample Rate** | 44100 Hz |
| **Frame Rate** | 30-60 fps (40 max for 1080p) |
| **Pixel Format** | yuv420p |
| **Max File Size** | 512 MB |
| **Max Duration** | 2 min 20 sec (140 seconds) |

### FFmpeg Preset

```bash
# Twitter/X optimized encoding
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps=30" \
  -c:v libx264 -preset fast -crf 23 -profile:v high -level 4.1 \
  -c:a aac -b:a 128k -ar 44100 -ac 2 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -fs 512M \
  -t 140 \
  output_twitter.mp4
```

---

## Multi-Platform Export Script

```bash
#!/bin/bash
# export_all_platforms.sh - Export video for all platforms at once

INPUT="$1"
BASENAME=$(basename "$INPUT" .mp4)

echo "Exporting $INPUT for all platforms..."

# TikTok
ffmpeg -i "$INPUT" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -pix_fmt yuv420p -movflags +faststart \
  -t 60 \
  "${BASENAME}_tiktok.mp4" &

# YouTube Shorts
ffmpeg -i "$INPUT" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -preset fast -crf 22 \
  -c:a aac -b:a 192k -ar 48000 \
  -pix_fmt yuv420p -movflags +faststart \
  -t 59 \
  "${BASENAME}_shorts.mp4" &

# Instagram Reels
ffmpeg -i "$INPUT" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -pix_fmt yuv420p -movflags +faststart \
  -t 90 \
  "${BASENAME}_reels.mp4" &

# Snapchat Spotlight
ffmpeg -i "$INPUT" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset fast -crf 24 \
  -c:a aac -b:a 128k -ar 44100 \
  -pix_fmt yuv420p -movflags +faststart \
  -fs 300M -t 60 \
  "${BASENAME}_spotlight.mp4" &

# Twitter/X
ffmpeg -i "$INPUT" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k -ar 44100 \
  -pix_fmt yuv420p -movflags +faststart \
  -t 140 \
  "${BASENAME}_twitter.mp4" &

wait
echo "All platform exports complete!"
ls -lh "${BASENAME}_*.mp4"
```

---

## File Size Optimization

### Calculate Target Bitrate for File Size

```bash
# Formula: bitrate = (target_size_MB * 8192) / duration_seconds - audio_bitrate

# Example: 50MB file, 60 seconds, 128kbps audio
# Video bitrate = (50 * 8192) / 60 - 128 = 6697 kbps

ffmpeg -i input.mp4 \
  -vf "scale=1080:1920" \
  -c:v libx264 -b:v 6500k -maxrate 7000k -bufsize 14000k \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -movflags +faststart \
  output_sized.mp4
```

### Two-Pass Encoding for Exact Size

```bash
# Pass 1
ffmpeg -y -i input.mp4 \
  -vf "scale=1080:1920" \
  -c:v libx264 -b:v 6500k -pass 1 -an -f null /dev/null

# Pass 2
ffmpeg -i input.mp4 \
  -vf "scale=1080:1920" \
  -c:v libx264 -b:v 6500k -pass 2 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output_2pass.mp4
```

---

## Platform Comparison: Algorithm Factors

| Factor | TikTok | Shorts | Reels | Priority |
|--------|--------|--------|-------|----------|
| **Hook (1-3s)** | Critical | Critical | Critical | #1 |
| **Completion Rate** | High | Highest | High | #1 |
| **Watch Time** | High | Highest | Medium | #2 |
| **Shares** | High | Medium | High | #3 |
| **Comments** | High | Medium | High | #3 |
| **Saves** | Medium | Medium | High | #4 |
| **Likes** | Medium | Low | Medium | #5 |
| **Captions** | 80% boost | Helpful | Important | Must-have |
| **Trending Audio** | Essential | N/A | Important | Platform-specific |
| **Original Content** | Preferred | Required | Preferred | Important |
| **Posting Frequency** | 1-3x/day | Daily | Daily | Consistency |

---

## Verification Commands

```bash
# Verify platform compliance
verify_platform() {
    local file=$1
    echo "=== Checking: $file ==="
    ffprobe -v error -select_streams v:0 \
      -show_entries stream=width,height,codec_name,pix_fmt,r_frame_rate,bit_rate \
      -show_entries format=duration,size,bit_rate \
      -of default=noprint_wrappers=1 "$file"

    # File size in MB
    size_mb=$(ls -l "$file" | awk '{print $5/1024/1024}')
    echo "File Size: ${size_mb}MB"
}

verify_platform output_tiktok.mp4
```

---

## Codec Comparison for Short-Form Video (2025-2026)

### H.264 vs H.265 vs AV1 Decision Matrix

| Codec | Compression | Encoding Speed | Platform Support | Recommendation |
|-------|-------------|----------------|------------------|----------------|
| **H.264** | Baseline | Fast | Universal | **Primary choice** - all platforms transcode to H.264 anyway |
| **H.265** | 40-50% better | 5-10x slower | Limited mobile | Avoid - platforms transcode, licensing issues |
| **AV1** | 50-60% better | 5-10x slower | Growing (YouTube, Netflix) | Future-proof for web, not for social uploads |
| **VP9** | 40% better | Slower | YouTube preferred | Only for YouTube Shorts WebM uploads |

### Platform Codec Recommendations

| Platform | Upload Codec | Platform Transcodes To | Best Practice |
|----------|--------------|------------------------|---------------|
| **TikTok** | H.264 | H.264 | Always H.264 |
| **YouTube Shorts** | H.264 or VP9 | VP9, AV1, H.264 | H.264 for compatibility, VP9 for quality |
| **Instagram** | H.264 | H.264 | H.264 only |
| **Facebook** | H.264 | H.264, VP9 | H.264 most reliable |

**Key Insight**: All platforms re-encode uploads. Upload high-quality H.264 to give platform encoders the best source material. H.265/AV1 add encoding time with no benefit for social media.

---

## Color Grading for Viral Appeal (2025-2026)

### Mobile-Optimized Color Parameters

**Research-backed findings**: Bold, saturated colors perform 2-3x better on mobile screens.

| Parameter | Conservative | Viral-Optimized | Bold/Stylized |
|-----------|--------------|-----------------|---------------|
| **Saturation** | 1.0-1.1 | 1.1-1.2 | 1.3-1.5 |
| **Contrast** | 1.0-1.1 | 1.15-1.25 | 1.3-1.4 |
| **Brightness** | 0 to +0.05 | -0.02 to 0 | -0.05 (cinematic) |
| **Sharpness** | Unsharp 5:5:0.3 | Unsharp 5:5:0.6 | Unsharp 5:5:1.0 |

### Viral Color Grading Presets

#### 1. Bold & Eye-Popping (Maximum Engagement)

```bash
# High saturation, punchy contrast for maximum mobile impact
ffmpeg -i input.mp4 \
  -vf "eq=saturation=1.2:contrast=1.2:brightness=-0.02,unsharp=5:5:0.8" \
  -c:v libx264 -preset medium -crf 22 \
  output_bold.mp4
```

#### 2. Orange & Teal (Cinematic Viral Look)

```bash
# Popular cinematic color grade - orange in highlights, teal in shadows
ffmpeg -i input.mp4 \
  -vf "\
    eq=contrast=1.15:saturation=1.1:brightness=-0.02,\
    colorbalance=rs=0.12:gs=-0.04:bs=-0.15:rm=0.08:gm=-0.02:bm=-0.08:rh=0.08:gh=-0.03:bh=-0.12,\
    curves=all='0/0.02 0.5/0.5 1/0.98',\
    unsharp=5:5:0.6\
  " \
  -c:v libx264 -preset medium -crf 22 \
  output_orange_teal.mp4
```

#### 3. Vibrant Social Media Look

```bash
# Optimized for TikTok/Reels - saturated, sharp, mobile-friendly
ffmpeg -i input.mp4 \
  -vf "\
    eq=saturation=1.25:contrast=1.18:brightness=0.01:gamma=1.05,\
    colorbalance=rs=0.05:bs=-0.05,\
    unsharp=5:5:0.7\
  " \
  -c:v libx264 -preset medium -crf 22 \
  output_vibrant.mp4
```

#### 4. Moody & Dramatic (Storytelling)

```bash
# Lower saturation, higher contrast, lifted blacks
ffmpeg -i input.mp4 \
  -vf "\
    eq=saturation=0.95:contrast=1.25:brightness=-0.03,\
    curves=all='0/0.05 0.5/0.48 1/0.95',\
    colorbalance=bs=0.08:bh=-0.05,\
    unsharp=5:5:0.5\
  " \
  -c:v libx264 -preset medium -crf 22 \
  output_moody.mp4
```

### Using LUTs for Consistent Branding

```bash
# Apply a .cube LUT file for professional color grading
ffmpeg -i input.mp4 \
  -vf "lut3d=file=cinematic.cube,unsharp=5:5:0.6" \
  -c:v libx264 -preset medium -crf 22 \
  output_lut.mp4
```

**Popular LUT sources**:
- CapCut built-in LUTs (export as .cube)
- DaVinci Resolve free LUTs
- RocketStock free LUTs

### Color Grading Best Practices

1. **Test on mobile first**: View on phone before posting
2. **Avoid over-saturation**: >1.3 saturation looks artificial
3. **Check dark scenes**: Compression artifacts most visible in shadows
4. **Platform compression**: Colors shift slightly after upload - compensate with +5% saturation
5. **Consistent branding**: Use same LUT across all videos for recognition

---

## Text & Caption Parameters for Mobile Readability (2025-2026)

### Font Size Guidelines (1080x1920 vertical)

| Content Type | Minimum Size | Recommended Size | Maximum Size |
|--------------|--------------|------------------|--------------|
| **Body text/captions** | 48px | 52-60px | 72px |
| **Titles/hooks** | 64px | 72-80px | 120px |
| **Secondary text** | 36px | 40-48px | 56px |

**Rule of thumb**: For 1080x1920, minimum 48px for readability on all devices.

### Safe Zones for Text Placement

```
┌─────────────────────┐
│   14% TOP MARGIN    │ ← Username, UI elements
├─────────────────────┤
│                     │
│   SAFE TEXT ZONE    │ ← Place all text here
│   (upper 2/3)       │
│                     │
├─────────────────────┤
│                     │
│  35% BOTTOM MARGIN  │ ← Captions, buttons, likes
└─────────────────────┘
    6%         6%
  ← margin  margin →
```

**Best text placement**: Upper-middle area (20-60% from top)

### FFmpeg Text Overlay Parameters

#### Optimal Readability Settings

```bash
# Maximum mobile readability - white text, thick black outline
ffmpeg -i input.mp4 \
  -vf "drawtext=text='YOUR TEXT':fontsize=56:fontcolor=white:borderw=4:bordercolor=black:x=(w-tw)/2:y=h*0.15" \
  -c:v libx264 -preset medium -crf 22 \
  output_text.mp4
```

#### High-Contrast Combinations (Best Performing)

| Text Color | Outline Color | Background | Readability Score |
|------------|---------------|------------|-------------------|
| White | Black (4px) | Any | 95% |
| Yellow | Black (4px) | Dark | 93% |
| Black | White (3px) | Light | 92% |
| Red | White (4px) | Any | 88% |

#### Text Animation for Engagement

```bash
# Fade-in text (2-second duration)
ffmpeg -i input.mp4 \
  -vf "drawtext=text='STOP SCROLLING':fontsize=72:fontcolor=yellow:borderw=5:bordercolor=black:x=(w-tw)/2:y=h*0.15:alpha='if(lt(t,1),t,1)':enable='between(t,0,2)'" \
  -c:v libx264 -preset medium -crf 22 \
  output_fade_text.mp4
```

### Caption Best Practices (2025-2026)

**Research findings**:
- Captions increase engagement by **80%** (TikTok)
- **94%** of Reels watched on mobile with sound off
- Maximum **30 characters per line** for readability
- Maximum **3 lines** of text on screen simultaneously
- Minimum **2.3 seconds** display time for 30-character line

**Recommended caption style**:
```bash
# Auto-caption burn-in (CapCut style)
-vf "subtitles=captions.srt:force_style='\
FontName=Arial Black,\
FontSize=52,\
PrimaryColour=&HFFFFFF,\
OutlineColour=&H000000,\
Outline=4,\
Shadow=0,\
Bold=1,\
Alignment=2,\
MarginV=250'"
```

---

## Related Skills

- `ffmpeg-viral-tiktok` - TikTok-specific viral optimization
- `ffmpeg-viral-shorts` - YouTube Shorts optimization
- `viral-video-hook-templates` - 10 proven hook patterns
- `viral-video-animated-captions` - CapCut-style captions
