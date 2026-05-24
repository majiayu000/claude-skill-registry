---
name: ffmpeg-waveforms-visualization
description: Complete audio visualization system. PROACTIVELY activate for: (1) Animated waveforms (showwaves), (2) Static waveform images (showwavespic), (3) Spectrum analyzers (showspectrum), (4) Frequency bar visualizations (showfreqs), (5) Stereo vectorscope (avectorscope), (6) Musical note display (showcqt), (7) SoundCloud-style waveforms, (8) Music video visualizers, (9) Podcast waveform videos, (10) Combined visualization dashboards. Provides: Filter parameter tables, color scheme options, scale comparisons, template commands for music videos and podcasts. Ensures: Professional audio visualizations for content creation.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

## Quick Reference

| Visualization | Filter | Output | Command Snippet |
|---------------|--------|--------|-----------------|
| Animated waveform | `showwaves` | Video | `[0:a]showwaves=s=1280x720:mode=line[v]` |
| Static waveform | `showwavespic` | Image | `[0:a]showwavespic=s=1280x240:colors=0x00FF00` |
| Spectrum | `showspectrum` | Video | `[0:a]showspectrum=s=1280x720:color=fire` |
| Frequency bars | `showfreqs` | Video | `[0:a]showfreqs=s=1280x720:mode=bar` |
| Vectorscope | `avectorscope` | Video | `[0:a]avectorscope=s=512x512:mode=lissajous` |

| Color Scheme | Effect |
|--------------|--------|
| `rainbow` | Full spectrum gradient |
| `fire` | Warm orange/red tones |
| `cool` | Blue tones |
| `viridis` | Scientific colormap |

## When to Use This Skill

Use for **audio visualization creation**:
- Music video waveform backgrounds
- Podcast video thumbnails
- SoundCloud-style waveform images
- Spectrum analyzer overlays
- Audio-reactive visualizations

---

# FFmpeg Waveforms and Audio Visualization (2025)

Complete guide to generating audio waveforms, spectrum analyzers, and audio-reactive visualizations using FFmpeg.

## Audio Visualization Filters

### Filter Overview

| Filter | Output | Use Case |
|--------|--------|----------|
| showwaves | Video of animated waveform | Music videos, live vis |
| showwavespic | Static waveform image | Thumbnails, podcasts |
| showspectrum | Spectrum analyzer video | Frequency analysis |
| showspectrumpic | Static spectrum image | Audio fingerprinting |
| showfreqs | Frequency bars video | Equalizer visualization |
| avectorscope | Stereo phase visualization | Audio engineering |
| ahistogram | Audio level histogram | Loudness analysis |
| showcqt | Constant-Q transform | Musical note visualization |

## Waveform Generation (showwaves)

### Basic Animated Waveform

```bash
# Simple waveform video
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x720:mode=line[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -c:a aac \
  waveform.mp4

# Waveform from video with audio
ffmpeg -i video.mp4 \
  -filter_complex "[0:a]showwaves=s=1920x200:mode=line[wave];[0:v][wave]overlay=0:H-200[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -c:a copy \
  video_with_wave.mp4
```

### Waveform Modes

```bash
# Line mode (default) - connected lines
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line[v]" \
  -map "[v]" waveform_line.mp4

# Point mode - individual points
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=point[v]" \
  -map "[v]" waveform_point.mp4

# Filled mode - filled area
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=p2p[v]" \
  -map "[v]" waveform_filled.mp4

# Centered line mode
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=cline[v]" \
  -map "[v]" waveform_centered.mp4
```

### Available Modes

| Mode | Description |
|------|-------------|
| point | Draw a point for each sample |
| line | Draw lines between samples |
| p2p | Draw point-to-point (filled) |
| cline | Centered line mode |

### Colored Waveforms

```bash
# Single color waveform
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=cline:colors=0x00FF00[v]" \
  -map "[v]" green_wave.mp4

# Multi-channel colors (stereo)
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:colors=red|blue:split_channels=1[v]" \
  -map "[v]" stereo_wave.mp4

# Gradient-style (requires multiple passes)
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=cline:colors=0xFF6600[v]" \
  -map "[v]" orange_wave.mp4
```

### Rate and Scale

```bash
# Adjust waveform speed (n = samples per column)
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:n=2[v]" \
  -map "[v]" fast_wave.mp4

# Adjust scale (amplitude)
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:scale=lin[v]" \
  -map "[v]" linear_wave.mp4

# Logarithmic scale (better for quiet audio)
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:scale=log[v]" \
  -map "[v]" log_wave.mp4

# Square root scale
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:scale=sqrt[v]" \
  -map "[v]" sqrt_wave.mp4

# Cube root scale (compressed dynamics)
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:scale=cbrt[v]" \
  -map "[v]" cbrt_wave.mp4
```

### Scale Options

| Scale | Description | Best For |
|-------|-------------|----------|
| lin | Linear amplitude | General use |
| log | Logarithmic | Quiet audio, speech |
| sqrt | Square root | Moderate compression |
| cbrt | Cube root | Heavy compression |

## Static Waveform Images (showwavespic)

### Basic Waveform Image

```bash
# Generate waveform PNG
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwavespic=s=1280x240:colors=0x00FF00" \
  -frames:v 1 \
  waveform.png

# High-resolution waveform
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwavespic=s=3840x480:colors=white" \
  -frames:v 1 \
  waveform_hires.png
```

### Styled Waveform Images

```bash
# Split stereo channels
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwavespic=s=1280x480:split_channels=1:colors=0xFF0000|0x0000FF" \
  -frames:v 1 \
  stereo_waveform.png

# Filled style
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwavespic=s=1280x240:colors=0x1E90FF:draw=full" \
  -frames:v 1 \
  filled_waveform.png

# Scale adjustment
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwavespic=s=1280x240:scale=sqrt:colors=0xFFD700" \
  -frames:v 1 \
  golden_waveform.png
```

### Waveform with Background

```bash
# Waveform on colored background
ffmpeg -i audio.mp3 \
  -filter_complex "color=c=0x1a1a2e:s=1280x240:d=1[bg];\
                   [0:a]showwavespic=s=1280x240:colors=0x00FF88[wave];\
                   [bg][wave]overlay[v]" \
  -map "[v]" -frames:v 1 \
  waveform_bg.png

# Waveform on gradient background
ffmpeg -f lavfi \
  -i "gradients=s=1280x240:c0=0x000033:c1=0x003366:duration=1" \
  -i audio.mp3 \
  -filter_complex "[1:a]showwavespic=s=1280x240:colors=0x00FFFF[wave];\
                   [0:v][wave]overlay[v]" \
  -map "[v]" -frames:v 1 \
  waveform_gradient.png
```

## Spectrum Visualization (showspectrum)

### Basic Spectrum Analyzer

```bash
# Animated spectrum
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:mode=combined:color=rainbow[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -c:a aac \
  spectrum.mp4

# Vertical spectrum
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=720x1280:orientation=vertical:color=fire[v]" \
  -map "[v]" -map 0:a \
  spectrum_vertical.mp4
```

### Spectrum Modes

```bash
# Combined channels
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:mode=combined[v]" \
  -map "[v]" spectrum_combined.mp4

# Separate channels
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:mode=separate[v]" \
  -map "[v]" spectrum_separate.mp4
```

### Color Schemes

```bash
# Rainbow spectrum
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:color=rainbow[v]" \
  -map "[v]" spectrum_rainbow.mp4

# Fire spectrum
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:color=fire[v]" \
  -map "[v]" spectrum_fire.mp4

# Cool spectrum
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:color=cool[v]" \
  -map "[v]" spectrum_cool.mp4

# Channel-based colors
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:color=channel[v]" \
  -map "[v]" spectrum_channel.mp4
```

### Available Color Schemes

| Color | Description |
|-------|-------------|
| channel | Use channel colors |
| rainbow | Rainbow gradient |
| moreland | Diverging color map |
| nebulae | Space-like colors |
| fire | Warm fire colors |
| fiery | Intense fire |
| fruit | Fruit-inspired |
| cool | Cool blue tones |
| magma | Volcanic colors |
| green | Green gradient |
| viridis | Scientific colormap |
| plasma | Plasma colormap |
| cividis | Colorblind-friendly |
| terrain | Terrain-like |

### Spectrum Scale and Window

```bash
# Logarithmic frequency scale
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:fscale=log:color=fire[v]" \
  -map "[v]" spectrum_log.mp4

# Different window functions
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:win_func=blackman:color=rainbow[v]" \
  -map "[v]" spectrum_blackman.mp4

# Higher frequency resolution
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1280x720:win_size=4096:color=fire[v]" \
  -map "[v]" spectrum_hires.mp4
```

## Static Spectrum Image (showspectrumpic)

```bash
# Full audio spectrogram
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrumpic=s=1920x480:color=fire[v]" \
  -map "[v]" \
  spectrogram.png

# With legend
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrumpic=s=1920x480:color=rainbow:legend=1[v]" \
  -map "[v]" \
  spectrogram_legend.png

# Logarithmic frequency scale
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrumpic=s=1920x480:fscale=log:color=viridis[v]" \
  -map "[v]" \
  spectrogram_log.png
```

## Frequency Bars (showfreqs)

### Basic Frequency Display

```bash
# Bar-style equalizer
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showfreqs=s=1280x720:mode=bar:ascale=log:colors=green[v]" \
  -map "[v]" -map 0:a \
  freqs_bar.mp4

# Line-style frequency display
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showfreqs=s=1280x720:mode=line:colors=cyan[v]" \
  -map "[v]" -map 0:a \
  freqs_line.mp4

# Dot-style display
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showfreqs=s=1280x720:mode=dot:colors=0xFF00FF[v]" \
  -map "[v]" -map 0:a \
  freqs_dot.mp4
```

### Equalizer-Style Visualization

```bash
# Classic equalizer bars
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showfreqs=s=1280x720:mode=bar:fscale=log:ascale=log:win_size=1024:colors=0x00FF00[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -c:a aac \
  equalizer.mp4
```

## Constant-Q Transform (showcqt)

### Musical Note Visualization

```bash
# Basic CQT visualization
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showcqt=s=1920x1080[v]" \
  -map "[v]" -map 0:a \
  cqt.mp4

# CQT with axis labels
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showcqt=s=1920x1080:axis=1:text=1:fontfile=/path/to/font.ttf[v]" \
  -map "[v]" -map 0:a \
  cqt_labeled.mp4

# Custom colors
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showcqt=s=1920x1080:sono_g='st(0, floor(log2(400*meter))); if(gt(ld(0),-2), if(lt(ld(0),0),ld(0)+2, if(lt(ld(0),3),1, 3-ld(0))),0)'[v]" \
  -map "[v]" -map 0:a \
  cqt_custom.mp4
```

## Vector Scope (avectorscope)

### Stereo Phase Visualization

```bash
# Basic vectorscope
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]avectorscope=s=512x512:mode=lissajous[v]" \
  -map "[v]" -map 0:a \
  vectorscope.mp4

# Polar mode
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]avectorscope=s=512x512:mode=polar:zoom=1.5[v]" \
  -map "[v]" -map 0:a \
  vectorscope_polar.mp4

# With color coding
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]avectorscope=s=512x512:mode=lissajous:draw=line:scale=sqrt[v]" \
  -map "[v]" -map 0:a \
  vectorscope_color.mp4
```

## Audio Histogram (ahistogram)

### Level Distribution Visualization

```bash
# Basic audio histogram
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]ahistogram=s=1280x720:dmode=separate[v]" \
  -map "[v]" -map 0:a \
  histogram.mp4

# Combined mode
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]ahistogram=s=1280x720:dmode=combined:slide=scroll[v]" \
  -map "[v]" -map 0:a \
  histogram_combined.mp4
```

## Combining Visualizations

### Waveform Over Video

```bash
# Waveform overlay at bottom
ffmpeg -i video.mp4 \
  -filter_complex "[0:a]showwaves=s=1920x200:mode=cline:colors=white@0.7[wave];\
                   [0:v][wave]overlay=0:H-200[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -c:a copy \
  video_waveform.mp4

# Transparent waveform overlay
ffmpeg -i video.mp4 \
  -filter_complex "[0:a]showwaves=s=1920x1080:mode=p2p:colors=0x00FF00@0.5:scale=sqrt[wave];\
                   [0:v][wave]blend=all_mode=addition[v]" \
  -map "[v]" -map 0:a \
  video_wave_blend.mp4
```

### Multiple Visualizations

```bash
# Waveform + Spectrum side by side
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]asplit=2[a1][a2];\
                   [a1]showwaves=s=640x360:mode=cline:colors=green[wave];\
                   [a2]showspectrum=s=640x360:color=fire[spec];\
                   [wave][spec]hstack[v]" \
  -map "[v]" -map 0:a \
  combined_vis.mp4

# Full visualization dashboard
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]asplit=4[a1][a2][a3][a4];\
                   [a1]showwaves=s=640x240:mode=cline:colors=cyan[wave];\
                   [a2]showspectrum=s=640x240:color=fire:scale=log[spec];\
                   [a3]showfreqs=s=640x240:mode=bar:colors=lime[freq];\
                   [a4]avectorscope=s=640x240:mode=lissajous[vec];\
                   [wave][spec]hstack[top];\
                   [freq][vec]hstack[bottom];\
                   [top][bottom]vstack[v]" \
  -map "[v]" -map 0:a \
  dashboard.mp4
```

### Visualization with Progress Bar

```bash
# Waveform with animated progress indicator
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwavespic=s=1280x200:colors=0x333333[bg];\
                   [0:a]showwaves=s=1280x200:mode=cline:colors=0x00FF00:n=4[wave];\
                   [bg][wave]overlay[v];\
                   color=c=red:s=4x200:d=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio.mp3)[bar];\
                   [v][bar]overlay=x='t/$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio.mp3)*W'[out]" \
  -map "[out]" -map 0:a \
  waveform_progress.mp4
```

## Podcast/Music Video Templates

### SoundCloud-Style Waveform

```bash
# Static waveform for music thumbnail
ffmpeg -i audio.mp3 \
  -filter_complex "color=c=0x1a1a2e:s=1200x300:d=1[bg];\
                   [0:a]showwavespic=s=1200x200:colors=0xFF6B00:scale=sqrt[wave];\
                   [bg][wave]overlay=0:50[v]" \
  -map "[v]" -frames:v 1 \
  soundcloud_wave.png
```

### Music Visualizer Video

```bash
# Full music visualizer
ffmpeg -i audio.mp3 -i album_art.jpg \
  -filter_complex "[1:v]scale=1920:1080,boxblur=30[bg];\
                   [0:a]showwaves=s=1920x300:mode=cline:colors=white:scale=sqrt[wave];\
                   [1:v]scale=400:400[art];\
                   [bg][wave]overlay=0:H-350[tmp];\
                   [tmp][art]overlay=(W-400)/2:(H-400)/2-100[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 192k \
  music_video.mp4
```

### Podcast Waveform Video

```bash
# Podcast with waveform and title
ffmpeg -i podcast.mp3 \
  -filter_complex "color=c=0x2d3436:s=1920x1080:d=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 podcast.mp3)[bg];\
                   [0:a]showwaves=s=1920x400:mode=cline:colors=0x74b9ff:scale=sqrt[wave];\
                   [bg][wave]overlay=0:(H-400)/2[tmp];\
                   [tmp]drawtext=text='Episode Title':fontsize=72:fontcolor=white:x=(w-tw)/2:y=100[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -c:a aac \
  podcast_video.mp4
```

## Performance Optimization

### Large Audio Files

```bash
# Use threading for faster processing
ffmpeg -i long_audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:n=4[v]" \
  -threads 0 \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset fast -c:a aac \
  output.mp4
```

### Hardware Acceleration

```bash
# NVENC encoding for visualization
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showspectrum=s=1920x1080:color=fire[v]" \
  -map "[v]" -map 0:a \
  -c:v h264_nvenc -preset fast -c:a aac \
  spectrum_nvenc.mp4
```

## Troubleshooting

### Common Issues

**"Buffer too small" error**
```bash
# Increase buffer size
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:n=1[v]" \
  -map "[v]" output.mp4
```

**Waveform appears silent/flat**
```bash
# Adjust scale for quiet audio
ffmpeg -i quiet_audio.mp3 \
  -filter_complex "[0:a]volume=10,showwaves=s=1280x360:mode=line:scale=log[v]" \
  -map "[v]" output.mp4
```

**Audio/video sync issues**
```bash
# Force frame rate
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:rate=30[v]" \
  -map "[v]" -map 0:a \
  -r 30 \
  output.mp4
```

**Visualization too fast/slow**
```bash
# Adjust samples per column (n)
# Higher n = faster scrolling
# Lower n = slower scrolling
ffmpeg -i audio.mp3 \
  -filter_complex "[0:a]showwaves=s=1280x360:mode=line:n=3[v]" \
  -map "[v]" output.mp4
```

This guide covers FFmpeg audio visualization. For video transitions and effects, see the transitions-effects skill.
