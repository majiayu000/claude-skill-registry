---
name: ffmpeg-filter-complex-patterns
description: Complete guide to FFmpeg filter_complex syntax, multi-input/output pipelines, and composition patterns. PROACTIVELY activate for: (1) filter_complex syntax questions, (2) Multi-input video composition (PiP, grids, overlays), (3) Video transitions (xfade, fades, wipes), (4) Audio mixing (amix, amerge), (5) Stream splitting and routing, (6) Named stream labels, (7) Complex filtergraphs, (8) GPU + CPU hybrid filter chains, (9) ABR encoding ladders, (10) Text and watermark overlays. Provides: Syntax reference, composition patterns, audio mixing examples, transition effects, GPU-accelerated filtergraphs, debugging tips.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Task | Command Pattern |
|------|-----------------|
| Basic filter_complex | `-filter_complex "[0:v][1:v]overlay"` |
| Named labels | `[input]filter[output]` |
| Chain filters | `filter1,filter2,filter3` |
| Separate chains | `chain1;chain2` |
| Map output | `-map "[label]"` |

## When to Use This Skill

Use for **complex filtergraph operations**:
- Multi-input compositions (PiP, grids, overlays)
- Video transitions and effects
- Audio mixing and routing
- Stream splitting for multiple outputs
- GPU + CPU hybrid processing

**For basic filters**: use `ffmpeg-fundamentals-2025`
**For hardware acceleration**: use `ffmpeg-hardware-acceleration`

---

# FFmpeg filter_complex Reference (2025)

Comprehensive guide to complex filtergraphs, multi-input compositions, and advanced filter chains.

## filter_complex Syntax

### Basic Structure

```
-filter_complex "filterchain1;filterchain2;..."
```

Each filterchain consists of:
- **Input labels**: `[input_label]`
- **Filter(s)**: `filter1,filter2,...` (comma-separated)
- **Output labels**: `[output_label]`

### Complete Syntax

```
[input_label1][input_label2]filter=param1=value1:param2=value2[output_label]
```

### Syntax Components

| Component | Description | Example |
|-----------|-------------|---------|
| `[0:v]` | Video stream from input 0 | First input video |
| `[0:a]` | Audio stream from input 0 | First input audio |
| `[1:v]` | Video stream from input 1 | Second input video |
| `[label]` | Custom named label | User-defined |
| `,` | Chain filters sequentially | `scale,fps` |
| `;` | Separate independent chains | `chain1;chain2` |
| `=` | Parameter assignment | `scale=1280:720` |
| `:` | Parameter separator | `w=1280:h=720` |

### Stream References

| Reference | Meaning |
|-----------|---------|
| `[0]` | First input (all streams) |
| `[0:v]` | First input, video stream |
| `[0:a]` | First input, audio stream |
| `[0:s]` | First input, subtitle stream |
| `[0:v:0]` | First input, first video stream |
| `[1:a:1]` | Second input, second audio stream |

### Default Labels

- Unlabeled first filter input uses `in`
- Unlabeled last filter output uses `out`
- Unlabeled pads connect sequentially

### Escaping Rules

```bash
# Wrap filtergraph in double quotes
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]drawtext=text='Hello World':fontsize=24[out]" \
  -map "[out]" output.mp4

# Using shell variables
text="Dynamic Text"
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]drawtext=text='$text':fontsize=24[out]" \
  -map "[out]" output.mp4

# Escaping special characters (colons in timestamps)
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]drawtext=text='Time\: %{pts\:hms}':fontsize=24[out]" \
  -map "[out]" output.mp4
```

---

## Common Composition Patterns

### 1. Picture-in-Picture (PiP)

```bash
# Basic PiP - small video in bottom-right corner
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "\
    [1:v]scale=320:240[pip];\
    [0:v][pip]overlay=W-w-10:H-h-10" \
  -c:v libx264 -c:a copy output.mp4

# PiP with border
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "\
    [1:v]scale=320:240,drawbox=x=0:y=0:w=iw:h=ih:c=white:t=3[pip];\
    [0:v][pip]overlay=W-w-10:H-h-10" \
  output.mp4

# Animated PiP (moving)
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "\
    [1:v]scale=320:240[pip];\
    [0:v][pip]overlay='W-w-10-sin(t)*20':'H-h-10-cos(t)*20'" \
  output.mp4

# PiP with fade-in
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "\
    [1:v]scale=320:240,fade=in:st=2:d=1[pip];\
    [0:v][pip]overlay=W-w-10:H-h-10:enable='gte(t,2)'" \
  output.mp4
```

### 2. Video Grid Layouts

**Using hstack/vstack (fast, simple):**

```bash
# 2x2 Grid
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 \
  -filter_complex "\
    [0:v]scale=640:360[v0];\
    [1:v]scale=640:360[v1];\
    [2:v]scale=640:360[v2];\
    [3:v]scale=640:360[v3];\
    [v0][v1]hstack=inputs=2[top];\
    [v2][v3]hstack=inputs=2[bottom];\
    [top][bottom]vstack=inputs=2[out]" \
  -map "[out]" output.mp4

# 3x2 Grid
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 -i 5.mp4 -i 6.mp4 \
  -filter_complex "\
    [0:v]scale=426:240[v0];\
    [1:v]scale=426:240[v1];\
    [2:v]scale=426:240[v2];\
    [3:v]scale=426:240[v3];\
    [4:v]scale=426:240[v4];\
    [5:v]scale=426:240[v5];\
    [v0][v1][v2]hstack=inputs=3[top];\
    [v3][v4][v5]hstack=inputs=3[bottom];\
    [top][bottom]vstack=inputs=2[out]" \
  -map "[out]" output.mp4
```

**Using xstack (more flexible positioning):**

```bash
# 2x2 Grid with xstack
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 \
  -filter_complex "\
    [0:v]scale=640:360[v0];\
    [1:v]scale=640:360[v1];\
    [2:v]scale=640:360[v2];\
    [3:v]scale=640:360[v3];\
    [v0][v1][v2][v3]xstack=inputs=4:layout=0_0|640_0|0_360|640_360[out]" \
  -map "[out]" output.mp4

# L-shaped layout
ffmpeg -i main.mp4 -i side1.mp4 -i side2.mp4 \
  -filter_complex "\
    [0:v]scale=960:720[main];\
    [1:v]scale=320:360[s1];\
    [2:v]scale=320:360[s2];\
    [main][s1][s2]xstack=inputs=3:layout=0_0|960_0|960_360[out]" \
  -map "[out]" output.mp4
```

### 3. Video Transitions (xfade)

```bash
# Simple fade transition
ffmpeg -i first.mp4 -i second.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=1:offset=4[v];\
    [0:a][1:a]acrossfade=d=1[a]" \
  -map "[v]" -map "[a]" output.mp4

# Dissolve transition
ffmpeg -i first.mp4 -i second.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=dissolve:duration=2:offset=3[v]" \
  -map "[v]" output.mp4

# Wipe transitions
ffmpeg -i first.mp4 -i second.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=wipeleft:duration=1:offset=4[v]" \
  -map "[v]" output.mp4

# Multiple transitions (3+ clips)
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 \
  -filter_complex "\
    [0:v]settb=AVTB,fps=30[v0];\
    [1:v]settb=AVTB,fps=30[v1];\
    [2:v]settb=AVTB,fps=30[v2];\
    [v0][v1]xfade=transition=fade:duration=1:offset=4[xf1];\
    [xf1][v2]xfade=transition=dissolve:duration=1:offset=8[out]" \
  -map "[out]" output.mp4
```

**Available xfade transitions:**
- `fade`, `fadeblack`, `fadewhite`
- `wipeleft`, `wiperight`, `wipeup`, `wipedown`
- `slideleft`, `slideright`, `slideup`, `slidedown`
- `circlecrop`, `rectcrop`, `distance`
- `radial`, `smoothleft`, `smoothright`
- `dissolve`, `pixelize`, `diagtl`, `diagtr`, `diagbl`, `diagbr`
- `hlslice`, `hrslice`, `vuslice`, `vdslice`
- `hblur`, `fadegrays`, `squeezev`, `squeezeh`

### 4. Audio Mixing

```bash
# Mix two audio tracks
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "\
    [0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]" \
  -map 0:v -map "[aout]" output.mp4

# Mix with volume control
ffmpeg -i vocals.mp4 -i music.mp3 \
  -filter_complex "\
    [0:a]volume=1.0[v0];\
    [1:a]volume=0.3[v1];\
    [v0][v1]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" output.mp4

# Audio with delay (ducking)
ffmpeg -i main.mp4 -i effect.mp3 \
  -filter_complex "\
    [1:a]adelay=2000|2000[delayed];\
    [0:a][delayed]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" output.mp4

# Merge channels (stereo from two mono)
ffmpeg -i left.wav -i right.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2[aout]" \
  -map "[aout]" stereo.wav

# Audio crossfade between tracks
ffmpeg -i track1.mp3 -i track2.mp3 \
  -filter_complex "[0:a][1:a]acrossfade=d=3:c1=tri:c2=tri[out]" \
  -map "[out]" mixed.mp3
```

### 5. Text and Watermark Overlays

```bash
# Static text overlay
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]drawtext=text='Watermark':\
    fontsize=48:fontcolor=white@0.8:\
    x=10:y=H-th-10[out]" \
  -map "[out]" output.mp4

# Fade-in text
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]drawtext=text='Hello':\
    fontsize=64:fontcolor=white:\
    x=(w-text_w)/2:y=(h-text_h)/2:\
    alpha='if(lt(t,1),t,1)'[out]" \
  -map "[out]" output.mp4

# Scrolling credits
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]drawtext=textfile=credits.txt:\
    fontsize=32:fontcolor=white:\
    x=(w-text_w)/2:y=h-t*50[out]" \
  -map "[out]" output.mp4

# Timed text (appear/disappear)
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]drawtext=text='Show at 2s':\
    fontsize=48:fontcolor=yellow:\
    x=100:y=100:\
    enable='between(t,2,5)'[out]" \
  -map "[out]" output.mp4

# Logo/image watermark
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "\
    [1:v]scale=150:-1[logo];\
    [0:v][logo]overlay=W-w-20:20[out]" \
  -map "[out]" -map 0:a output.mp4
```

### 6. Stream Splitting and Multiple Outputs

```bash
# Split for multiple resolutions
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]split=3[v1][v2][v3];\
    [v1]scale=1920:1080[hd];\
    [v2]scale=1280:720[sd];\
    [v3]scale=640:360[mobile]" \
  -map "[hd]" hd.mp4 \
  -map "[sd]" sd.mp4 \
  -map "[mobile]" mobile.mp4

# Split video and audio separately
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]split=2[v1][v2];\
    [0:a]asplit=2[a1][a2];\
    [v1]scale=1280:720[vout1];\
    [v2]scale=640:360[vout2]" \
  -map "[vout1]" -map "[a1]" output1.mp4 \
  -map "[vout2]" -map "[a2]" output2.mp4
```

### 7. Video Concatenation with Filters

```bash
# Concatenate with format normalization
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 \
  -filter_complex "\
    [0:v]scale=1920:1080,fps=30,setpts=PTS-STARTPTS[v0];\
    [1:v]scale=1920:1080,fps=30,setpts=PTS-STARTPTS[v1];\
    [2:v]scale=1920:1080,fps=30,setpts=PTS-STARTPTS[v2];\
    [0:a]aformat=sample_rates=48000:channel_layouts=stereo[a0];\
    [1:a]aformat=sample_rates=48000:channel_layouts=stereo[a1];\
    [2:a]aformat=sample_rates=48000:channel_layouts=stereo[a2];\
    [v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" output.mp4
```

---

## GPU-Accelerated Filtergraphs

### Full CUDA Pipeline

```bash
# GPU decode -> GPU filter -> GPU encode
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i main.mp4 \
  -hwaccel cuda -hwaccel_output_format cuda -i overlay.mp4 \
  -filter_complex "\
    [0:v]scale_cuda=1920:1080[main];\
    [1:v]scale_cuda=320:180[pip];\
    [main][pip]overlay_cuda=W-w-10:H-h-10[out]" \
  -map "[out]" -map 0:a \
  -c:v h264_nvenc -preset p4 output.mp4
```

### Hybrid GPU + CPU Pipeline

When you need CPU-only filters (drawtext, subtitles), use hwdownload/hwupload:

```bash
# GPU scale -> CPU text -> GPU encode
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -filter_complex "\
    [0:v]scale_cuda=1920:1080[scaled];\
    [scaled]hwdownload,format=nv12[cpu];\
    [cpu]drawtext=text='Watermark':fontsize=48:x=10:y=10[text];\
    [text]hwupload_cuda[out]" \
  -map "[out]" \
  -c:v h264_nvenc output.mp4
```

### ABR Ladder with GPU

```bash
# Generate multiple resolutions on GPU
ffmpeg -y -vsync 0 \
  -hwaccel cuda \
  -hwaccel_output_format cuda \
  -i input.mp4 \
  -filter_complex "[0:v]split=3[v1][v2][v3];\
    [v1]scale_cuda=1920:1080[hd];\
    [v2]scale_cuda=1280:720[sd];\
    [v3]scale_cuda=640:360[mobile]" \
  -map "[hd]" -c:v h264_nvenc -b:v 5M output_1080p.mp4 \
  -map "[sd]" -c:v h264_nvenc -b:v 2M output_720p.mp4 \
  -map "[mobile]" -c:v h264_nvenc -b:v 500k output_360p.mp4
```

---

## Advanced Patterns

### Multi-Layer Composition

```bash
# Video with lower third, logo, and timecode
ffmpeg -i main.mp4 -i logo.png -i lower_third.png \
  -filter_complex "\
    [1:v]scale=150:-1[logo];\
    [2:v]scale=400:-1[third];\
    [0:v][logo]overlay=W-w-20:20[step1];\
    [step1][third]overlay=50:H-h-80:enable='between(t,5,55)'[step2];\
    [step2]drawtext=text='%{pts\\:hms}':\
      fontsize=32:fontcolor=white:\
      x=W-tw-20:y=H-th-20[out]" \
  -map "[out]" -map 0:a output.mp4
```

### Audio Visualization Overlay

```bash
# Waveform overlay on video
ffmpeg -i video.mp4 -i audio.mp3 \
  -filter_complex "\
    [1:a]showwaves=s=1920x200:mode=cline:colors=white@0.8[wave];\
    [0:v][wave]overlay=0:H-h-50[out]" \
  -map "[out]" -map 1:a output.mp4

# Spectrum analyzer
ffmpeg -i video.mp4 \
  -filter_complex "\
    [0:a]showspectrum=s=1920x200:legend=0:color=rainbow[spec];\
    [0:v][spec]overlay=0:H-h[out]" \
  -map "[out]" -map 0:a output.mp4
```

### Time-Based Effects

```bash
# Different effects at different times
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]split=3[v1][v2][v3];\
    [v1]trim=0:5,setpts=PTS-STARTPTS[part1];\
    [v2]trim=5:10,setpts=PTS-STARTPTS,eq=brightness=0.2:saturation=2.0[part2];\
    [v3]trim=10,setpts=PTS-STARTPTS[part3];\
    [part1][part2][part3]concat=n=3:v=1:a=0[out]" \
  -map "[out]" -map 0:a output.mp4
```

---

## Debugging Filtergraphs

### Verbose Logging

```bash
# Enable debug logging
ffmpeg -loglevel debug -i input.mp4 -filter_complex "..." output.mp4

# Show filter graph info
ffmpeg -filter_complex_script script.txt -lavfi "..." 2>&1 | grep -i filter
```

### Validate Filtergraph

```bash
# Test filtergraph without encoding (null output)
ffmpeg -i input.mp4 -filter_complex "..." -f null -

# Check specific filter options
ffmpeg -h filter=overlay
ffmpeg -h filter=xfade
ffmpeg -h filter=amix
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Input pad not connected" | Missing input label | Add `[0:v]` or correct label |
| "Output pad not connected" | Unused filter output | Add `-map` or connect to next filter |
| "Stream specifier not found" | Invalid stream reference | Check input has that stream type |
| "Filter not found" | Missing filter in FFmpeg build | Check `ffmpeg -filters` |
| "Discarding frame" | Timestamp discontinuity | Add `setpts=PTS-STARTPTS` |

### Performance Tips

1. **Order matters** - Put expensive filters later in the chain
2. **Use GPU filters** when available (scale_cuda, overlay_cuda)
3. **Avoid unnecessary format conversions** - Keep same pixel format
4. **Split before filters** if creating multiple outputs
5. **Use `-threads 0`** to auto-detect optimal thread count

---

## Best Practices

1. **Use meaningful labels** - `[scaled]` not `[v1]` for clarity
2. **Test on short clips** - Use `-t 5` to test first 5 seconds
3. **Check all streams** - Verify audio mapping with `-map`
4. **Normalize inputs** - Match fps, resolution before concat/transitions
5. **Quote the filtergraph** - Use double quotes around entire -filter_complex
6. **Handle audio separately** - Video and audio often need different processing

This guide covers filter_complex patterns for 2025. For hardware acceleration details, see `ffmpeg-hardware-acceleration`. For basic filter syntax, see `ffmpeg-fundamentals-2025`.
