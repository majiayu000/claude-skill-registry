---
name: ffmpeg-captions-subtitles
description: Complete subtitle and caption system for FFmpeg 7.1 LTS and 8.0.1 (latest stable, released 2025-11-20). PROACTIVELY activate for: (1) Burning subtitles (hardcoding SRT/ASS/VTT), (2) Adding soft subtitle tracks, (3) Extracting subtitles from video, (4) Subtitle format conversion, (5) Styled captions (font, color, outline, shadow), (6) Subtitle positioning and alignment, (7) CEA-608/708 closed captions, (8) Text overlays with drawtext, (9) Whisper AI automatic transcription (FFmpeg 8.0+ with VAD, multi-language, GPU), (10) Batch subtitle processing. Provides: Format reference tables, styling parameter guide, position alignment charts, Whisper model comparison, VAD configuration, dynamic text examples, accessibility best practices. Ensures: Professional captions with proper styling and accessibility compliance.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

## Quick Reference

| Task | Command |
|------|---------|
| Burn SRT | `ffmpeg -i video.mp4 -vf "subtitles=subs.srt" output.mp4` |
| Burn ASS | `ffmpeg -i video.mp4 -vf "ass=subs.ass" output.mp4` |
| Add soft sub | `ffmpeg -i video.mp4 -i subs.srt -c copy -c:s mov_text output.mp4` |
| Extract sub | `ffmpeg -i video.mkv -map 0:s:0 output.srt` |
| Style subs | `-vf "subtitles=s.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF'"` |
| Text overlay | `-vf "drawtext=text='Hello':x=10:y=10:fontsize=24:fontcolor=white"` |

| Format | Extension | Best For |
|--------|-----------|----------|
| SRT | .srt | Simple, universal |
| ASS | .ass | Styled, animated, anime |
| VTT | .vtt | Web/HTML5 video |

## When to Use This Skill

Use for **subtitle and caption operations**:
- Hardcoding (burning) subtitles into video
- Adding soft subtitle tracks to containers
- Extracting subtitles from MKV/MP4
- Styling captions (font, color, position)
- Dynamic text overlays

---

# FFmpeg Captions and Subtitles (2025)

Complete guide to working with subtitles, closed captions, and text overlays using FFmpeg.

## Subtitle Format Reference

### Supported Formats

| Format | Extension | Features | Use Case |
|--------|-----------|----------|----------|
| SubRip | .srt | Simple timing + text | Universal, web |
| Advanced SubStation Alpha | .ass/.ssa | Rich styling, positioning, effects | Anime, styled subs |
| WebVTT | .vtt | Web standard, cues, styling | HTML5 video |
| TTML/DFXP | .ttml/.dfxp | Broadcast, accessibility | Streaming services |
| MOV Text | .mov (embedded) | QuickTime native | Apple ecosystem |
| DVB Subtitle | (embedded) | Bitmap-based | European broadcast |
| PGS | .sup | Blu-ray bitmap subtitles | Blu-ray |
| CEA-608/708 | (embedded) | Closed captions | US broadcast, streaming |

### Format Characteristics

```
SRT (SubRip):
- Simple text-based format
- Supports basic HTML tags (<b>, <i>, <u>)
- Widely compatible
- No positioning or advanced styling

ASS/SSA:
- Advanced styling (fonts, colors, outlines)
- Precise positioning anywhere on screen
- Animation and effects support
- Karaoke timing

WebVTT:
- HTML5 standard format
- CSS-like styling
- Cue settings for positioning
- Speaker identification
```

## Burning Subtitles (Hardcoding)

### Basic Subtitle Burn-in

```bash
# Burn SRT subtitles
ffmpeg -i video.mp4 -vf "subtitles=subs.srt" output.mp4

# Burn ASS/SSA subtitles (preserves styling)
ffmpeg -i video.mp4 -vf "ass=subs.ass" output.mp4

# Burn subtitles from MKV container
ffmpeg -i video.mkv -vf "subtitles=video.mkv" output.mp4

# Burn specific subtitle track (index 0)
ffmpeg -i video.mkv -vf "subtitles=video.mkv:si=0" output.mp4

# Burn subtitles with stream index
ffmpeg -i video.mkv -vf "subtitles=video.mkv:stream_index=1" output.mp4
```

### Styled Subtitle Burn-in

```bash
# Force style (overrides subtitle styling)
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Shadow=1'" \
  output.mp4

# Yellow subtitles with black outline
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:force_style='FontSize=28,PrimaryColour=&H00FFFF,OutlineColour=&H000000,Outline=3'" \
  output.mp4

# Larger font for accessibility
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:force_style='FontSize=36,Bold=1'" \
  output.mp4
```

### ASS Style Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| FontName | Font family | `FontName=Arial` |
| FontSize | Size in points | `FontSize=24` |
| PrimaryColour | Text color (AABBGGRR) | `PrimaryColour=&HFFFFFF` |
| SecondaryColour | Karaoke color | `SecondaryColour=&H00FFFF` |
| OutlineColour | Outline/border color | `OutlineColour=&H000000` |
| BackColour | Shadow/background color | `BackColour=&H80000000` |
| Bold | Bold text (0/1) | `Bold=1` |
| Italic | Italic text (0/1) | `Italic=1` |
| Underline | Underlined text (0/1) | `Underline=1` |
| Outline | Outline width | `Outline=2` |
| Shadow | Shadow depth | `Shadow=1` |
| Alignment | Position (numpad style) | `Alignment=2` |
| MarginL/R/V | Margins in pixels | `MarginV=50` |

### Color Format (ASS)

```
ASS uses &HAABBGGRR format (Alpha, Blue, Green, Red):
- White: &HFFFFFF or &H00FFFFFF
- Black: &H000000 or &H00000000
- Yellow: &H00FFFF (00-Blue, FF-Green, FF-Red)
- Red: &H0000FF
- Blue: &HFF0000
- 50% transparent black: &H80000000
```

## Adding Subtitle Tracks (Soft Subs)

### Embed SRT as Track

```bash
# Add SRT to MP4 (MOV text)
ffmpeg -i video.mp4 -i subs.srt \
  -c copy -c:s mov_text \
  output.mp4

# Add SRT to MKV
ffmpeg -i video.mp4 -i subs.srt \
  -c copy -c:s srt \
  output.mkv

# Add SRT to WebM (WebVTT)
ffmpeg -i video.webm -i subs.srt \
  -c copy -c:s webvtt \
  output.webm
```

### Multiple Subtitle Tracks

```bash
# Add multiple languages
ffmpeg -i video.mp4 -i subs_en.srt -i subs_es.srt -i subs_fr.srt \
  -map 0:v -map 0:a -map 1 -map 2 -map 3 \
  -c copy -c:s mov_text \
  -metadata:s:s:0 language=eng -metadata:s:s:0 title="English" \
  -metadata:s:s:1 language=spa -metadata:s:s:1 title="Spanish" \
  -metadata:s:s:2 language=fra -metadata:s:s:2 title="French" \
  output.mp4

# Add ASS subtitles to MKV (preserves styling)
ffmpeg -i video.mp4 -i styled.ass \
  -map 0 -map 1 \
  -c copy -c:s ass \
  output.mkv
```

### Set Default Subtitle Track

```bash
# Set subtitle as default
ffmpeg -i video.mp4 -i subs.srt \
  -c copy -c:s mov_text \
  -disposition:s:0 default \
  output.mp4

# Set forced subtitles (always display)
ffmpeg -i video.mp4 -i forced.srt \
  -c copy -c:s mov_text \
  -disposition:s:0 forced \
  output.mp4
```

## Extracting Subtitles

### Extract to External File

```bash
# Extract first subtitle track to SRT
ffmpeg -i video.mkv -map 0:s:0 output.srt

# Extract specific subtitle stream
ffmpeg -i video.mkv -map 0:s:1 output.srt

# Extract to ASS format
ffmpeg -i video.mkv -map 0:s:0 output.ass

# Extract to WebVTT
ffmpeg -i video.mkv -map 0:s:0 output.vtt

# Extract all subtitle tracks
ffmpeg -i video.mkv -map 0:s subs_%d.srt
```

### List Available Subtitle Tracks

```bash
# Show all streams including subtitles
ffprobe -v error -show_entries stream=index,codec_name,codec_type:stream_tags=language,title \
  -of csv=p=0 video.mkv

# Show only subtitle streams
ffprobe -v error -select_streams s \
  -show_entries stream=index,codec_name:stream_tags=language,title \
  -of csv=p=0 video.mkv
```

### Convert Subtitle Formats

```bash
# SRT to ASS
ffmpeg -i subs.srt subs.ass

# ASS to SRT (loses styling)
ffmpeg -i subs.ass subs.srt

# SRT to WebVTT
ffmpeg -i subs.srt subs.vtt

# WebVTT to SRT
ffmpeg -i subs.vtt subs.srt
```

## Text Overlays (drawtext)

### Basic Text Overlay

```bash
# Simple text overlay
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Hello World':x=10:y=10:fontsize=24:fontcolor=white" \
  output.mp4

# Centered text
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Centered Text':x=(w-tw)/2:y=(h-th)/2:fontsize=48:fontcolor=white" \
  output.mp4

# Text at bottom center
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Bottom Text':x=(w-tw)/2:y=h-th-20:fontsize=32:fontcolor=white" \
  output.mp4
```

### Styled Text Overlays

```bash
# Text with background box
ffmpeg -i video.mp4 \
  -vf "drawtext=text='With Background':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=5" \
  output.mp4

# Text with outline (border)
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Outlined Text':x=10:y=10:fontsize=48:fontcolor=white:borderw=3:bordercolor=black" \
  output.mp4

# Shadow effect
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Shadow Text':x=10:y=10:fontsize=36:fontcolor=white:shadowcolor=black:shadowx=3:shadowy=3" \
  output.mp4

# Custom font
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Custom Font':fontfile=/path/to/font.ttf:fontsize=24:fontcolor=white" \
  output.mp4
```

### Dynamic Text

```bash
# Display timestamp
ffmpeg -i video.mp4 \
  -vf "drawtext=text='%{pts\:hms}':x=10:y=10:fontsize=24:fontcolor=white" \
  output.mp4

# Display frame number
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Frame\: %{n}':x=10:y=10:fontsize=24:fontcolor=white" \
  output.mp4

# Display current date/time
ffmpeg -i video.mp4 \
  -vf "drawtext=text='%{localtime\:%Y-%m-%d %H\\\:%M\\\:%S}':x=10:y=10:fontsize=24:fontcolor=white" \
  output.mp4

# Text from file
ffmpeg -i video.mp4 \
  -vf "drawtext=textfile=message.txt:x=10:y=10:fontsize=24:fontcolor=white:reload=1" \
  output.mp4
```

### Animated Text

```bash
# Scrolling text (credits)
ffmpeg -i video.mp4 \
  -vf "drawtext=textfile=credits.txt:x=(w-tw)/2:y=h-t*50:fontsize=24:fontcolor=white" \
  output.mp4

# Fade in text
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Fade In':x=(w-tw)/2:y=(h-th)/2:fontsize=48:fontcolor=white:alpha='if(lt(t,1),t,1)'" \
  output.mp4

# Text appears at specific time (3 seconds)
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Appears at 3s':x=10:y=10:fontsize=24:fontcolor=white:enable='gte(t,3)'" \
  output.mp4

# Text visible between 2-5 seconds
ffmpeg -i video.mp4 \
  -vf "drawtext=text='Visible 2-5s':x=10:y=10:fontsize=24:fontcolor=white:enable='between(t,2,5)'" \
  output.mp4

# Blinking text
ffmpeg -i video.mp4 \
  -vf "drawtext=text='BLINK':x=10:y=10:fontsize=36:fontcolor=red:alpha='if(mod(floor(t*2),2),1,0)'" \
  output.mp4
```

## Whisper AI Integration (FFmpeg 8.0+)

FFmpeg 8.0 integrates OpenAI's Whisper speech recognition model via whisper.cpp, enabling fully local and offline automatic transcription and subtitle generation.

### Features
- **Speech to Text**: High accuracy transcription
- **Multi-language**: 99 languages supported
- **Flexible Output**: SRT subtitles, JSON, or plain text
- **GPU Acceleration**: Uses system GPU by default
- **Voice Activity Detection**: Silero VAD support for better segmentation
- **Real-time**: Works with live audio streams

### Generate SRT Subtitles

```bash
# Generate subtitles from video using Whisper
ffmpeg -i video.mp4 -vn \
  -af "whisper=model=ggml-base.bin:language=auto:queue=3:destination=output.srt:format=srt" \
  -f null -

# Specify language for better accuracy
ffmpeg -i video.mp4 -vn \
  -af "whisper=model=ggml-base.bin:language=en:destination=english.srt:format=srt" \
  -f null -

# Use larger model for higher quality
ffmpeg -i video.mp4 -vn \
  -af "whisper=model=ggml-medium.bin:language=auto:destination=output.srt:format=srt" \
  -f null -
```

### Live Transcription

```bash
# Live transcription from microphone (Linux PulseAudio)
ffmpeg -loglevel warning -f pulse -i default \
  -af "highpass=f=200,lowpass=f=3000,whisper=model=ggml-medium-q5_0.bin:language=en:queue=10:destination=-:format=json:vad_model=for-tests-silero-v5.1.2-ggml.bin" \
  -f null -

# Live transcription from microphone (Windows)
ffmpeg -loglevel warning -f dshow -i audio="Microphone" \
  -af "whisper=model=ggml-base.bin:language=en:queue=10:destination=-:format=text" \
  -f null -

# Live transcription from microphone (macOS)
ffmpeg -loglevel warning -f avfoundation -i ":0" \
  -af "whisper=model=ggml-base.bin:language=en:queue=10:destination=-:format=text" \
  -f null -
```

### Display Live Subtitles on Video

```bash
# Whisper writes to frame metadata, drawtext reads it
ffmpeg -i input.mp4 \
  -af "whisper=model=ggml-base.en.bin:language=en" \
  -vf "drawtext=text='%{metadata\:lavfi.whisper.text}':fontsize=24:fontcolor=white:x=10:y=h-th-10:box=1:boxcolor=black@0.5:boxborderw=5" \
  output_with_subtitles.mp4

# Centered subtitles with styling
ffmpeg -i input.mp4 \
  -af "whisper=model=ggml-base.bin:language=auto" \
  -vf "drawtext=text='%{metadata\:lavfi.whisper.text}':fontsize=32:fontcolor=white:x=(w-tw)/2:y=h-th-50:borderw=2:bordercolor=black" \
  output.mp4
```

### JSON Output for Post-Processing

```bash
# Generate JSON for custom processing
ffmpeg -i video.mp4 -vn \
  -af "whisper=model=ggml-base.bin:language=auto:destination=output.json:format=json" \
  -f null -
```

### With Voice Activity Detection (VAD)

```bash
# Use Silero VAD for better speech detection
ffmpeg -i video.mp4 -vn \
  -af "whisper=model=ggml-base.bin:language=en:queue=20:destination=output.srt:format=srt:vad_model=for-tests-silero-v5.1.2-ggml.bin:vad_threshold=0.5" \
  -f null -

# VAD parameters for noisy audio
ffmpeg -i noisy_video.mp4 -vn \
  -af "whisper=model=ggml-medium.bin:language=en:queue=20:destination=output.srt:format=srt:vad_model=silero.bin:vad_threshold=0.6:vad_min_speech_duration=0.2:vad_min_silence_duration=0.3" \
  -f null -
```

### Disable GPU (CPU-only processing)

```bash
# Force CPU processing (slower but works without GPU)
ffmpeg -i video.mp4 -vn \
  -af "whisper=model=ggml-base.bin:language=en:use_gpu=false:destination=output.srt:format=srt" \
  -f null -
```

### Whisper Models

| Model | Size | Speed | Quality | VRAM | Recommended For |
|-------|------|-------|---------|------|-----------------|
| tiny | 39 MB | Fastest | Basic | ~1 GB | Quick previews, low-resource |
| base | 74 MB | Fast | Good | ~1 GB | General use, balanced |
| small | 244 MB | Medium | Better | ~2 GB | Higher accuracy |
| medium | 769 MB | Slow | High | ~5 GB | Quality-critical |
| large | 1.55 GB | Slowest | Best | ~10 GB | Maximum accuracy |

### Whisper Filter Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `model` | Path to GGML model file | Required |
| `language` | Language code or "auto" | "auto" |
| `format` | Output format: "text", "srt", "json" | "text" |
| `destination` | Output file path or "-" for stdout | Required |
| `queue` | Buffer size in seconds | 3 |
| `vad_model` | Path to Silero VAD model | None |
| `vad_threshold` | VAD sensitivity (0-1) | 0.5 |
| `vad_min_speech_duration` | Min speech duration (seconds) | 0.1 |
| `vad_min_silence_duration` | Min silence duration (seconds) | 0.5 |
| `use_gpu` | Enable GPU acceleration | true |

### Model Download

Download GGML models from the whisper.cpp project:
```bash
# Download base model
curl -L -o ggml-base.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin

# Download medium model for better quality
curl -L -o ggml-medium.bin https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.bin
```

## CEA-608/708 Closed Captions

### Extract Closed Captions

```bash
# Extract CEA-608 captions from ATSC stream
ffmpeg -f lavfi -i "movie=broadcast.ts[out0+subcc]" -map 0:1 captions.srt

# Extract from video with embedded CC
ffmpeg -i video_with_cc.mp4 \
  -filter_complex "[0:v]format=yuv420p[v];[0:v]crop=1:1:0:0[c]" \
  -map "[c]" -c:v libx264 -f null - 2>&1 | grep -A 1 "Closed caption"
```

### Add CEA-608 Captions

```bash
# Embed CEA-608 captions (requires eia608 line)
ffmpeg -i video.mp4 -i captions.scc \
  -c:v libx264 -c:a copy \
  -vf "movie=captions.scc[captions];[0:v][captions]overlay" \
  output.mp4
```

## Subtitle Positioning

### ASS Alignment Values

```
7 (top-left)     8 (top-center)     9 (top-right)
4 (mid-left)     5 (mid-center)     6 (mid-right)
1 (bottom-left)  2 (bottom-center)  3 (bottom-right)
```

### Position Examples

```bash
# Top center subtitles
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:force_style='Alignment=8,MarginV=20'" \
  output.mp4

# Left-aligned subtitles
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:force_style='Alignment=1,MarginL=50,MarginV=30'" \
  output.mp4

# Right side for speaker identification
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:force_style='Alignment=3,MarginR=50'" \
  output.mp4
```

### Multiple Subtitle Positions

```bash
# Two subtitle tracks at different positions
ffmpeg -i video.mp4 \
  -vf "[in]subtitles=speaker1.srt:force_style='Alignment=1,MarginL=50'[tmp];\
       [tmp]subtitles=speaker2.srt:force_style='Alignment=3,MarginR=50'" \
  output.mp4
```

## Batch Processing

### Burn Subtitles to Multiple Videos

```bash
#!/bin/bash
# burn_subs_batch.sh

for video in *.mp4; do
    base="${video%.mp4}"
    if [ -f "${base}.srt" ]; then
        ffmpeg -i "$video" \
          -vf "subtitles=${base}.srt:force_style='FontSize=24,Outline=2'" \
          -c:a copy \
          "output/${base}_subbed.mp4"
    fi
done
```

### Convert Subtitle Format Batch

```bash
#!/bin/bash
# convert_subs.sh

for srt in *.srt; do
    base="${srt%.srt}"
    ffmpeg -i "$srt" "${base}.vtt"
done
```

## Troubleshooting

### Common Issues

**"Unable to find a suitable output format"**
```bash
# Specify output format explicitly
ffmpeg -i video.mkv -map 0:s:0 -f srt output.srt
```

**Garbled characters in subtitles**
```bash
# Force UTF-8 encoding
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:charenc=UTF-8" \
  output.mp4
```

**Font not found**
```bash
# Specify fonts directory
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:fontsdir=/path/to/fonts" \
  output.mp4

# List available fonts
fc-list : family | sort | uniq
```

**Subtitle timing offset**
```bash
# Delay subtitles by 2 seconds
ffmpeg -i video.mp4 \
  -vf "subtitles=subs.srt:itsoffset=2" \
  output.mp4

# Or use setpts to adjust
ffmpeg -i subs.srt -itsoffset 2 delayed.srt
```

**Subtitle not showing on high-res video**
```bash
# Scale subtitle rendering to video resolution
ffmpeg -i video_4k.mp4 \
  -vf "subtitles=subs.srt:force_style='FontSize=48,Outline=3'" \
  output.mp4
```

### Verification Commands

```bash
# Check if subtitles are present
ffprobe -v error -select_streams s -show_entries stream=codec_name -of default=nw=1 video.mp4

# Count subtitle lines
grep -c "^[0-9]" subs.srt

# Validate SRT format
ffmpeg -i subs.srt -f null -
```

## Best Practices

### Accessibility
1. Use high contrast colors (white on dark, yellow on dark)
2. Minimum font size of 24pt for standard video
3. Include speaker identification for multiple speakers
4. Position subtitles to avoid obscuring important visual content
5. Keep lines short (42 characters max per line)
6. Display duration: minimum 1 second, maximum 7 seconds per caption

### Quality
1. Use ASS format for styled subtitles (anime, music videos)
2. Use SRT for simple dialogue
3. Use WebVTT for web delivery
4. Preserve original styling when possible
5. Test on target devices before distribution

### Performance
1. Burn subtitles only when necessary (streaming, compatibility)
2. Prefer soft subs for archival and flexibility
3. Use hardware encoding when burning subtitles to large files
4. Process in parallel for batch operations

This guide covers FFmpeg subtitle and caption operations. For text overlays with shapes and graphics, see the shapes-graphics skill.
