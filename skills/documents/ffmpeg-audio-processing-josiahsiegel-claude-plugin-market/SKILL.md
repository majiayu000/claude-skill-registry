---
name: ffmpeg-audio-processing
description: Complete audio encoding and normalization system. PROACTIVELY activate for: (1) Audio codec selection (AAC, MP3, Opus, FLAC), (2) Loudness normalization (EBU R128, loudnorm), (3) Audio extraction from video, (4) Format conversion, (5) Volume adjustment and dynamics, (6) Noise reduction and EQ, (7) Channel operations (stereo/mono/surround), (8) Sample rate and bit depth conversion, (9) Audio fade in/out and crossfades, (10) Podcast and broadcast processing chains. Provides: Codec comparison tables, loudness standards reference, two-pass normalization scripts, professional mastering chains. Ensures: Broadcast-compliant audio with proper loudness and quality.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Task | Command |
|------|---------|
| Extract audio | `ffmpeg -i video.mp4 -vn -c:a copy audio.m4a` |
| Convert to MP3 | `ffmpeg -i input.flac -c:a libmp3lame -q:a 2 output.mp3` |
| Normalize (EBU R128) | `-af loudnorm=I=-23:LRA=7:TP=-2` |
| Podcast standard | `-af loudnorm=I=-16:TP=-1.5` |
| Adjust volume | `-af "volume=1.5"` or `-af "volume=6dB"` |
| Mono to stereo | `-ac 2` |

| Codec | Recommended Bitrate | Use Case |
|-------|---------------------|----------|
| AAC | 128-192k (music), 64k (speech) | Streaming, mobile |
| MP3 | 192-320k (music), 128k (speech) | Universal compatibility |
| Opus | 96-128k (music), 48k (speech) | WebM, VoIP, modern |

## When to Use This Skill

Use for **audio-focused operations**:
- Extracting audio from video files
- Loudness normalization for broadcast/streaming compliance
- Podcast and audiobook processing
- Audio format conversion
- Audio effects (EQ, compression, noise reduction)

---

# FFmpeg Audio Processing (2025)

Complete guide to audio encoding, normalization, and professional audio workflows with FFmpeg.

## Audio Codec Reference

### Codec Comparison

| Codec | Encoder | Bitrate Range | Quality | Compatibility | Use Case |
|-------|---------|---------------|---------|---------------|----------|
| AAC | aac, libfdk_aac | 64-320 kbps | Excellent | Universal | Streaming, mobile |
| MP3 | libmp3lame | 96-320 kbps | Good | Universal | Legacy, podcasts |
| Opus | libopus | 32-256 kbps | Best | Modern | VoIP, WebM |
| FLAC | flac | ~900 kbps | Lossless | Wide | Archival |
| ALAC | alac | ~900 kbps | Lossless | Apple | Apple ecosystem |
| Vorbis | libvorbis | 64-500 kbps | Very Good | Wide | WebM, games |
| AC3 | ac3 | 192-640 kbps | Good | Universal | DVD, Blu-ray |
| EAC3 | eac3 | 192-768 kbps | Very Good | Wide | Streaming |
| xHE-AAC | - (decode only) | 12-64 kbps | Excellent | Emerging | Ultra-low bitrate |

### Recommended Bitrates

| Use Case | AAC | MP3 | Opus |
|----------|-----|-----|------|
| Podcast/Speech | 64-96k | 96-128k | 48-64k |
| Music (Standard) | 128-192k | 192-256k | 96-128k |
| Music (High Quality) | 256-320k | 320k | 160-256k |
| Transparent Quality | 256k+ | 320k | 192k+ |

## Basic Audio Operations

### Extract Audio

```bash
# Extract to original format (no re-encode)
ffmpeg -i video.mp4 -vn -c:a copy audio.m4a

# Extract to MP3
ffmpeg -i video.mp4 -vn -c:a libmp3lame -b:a 320k audio.mp3

# Extract to AAC
ffmpeg -i video.mp4 -vn -c:a aac -b:a 256k audio.m4a

# Extract to FLAC (lossless)
ffmpeg -i video.mp4 -vn -c:a flac audio.flac

# Extract to WAV (uncompressed)
ffmpeg -i video.mp4 -vn -c:a pcm_s16le audio.wav
```

### Convert Audio Formats

```bash
# MP3 to AAC
ffmpeg -i input.mp3 -c:a aac -b:a 256k output.m4a

# WAV to MP3
ffmpeg -i input.wav -c:a libmp3lame -b:a 320k output.mp3

# FLAC to MP3
ffmpeg -i input.flac -c:a libmp3lame -b:a 320k output.mp3

# Multiple files (batch)
for f in *.flac; do
  ffmpeg -i "$f" -c:a libmp3lame -b:a 320k "${f%.flac}.mp3"
done
```

### Quality Settings

```bash
# AAC VBR quality (1-5, higher = better)
ffmpeg -i input.wav -c:a aac -q:a 2 output.m4a

# MP3 VBR quality (0-9, lower = better)
ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3

# Opus with target bitrate
ffmpeg -i input.wav -c:a libopus -b:a 128k output.opus
```

## Audio Normalization

### Loudness Standards

| Standard | Target | TP (True Peak) | Use Case |
|----------|--------|----------------|----------|
| EBU R128 | -23 LUFS | -1 dBTP | European broadcast |
| ATSC A/85 | -24 LKFS | -2 dBTP | US broadcast |
| Spotify | -14 LUFS | -1 dBTP | Streaming |
| YouTube | -14 LUFS | -1 dBTP | Video platform |
| Apple Music | -16 LUFS | -1 dBTP | Music streaming |
| Podcast | -16 to -19 LUFS | -1 dBTP | Podcast |

### EBU R128 Normalization (loudnorm)

#### Single-Pass (Live/Real-time)
```bash
# Quick normalization (less accurate)
ffmpeg -i input.mp3 \
  -af loudnorm=I=-16:TP=-1.5:LRA=11 \
  output.mp3
```

#### Two-Pass (Recommended)

```bash
# Pass 1: Analyze
ffmpeg -i input.mp3 \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json \
  -f null -

# Output will include:
# "input_i": "-25.23"
# "input_tp": "-0.50"
# "input_lra": "8.32"
# "input_thresh": "-35.87"
# "target_offset": "1.23"

# Pass 2: Normalize with measured values
ffmpeg -i input.mp3 \
  -af loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=-25.23:measured_TP=-0.50:measured_LRA=8.32:measured_thresh=-35.87:offset=1.23:linear=true \
  -ar 48000 \
  output.mp3
```

#### Two-Pass Script

```bash
#!/bin/bash
# loudnorm-2pass.sh

INPUT="$1"
OUTPUT="$2"
TARGET_I="${3:--16}"
TARGET_TP="${4:--1.5}"
TARGET_LRA="${5:-11}"

# Pass 1: Analyze
stats=$(ffmpeg -i "$INPUT" \
  -af loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=${TARGET_LRA}:print_format=json \
  -f null - 2>&1 | grep -A 12 "Parsed_loudnorm")

# Extract values
input_i=$(echo "$stats" | grep input_i | tr -d '", ' | cut -d':' -f2)
input_tp=$(echo "$stats" | grep input_tp | tr -d '", ' | cut -d':' -f2)
input_lra=$(echo "$stats" | grep input_lra | tr -d '", ' | cut -d':' -f2)
input_thresh=$(echo "$stats" | grep input_thresh | tr -d '", ' | cut -d':' -f2)
offset=$(echo "$stats" | grep target_offset | tr -d '", ' | cut -d':' -f2)

# Pass 2: Normalize
ffmpeg -i "$INPUT" \
  -af "loudnorm=I=${TARGET_I}:TP=${TARGET_TP}:LRA=${TARGET_LRA}:measured_I=${input_i}:measured_TP=${input_tp}:measured_LRA=${input_lra}:measured_thresh=${input_thresh}:offset=${offset}:linear=true" \
  -ar 48000 \
  "$OUTPUT"
```

### Peak Normalization

```bash
# Normalize to peak level
ffmpeg -i input.mp3 \
  -af "volume=0dB:eval=once:precision=fixed" \
  -af "loudnorm=I=-16:TP=-1:LRA=11" \
  output.mp3

# Simple peak normalization
ffmpeg -i input.mp3 \
  -filter:a "volume=replaygain=peak" \
  output.mp3
```

### RMS Normalization

```bash
# Normalize to specific RMS level
ffmpeg -i input.mp3 \
  -af "loudnorm=I=-23:LRA=7:TP=-2" \
  output.mp3
```

### ffmpeg-normalize Tool

The `ffmpeg-normalize` Python utility provides an easier interface:

```bash
# Install
pip install ffmpeg-normalize

# Basic usage
ffmpeg-normalize input.mp3 -o output.mp3

# Custom target
ffmpeg-normalize input.mp3 -o output.mp3 -t -14

# Batch normalize (album mode - preserves relative loudness)
ffmpeg-normalize *.mp3 --batch -o normalized/

# Use built-in presets (v1.36.0+)
ffmpeg-normalize input.mp3 --preset podcast -o output.mp3
ffmpeg-normalize *.mp3 --preset music --batch -o normalized/
```

## Audio Filters

### Volume Control

```bash
# Increase volume by 50%
ffmpeg -i input.mp3 -af "volume=1.5" output.mp3

# Increase by 6dB
ffmpeg -i input.mp3 -af "volume=6dB" output.mp3

# Decrease by 3dB
ffmpeg -i input.mp3 -af "volume=-3dB" output.mp3
```

### Fade In/Out

```bash
# Fade in 3 seconds, fade out last 3 seconds
ffmpeg -i input.mp3 \
  -af "afade=t=in:ss=0:d=3,afade=t=out:st=57:d=3" \
  output.mp3

# Calculate fade out start automatically
duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp3)
fadeout_start=$(echo "$duration - 3" | bc)
ffmpeg -i input.mp3 \
  -af "afade=t=in:ss=0:d=3,afade=t=out:st=${fadeout_start}:d=3" \
  output.mp3
```

### Equalization

```bash
# Bass boost
ffmpeg -i input.mp3 \
  -af "equalizer=f=100:width_type=o:width=2:g=5" \
  output.mp3

# Treble reduction
ffmpeg -i input.mp3 \
  -af "equalizer=f=8000:width_type=o:width=2:g=-3" \
  output.mp3

# Multi-band EQ
ffmpeg -i input.mp3 \
  -af "equalizer=f=100:width_type=o:width=2:g=3,equalizer=f=1000:width_type=o:width=2:g=-2,equalizer=f=8000:width_type=o:width=2:g=2" \
  output.mp3
```

### High-Pass / Low-Pass Filters

```bash
# High-pass filter (remove below 80Hz)
ffmpeg -i input.mp3 -af "highpass=f=80" output.mp3

# Low-pass filter (remove above 8kHz)
ffmpeg -i input.mp3 -af "lowpass=f=8000" output.mp3

# Band-pass filter
ffmpeg -i input.mp3 -af "highpass=f=80,lowpass=f=12000" output.mp3
```

### Noise Reduction

```bash
# FFT-based noise reduction
ffmpeg -i input.mp3 \
  -af "afftdn=nf=-25" \
  output.mp3

# With noise floor adjustment
ffmpeg -i input.mp3 \
  -af "afftdn=nf=-20:tn=1" \
  output.mp3
```

### Compressor / Limiter

```bash
# Dynamic range compression
ffmpeg -i input.mp3 \
  -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50" \
  output.mp3

# Limiter
ffmpeg -i input.mp3 \
  -af "alimiter=limit=0.9:attack=5:release=50" \
  output.mp3

# De-esser
ffmpeg -i input.mp3 \
  -af "deesser=i=0.4:f=4000:w=0.5" \
  output.mp3
```

### Silence Detection/Removal

```bash
# Detect silence
ffmpeg -i input.mp3 \
  -af silencedetect=noise=-30dB:d=0.5 \
  -f null -

# Remove silence
ffmpeg -i input.mp3 \
  -af "silenceremove=start_periods=1:start_silence=0.5:start_threshold=-50dB:stop_periods=1:stop_silence=0.5:stop_threshold=-50dB" \
  output.mp3
```

## Channel Operations

### Stereo to Mono

```bash
# Average both channels
ffmpeg -i stereo.mp3 \
  -af "pan=mono|c0=0.5*c0+0.5*c1" \
  mono.mp3

# Use only left channel
ffmpeg -i stereo.mp3 -af "pan=mono|c0=c0" mono.mp3

# Downmix stereo to mono
ffmpeg -i stereo.mp3 -ac 1 mono.mp3
```

### Mono to Stereo

```bash
# Duplicate mono to both channels
ffmpeg -i mono.mp3 -af "pan=stereo|c0=c0|c1=c0" stereo.mp3

# Simple conversion
ffmpeg -i mono.mp3 -ac 2 stereo.mp3
```

### Extract Specific Channels

```bash
# Extract left channel
ffmpeg -i stereo.mp3 \
  -filter_complex "[0:a]channelsplit=channel_layout=stereo:channels=FL[left]" \
  -map "[left]" left.mp3

# Extract right channel
ffmpeg -i stereo.mp3 \
  -filter_complex "[0:a]channelsplit=channel_layout=stereo:channels=FR[right]" \
  -map "[right]" right.mp3
```

### 5.1 Surround Operations

```bash
# Downmix 5.1 to stereo
ffmpeg -i surround.ac3 \
  -af "pan=stereo|FL=0.5*FC+0.707*FL+0.707*BL+0.5*LFE|FR=0.5*FC+0.707*FR+0.707*BR+0.5*LFE" \
  stereo.mp3

# Extract center channel
ffmpeg -i surround.ac3 \
  -filter_complex "[0:a]channelsplit=channel_layout=5.1:channels=FC[center]" \
  -map "[center]" center.mp3
```

## Sample Rate & Bit Depth

### Sample Rate Conversion

```bash
# Convert to 44.1kHz
ffmpeg -i input.wav -ar 44100 output.wav

# Convert to 48kHz
ffmpeg -i input.wav -ar 48000 output.wav

# High-quality resampling
ffmpeg -i input.wav \
  -af "aresample=resampler=soxr:precision=33:cheby=1" \
  -ar 44100 output.wav
```

### Bit Depth Conversion

```bash
# Convert to 16-bit
ffmpeg -i input.wav -c:a pcm_s16le output.wav

# Convert to 24-bit
ffmpeg -i input.wav -c:a pcm_s24le output.wav

# Convert to 32-bit float
ffmpeg -i input.wav -c:a pcm_f32le output.wav
```

## Speed & Pitch

### Speed Change (Affects Pitch)

```bash
# 2x speed (chipmunk effect)
ffmpeg -i input.mp3 -af "atempo=2.0" output.mp3

# 0.5x speed (slow motion)
ffmpeg -i input.mp3 -af "atempo=0.5" output.mp3

# For >2x, chain filters
ffmpeg -i input.mp3 -af "atempo=2.0,atempo=2.0" output.mp3  # 4x
```

### Pitch Change (Preserves Speed)

```bash
# Pitch shift using rubberband
ffmpeg -i input.mp3 \
  -af "rubberband=pitch=1.5" \
  output.mp3

# Pitch shift semitones
ffmpeg -i input.mp3 \
  -af "asetrate=44100*2^(2/12),aresample=44100" \
  output.mp3  # +2 semitones
```

## Trimming & Concatenation

### Trim Audio

```bash
# Extract 30 seconds starting at 1 minute
ffmpeg -ss 00:01:00 -i input.mp3 -t 00:00:30 -c copy output.mp3

# Extract from 1:00 to 2:30
ffmpeg -ss 00:01:00 -to 00:02:30 -i input.mp3 -c copy output.mp3
```

### Concatenate Audio

```bash
# Create file list
echo "file 'part1.mp3'" > list.txt
echo "file 'part2.mp3'" >> list.txt

# Concatenate (same format)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp3

# Concatenate with re-encode
ffmpeg -f concat -safe 0 -i list.txt -c:a aac -b:a 256k output.m4a
```

### Crossfade

```bash
# Crossfade two files (3 second overlap)
ffmpeg -i part1.mp3 -i part2.mp3 \
  -filter_complex "acrossfade=d=3:c1=tri:c2=tri" \
  output.mp3
```

## Professional Workflows

### Podcast Processing

```bash
# Complete podcast processing chain
ffmpeg -i raw_podcast.wav \
  -af "highpass=f=80,\
       acompressor=threshold=-20dB:ratio=4:attack=5:release=50,\
       loudnorm=I=-16:TP=-1.5:LRA=11,\
       silenceremove=start_periods=1:start_silence=1:start_threshold=-50dB" \
  -c:a aac -b:a 96k \
  podcast.m4a
```

### Music Mastering Chain

```bash
# Mastering chain
ffmpeg -i mix.wav \
  -af "equalizer=f=60:width_type=o:width=1:g=1,\
       equalizer=f=12000:width_type=o:width=1:g=0.5,\
       acompressor=threshold=-12dB:ratio=2:attack=20:release=200,\
       alimiter=limit=0.95,\
       loudnorm=I=-14:TP=-1:LRA=9" \
  -c:a flac \
  master.flac
```

### Broadcast Normalization

```bash
# EBU R128 broadcast compliance
ffmpeg -i input.wav \
  -af "loudnorm=I=-23:TP=-1:LRA=11:dual_mono=true" \
  -ar 48000 \
  -c:a pcm_s24le \
  broadcast.wav
```

## Troubleshooting

### Common Issues

**"loudnorm resamples to 192kHz"**
```bash
# Force output sample rate
ffmpeg -i input.mp3 \
  -af loudnorm=I=-16:TP=-1.5:LRA=11 \
  -ar 48000 \
  output.mp3
```

**Audio/video sync after processing**
```bash
# Maintain sync with video
ffmpeg -i video.mp4 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=async=1" \
  -c:v copy \
  output.mp4
```

**Quality loss from re-encoding**
- Use lossless intermediate format (FLAC, WAV)
- Avoid multiple lossy conversions
- Use high bitrates for final lossy encode

## Audio Analysis & Measurement

### Audio Statistics (astats)

Measure comprehensive audio statistics including RMS, peak levels, crest factor, bit depth, and DC offset.

```bash
# Full audio statistics
ffmpeg -i input.mp3 -af "astats=metadata=1:reset=1" -f null -

# Output includes:
# - RMS level and peak level
# - Crest factor
# - Dynamic range
# - DC offset
# - Min/Max sample values
# - Number of samples

# Per-channel statistics
ffmpeg -i input.mp3 -af "astats=metadata=1:reset=1:measure_perchannel=all" -f null -

# Measure specific metrics
ffmpeg -i input.mp3 -af "astats=measure_overall=RMS_level+Peak_level:reset=1" -f null -
```

**astats Metrics:**
| Metric | Description |
|--------|-------------|
| `DC_offset` | DC bias in signal |
| `Min_level` | Minimum sample value |
| `Max_level` | Maximum sample value |
| `Min_difference` | Minimum sample-to-sample difference |
| `Max_difference` | Maximum sample-to-sample difference |
| `Mean_difference` | Average sample-to-sample difference |
| `RMS_level` | Root Mean Square level (dB) |
| `Peak_level` | Peak level (dB) |
| `RMS_peak` | RMS peak level |
| `RMS_trough` | RMS trough level |
| `Crest_factor` | Peak to RMS ratio |
| `Flat_factor` | Flatness measure |
| `Peak_count` | Number of samples at peak |
| `Bit_depth` | Actual bit depth used |
| `Dynamic_range` | Dynamic range in dB |

### EBU R128 Loudness Measurement (ebur128)

Comprehensive loudness measurement per EBU R128 / ITU-R BS.1770 standards.

```bash
# Basic loudness measurement
ffmpeg -i input.mp3 -af "ebur128=peak=true" -f null -

# Output includes:
# - Momentary loudness (M)
# - Short-term loudness (S)
# - Integrated loudness (I)
# - Loudness Range (LRA)
# - True Peak (dBTP)

# Frame-by-frame measurement
ffmpeg -i input.mp3 -af "ebur128=framelog=verbose:peak=true" -f null - 2>&1 | grep Summary

# Generate loudness graph (PNG)
ffmpeg -i input.mp3 \
  -filter_complex "ebur128=video=1:meter=18:gauge=1[v];[v]scale=1280:720[out]" \
  -map "[out]" \
  -frames:v 1 \
  loudness_graph.png

# Create loudness monitoring video
ffmpeg -i input.mp3 \
  -filter_complex "ebur128=video=1:meter=18:gauge=1:scale=absolute[v]" \
  -map "[v]" -map 0:a \
  -c:a copy \
  loudness_monitor.mp4

# Measure with dual mono (speech)
ffmpeg -i input.mp3 -af "ebur128=dualmono=1:peak=true" -f null -
```

**ebur128 Parameters:**
| Parameter | Description | Values |
|-----------|-------------|--------|
| `video` | Generate video output | 0 or 1 |
| `meter` | Loudness meter level | 9, 12, 18 |
| `gauge` | Show gauge overlay | 0 or 1 |
| `scale` | Scale type | `absolute`, `relative` |
| `peak` | Measure true peak | `true`, `sample`, `none` |
| `dualmono` | Dual mono mode | 0 or 1 |
| `framelog` | Logging level | `quiet`, `info`, `verbose` |

### Speech Normalization (speechnorm)

Specialized normalizer for speech content that adapts to dynamic speech patterns.

```bash
# Basic speech normalization
ffmpeg -i speech.mp3 -af "speechnorm" output.mp3

# Speech normalization with custom parameters
ffmpeg -i speech.mp3 \
  -af "speechnorm=p=0.95:m=10:r=0.0005:l=1" \
  output.mp3

# Aggressive speech normalization
ffmpeg -i speech.mp3 \
  -af "speechnorm=p=0.9:e=15:r=0.001:l=1" \
  output.mp3

# Podcast processing with speech normalization
ffmpeg -i podcast.wav \
  -af "highpass=f=80,speechnorm=p=0.95:e=12.5:r=0.0005,loudnorm=I=-16:TP=-1.5" \
  -c:a aac -b:a 96k \
  podcast.m4a
```

**speechnorm Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `p` | Peak value target | 0.95 | 0-1 |
| `e` | Expansion factor | 12.5 | 1-50 |
| `r` | Rise time (speed of increase) | 0.0005 | 0-1 |
| `f` | Fall time (speed of decrease) | 0.001 | 0-1 |
| `c` | Compression factor | 0 | 0-1 |
| `l` | Link channels | 0 | 0 or 1 |

### Dialogue Enhancement (dialoguenhance) - FFmpeg 8.0+

Enhance dialogue clarity by separating and boosting voice frequencies.

```bash
# Basic dialogue enhancement
ffmpeg -i input.mp4 -af "dialoguenhance" -c:v copy output.mp4

# Custom dialogue enhancement
ffmpeg -i input.mp4 \
  -af "dialoguenhance=original=0.3:enhance=0.7:voice=0.8" \
  -c:v copy output.mp4

# Heavy enhancement for poor recordings
ffmpeg -i input.mp4 \
  -af "dialoguenhance=original=0.2:enhance=0.9" \
  -c:v copy output.mp4
```

**dialoguenhance Parameters:**
| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `original` | Original signal mix | 1 | 0-1 |
| `enhance` | Enhanced signal mix | 1 | 0-1 |
| `voice` | Voice clarity boost | 2 | 2-32 |

### 3D Audio / Binaural (sofalizer)

Apply HRTF (Head-Related Transfer Function) for 3D audio and binaural processing using SOFA files.

```bash
# Basic binaural conversion (requires SOFA file)
ffmpeg -i surround.ac3 \
  -af "sofalizer=sofa=/path/to/hrtf.sofa" \
  binaural.mp3

# With custom gain and rotation
ffmpeg -i surround.ac3 \
  -af "sofalizer=sofa=/path/to/hrtf.sofa:gain=0:rotation=0" \
  binaural.mp3

# Binaural conversion with elevation
ffmpeg -i surround.ac3 \
  -af "sofalizer=sofa=/path/to/hrtf.sofa:elevation=0:radius=1" \
  binaural.mp3
```

**SOFA Files:**
- Download HRTF databases from: https://sofacoustics.org/data/database/
- Common formats: CIPIC, MIT KEMAR, LISTEN databases

**sofalizer Parameters:**
| Parameter | Description | Range |
|-----------|-------------|-------|
| `sofa` | Path to SOFA file | - |
| `gain` | Additional gain (dB) | -20 to 40 |
| `rotation` | Head rotation (degrees) | -360 to 360 |
| `elevation` | Head elevation (degrees) | -90 to 90 |
| `radius` | Distance scaling | 0 to 3 |
| `type` | Interpolation type | `time`, `freq` |

### Volume Detection

```bash
# Detect volume levels
ffmpeg -i input.mp3 -af "volumedetect" -f null -

# Output includes:
# - mean_volume (average)
# - max_volume (peak)
# - histogram data
```

### A-Weighting (aweighting)

Apply A-weighting curve for perceived loudness measurement.

```bash
# Apply A-weighting filter
ffmpeg -i input.mp3 -af "aweighting" output_aweighted.wav

# Measure A-weighted levels
ffmpeg -i input.mp3 -af "aweighting,astats=measure_overall=RMS_level" -f null -
```

### Audio Fingerprinting (chromaprint)

Generate audio fingerprints for identification.

```bash
# Generate chromaprint fingerprint
ffmpeg -i input.mp3 -f chromaprint -fp_format raw fingerprint.txt

# Generate Base64 fingerprint
ffmpeg -i input.mp3 -f chromaprint -fp_format base64 - 2>&1 | grep FINGERPRINT
```

### Complete Analysis Workflow

```bash
#!/bin/bash
# audio-analysis.sh - Complete audio analysis

INPUT="$1"

echo "=== Audio Analysis Report ==="
echo "File: $INPUT"
echo ""

echo "--- Basic Statistics ---"
ffmpeg -i "$INPUT" -af "astats=measure_overall=all" -f null - 2>&1 | grep -A 50 "Parsed_astats"

echo ""
echo "--- Loudness (EBU R128) ---"
ffmpeg -i "$INPUT" -af "ebur128=peak=true" -f null - 2>&1 | grep -E "(Summary|I:|LRA:|Peak:)"

echo ""
echo "--- Volume Detection ---"
ffmpeg -i "$INPUT" -af "volumedetect" -f null - 2>&1 | grep -E "(mean_volume|max_volume)"

echo ""
echo "--- Silence Detection ---"
ffmpeg -i "$INPUT" -af "silencedetect=noise=-50dB:d=0.5" -f null - 2>&1 | grep silence
```

This guide covers FFmpeg audio processing. For video operations, see the fundamentals skill. For noise reduction details, see `ffmpeg-noise-reduction`.
