---
name: ffmpeg-deinterlacing-telecine
description: Complete FFmpeg deinterlacing, field processing, and telecine removal for broadcast and professional video. PROACTIVELY activate for: (1) Deinterlacing interlaced video (yadif, bwdif, w3fdif), (2) Hardware-accelerated deinterlacing (yadif_cuda, bwdif_cuda, bwdif_vulkan), (3) Inverse telecine/pulldown removal (pullup, fieldmatch), (4) Field order correction (fieldorder), (5) Field separation/weaving (separatefields, weave, tinterlace), (6) Interlace detection (idet), (7) DVD/Blu-ray processing, (8) Broadcast content conversion. Provides: Deinterlacing filters, telecine removal, field processing, hardware acceleration options.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Task | Filter | Command Pattern |
|------|--------|-----------------|
| Basic deinterlace | `yadif` | `-vf yadif` |
| High quality deinterlace | `bwdif` | `-vf bwdif` |
| CUDA deinterlace | `yadif_cuda` | `-vf yadif_cuda` |
| Inverse telecine | `pullup` | `-vf pullup` |
| Field order | `fieldorder` | `-vf fieldorder=tff` |
| Detect interlace | `idet` | `-vf idet` |

## When to Use This Skill

Use for **interlaced and telecined content**:
- Converting broadcast/TV content to progressive
- DVD and Blu-ray processing
- Legacy video digitization
- Professional video production
- Field order correction
- Telecine removal (3:2 pulldown)

---

# FFmpeg Deinterlacing & Telecine (2025)

Comprehensive guide to deinterlacing, field processing, and telecine removal.

## Understanding Interlaced Video

### What is Interlacing?

Interlaced video stores two half-resolution fields per frame:
- **Top Field (TFF)**: Odd lines (1, 3, 5, ...)
- **Bottom Field (BFF)**: Even lines (2, 4, 6, ...)

Common interlaced formats:
- 1080i (1920x1080, 50i or 60i)
- 576i (720x576, 50i - PAL)
- 480i (720x480, 60i - NTSC)

### Detecting Interlaced Content

```bash
# Use idet filter to detect interlacing
ffmpeg -i input.mp4 -vf "idet" -frames:v 500 -f null -

# Output shows field types:
# TFF = Top Field First
# BFF = Bottom Field First
# Progressive = Not interlaced
# Undetermined = Mixed or uncertain
```

---

## Deinterlacing Filters

### yadif - Yet Another DeInterlacing Filter

The most widely used deinterlacing filter. Good balance of speed and quality.

```bash
# Basic deinterlacing (output same frame rate)
ffmpeg -i interlaced.mp4 -vf "yadif" output.mp4

# Double frame rate (output both fields as frames)
ffmpeg -i interlaced.mp4 -vf "yadif=1" output.mp4

# Specify field parity (auto-detect by default)
ffmpeg -i interlaced.mp4 -vf "yadif=0:0:0" output.mp4  # TFF
ffmpeg -i interlaced.mp4 -vf "yadif=0:1:0" output.mp4  # BFF

# Only deinterlace if detected as interlaced
ffmpeg -i input.mp4 -vf "yadif=deint=interlaced" output.mp4
```

**Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `mode` | Output mode | 0=same fps, 1=double fps |
| `parity` | Field parity | -1=auto, 0=TFF, 1=BFF |
| `deint` | Frames to deinterlace | 0=all, 1=interlaced only |

**Mode options:**
- `0` / `send_frame` - Output one frame per input frame
- `1` / `send_field` - Output one frame per field (double fps)
- `2` / `send_frame_nospatial` - Like 0, without spatial interlacing check
- `3` / `send_field_nospatial` - Like 1, without spatial interlacing check

### bwdif - Bob Weaver Deinterlacing Filter

Higher quality than yadif, uses more frames for interpolation.

```bash
# Basic bwdif
ffmpeg -i interlaced.mp4 -vf "bwdif" output.mp4

# Double frame rate
ffmpeg -i interlaced.mp4 -vf "bwdif=1" output.mp4

# Specify parity
ffmpeg -i interlaced.mp4 -vf "bwdif=0:-1:1" output.mp4
```

**Parameters:** Same as yadif

### w3fdif - Martin Weston 3-Field Deinterlacing

Uses three fields for even higher quality interpolation.

```bash
# Simple filter (faster)
ffmpeg -i interlaced.mp4 -vf "w3fdif=filter=simple" output.mp4

# Complex filter (better quality)
ffmpeg -i interlaced.mp4 -vf "w3fdif=filter=complex" output.mp4
```

**Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `filter` | Filter coefficients | simple, complex |
| `deint` | Frames to deinterlace | all, interlaced |

### kerndeint - Kernel Deinterlacing

Adaptive kernel-based deinterlacing.

```bash
# Basic kerndeint
ffmpeg -i interlaced.mp4 -vf "kerndeint" output.mp4

# With threshold adjustment
ffmpeg -i interlaced.mp4 -vf "kerndeint=thresh=10:map=0:order=0:sharp=0:twoway=0" output.mp4
```

---

## Hardware-Accelerated Deinterlacing

### yadif_cuda - NVIDIA CUDA

```bash
# Full GPU pipeline with CUDA deinterlacing
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i interlaced.mp4 \
  -vf "yadif_cuda=0:-1:0" \
  -c:v h264_nvenc output.mp4

# Double framerate with CUDA
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i interlaced.mp4 \
  -vf "yadif_cuda=1" \
  -c:v h264_nvenc output.mp4
```

### bwdif_cuda - NVIDIA CUDA (FFmpeg 7.0+)

```bash
# Higher quality CUDA deinterlacing
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i interlaced.mp4 \
  -vf "bwdif_cuda" \
  -c:v h264_nvenc output.mp4
```

### bwdif_vulkan - Vulkan (FFmpeg 8.0+)

Cross-platform GPU deinterlacing.

```bash
# Vulkan deinterlacing (works on AMD, Intel, NVIDIA)
ffmpeg -init_hw_device vulkan \
  -hwaccel vulkan -hwaccel_output_format vulkan \
  -i interlaced.mp4 \
  -vf "bwdif_vulkan" \
  -c:v h264_vulkan output.mp4
```

### deinterlace_vaapi - VAAPI (Linux)

```bash
# VAAPI deinterlacing
ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 \
  -hwaccel_output_format vaapi \
  -i interlaced.mp4 \
  -vf "deinterlace_vaapi" \
  -c:v h264_vaapi output.mp4

# Specify deinterlace mode
ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 \
  -hwaccel_output_format vaapi \
  -i interlaced.mp4 \
  -vf "deinterlace_vaapi=mode=motion_adaptive:rate=frame" \
  -c:v h264_vaapi output.mp4
```

**VAAPI deinterlace modes:**
- `default` - Use driver default
- `bob` - Simple bob (double rate)
- `weave` - Weave fields together
- `motion_adaptive` - Motion-adaptive (best quality)
- `motion_compensated` - Motion-compensated (highest quality)

### deinterlace_qsv - Intel QSV

```bash
# QSV deinterlacing
ffmpeg -hwaccel qsv -hwaccel_output_format qsv \
  -i interlaced.mp4 \
  -vf "vpp_qsv=deinterlace=2" \
  -c:v h264_qsv output.mp4
```

**VPP_QSV deinterlace modes:**
- `0` - Off
- `1` - Bob
- `2` - Advanced (motion adaptive)

---

## Inverse Telecine (IVTC)

### Understanding Telecine (3:2 Pulldown)

Telecine converts 24fps film to 30fps video by duplicating fields:
```
Film:   A  B  C  D
Video:  AA AB BB BC CC CD DD DA
```

### pullup - Pullup Filter

Removes 3:2 telecine by detecting and removing duplicate fields.

```bash
# Basic IVTC
ffmpeg -i telecined.mp4 -vf "pullup" -r 24000/1001 output.mp4

# With metric output
ffmpeg -i telecined.mp4 -vf "pullup=mp=y" -r 24000/1001 output.mp4
```

**Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `jl`, `jr` | Left/right junk pixels | 1-width |
| `jt`, `jb` | Top/bottom junk pixels | 1-height |
| `sb` | Strict breaks | 0 or 1 |
| `mp` | Metric plane | y, u, v |

### fieldmatch - Field Matching

More advanced telecine removal with field matching.

```bash
# Basic field matching
ffmpeg -i telecined.mp4 -vf "fieldmatch" output.mp4

# Full IVTC pipeline with decimation
ffmpeg -i telecined.mp4 -vf "fieldmatch,decimate" output.mp4

# Specify field order
ffmpeg -i telecined.mp4 -vf "fieldmatch=order=tff,decimate" output.mp4
```

**Combined IVTC workflow:**
```bash
# Complete telecine removal pipeline
ffmpeg -i telecined.mp4 \
  -vf "fieldmatch=order=auto:combmatch=full,decimate" \
  -r 24000/1001 \
  output.mp4
```

### decimate - Frame Decimation

Removes duplicate frames (used after fieldmatch).

```bash
# Remove every 5th frame (30->24 fps)
ffmpeg -i input.mp4 -vf "decimate=cycle=5" output.mp4

# Detect duplicates
ffmpeg -i input.mp4 -vf "decimate=cycle=5:ppsrc=1" output.mp4
```

---

## Field Processing

### fieldorder - Change Field Order

Transforms field order between TFF and BFF.

```bash
# Convert BFF to TFF
ffmpeg -i bff_input.mp4 -vf "fieldorder=tff" output.mp4

# Convert TFF to BFF
ffmpeg -i tff_input.mp4 -vf "fieldorder=bff" output.mp4
```

### separatefields - Separate Fields

Splits each frame into two fields.

```bash
# Separate fields (doubles frame count, halves height)
ffmpeg -i interlaced.mp4 -vf "separatefields" output.mp4
```

### weave - Weave Fields Together

Combines two consecutive frames into one interlaced frame.

```bash
# Weave fields (opposite of separatefields)
ffmpeg -i progressive.mp4 -vf "weave" interlaced.mp4

# Specify first field
ffmpeg -i progressive.mp4 -vf "weave=first_field=top" interlaced.mp4
```

### tinterlace - Temporal Interlacing

Create interlaced output from progressive or modify interlaced content.

```bash
# Create interlaced from progressive (merge adjacent frames)
ffmpeg -i progressive.mp4 -vf "tinterlace=merge" interlaced.mp4

# Bob deinterlace (simple doubling)
ffmpeg -i interlaced.mp4 -vf "tinterlace=4" bobbed.mp4

# Create interlaced at half frame rate
ffmpeg -i progressive.mp4 -vf "tinterlace=interleave_top" interlaced.mp4
```

**Modes:**
| Mode | Description |
|------|-------------|
| `merge` / `0` | Merge fields from consecutive frames |
| `drop_even` / `1` | Drop even frames, interleave remaining |
| `drop_odd` / `2` | Drop odd frames, interleave remaining |
| `pad` / `3` | Pad alternating lines with black |
| `interleave_top` / `4` | Interleave, TFF |
| `interleave_bottom` / `5` | Interleave, BFF |
| `interlacex2` / `6` | Double rate interlacing |
| `mergex2` / `7` | Double rate field merge |

### il - Interleave/Deinterleave Lines

Low-level line interleaving.

```bash
# Swap luma and chroma lines
ffmpeg -i input.mp4 -vf "il=l=s:c=s" output.mp4
```

---

## Common Workflows

### DVD to Progressive MP4

```bash
# Step 1: Detect interlacing
ffmpeg -i dvd_rip.vob -vf "idet" -frames:v 500 -f null -

# Step 2: Deinterlace (if interlaced)
ffmpeg -i dvd_rip.vob \
  -vf "yadif=1:-1:1" \
  -c:v libx264 -crf 18 \
  -c:a aac -b:a 192k \
  output.mp4

# For telecined content (film-based DVDs):
ffmpeg -i dvd_rip.vob \
  -vf "fieldmatch,decimate" \
  -r 24000/1001 \
  -c:v libx264 -crf 18 \
  output.mp4
```

### Broadcast 1080i to 1080p

```bash
# High quality deinterlacing
ffmpeg -i broadcast_1080i.ts \
  -vf "bwdif=1:-1:0" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a copy \
  output_1080p.mp4

# With GPU acceleration
ffmpeg -hwaccel cuda -hwaccel_output_format cuda \
  -i broadcast_1080i.ts \
  -vf "bwdif_cuda=1" \
  -c:v h264_nvenc -preset p4 \
  -c:a copy \
  output_1080p.mp4
```

### Mixed Content Detection and Processing

```bash
#!/bin/bash
# Detect and process based on content type

INPUT="$1"

# Detect interlacing type
result=$(ffmpeg -i "$INPUT" -vf "idet" -frames:v 1000 -f null - 2>&1)

if echo "$result" | grep -q "Multi.*[1-9]"; then
  echo "Interlaced content detected - applying bwdif"
  ffmpeg -i "$INPUT" -vf "bwdif" -c:v libx264 -crf 18 output.mp4
elif echo "$result" | grep -q "Repeated.*[1-9]"; then
  echo "Telecined content detected - applying IVTC"
  ffmpeg -i "$INPUT" -vf "fieldmatch,decimate" -c:v libx264 -crf 18 output.mp4
else
  echo "Progressive content - no deinterlacing needed"
  ffmpeg -i "$INPUT" -c:v libx264 -crf 18 output.mp4
fi
```

---

## Quality Comparison

| Filter | Quality | Speed | Best For |
|--------|---------|-------|----------|
| `yadif` | Good | Fast | General use |
| `bwdif` | Better | Medium | Quality-focused |
| `w3fdif` | Best | Slow | Critical work |
| `yadif_cuda` | Good | Very Fast | GPU systems |
| `bwdif_cuda` | Better | Fast | GPU systems |
| `deinterlace_vaapi` | Good | Very Fast | Linux/VAAPI |

---

## Best Practices

1. **Always detect first** - Use `idet` to determine content type
2. **Preserve frame rate** - Use mode 0 for same fps, mode 1 for double
3. **Match field order** - Use auto-detection or specify correct parity
4. **Use GPU when available** - CUDA/VAAPI filters are much faster
5. **IVTC for film content** - Don't deinterlace telecined film, use pullup/fieldmatch
6. **Test on sample** - Check a short segment before processing full video

This guide covers deinterlacing and telecine for 2025. For hardware acceleration details, see `ffmpeg-hardware-acceleration`. For video analysis, see `ffmpeg-video-analysis`.
