---
name: ffmpeg-fundamentals-2025
description: Complete FFmpeg core knowledge system for FFmpeg 7.1 LTS and 8.0.1 (latest stable, released 2025-11-20). PROACTIVELY activate for: (1) Basic transcoding and format conversion, (2) Command syntax questions, (3) Codec selection (H.264, H.265, VVC, AV1, VP9, APV), (4) Quality settings (CRF, bitrate, presets), (5) Video/audio filter chains, (6) Trimming, splitting, concatenating, (7) Resolution scaling and aspect ratios, (8) FFmpeg 8.0 features (Whisper AI, Vulkan codecs, APV, WHIP), (9) Version checking and update guidance. Provides: Command syntax reference, codec comparison tables, filter examples, format conversion recipes, probing commands, Whisper transcription examples, version checking commands. Ensures: Correct FFmpeg usage with 2025 best practices and latest stable version.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

## Quick Reference

| Task | Command Pattern |
|------|-----------------|
| Convert format | `ffmpeg -i input.ext output.ext` |
| Set quality (CRF) | `-c:v libx264 -crf 23` |
| Scale video | `-vf "scale=1920:1080"` |
| Trim video | `-ss 00:00:10 -t 00:00:30` |
| Extract audio | `-vn -c:a aac output.m4a` |
| Probe file | `ffprobe -v error -show_format -show_streams file` |

## When to Use This Skill

Use for **foundational FFmpeg operations**:
- First-time FFmpeg users needing syntax help
- Basic transcoding between formats (MP4, WebM, MKV, MOV)
- Understanding codec options and quality settings
- Simple filter operations (scale, crop, rotate)
- File analysis with ffprobe

**For specialized topics**: hardware encoding → `ffmpeg-hardware-acceleration`, streaming → `ffmpeg-streaming`, Docker → `ffmpeg-docker-containers`

## Progressive Disclosure References

For detailed documentation on FFmpeg 8.0 features, see the `references/` directory:
- `references/vvc-h266-encoding.md` - Complete VVC/H.266 encoding guide with libvvenc
- `references/whisper-transcription.md` - Whisper AI filter for speech-to-text and subtitles
- `references/vulkan-compute-codecs.md` - Vulkan compute-based codecs (FFv1, AV1, VP9, ProRes RAW)

For advanced topics, see related skills:
- `ffmpeg-filter-complex-patterns` - Multi-input compositions, transitions, audio mixing, GPU filtergraphs
- `ffmpeg-hardware-acceleration` - GPU encoding/decoding, CUDA filters, multi-GPU setups

---

# FFmpeg Fundamentals (2025)

Complete guide to FFmpeg core concepts, syntax, and essential operations with FFmpeg 7.1 LTS and 8.0.1 (latest stable).

## FFmpeg Version Overview

**IMPORTANT: Always verify you are using the latest FFmpeg version for security and bug fixes.**

### Checking Your Version
```bash
# Check installed version
ffmpeg -version

# Check build configuration
ffmpeg -buildconf
```

### Official Sources for Latest Version
- **Official Download Page**: https://ffmpeg.org/download.html
- **Official Git Repository**: https://git.ffmpeg.org/gitweb/ffmpeg.git
- **GitHub Releases**: https://github.com/FFmpeg/FFmpeg/releases

### FFmpeg 8.0.1 (Released 2025-11-20) - Current Latest Stable
The latest stable release from the 8.0 "Huffman" branch (originally cut from master on 2025-08-09). This patch release contains important bug fixes and security updates.

FFmpeg 8.0 is one of the largest releases to date, named after the Huffman code algorithm invented in 1952.

**AI and Transcription:**
- **Whisper AI Filter**: Built-in speech recognition via whisper.cpp for live subtitle generation and transcription
- Supports 99 languages with automatic language detection
- Outputs to SRT, JSON, or plain text formats
- Voice Activity Detection (VAD) support with Silero VAD

**Vulkan Compute Codecs (Cross-Platform GPU):**
- **FFv1 Vulkan**: Encode and decode via Vulkan 1.3 compute shaders
- **ProRes RAW Vulkan**: Hardware-accelerated decode
- **AV1 Vulkan Encoder**: GPU-accelerated AV1 encoding
- **VP9 Vulkan Decoder**: Hardware-accelerated VP9 decode
- Works on any Vulkan 1.3 implementation (AMD, Intel, NVIDIA)

**New Codecs:**
- **APV Codec**: Samsung Advanced Professional Video encoder (via libopenapv) and native decoder
- **ProRes RAW Decoder**: Native Apple ProRes RAW decode
- **RealVideo 6.0 Decoder**: Native RV6 decode support
- **G.728 Decoder**: Low-delay CELP audio codec
- **Sanyo LD-ADPCM Decoder**: Sanyo audio format
- **ADPCM IMA Xbox Decoder**: Xbox audio format
- **libx265 Alpha Layer Encoding**: HEVC with alpha channel

**Hardware Acceleration:**
- **VVC VA-API Decoding**: H.266/VVC hardware decode on Intel/AMD Linux
- **VVC QSV Decoding**: Intel Quick Sync VVC hardware decode
- **OpenHarmony Support**: H.264/H.265 encode/decode for HarmonyOS platform

**New Features:**
- **WHIP Muxer**: Sub-second latency WebRTC ingestion
- **Animated JPEG XL Encoding**: Via libjxl library
- **FLV v2 Support**: Multitrack audio/video and modern codecs
- **VVC in Matroska**: H.266/VVC support in MKV container
- **VVC SCC Support**: Screen Content Coding with IBC, Palette Mode, ACT
- **TLS Verification**: Enabled by default for HTTPS connections

**New Filters:**
- **whisper**: AI speech recognition filter
- **colordetect**: Detect JPEG/MPEG range and alpha channel properties
- **pad_cuda**: GPU-accelerated padding filter
- **scale_d3d11**: Direct3D 11 hardware scaling filter

**Breaking Changes:**
- **Dropped**: OpenSSL 1.1.0 support (requires 1.1.1+)
- **Dropped**: yasm assembler support (use nasm instead)
- **Deprecated**: OpenMAX encoders
- **Changed**: Default PNG prediction method set to PAETH
- **Changed**: GCC autovectorization no longer disabled on x86/ARM/AArch64

**Infrastructure:**
- New Forgejo-based code hosting at code.ffmpeg.org
- Modernized mailing list infrastructure

### FFmpeg 7.1 "Péter" LTS (September 2024)
- **VVC Decoder Stable**: Full native H.266/VVC decoder (production-ready)
- **MV-HEVC Decoder**: 3D HEVC for Apple Vision Pro / iPhone spatial video
- **LC-EVC Decoder**: MPEG-5 Part 2 enhancement layer
- **xHE-AAC Decoder**: Extended High Efficiency AAC
- **Vulkan H.264/H.265 Encoders**: GPU encoding via Vulkan Video
- **Native Intel QSV VVC Decoder**: Hardware-accelerated VVC
- **AVX2 VVC Optimizations**: Faster software VVC decoding
- **Full-Range Color Fixes**: Correct color range handling throughout pipeline

## Basic Command Syntax

```bash
ffmpeg [global_options] {[input_options] -i input} ... {[output_options] output} ...
```

### Essential Options

```bash
# Basic transcode
ffmpeg -i input.mp4 output.mkv

# Specify codecs
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4

# Copy streams without re-encoding (remux)
ffmpeg -i input.mkv -c copy output.mp4

# Set quality (CRF mode)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# Set bitrate
ffmpeg -i input.mp4 -c:v libx264 -b:v 5M output.mp4

# Overwrite output without asking
ffmpeg -y -i input.mp4 output.mp4

# Show progress/stats
ffmpeg -progress - -i input.mp4 output.mp4
```

## Codec Reference (2025)

### Video Codecs

| Codec | Encoder | Use Case | Quality | Speed |
|-------|---------|----------|---------|-------|
| H.264/AVC | libx264 | Universal compatibility | Excellent | Medium |
| H.265/HEVC | libx265 | 4K, HDR, storage efficiency | Excellent | Slow |
| H.266/VVC | libvvenc | Next-gen, 8K | Best | Very Slow |
| AV1 | libsvtav1, libaom-av1 | Web streaming, royalty-free | Excellent | Slow-Medium |
| VP9 | libvpx-vp9 | WebM, YouTube | Very Good | Slow |
| ProRes | prores_ks | Professional editing | Lossless | Fast |

### Hardware Encoders

| Platform | H.264 | H.265 | AV1 | VVC | FFv1 |
|----------|-------|-------|-----|-----|------|
| NVIDIA | h264_nvenc | hevc_nvenc | av1_nvenc | - | - |
| Intel | h264_qsv | hevc_qsv | av1_qsv | - | - |
| AMD | h264_amf | hevc_amf | av1_amf | - | - |
| Apple | h264_videotoolbox | hevc_videotoolbox | - | - | - |
| Vulkan | h264_vulkan | hevc_vulkan | av1_vulkan (8.0+) | - | ffv1_vulkan (8.0+) |

### Hardware Decoders (FFmpeg 8.0+)

| Platform | VVC/H.266 | VP9 | ProRes RAW |
|----------|-----------|-----|------------|
| VAAPI | vvc (8.0+) | Yes | - |
| QSV | vvc_qsv (7.1+) | Yes | - |
| Vulkan | - | vp9 (8.0+) | Yes (8.0+) |

### Audio Codecs

| Codec | Encoder | Use Case | Bitrate Range |
|-------|---------|----------|---------------|
| AAC | aac, libfdk_aac | Universal, streaming | 96-320 kbps |
| MP3 | libmp3lame | Legacy compatibility | 128-320 kbps |
| Opus | libopus | VoIP, streaming, WebM | 32-256 kbps |
| FLAC | flac | Lossless archival | ~900 kbps |
| AC3 | ac3 | DVD, Blu-ray | 384-640 kbps |
| EAC3 | eac3 | Streaming, Dolby Digital+ | 192-768 kbps |

## Common Operations

### Format Conversion

```bash
# MP4 to WebM
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# MKV to MP4 (no re-encoding)
ffmpeg -i input.mkv -c copy output.mp4

# AVI to MP4 with H.265
ffmpeg -i input.avi -c:v libx265 -crf 28 -c:a aac output.mp4

# GIF to MP4
ffmpeg -i input.gif -movflags +faststart -pix_fmt yuv420p output.mp4

# MP4 to GIF (optimized)
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

### Resolution & Scaling

```bash
# Scale to 1080p (maintain aspect ratio)
ffmpeg -i input.mp4 -vf "scale=1920:-2" output.mp4

# Scale to 720p
ffmpeg -i input.mp4 -vf "scale=-2:720" output.mp4

# Scale to fit within bounds
ffmpeg -i input.mp4 -vf "scale='min(1920,iw)':'min(1080,ih)':force_original_aspect_ratio=decrease" output.mp4

# Scale with padding (letterbox)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

### Trimming & Splitting

```bash
# Extract segment (fast seek)
ffmpeg -ss 00:01:00 -i input.mp4 -t 00:00:30 -c copy output.mp4

# Extract from timestamp to end
ffmpeg -ss 00:05:00 -i input.mp4 -c copy output.mp4

# Extract first 10 seconds
ffmpeg -i input.mp4 -t 10 -c copy output.mp4

# Split into segments
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 60 -f segment output_%03d.mp4

# Accurate trim (re-encode)
ffmpeg -i input.mp4 -ss 00:01:00 -t 00:00:30 -c:v libx264 -c:a aac output.mp4
```

### Concatenation

```bash
# Create file list
echo "file 'part1.mp4'" > list.txt
echo "file 'part2.mp4'" >> list.txt
echo "file 'part3.mp4'" >> list.txt

# Concatenate (same codecs)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concatenate with re-encoding
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

### Audio Operations

```bash
# Extract audio
ffmpeg -i input.mp4 -vn -c:a copy output.aac
ffmpeg -i input.mp4 -vn -c:a libmp3lame -b:a 320k output.mp3

# Replace audio
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# Add audio to video
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest output.mp4

# Remove audio
ffmpeg -i input.mp4 -an -c:v copy output.mp4

# Adjust volume
ffmpeg -i input.mp4 -af "volume=1.5" output.mp4
ffmpeg -i input.mp4 -af "volume=6dB" output.mp4

# Normalize audio (EBU R128)
ffmpeg -i input.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11 output.mp4
```

### Subtitles

```bash
# Burn subtitles (hardcode)
ffmpeg -i input.mp4 -vf "subtitles=subs.srt" output.mp4

# Add subtitle track
ffmpeg -i input.mp4 -i subs.srt -c copy -c:s mov_text output.mp4

# Extract subtitles
ffmpeg -i input.mkv -map 0:s:0 output.srt
```

### Whisper AI Transcription (FFmpeg 8.0+)

```bash
# Generate SRT subtitles from video using Whisper
ffmpeg -i input.mp4 -vn \
  -af "whisper=model=ggml-base.bin:language=auto:queue=3:destination=output.srt:format=srt" \
  -f null -

# Live transcription from microphone
ffmpeg -loglevel warning -f pulse -i default \
  -af "highpass=f=200,lowpass=f=3000,whisper=model=ggml-medium-q5_0.bin:language=en:queue=10:destination=-:format=json:vad_model=for-tests-silero-v5.1.2-ggml.bin" \
  -f null -

# Display live subtitles on video (reads from frame metadata)
ffmpeg -i input.mp4 \
  -af "whisper=model=ggml-base.en.bin:language=en" \
  -vf "drawtext=text='%{metadata\:lavfi.whisper.text}':fontsize=24:fontcolor=white:x=10:y=h-th-10" \
  output_with_subtitles.mp4
```

**Whisper Model Sizes:**
| Model | Size | Speed | Quality | VRAM |
|-------|------|-------|---------|------|
| tiny | 39 MB | Fastest | Basic | ~1 GB |
| base | 74 MB | Fast | Good | ~1 GB |
| small | 244 MB | Medium | Better | ~2 GB |
| medium | 769 MB | Slow | High | ~5 GB |
| large | 1.55 GB | Slowest | Best | ~10 GB |

**Whisper Filter Parameters:**
- `model`: Path to GGML model file
- `language`: Language code or "auto" for detection
- `format`: Output format - "text", "srt", or "json"
- `destination`: Output file path (or "-" for stdout)
- `queue`: Buffer size (increase for VAD, e.g., 20)
- `vad_model`: Path to Silero VAD model for voice detection
- `use_gpu`: Set to "false" to disable GPU acceleration

### Image Operations

```bash
# Video to images
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.png

# Images to video
ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4

# Extract single frame
ffmpeg -ss 00:00:10 -i input.mp4 -vframes 1 thumbnail.jpg

# Create video from single image
ffmpeg -loop 1 -i image.jpg -c:v libx264 -t 10 -pix_fmt yuv420p output.mp4
```

## Filter Essentials

### Video Filters (-vf)

```bash
# Chain multiple filters
ffmpeg -i input.mp4 -vf "scale=1280:720,fps=30,format=yuv420p" output.mp4

# Crop
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4

# Rotate
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4  # 90° clockwise
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4  # 90° counter-clockwise
ffmpeg -i input.mp4 -vf "hflip" output.mp4        # Horizontal flip
ffmpeg -i input.mp4 -vf "vflip" output.mp4        # Vertical flip

# Overlay/Watermark
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# Text overlay
ffmpeg -i input.mp4 -vf "drawtext=text='Hello World':x=10:y=10:fontsize=24:fontcolor=white" output.mp4

# Fade in/out
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" output.mp4

# Speed up/slow down
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" output.mp4  # 2x speed
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" -af "atempo=0.5" output.mp4  # 0.5x speed

# Deinterlace
ffmpeg -i input.mp4 -vf "yadif" output.mp4

# Denoise
ffmpeg -i input.mp4 -vf "nlmeans" output.mp4
ffmpeg -i input.mp4 -vf "hqdn3d" output.mp4

# Sharpen
ffmpeg -i input.mp4 -vf "unsharp=5:5:1.0:5:5:0.0" output.mp4

# Color correction
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3" output.mp4
```

### Audio Filters (-af)

```bash
# Multiple audio filters
ffmpeg -i input.mp4 -af "volume=1.5,highpass=f=200,lowpass=f=3000" output.mp4

# Noise reduction
ffmpeg -i input.mp4 -af "afftdn=nf=-25" output.mp4

# Compressor/limiter
ffmpeg -i input.mp4 -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50" output.mp4

# Equalizer
ffmpeg -i input.mp4 -af "equalizer=f=1000:width_type=h:width=200:g=-10" output.mp4

# Fade audio
ffmpeg -i input.mp4 -af "afade=t=in:ss=0:d=3,afade=t=out:st=57:d=3" output.mp4

# Channel remix (stereo to mono)
ffmpeg -i input.mp4 -af "pan=mono|c0=0.5*c0+0.5*c1" output.mp4
```

### Complex Filtergraphs

```bash
# Picture-in-picture
ffmpeg -i main.mp4 -i pip.mp4 -filter_complex "[1:v]scale=320:240[pip];[0:v][pip]overlay=W-w-10:H-h-10" output.mp4

# Side by side
ffmpeg -i left.mp4 -i right.mp4 -filter_complex "[0:v]pad=iw*2:ih[bg];[bg][1:v]overlay=W/2:0" output.mp4

# Grid layout (2x2)
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 -filter_complex \
  "[0:v]scale=640:360[v0];[1:v]scale=640:360[v1];[2:v]scale=640:360[v2];[3:v]scale=640:360[v3];\
   [v0][v1]hstack[top];[v2][v3]hstack[bottom];[top][bottom]vstack" output.mp4
```

### filter_complex Quick Reference

**Syntax Components:**

| Component | Description | Example |
|-----------|-------------|---------|
| `[0:v]` | First input video | `[0:v]scale=1280:720` |
| `[1:a]` | Second input audio | `[0:a][1:a]amix` |
| `[label]` | Custom named label | `[scaled]`, `[mixed]` |
| `,` | Chain filters | `scale,fps,format` |
| `;` | Separate chains | `chain1;chain2` |
| `-map "[label]"` | Output specific label | `-map "[out]"` |

**Common Patterns:**

```bash
# Video transition (xfade)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=1:offset=4[v]" \
  -map "[v]" output.mp4

# Audio mixing
ffmpeg -i video.mp4 -i music.mp3 -filter_complex \
  "[0:a]volume=1.0[v0];[1:a]volume=0.3[v1];[v0][v1]amix=inputs=2[a]" \
  -map 0:v -map "[a]" output.mp4

# Multi-output (ABR ladder)
ffmpeg -i input.mp4 -filter_complex \
  "[0:v]split=2[v1][v2];[v1]scale=1920:1080[hd];[v2]scale=1280:720[sd]" \
  -map "[hd]" hd.mp4 -map "[sd]" sd.mp4
```

**For comprehensive filter_complex patterns**: See `ffmpeg-filter-complex-patterns` skill for PiP, grids, transitions, audio mixing, and GPU-accelerated filtergraphs.

## Frame Manipulation

### Frame Rate Conversion

```bash
# Change frame rate (drop/duplicate frames)
ffmpeg -i input.mp4 -vf "fps=30" output.mp4
ffmpeg -i input.mp4 -vf "fps=24000/1001" output.mp4  # 23.976 fps

# Motion-interpolated frame rate conversion (smoother)
ffmpeg -i input.mp4 -vf "framerate=fps=60" output.mp4

# High-quality motion interpolation (minterpolate)
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" output.mp4

# Simple motion interpolation (faster)
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:mi_mode=blend" output.mp4
```

**minterpolate Modes:**
| mi_mode | Description | Speed | Quality |
|---------|-------------|-------|---------|
| `dup` | Duplicate frames | Fastest | Lowest |
| `blend` | Blend adjacent frames | Fast | Medium |
| `mci` | Motion-compensated interpolation | Slow | Best |

### Timestamp Manipulation (setpts)

```bash
# Speed up 2x (halve timestamps)
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" output.mp4

# Slow down 2x (double timestamps)
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" output.mp4

# Start from timestamp 0 (reset PTS)
ffmpeg -i input.mp4 -vf "setpts=PTS-STARTPTS" output.mp4

# Time-lapse: keep every 10th frame, at 30fps output
ffmpeg -i input.mp4 -vf "select='not(mod(n,10))',setpts=N/30/TB" output.mp4

# Variable speed (accelerate over time)
ffmpeg -i input.mp4 -vf "setpts='PTS/(1+0.001*N)'" output.mp4
```

**setpts Variables:**
| Variable | Description |
|----------|-------------|
| `PTS` | Input presentation timestamp |
| `N` | Frame count (starting at 0) |
| `PREV_PTS` | Previous frame timestamp |
| `TB` | Timebase |
| `STARTPTS` | First frame timestamp |
| `RTCSTART` | Real-time clock start |

### Frame Selection (select)

```bash
# Select every 5th frame
ffmpeg -i input.mp4 -vf "select='not(mod(n,5))',setpts=N/FRAME_RATE/TB" output.mp4

# Select I-frames only (keyframes)
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)',setpts=N/FRAME_RATE/TB" keyframes.mp4

# Select frames with scene change
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)',setpts=N/FRAME_RATE/TB" scenes.mp4

# Select frames based on time range
ffmpeg -i input.mp4 -vf "select='between(t,5,10)',setpts=N/FRAME_RATE/TB" output.mp4

# Select frames by expression (dark frames)
ffmpeg -i input.mp4 -vf "select='lt(avg(scene),0.1)'" output.mp4
```

**select Expressions:**
| Expression | Description |
|------------|-------------|
| `n` | Frame number |
| `t` | Timestamp (seconds) |
| `pict_type` | Picture type (I, P, B) |
| `scene` | Scene change score |
| `key` | 1 for keyframes |
| `interlace_type` | Interlace type |

### Thumbnail Generation

```bash
# Generate thumbnail from best frame
ffmpeg -i input.mp4 -vf "thumbnail" -frames:v 1 thumbnail.jpg

# Thumbnail with custom frames to analyze
ffmpeg -i input.mp4 -vf "thumbnail=n=100" -frames:v 1 thumbnail.jpg

# Generate multiple thumbnails (every 10 seconds)
ffmpeg -i input.mp4 -vf "fps=1/10,thumbnail=n=1" thumb_%04d.jpg

# Thumbnail at specific time
ffmpeg -ss 00:00:30 -i input.mp4 -vframes 1 thumbnail.jpg
```

### Tile / Contact Sheet

```bash
# Create 4x4 tile mosaic
ffmpeg -i input.mp4 -vf "fps=1/5,scale=320:180,tile=4x4" -frames:v 1 contact_sheet.jpg

# Create tile with padding
ffmpeg -i input.mp4 -vf "fps=1/10,scale=256:144,tile=5x4:margin=5:padding=5" contact.png

# Video tile mosaic (animated)
ffmpeg -i input.mp4 -vf "scale=320:180,tile=2x2" tiled.mp4
```

**tile Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `layout` | Grid dimensions | `4x4` |
| `margin` | Outer margin | `10` |
| `padding` | Inter-tile padding | `5` |
| `color` | Background color | `black` |

### Frame Freezing

```bash
# Freeze first frame for 3 seconds, then play
ffmpeg -i input.mp4 -vf "tpad=start_mode=clone:start_duration=3" output.mp4

# Freeze last frame for 3 seconds
ffmpeg -i input.mp4 -vf "tpad=stop_mode=clone:stop_duration=3" output.mp4

# Add black frames at start
ffmpeg -i input.mp4 -vf "tpad=start=90:color=black" output.mp4

# Freeze specific frame range (frames 100-150)
ffmpeg -i input.mp4 -vf "freezeframes=first=100:last=150:replace=100" output.mp4
```

### Loop and Reverse

```bash
# Loop video 3 times
ffmpeg -stream_loop 3 -i input.mp4 -c copy output.mp4

# Loop filter (within filter graph)
ffmpeg -i input.mp4 -vf "loop=loop=3:size=30:start=0" output.mp4

# Reverse video
ffmpeg -i input.mp4 -vf "reverse" reversed.mp4

# Reverse audio too
ffmpeg -i input.mp4 -vf "reverse" -af "areverse" reversed.mp4

# Boomerang effect (forward then reverse)
ffmpeg -i input.mp4 -filter_complex "[0:v]split[v1][v2];[v2]reverse[r];[v1][r]concat=n=2:v=1:a=0" boomerang.mp4
```

### Frame Extraction Patterns

```bash
# Extract all frames
ffmpeg -i input.mp4 frames/frame_%05d.png

# Extract at specific FPS
ffmpeg -i input.mp4 -vf "fps=1" frames/frame_%04d.jpg

# Extract keyframes only
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr keyframe_%04d.png

# Extract frames with timestamp filename
ffmpeg -i input.mp4 -vf "fps=1" -frame_pts 1 "frame_%d.jpg"
```

## Probing & Analysis

```bash
# Get media info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Get duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4

# Get resolution
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input.mp4

# Get codec
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 input.mp4

# Check if file is valid
ffprobe -v error input.mp4 && echo "Valid" || echo "Invalid"
```

## Output Optimization

### Web Delivery

```bash
# MP4 for web (faststart)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k -movflags +faststart output.mp4

# WebM for web
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus -b:a 128k output.webm
```

### iOS/Apple Compatibility

```bash
# H.265 with hvc1 tag (required for Apple)
ffmpeg -i input.mp4 -c:v libx265 -vtag hvc1 -c:a aac output.mp4

# Baseline profile for older iOS
ffmpeg -i input.mp4 -c:v libx264 -profile:v baseline -level 3.0 -c:a aac output.mp4
```

### Android Compatibility

```bash
# Widely compatible H.264
ffmpeg -i input.mp4 -c:v libx264 -profile:v main -level 4.0 -c:a aac output.mp4
```

## Best Practices

### Performance
1. Use `-threads 0` to auto-detect optimal thread count
2. Place `-ss` before `-i` for fast seeking (may be less accurate)
3. Use `-c copy` when possible to avoid re-encoding
4. Use hardware acceleration when available

### Quality
1. Prefer CRF over bitrate for single-pass encoding
2. Use `-preset slow` or slower for better compression
3. Use `-tune` options (film, animation, grain) when appropriate
4. Maintain pixel format: `-pix_fmt yuv420p` for compatibility

### Compatibility
1. Use `-movflags +faststart` for web MP4 files
2. Use `-vtag hvc1` for HEVC on Apple devices
3. Test on target devices before mass conversion
4. Consider fallback formats for older browsers

### Error Prevention
1. Always test commands on a sample file first
2. Use `-report` for detailed logging
3. Check output file size and duration
4. Verify audio/video sync on converted files

## Quick Reference

### Get FFmpeg Capabilities
```bash
ffmpeg -encoders          # List all encoders
ffmpeg -decoders          # List all decoders
ffmpeg -formats           # List all formats
ffmpeg -filters           # List all filters
ffmpeg -hwaccels          # List hardware acceleration methods
ffmpeg -h encoder=libx264 # Get encoder options
```

### Common Exit Codes
- 0: Success
- 1: Error (check stderr for details)
- 255: Interrupted (Ctrl+C)

## Staying Up-to-Date

### Why Version Matters
- **Security fixes**: Patch releases address vulnerabilities
- **Bug fixes**: Issues with specific codecs or filters get resolved
- **New features**: Major versions add codec support and filters
- **Performance**: Optimizations improve encoding speed

### Recommended Update Strategy
1. **Production**: Use LTS releases (7.1) for stability, apply patch updates
2. **Development**: Use latest stable (8.0.1) for new features
3. **Always**: Check release notes before upgrading

### Official Resources
- **Release Notes**: https://ffmpeg.org/download.html
- **Security Advisories**: https://ffmpeg.org/security.html
- **Mailing Lists**: https://ffmpeg.org/contact.html

This guide covers FFmpeg fundamentals for 2025. For hardware acceleration, streaming, containers, and advanced topics, see the specialized skill documents.
