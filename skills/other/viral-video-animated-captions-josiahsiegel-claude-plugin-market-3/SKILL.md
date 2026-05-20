---
name: viral-video-animated-captions
description: CapCut-style animated word-level captions for viral video with FFmpeg. PROACTIVELY activate for: (1) Word-by-word caption highlighting, (2) Animated subtitle effects, (3) CapCut-style captions, (4) Karaoke-style text, (5) Bounce/pop text animations, (6) Color-changing words, (7) Emoji integration in captions, (8) Multi-style caption presets, (9) Trending caption styles, (10) Social media caption optimization. Provides: ASS subtitle generation scripts, word-level timing workflows, animation presets, color schemes, font recommendations, and platform-specific caption styles for TikTok, YouTube Shorts, and Instagram Reels.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

# CapCut-Style Animated Captions (2025-2026)

## Why Animated Captions Matter

- **80% engagement boost** when captions are present
- **85% of social video** is watched without sound
- **Animated word highlighting** increases retention by 25-40%
- CapCut-style captions are now **expected** by viewers

---

## Quick Reference

| Style | Effect | Best For |
|-------|--------|----------|
| Word Pop | Words bounce in one at a time | High energy, Gen Z |
| Highlight Sweep | Color sweeps across words | Professional, educational |
| Karaoke | Words light up with audio timing | Music, voiceover |
| Typewriter | Characters appear sequentially | Storytelling, dramatic |
| Scale Pulse | Words pulse larger on appear | Emphasis, key points |

---

## Caption Workflow Overview

### Standard Workflow

1. **Generate transcript** with word-level timestamps (Whisper)
2. **Convert to ASS format** with animation styles
3. **Burn captions** into video with FFmpeg

---

## Step 1: Generate Word-Level Timestamps

### Using Whisper (FFmpeg 8.0+)

```bash
# Generate JSON with word-level timestamps
ffmpeg -i input.mp4 -vn \
  -af "whisper=model=ggml-base.bin:language=auto:format=json" \
  transcript.json
```

### Using whisper.cpp Directly (More Control)

```bash
# Generate word-level JSON
whisper.cpp/main -m ggml-base.bin -f audio.wav -ojf -ml 1

# Output: audio.wav.json with word timings
```

### Using OpenAI Whisper API

```python
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3", word_timestamps=True)

# Access word-level timing
for segment in result["segments"]:
    for word in segment["words"]:
        print(f"{word['word']}: {word['start']:.2f} - {word['end']:.2f}")
```

---

## Step 2: Create Animated ASS Subtitles

### ASS File Structure

```ass
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,72,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,10,10,200,1
Style: Highlight,Arial Black,72,&H0000FFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,10,10,200,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
```

### Style 1: Word Pop (CapCut Default)

Each word pops in with a scale animation.

```ass
[V4+ Styles]
Style: WordPop,Montserrat,80,&H00FFFFFF,&H00FFFF00,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,5,0,2,10,10,250,1

[Events]
; Word "This" pops in at 0.0s
Dialogue: 0,0:00:00.00,0:00:00.50,WordPop,,0,0,0,,{\fscx50\fscy50\t(0,100,\fscx110\fscy110)\t(100,200,\fscx100\fscy100)}This
; Word "is" pops in at 0.3s
Dialogue: 0,0:00:00.30,0:00:00.80,WordPop,,0,0,0,,{\fscx50\fscy50\t(0,100,\fscx110\fscy110)\t(100,200,\fscx100\fscy100)}is
; Word "AMAZING" pops in with emphasis at 0.5s
Dialogue: 0,0:00:00.50,0:00:01.20,WordPop,,0,0,0,,{\c&H00FFFF&\fscx50\fscy50\t(0,100,\fscx120\fscy120)\t(100,250,\fscx100\fscy100)}AMAZING
```

### Style 2: Highlight Sweep

Words appear white, then highlight yellow as spoken.

```ass
[V4+ Styles]
Style: Sweep,Arial Black,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,4,0,2,10,10,250,1

[Events]
; Full sentence appears, words highlight in sequence
Dialogue: 0,0:00:00.00,0:00:02.00,Sweep,,0,0,0,,{\k20}This {\k15}is {\k25}how {\k20}you {\k30}do {\k20}it
```

### Style 3: Karaoke (Music/Voiceover)

Progressive color fill across each word.

```ass
[V4+ Styles]
Style: Karaoke,Impact,80,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,5,0,2,10,10,250,1

[Events]
; Karaoke timing (values in centiseconds)
Dialogue: 0,0:00:00.00,0:00:03.00,Karaoke,,0,0,0,,{\kf50}This {\kf40}is {\kf60}the {\kf45}secret {\kf70}formula
```

### Style 4: Typewriter Effect

Characters appear one at a time.

```ass
[V4+ Styles]
Style: Typewriter,Courier New,64,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,3,0,2,10,10,250,1

[Events]
; Each character has its own timing
Dialogue: 0,0:00:00.00,0:00:00.10,Typewriter,,0,0,0,,T
Dialogue: 0,0:00:00.10,0:00:00.20,Typewriter,,0,0,0,,Th
Dialogue: 0,0:00:00.20,0:00:00.30,Typewriter,,0,0,0,,Thi
Dialogue: 0,0:00:00.30,0:00:00.40,Typewriter,,0,0,0,,This
; ... continue for each character
```

### Style 5: Bounce In

Words bounce from below with overshoot.

```ass
[V4+ Styles]
Style: Bounce,Arial Black,76,&H00FFFFFF,&H0000FFFF,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,4,0,2,10,10,250,1

[Events]
; Word bounces up from bottom
Dialogue: 0,0:00:00.00,0:00:00.80,Bounce,,0,0,0,,{\move(540,1200,540,960)\t(0,150,\fscx110\fscy110)\t(150,300,\fscx95\fscy95)\t(300,400,\fscx100\fscy100)}Word
```

---

## Caption Generation Scripts

### Python Script: JSON to Animated ASS

```python
#!/usr/bin/env python3
"""
Convert Whisper JSON transcript to animated ASS subtitles.
Usage: python json_to_ass.py transcript.json output.ass [style]
Styles: pop, sweep, karaoke, bounce
"""

import json
import sys

def format_time(seconds):
    """Convert seconds to ASS timestamp format (H:MM:SS.cc)"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def generate_pop_style(words):
    """Generate word-pop animation (CapCut default style)"""
    events = []
    for word_data in words:
        word = word_data['word'].strip()
        start = word_data['start']
        end = word_data['end']

        # Pop animation: scale from 50% to 110% to 100%
        # NOTE: ASS \t() animation tags use MILLISECONDS (not centiseconds!)
        # \t(0,80,...) = 0-80ms scale up, \t(80,180,...) = 80-180ms scale down
        effect = r"{\fscx50\fscy50\t(0,80,\fscx115\fscy115)\t(80,180,\fscx100\fscy100)}"

        events.append(
            f"Dialogue: 0,{format_time(start)},{format_time(end)},WordPop,,0,0,0,,{effect}{word}"
        )
    return events

def generate_sweep_style(segments):
    """Generate highlight sweep animation"""
    events = []
    for segment in segments:
        words = segment.get('words', [])
        if not words:
            continue

        start_time = words[0]['start']
        end_time = words[-1]['end']

        # Build karaoke timing string
        # NOTE: ASS karaoke \k tags use CENTISECONDS (multiply seconds by 100)
        karaoke_text = ""
        for i, word_data in enumerate(words):
            word = word_data['word'].strip()
            # Convert seconds to centiseconds: 0.5s * 100 = 50 centiseconds = {\k50}
            duration = int((word_data['end'] - word_data['start']) * 100)
            karaoke_text += f"{{\\k{duration}}}{word} "

        events.append(
            f"Dialogue: 0,{format_time(start_time)},{format_time(end_time)},Sweep,,0,0,0,,{karaoke_text.strip()}"
        )
    return events

def generate_karaoke_style(segments):
    """Generate karaoke-fill animation"""
    events = []
    for segment in segments:
        words = segment.get('words', [])
        if not words:
            continue

        start_time = words[0]['start']
        end_time = words[-1]['end']

        # Build karaoke fill timing
        karaoke_text = ""
        for word_data in words:
            word = word_data['word'].strip()
            duration = int((word_data['end'] - word_data['start']) * 100)
            karaoke_text += f"{{\\kf{duration}}}{word} "

        events.append(
            f"Dialogue: 0,{format_time(start_time)},{format_time(end_time)},Karaoke,,0,0,0,,{karaoke_text.strip()}"
        )
    return events

def generate_bounce_style(words):
    """Generate bounce-in animation"""
    events = []
    for word_data in words:
        word = word_data['word'].strip()
        start = word_data['start']
        end = word_data['end']

        # Bounce from below with overshoot
        # NOTE: ASS \t() and \move() use MILLISECONDS
        # 0-120ms: scale up, 120-200ms: overshoot, 200-280ms: settle (total 280ms bounce)
        effect = r"{\move(540,1100,540,960)\t(0,120,\fscx115\fscy115)\t(120,200,\fscx95\fscy95)\t(200,280,\fscx100\fscy100)}"

        events.append(
            f"Dialogue: 0,{format_time(start)},{format_time(end)},Bounce,,0,0,0,,{effect}{word}"
        )
    return events

def create_ass_file(transcript_path, output_path, style='pop'):
    """Create ASS file from Whisper JSON transcript"""

    with open(transcript_path, 'r') as f:
        data = json.load(f)

    # ASS header
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
Title: Animated Captions

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: WordPop,Arial Black,80,&H00FFFFFF,&H0000FFFF,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,5,0,2,10,10,250,1
Style: Sweep,Arial Black,72,&H00FFFFFF,&H0000FFFF,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,4,0,2,10,10,250,1
Style: Karaoke,Impact,80,&H00FFFFFF,&H0000FFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,5,0,2,10,10,250,1
Style: Bounce,Arial Black,76,&H00FFFFFF,&H0000FFFF,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,4,0,2,10,10,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    # Extract all words from segments
    all_words = []
    segments = data.get('segments', [])
    for segment in segments:
        words = segment.get('words', [])
        all_words.extend(words)

    # Generate events based on style
    if style == 'pop':
        events = generate_pop_style(all_words)
    elif style == 'sweep':
        events = generate_sweep_style(segments)
    elif style == 'karaoke':
        events = generate_karaoke_style(segments)
    elif style == 'bounce':
        events = generate_bounce_style(all_words)
    else:
        events = generate_pop_style(all_words)

    # Write ASS file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)
        f.write('\n'.join(events))

    print(f"Created {output_path} with {len(events)} caption events ({style} style)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python json_to_ass.py transcript.json output.ass [style]")
        print("Styles: pop, sweep, karaoke, bounce")
        sys.exit(1)

    transcript = sys.argv[1]
    output = sys.argv[2]
    style = sys.argv[3] if len(sys.argv) > 3 else 'pop'

    create_ass_file(transcript, output, style)
```

### Bash Script: Full Caption Pipeline

```bash
#!/bin/bash
# animated_captions.sh - Full pipeline for animated captions
# Usage: ./animated_captions.sh input.mp4 [style]

INPUT="$1"
STYLE="${2:-pop}"  # Default to 'pop' style
OUTPUT="${INPUT%.mp4}_captioned.mp4"

echo "=== Animated Caption Pipeline ==="
echo "Input: $INPUT"
echo "Style: $STYLE"

# Step 1: Extract audio
echo "[1/4] Extracting audio..."
ffmpeg -y -i "$INPUT" -vn -acodec pcm_s16le -ar 16000 -ac 1 audio_temp.wav

# Step 2: Generate transcript with Whisper
echo "[2/4] Generating transcript with Whisper..."
# Using FFmpeg's built-in Whisper (FFmpeg 8.0+)
ffmpeg -y -i audio_temp.wav \
  -af "whisper=model=ggml-base.bin:language=auto:destination=transcript.json:format=json" \
  -f null -

# Step 3: Convert to animated ASS
echo "[3/4] Creating animated ASS subtitles ($STYLE style)..."
python3 json_to_ass.py transcript.json captions.ass "$STYLE"

# Step 4: Burn subtitles into video
echo "[4/4] Burning captions into video..."
ffmpeg -y -i "$INPUT" \
  -vf "ass=captions.ass" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  "$OUTPUT"

# Cleanup
rm -f audio_temp.wav transcript.json

echo "=== Complete! ==="
echo "Output: $OUTPUT"
```

---

## FFmpeg Caption Presets

### Burn ASS Captions

```bash
# Standard ASS burn
ffmpeg -i input.mp4 \
  -vf "ass=captions.ass" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  output_captioned.mp4

# With custom fonts directory
ffmpeg -i input.mp4 \
  -vf "ass=captions.ass:fontsdir=/path/to/fonts" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  output_captioned.mp4
```

### Real-Time Caption Overlay (Whisper + Drawtext)

```bash
# Live captions from Whisper directly overlaid
ffmpeg -i input.mp4 \
  -af "whisper=model=ggml-base.bin:language=en" \
  -vf "drawtext=text='%{metadata\:lavfi.whisper.text}':fontsize=56:fontcolor=white:borderw=4:bordercolor=black:x=(w-tw)/2:y=h-th-200:box=1:boxcolor=black@0.4:boxborderw=10" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  output_live_captions.mp4
```

---

## Caption Style Presets

### TikTok Viral Style

```ass
Style: TikTokViral,Arial Black,84,&H00FFFFFF,&H0000FFFF,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,6,0,2,10,10,300,1
```

- **Font**: Arial Black (bold, readable)
- **Size**: 84 (large for mobile)
- **Colors**: White text, yellow highlight
- **Position**: Lower third (MarginV=300)

### YouTube Shorts Professional

```ass
Style: ShortsPro,Montserrat,72,&H00FFFFFF,&H00FFFFFF,&H00333333,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,10,10,280,1
```

- **Font**: Montserrat (modern, clean)
- **Size**: 72
- **Colors**: White with gray outline
- **Shadow**: Yes (professional look)

### Instagram Reels Trendy

```ass
Style: ReelsTrend,Impact,80,&H00FFFFFF,&H00FF00FF,&H00000000,&H00000000,1,0,0,0,100,100,2,0,1,5,0,2,10,10,260,1
```

- **Font**: Impact
- **Size**: 80
- **Colors**: White text, magenta highlight
- **Letter spacing**: 2 (spread out)

### Mr. Beast Style (High Energy)

```ass
Style: MrBeast,Impact,96,&H0000FFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,110,110,0,0,1,8,0,2,10,10,200,1
```

- **Font**: Impact
- **Size**: 96 (HUGE)
- **Colors**: Yellow text, red highlight
- **Scale**: 110% (extra impact)

---

## Color Schemes for Different Content

### High Energy / Gaming

```
Primary: &H0000FFFF (Yellow)
Highlight: &H000000FF (Red)
Outline: &H00000000 (Black)
```

### Professional / Educational

```
Primary: &H00FFFFFF (White)
Highlight: &H00FFD700 (Gold)
Outline: &H00333333 (Dark Gray)
```

### Lifestyle / Aesthetic

```
Primary: &H00FFFFFF (White)
Highlight: &H00FFC0CB (Pink)
Outline: &H00000000 (Black)
```

### Comedy / Casual

```
Primary: &H00FFFFFF (White)
Highlight: &H0000FF00 (Green)
Outline: &H00000000 (Black)
```

---

## Emoji Integration

### Adding Emojis to Captions

```ass
; Emoji in ASS subtitles (requires emoji font)
Dialogue: 0,0:00:01.00,0:00:02.00,Default,,0,0,0,,This is FIRE 🔥

; Using emoji font explicitly
Dialogue: 0,0:00:01.00,0:00:02.00,Default,,0,0,0,,{\fnSegoe UI Emoji}🔥{\fnArial Black} AMAZING
```

### Common Viral Emojis

```
🔥 - Fire (excitement, trending)
💀 - Skull (dying laughing)
😱 - Shocked (reactions)
✅ - Checkmark (lists, confirmations)
❌ - X mark (wrong/avoid)
💯 - 100 (emphasis, agreement)
👀 - Eyes (attention, looking)
🚨 - Alert (important, breaking)
```

---

## Platform-Specific Caption Guidelines

| Platform | Font Size | Position | Max Words/Screen | Animation |
|----------|-----------|----------|------------------|-----------|
| **TikTok** | 80-96 | Center/Lower | 3-5 words | Fast, punchy |
| **YouTube Shorts** | 72-84 | Lower third | 4-6 words | Smooth, readable |
| **Instagram Reels** | 76-88 | Center | 3-5 words | Trendy, stylish |
| **Facebook Reels** | 72-80 | Lower third | 5-7 words | Clear, accessible |

---

## Troubleshooting

### Captions Not Showing

```bash
# Verify ASS file is valid
ffmpeg -i captions.ass -f null -

# Check font availability
fc-list | grep -i "arial"
```

### Timing Issues

```bash
# Shift all captions by 0.5 seconds
ffmpeg -itsoffset 0.5 -i captions.ass shifted.ass
```

### Wrong Position on 9:16

```bash
# Adjust MarginV in ASS style for vertical video
# MarginV=250-350 is typical for 1920px height
```

---

## Advanced Animation Parameters for Viral Content

### Spring Physics Formulas for Bounce Animations

Spring physics create natural, organic motion that feels more engaging than linear animations.

#### Core Spring Formula

```
Position = equilibrium + amplitude * e^(-damping*t) * sin(frequency*t)
```

#### Practical Spring Parameters

| Parameter | Value Range | Effect | Recommended |
|-----------|-------------|--------|-------------|
| **Damping** | 0.5-5.0 | How quickly bounce settles | 2.5-3.5 for captions |
| **Frequency** | 5-20 rad/s | Bounce speed | 12-15 for punchy feel |
| **Amplitude** | 10-50 pixels | Bounce height | 20-30 for text |

#### Spring Bounce Examples

```ass
; Subtle spring bounce (0.4s total)
; Scale: 50% → 115% → 95% → 100% (overshoot then settle)
{\fscx50\fscy50\t(0,120,\fscx115\fscy115)\t(120,240,\fscx95\fscy95)\t(240,400,\fscx100\fscy100)}Word

; Aggressive spring bounce (0.6s total)
; Scale: 40% → 130% → 90% → 105% → 100% (multiple oscillations)
{\fscx40\fscy40\t(0,100,\fscx130\fscy130)\t(100,250,\fscx90\fscy90)\t(250,450,\fscx105\fscy105)\t(450,600,\fscx100\fscy100)}IMPACT

; Position spring bounce (from below)
{\move(540,1300,540,960,0,150)\t(0,150,\fscy115)\t(150,300,\fscy95)\t(300,450,\fscy100)}Bounce
```

#### Mathematical Reasoning

The overshoot (115% → 95%) simulates spring physics where momentum carries the object past equilibrium before settling. The exponential decay factor `e^(-damping*t)` ensures the oscillation amplitude decreases over time, creating a natural settling effect.

**Damping ratio formula:**
- ζ = damping / (2 * sqrt(stiffness * mass))
- Under-damped (0 < ζ < 1): Bouncy, overshoots (viral content)
- Critically damped (ζ = 1): No overshoot, fastest settle (professional)
- Over-damped (ζ > 1): Slow, sluggish (avoid)

### Easing Functions for Natural Motion

#### Cubic Bezier Curve Approximations

ASS doesn't support cubic-bezier directly, but we can approximate with multi-stage `\t()` transforms:

**Ease-Out (Deceleration - elements appearing):**
```ass
; Approximates cubic-bezier(0, 0, 0.2, 1)
; Fast start (70% in first 40%), slow finish
{\fscx50\fscy50\t(0,120,\fscx85\fscy85)\t(120,200,\fscx95\fscy95)\t(200,300,\fscx100\fscy100)}EaseOut
```

**Ease-In (Acceleration - elements disappearing):**
```ass
; Approximates cubic-bezier(0.8, 0, 1, 1)
; Slow start, fast finish
{\fscx100\fscy100\t(0,100,\fscx95\fscy95)\t(100,180,\fscx85\fscy85)\t(180,300,\fscx50\fscy50)}EaseIn
```

**Ease-In-Out (Smooth both ends):**
```ass
; Approximates cubic-bezier(0.4, 0, 0.2, 1) - Material Design standard
{\fscx50\fscy50\t(0,80,\fscx70\fscy70)\t(80,220,\fscx90\fscy90)\t(220,300,\fscx100\fscy100)}EaseInOut
```

#### Elastic Easing (Rubber Band Effect)

```ass
; Elastic overshoot - great for emphasis
; Formula: sin((t*10 - 0.75)*PI) * e^(-t*5)
{\fscx50\fscy50\t(0,80,\fscx140\fscy140)\t(80,180,\fscx85\fscy85)\t(180,320,\fscx110\fscy110)\t(320,500,\fscx100\fscy100)}ELASTIC
```

Mathematical basis: `sin((x*10 - 0.75)*(2*PI/3)) * pow(2, -10*x)` where x = normalized time (0-1)

### Optimal Timing Parameters by Platform (2026 Research)

Based on 2026 viral content analysis and WCAG accessibility guidelines:

#### TikTok Timing Profile

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| Caption appear speed | 80-150ms | Fast platform, snappy expectations |
| Word dwell time | 250-400ms | Minimum: 250ms, longer for emphasis |
| Bounce duration | 180-300ms | Quick, energetic feel |
| Shake amplitude | 3-8 pixels | Readable but noticeable |
| Max words/screen | 3-5 words | Mobile-first, quick reading |
| Animation delay between words | 50-100ms | Rapid succession |

#### YouTube Shorts Timing Profile

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| Caption appear speed | 150-250ms | Slightly more polished than TikTok |
| Word dwell time | 400-600ms | Better readability on larger screens |
| Bounce duration | 250-400ms | Smooth, professional feel |
| Shake amplitude | 2-5 pixels | Subtle, not distracting |
| Max words/screen | 4-6 words | Comfortable reading chunk |
| Animation delay between words | 80-150ms | Measured pacing |

#### Instagram Reels Timing Profile

| Parameter | Value | Reasoning |
|-----------|-------|-----------|
| Caption appear speed | 150-250ms | Aesthetic, stylish timing |
| Word dwell time | 300-500ms | Visual-first platform |
| Bounce duration | 200-350ms | Trendy, polished |
| Shake amplitude | 4-10 pixels | More dramatic for aesthetics |
| Max words/screen | 3-5 words | Short, impactful phrases |
| Animation delay between words | 100-180ms | Rhythmic pacing |

### Shake/Tremor Effects with Readability Limits

#### Maximum Readable Shake Amplitudes

Research shows text readability degrades rapidly with excessive motion:

| Font Size | Max Horizontal Shake | Max Vertical Shake | Frequency Limit |
|-----------|---------------------|-------------------|-----------------|
| 64-72px | 8-10 pixels | 6-8 pixels | 8-12 Hz |
| 76-84px | 10-15 pixels | 8-12 pixels | 8-12 Hz |
| 88-96px | 15-20 pixels | 12-16 pixels | 6-10 Hz |

**Rule of thumb:** Shake amplitude should not exceed 15% of font size for readability.

#### Shake Animation Examples

```ass
; Subtle shake (emphasis without distraction)
; Horizontal: ±5px, 12Hz oscillation, 0.3s duration
{\pos(540,960)\t(0,50,\pos(545,960))\t(50,100,\pos(535,960))\t(100,150,\pos(543,960))\t(150,200,\pos(537,960))\t(200,250,\pos(541,960))\t(250,300,\pos(540,960))}Text

; Impact shake (decay pattern)
; Amplitude decreases: 10px → 6px → 3px → 0px
{\pos(540,960)\t(0,60,\pos(550,960))\t(60,120,\pos(534,960))\t(120,200,\pos(543,960))\t(200,300,\pos(540,960))}BOOM
```

**FFmpeg drawtext shake (continuous):**
```bash
# Subtle shake: x offset = 5 * sin(t*40) (40 rad/s ≈ 6.4 Hz)
-vf "drawtext=text='LIVE':fontsize=80:fontcolor=red:\
     x='(w-tw)/2+5*sin(t*40)':\
     y='(h-th)/2+3*sin(t*40+1.57)'"

# Decaying shake (impact effect): amplitude decreases exponentially
-vf "drawtext=text='BOOM':fontsize=120:fontcolor=white:\
     x='(w-tw)/2+15*exp(-t*3)*sin(t*50)':\
     y='(h-th)/2+10*exp(-t*3)*cos(t*50)'"
```

### Pulse/Breathing Effects

#### Scale Pulse (Heartbeat Effect)

```ass
; Continuous pulse: 100% ↔ 105% every 1 second
; Use with looping for sustained emphasis
{\t(0,500,\fscx105\fscy105)\t(500,1000,\fscx100\fscy100)}Word
```

**FFmpeg drawtext pulse:**
```bash
# Sine wave pulse: fontsize oscillates 72 ± 8 pixels at 2 Hz
-vf "drawtext=text='SUBSCRIBE':fontsize='72+8*sin(t*12.56)':\
     fontcolor=yellow:x=(w-tw)/2:y=h-150"
# 12.56 rad/s = 2π rad/cycle × 2 cycles/s = 2 Hz
```

Mathematical reasoning: `sin(2πf*t)` where f = frequency in Hz
- 1 Hz (slow): `sin(6.28*t)` = `sin(t*6.28)`
- 2 Hz (medium): `sin(12.56*t)` = `sin(t*12.56)`
- 3 Hz (fast): `sin(18.85*t)` = `sin(t*18.85)`

### Per-Character vs Per-Word Timing

#### Character-Level Animation (Typewriter)

Optimal timing: **30-80ms per character** for comfortable reading

```python
# Typewriter timing formula
chars_per_second = 1000 / ms_per_char
# 50ms per char = 20 chars/second (comfortable)
# 30ms per char = 33 chars/second (fast, energetic)
# 80ms per char = 12.5 chars/second (dramatic, slow)
```

**ASS character reveal (manual):**
```ass
; Each character appears with 50ms delay
Dialogue: 0,0:00:00.00,0:00:00.05,Style,,0,0,0,,H
Dialogue: 0,0:00:00.05,0:00:00.10,Style,,0,0,0,,He
Dialogue: 0,0:00:00.10,0:00:00.15,Style,,0,0,0,,Hel
Dialogue: 0,0:00:00.15,0:00:00.20,Style,,0,0,0,,Hell
Dialogue: 0,0:00:00.20,0:00:01.00,Style,,0,0,0,,Hello
```

#### Word-Level Animation (CapCut Style)

Optimal timing: **200-400ms per word** with **50-150ms gap** between words

```python
# Word animation timing formula
def word_timing(word_count, platform='tiktok'):
    timings = {
        'tiktok': {'appear': 120, 'dwell': 300, 'gap': 80},
        'youtube': {'appear': 180, 'dwell': 450, 'gap': 120},
        'instagram': {'appear': 150, 'dwell': 350, 'gap': 100}
    }
    t = timings[platform]

    total_duration = 0
    for i in range(word_count):
        total_duration += t['appear'] + t['dwell'] + t['gap']

    return total_duration  # in milliseconds
```

### Accessibility Considerations

#### WCAG 2.2 Animation Guidelines

1. **Maximum flash frequency:** 3 flashes per second (avoid seizures)
   - Do NOT use animations faster than 333ms cycle time

2. **Motion reduction:** Provide `prefers-reduced-motion` alternative
   - For web: CSS `@media (prefers-reduced-motion: reduce)`
   - For video: Export both animated and static caption versions

3. **Minimum caption duration:** 1.5 seconds (WCAG Level AA)
   - Even fast platforms should respect this for accessibility

4. **Maximum reading speed:** 200 WPM (3.3 words/second)
   - Formula: `duration >= (word_count / 3.3) + animation_time`

#### Safe Animation Parameters

| Animation Type | Safe Range | Accessibility Limit | Notes |
|----------------|------------|---------------------|-------|
| Shake amplitude | 0-15px | 10px max | Higher risks illegibility |
| Shake frequency | 2-10 Hz | 8 Hz max | Above 10 Hz may trigger seizures |
| Pulse magnitude | 100-110% | 108% max | Excessive scale distracts |
| Flash duration | 100-300ms | Must be < 333ms | 3 flash/sec limit |

### Mathematical Formulas Reference

#### Oscillation Functions

**Sine wave (smooth oscillation):**
```
y = amplitude * sin(frequency * t + phase)
```

Example: `5*sin(t*12)` = 5 pixel amplitude, 12 rad/s ≈ 1.9 Hz

**Cosine wave (90° phase shift from sine):**
```
y = amplitude * cos(frequency * t)
```

Use cosine for perpendicular motion (e.g., circular paths)

**Exponential decay (settling):**
```
y = initial * e^(-decay_rate * t)
```

Example: `10*exp(-t*3)` = 10 pixels decaying with rate 3/sec

**Damped oscillation (spring bounce):**
```
y = amplitude * e^(-damping*t) * sin(frequency*t)
```

Example: `20*exp(-t*2.5)*sin(t*12)` = spring with damping 2.5, frequency 12 rad/s

#### Bezier Curve Approximation

Cubic bezier `(p0, p1, p2, p3)` can be approximated with 3-stage linear transitions:

**Standard ease-out (0, 0, 0.2, 1):**
- Stage 1 (0-40%): 50% of total change
- Stage 2 (40-70%): 35% of total change
- Stage 3 (70-100%): 15% of total change

**Standard ease-in (0.8, 0, 1, 1):**
- Stage 1 (0-30%): 15% of total change
- Stage 2 (30-60%): 35% of total change
- Stage 3 (60-100%): 50% of total change

### Platform Caption Accessibility Summary (2026)

Based on research from OpusClip, Instagram, and YouTube best practices:

#### Critical Requirements

1. **Silent viewing optimization:** 85% of social video watched without sound
2. **Contrast ratio:** Minimum 4.5:1 (WCAG Level AA)
3. **Font choice:** Sans-serif (Arial, Helvetica, Montserrat)
4. **Burned-in preferred:** Platform auto-captions often inaccurate
5. **Word-level timing:** Higher engagement than full-sentence captions

#### Recommended Safe Zone (Mobile)

```
Top margin: 150-200px (avoid notch, status bar)
Bottom margin: 200-300px (avoid UI, captions, CTA)
Side margins: 40-60px (safe for all aspect ratios)
```

**ASS safe zone positioning:**
```ass
; 1080x1920 vertical video safe zone
Style: SafeZone,Arial Black,80,&H00FFFFFF,&H0000FFFF,&H00000000,&H40000000,1,0,0,0,100,100,0,0,1,5,0,2,50,50,280,1
;                                                                                           ↑  ↑   ↑
;                                                                                        Left Right Bottom
;                                                                                        50px 50px 280px
```

---

## Sources

This skill was enhanced with research from:
- [Instagram Reels Caption Best Practices 2026](https://www.opus.pro/blog/instagram-reels-caption-subtitle-best-practices)
- [YouTube Shorts Caption Best Practices 2026](https://www.opus.pro/blog/youtube-shorts-caption-subtitle-best-practices)
- [Short-Form Video Mastery Guide 2026](https://almcorp.com/blog/short-form-video-mastery-tiktok-reels-youtube-shorts-2026/)
- [FFmpeg Drawtext Animation Exploration](https://www.braydenblackwell.com/blog/ffmpeg-text-rendering)
- [Spring Physics for UI Animations](https://www.kvin.me/posts/effortless-ui-spring-animations)
- [ASS Karaoke Documentation](https://docs.karaokes.moe/contrib-guide/create-karaoke/karaoke/)
- [WCAG Animation Accessibility](https://www.a11y-collective.com/blog/wcag-animation/)

---

## Related Skills

- `ffmpeg-captions-subtitles` - Full caption system
- `ffmpeg-karaoke-animated-text` - Advanced karaoke effects
- `ffmpeg-animation-timing-reference` - Timing formulas and parameters
- `viral-video-platform-specs` - Platform requirements
- `viral-video-hook-templates` - Hook patterns
