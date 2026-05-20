---
name: ffmpeg-video-analysis
description: Complete FFmpeg video analysis and quality control filters for automation and broadcast workflows. PROACTIVELY activate for: (1) Detecting black frames (blackdetect, blackframe), (2) Finding blurry/frozen frames (blurdetect, freezedetect), (3) Auto crop detection (cropdetect), (4) Scene change detection (scdet), (5) Interlace detection (idet), (6) Quality metrics (PSNR, SSIM, VMAF), (7) Signal analysis (signalstats), (8) Frame information logging (showinfo), (9) QC automation scripts, (10) Broadcast compliance checking. Provides: Detection filters, quality metrics, analysis commands, automation patterns.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Task | Filter | Command Pattern |
|------|--------|-----------------|
| Detect black frames | `blackdetect` | `-vf blackdetect=d=0.5:pic_th=0.98` |
| Detect frozen frames | `freezedetect` | `-vf freezedetect=n=0.003:d=2` |
| Detect blur | `blurdetect` | `-vf blurdetect=low=5:high=15` |
| Auto crop | `cropdetect` | `-vf cropdetect=24:16:0` |
| Scene changes | `scdet` | `-vf scdet=threshold=10` |
| Quality metrics | `psnr`, `ssim` | `-lavfi "[0:v][1:v]psnr" -f null -` |
| Frame info | `showinfo` | `-vf showinfo` |

## When to Use This Skill

Use for **quality control and automation workflows**:
- Automated video analysis pipelines
- Detecting problematic frames (black, frozen, blurry)
- Finding optimal crop parameters
- Measuring quality after encoding
- Broadcast compliance checking
- Content-aware editing decisions

---

# FFmpeg Video Analysis Filters (2025)

Comprehensive guide to video analysis filters for quality control, automation, and professional workflows.

## Detection Filters

### blackdetect - Detect Black Frames

Detects video sequences that are completely black, useful for finding commercial breaks, scene boundaries, or encoding issues.

```bash
# Basic black detection
ffmpeg -i input.mp4 -vf "blackdetect=d=0.5:pic_th=0.98:pix_th=0.10" -f null -

# More sensitive detection (darker threshold)
ffmpeg -i input.mp4 -vf "blackdetect=d=0.1:pic_th=0.90" -f null -

# Save detection results to log
ffmpeg -i input.mp4 -vf "blackdetect=d=0.5" -f null - 2>&1 | grep blackdetect

# Detect and extract black segments
ffmpeg -i input.mp4 -vf "blackdetect=d=2.0" -f null - 2>&1 | \
  grep -oP 'black_start:\K[0-9.]+|black_end:\K[0-9.]+'
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `d` | Minimum duration (seconds) | 2.0 | > 0 |
| `pic_th` | Picture black ratio threshold | 0.98 | 0-1 |
| `pix_th` | Pixel black threshold | 0.10 | 0-1 |

**Output format:**
```
[blackdetect @ 0x...] black_start:10.5 black_end:12.3 black_duration:1.8
```

### blackframe - Detect Nearly Black Frames

Similar to blackdetect but reports individual frames and their blackness amount.

```bash
# Detect frames that are 98% black
ffmpeg -i input.mp4 -vf "blackframe=amount=98:threshold=32" -f null -

# Output includes frame number and percentage
ffmpeg -i input.mp4 -vf "blackframe=amount=90" -f null - 2>&1 | grep blackframe
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `amount` | Percentage threshold | 98 | 0-100 |
| `threshold` | Pixel brightness threshold | 32 | 0-255 |

### freezedetect - Detect Frozen Frames

Detects sequences where the video appears frozen (repeated frames).

```bash
# Basic freeze detection
ffmpeg -i input.mp4 -vf "freezedetect=n=0.003:d=2" -f null -

# More sensitive (detect shorter freezes)
ffmpeg -i input.mp4 -vf "freezedetect=n=0.001:d=0.5" -f null -

# Very strict (only perfectly identical frames)
ffmpeg -i input.mp4 -vf "freezedetect=n=0:d=1" -f null -
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `n` | Noise tolerance (frame diff) | 0.001 | 0-1 |
| `d` | Minimum freeze duration | 2.0 | > 0 |

**Output format:**
```
[freezedetect @ 0x...] freeze_start: 45.2
[freezedetect @ 0x...] freeze_duration: 3.5
[freezedetect @ 0x...] freeze_end: 48.7
```

### blurdetect - Detect Blurry Frames

Detects frames that are out of focus or motion blurred.

```bash
# Basic blur detection
ffmpeg -i input.mp4 -vf "blurdetect=low=5:high=15:radius=50" -f null -

# More sensitive detection
ffmpeg -i input.mp4 -vf "blurdetect=low=3:high=10" -f null -

# Output blur values per frame
ffmpeg -i input.mp4 -vf "blurdetect,metadata=print:file=blur.txt" -f null -
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `low` | Low edge threshold | 5 | 1-100 |
| `high` | High edge threshold | 15 | 1-100 |
| `radius` | Search radius | 50 | 1-100 |
| `block_pct` | Block percentage | 80 | 0-100 |
| `block_width` | Block width | - | > 0 |
| `block_height` | Block height | - | > 0 |
| `planes` | Planes to analyze | 1 | 0-15 |

**Output metadata:**
- `lavfi.blur` - Blur value (lower = blurrier)

### scdet - Scene Change Detection

Detects scene changes based on frame-to-frame differences.

```bash
# Basic scene detection
ffmpeg -i input.mp4 -vf "scdet=threshold=10:sc_pass=1" -f null -

# More sensitive (detect more scene changes)
ffmpeg -i input.mp4 -vf "scdet=threshold=5" -f null -

# Output scene changes with timestamps
ffmpeg -i input.mp4 -vf "scdet=t=10,metadata=print:file=scenes.txt" -f null -

# Combined with select filter to extract scene thumbnails
ffmpeg -i input.mp4 -vf "scdet=threshold=10,select='gt(scene,0.4)',showinfo" \
  -vsync vfr scene_%04d.jpg
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `threshold` / `t` | Scene change threshold | 10.0 | 0-100 |
| `sc_pass` | Pass scene score to output | 0 | 0-1 |

**Output metadata:**
- `lavfi.scd.score` - Scene change score (0-1)
- `lavfi.scd.mafd` - Mean absolute frame difference
- `lavfi.scd.time` - Timestamp of scene change

### cropdetect - Auto Crop Detection

Automatically detects optimal crop values to remove black borders.

```bash
# Basic crop detection
ffmpeg -i input.mp4 -vf "cropdetect=24:16:0" -f null -

# More aggressive detection (lower threshold)
ffmpeg -i input.mp4 -vf "cropdetect=16:2:0" -f null -

# Detect and apply crop in one command
crop=$(ffmpeg -i input.mp4 -vf "cropdetect=24:16:0" -f null - 2>&1 | \
  grep -oP 'crop=\K[0-9:]+' | tail -1)
ffmpeg -i input.mp4 -vf "crop=$crop" output.mp4

# Detect letterbox dimensions
ffmpeg -i input.mp4 -vf "cropdetect=round=2:reset=0" -f null - 2>&1 | grep crop
```

**Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `limit` | Threshold for black pixels | 24 | 0-255 |
| `round` | Round to nearest multiple | 16 | >= 2 |
| `reset` | Reset counter (frames) | 0 | >= 0 |
| `skip` | Skip initial frames | 0 | >= 0 |

**Output format:**
```
[cropdetect @ 0x...] x1:0 x2:1919 y1:140 y2:939 w:1920 h:800 x:0 y:140 crop=1920:800:0:140
```

### idet - Interlace Detection

Detects whether video is interlaced and identifies field order.

```bash
# Basic interlace detection
ffmpeg -i input.mp4 -vf "idet" -frames:v 500 -f null -

# Output detection summary
ffmpeg -i input.mp4 -vf "idet" -f null - 2>&1 | grep -A5 "Repeated Fields"
```

**Output includes:**
- Single (progressive frames)
- Multi (interlaced - multiple fields from same frame)
- Repeated (repeated fields - pulldown)
- Top Field First (TFF) vs Bottom Field First (BFF)

---

## Quality Metrics

### psnr - Peak Signal-to-Noise Ratio

Compares two videos and outputs PSNR quality metric.

```bash
# Compare original vs encoded
ffmpeg -i original.mp4 -i encoded.mp4 \
  -lavfi "[0:v][1:v]psnr" -f null -

# Output PSNR per frame to file
ffmpeg -i original.mp4 -i encoded.mp4 \
  -lavfi "[0:v][1:v]psnr=stats_file=psnr.log" -f null -

# Get average PSNR only
ffmpeg -i original.mp4 -i encoded.mp4 \
  -lavfi "[0:v][1:v]psnr" -f null - 2>&1 | grep "average"
```

**Output format:**
```
[Parsed_psnr_0 @ 0x...] PSNR y:45.123 u:48.456 v:49.789 average:46.234 min:35.123 max:inf
```

**Quality guidelines:**
| PSNR (dB) | Quality |
|-----------|---------|
| > 40 | Excellent (indistinguishable) |
| 35-40 | Good |
| 30-35 | Fair |
| < 30 | Poor |

### ssim - Structural Similarity Index

More perceptually accurate than PSNR for quality comparison.

```bash
# Compare original vs encoded
ffmpeg -i original.mp4 -i encoded.mp4 \
  -lavfi "[0:v][1:v]ssim" -f null -

# Output SSIM per frame to file
ffmpeg -i original.mp4 -i encoded.mp4 \
  -lavfi "[0:v][1:v]ssim=stats_file=ssim.log" -f null -
```

**Output format:**
```
[Parsed_ssim_0 @ 0x...] SSIM Y:0.987 (18.87) U:0.992 (20.97) V:0.993 (21.55) All:0.989 (19.59)
```

**Quality guidelines:**
| SSIM | Quality |
|------|---------|
| > 0.98 | Excellent |
| 0.95-0.98 | Good |
| 0.90-0.95 | Fair |
| < 0.90 | Poor |

### vmafmotion - VMAF Motion Score

Calculates motion activity score used by VMAF.

```bash
# Calculate motion score
ffmpeg -i input.mp4 -vf "vmafmotion" -f null - 2>&1 | grep vmafmotion

# Get average motion
ffmpeg -i input.mp4 -vf "vmafmotion" -f null - 2>&1 | tail -1
```

### signalstats - Video Signal Statistics

Comprehensive signal analysis for broadcast QC.

```bash
# Full signal analysis
ffmpeg -i input.mp4 -vf "signalstats=stat=tout+vrep+brng" -f null -

# Output to file
ffmpeg -i input.mp4 -vf "signalstats,metadata=print:file=stats.txt" -f null -

# Check for broadcast-safe levels
ffmpeg -i input.mp4 -vf "signalstats=stat=brng,metadata=print" -f null - 2>&1 | \
  grep "lavfi.signalstats.BRNG"
```

**Statistics available:**
| Stat | Description |
|------|-------------|
| `tout` | Temporal outliers |
| `vrep` | Vertical line repetition |
| `brng` | Broadcast range violations |

**Output metadata includes:**
- `YMIN`, `YMAX` - Luma range
- `YAVG` - Average luma
- `UMIN`, `UMAX`, `VMIN`, `VMAX` - Chroma range
- `SATMIN`, `SATMAX`, `SATAVG` - Saturation
- `HUEAVG` - Average hue
- `BRNG` - Out of broadcast range pixel count

---

## Frame Information

### showinfo - Display Frame Information

Outputs detailed information about each frame.

```bash
# Show all frame info
ffmpeg -i input.mp4 -vf "showinfo" -f null -

# Show specific frames only
ffmpeg -i input.mp4 -vf "select='eq(n,0)+eq(n,100)',showinfo" -f null -

# Parse specific information
ffmpeg -i input.mp4 -vf "showinfo" -f null - 2>&1 | grep "pts_time"
```

**Output includes:**
```
[Parsed_showinfo_0 @ 0x...] n:   0 pts:      0 pts_time:0       duration:   1001
 duration_time:0.0417083 fmt:yuv420p cl:left sar:1/1 s:1920x1080 i:P iskey:1
 type:I checksum:12345678 plane_checksum:[AAAAAAAA BBBBBBBB CCCCCCCC]
```

**Fields:**
- `n` - Frame number
- `pts` - Presentation timestamp
- `pts_time` - PTS in seconds
- `duration` - Frame duration
- `fmt` - Pixel format
- `s` - Size (resolution)
- `i` - Interlaced (P=progressive, T=top, B=bottom)
- `iskey` - Is keyframe
- `type` - Frame type (I/P/B)

### siti - Spatial and Temporal Information

ITU-T P.910 compliant SI/TI calculation.

```bash
# Calculate SI/TI
ffmpeg -i input.mp4 -vf "siti" -f null - 2>&1 | grep siti

# Output to file
ffmpeg -i input.mp4 -vf "siti=print_summary=1" -f null -
```

**Output:**
- `SI` - Spatial Information (edge/texture complexity)
- `TI` - Temporal Information (motion activity)

---

## Automation Patterns

### QC Pipeline Script

```bash
#!/bin/bash
# Comprehensive video QC analysis

INPUT="$1"
OUTPUT_DIR="qc_results"
mkdir -p "$OUTPUT_DIR"

echo "Analyzing: $INPUT"

# 1. Black frame detection
ffmpeg -i "$INPUT" -vf "blackdetect=d=0.5" -f null - 2>&1 | \
  grep blackdetect > "$OUTPUT_DIR/black_frames.txt"

# 2. Freeze detection
ffmpeg -i "$INPUT" -vf "freezedetect=n=0.003:d=2" -f null - 2>&1 | \
  grep freeze > "$OUTPUT_DIR/frozen_frames.txt"

# 3. Scene detection
ffmpeg -i "$INPUT" -vf "scdet=threshold=10,metadata=print:file=$OUTPUT_DIR/scenes.txt" -f null -

# 4. Crop detection
ffmpeg -i "$INPUT" -vf "cropdetect=24:16:0" -f null - 2>&1 | \
  grep crop | tail -1 > "$OUTPUT_DIR/crop.txt"

# 5. Interlace detection
ffmpeg -i "$INPUT" -vf "idet" -frames:v 500 -f null - 2>&1 | \
  grep -A5 "Repeated" > "$OUTPUT_DIR/interlace.txt"

# 6. Signal stats
ffmpeg -i "$INPUT" -vf "signalstats=stat=brng,metadata=print:file=$OUTPUT_DIR/signal.txt" \
  -f null -

echo "QC analysis complete. Results in $OUTPUT_DIR/"
```

### Extract Frames at Scene Changes

```bash
# Extract one frame per scene
ffmpeg -i input.mp4 \
  -vf "scdet=threshold=10,select='gt(scene,0.4)'" \
  -vsync vfr \
  -frame_pts 1 \
  scene_%04d.jpg

# Extract with timestamp in filename
ffmpeg -i input.mp4 \
  -vf "scdet=threshold=10,select='gt(scene,0.4)',showinfo" \
  -vsync vfr \
  "scene_%04d_%{pts}.jpg"
```

### Quality Comparison Batch

```bash
#!/bin/bash
# Compare multiple encodes against reference

REFERENCE="reference.mp4"

for encoded in encode_*.mp4; do
  echo "Comparing: $encoded"

  # PSNR
  psnr=$(ffmpeg -i "$REFERENCE" -i "$encoded" \
    -lavfi "[0:v][1:v]psnr" -f null - 2>&1 | \
    grep -oP 'average:\K[0-9.]+')

  # SSIM
  ssim=$(ffmpeg -i "$REFERENCE" -i "$encoded" \
    -lavfi "[0:v][1:v]ssim" -f null - 2>&1 | \
    grep -oP 'All:\K[0-9.]+')

  echo "  PSNR: $psnr dB, SSIM: $ssim"
done
```

---

## Best Practices

1. **Use appropriate thresholds** - Start with defaults, adjust based on content
2. **Sample long videos** - Use `-t` to analyze portions first
3. **Combine filters** - Chain detection filters for comprehensive analysis
4. **Parse output** - Use grep/awk to extract relevant data
5. **Batch processing** - Create scripts for consistent QC workflows
6. **Log results** - Use `metadata=print:file=` to save results

This guide covers video analysis filters for 2025. For encoding quality, see `ffmpeg-fundamentals-2025`. For hardware-accelerated analysis, check GPU filter support in `ffmpeg-hardware-acceleration`.
