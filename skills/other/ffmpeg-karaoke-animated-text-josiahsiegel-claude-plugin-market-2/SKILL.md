---
name: ffmpeg-karaoke-animated-text
description: Complete karaoke subtitle system and advanced animated text effects. PROACTIVELY activate for: (1) Karaoke-style highlighted lyrics, (2) ASS/SSA advanced subtitle styling, (3) Scrolling credits (horizontal/vertical), (4) Typewriter text animation, (5) Bouncing/moving text, (6) Text fade in/out effects, (7) Word-by-word text reveal, (8) Kinetic typography, (9) Lower thirds animation, (10) Countdown timers and dynamic text. Provides: ASS karaoke timing format, drawtext with time expressions, scrolling text patterns, text animation formulas, kinetic typography techniques, subtitle styling reference, multi-line animated text.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

---

## Quick Reference

| Effect | Command |
|--------|---------|
| Scrolling credits | `-vf "drawtext=textfile=credits.txt:y=h-80*t"` |
| Typewriter | `-vf "drawtext=text='Hello':enable='gte(t,n*0.1)'"` |
| Fade in text | `-vf "drawtext=text='Title':alpha='min(1,t/2)'"` |
| Bouncing text | `-vf "drawtext=text='Bounce':y='h/2+50*sin(t*5)'"` |
| Karaoke ASS | Use ASS format with `\k` timing tags |
| Moving text | `-vf "drawtext=text='Move':x='w-mod(t*100,w+tw)'"` |

## When to Use This Skill

Use for **animated text and karaoke**:
- Music video lyrics with karaoke highlighting
- Movie-style scrolling credits
- Animated titles and lower thirds
- Typewriter text reveal
- Kinetic typography
- Countdown timers

---

# FFmpeg Karaoke & Animated Text (2025)

Complete guide to karaoke subtitles, kinetic typography, scrolling credits, and advanced text animation with FFmpeg.

## Karaoke Subtitles (ASS/SSA Format)

### ASS Karaoke Basics

ASS (Advanced SubStation Alpha) supports karaoke timing with `\k` tags.

```ass
[Script Info]
Title: Karaoke Example
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Karaoke,Arial,72,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,2,2,10,10,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:01.00,0:00:05.00,Karaoke,,0,0,0,,{\k50}Twinkle {\k50}twinkle {\k50}little {\k50}star
Dialogue: 0,0:00:05.00,0:00:09.00,Karaoke,,0,0,0,,{\k50}How {\k50}I {\k50}wonder {\k50}what {\k50}you {\k50}are
```

### Karaoke Timing Tags

| Tag | Effect | Example |
|-----|--------|---------|
| `\k` | Fill from left | `{\k100}Word` = 1 second fill |
| `\kf` or `\K` | Smooth fill (fade) | `{\kf100}Word` |
| `\ko` | Outline highlight | `{\ko100}Word` |

Duration is in **centiseconds** (100 = 1 second).

---

## CRITICAL: ASS Time Unit Reference

**ASS uses TWO DIFFERENT time unit systems - this is a common source of bugs!**

### Karaoke Tags = CENTISECONDS (1/100 second)

| Tag | Unit | Example | Duration |
|-----|------|---------|----------|
| `\k` | centiseconds | `{\k50}` | 0.5 seconds |
| `\kf` | centiseconds | `{\kf100}` | 1.0 second |
| `\ko` | centiseconds | `{\ko25}` | 0.25 seconds |

**Conversion**: seconds × 100 = centiseconds

### Animation Tags = MILLISECONDS (1/1000 second)

| Tag | Unit | Example | Duration |
|-----|------|---------|----------|
| `\t(t1,t2,...)` | milliseconds | `\t(0,500,...)` | 0-500ms animation |
| `\fad(in,out)` | milliseconds | `\fad(200,300)` | 200ms in, 300ms out |
| `\move(x1,y1,x2,y2,t1,t2)` | milliseconds | `\move(0,0,100,100,0,1000)` | 1 second move |

**Conversion**: seconds × 1000 = milliseconds

### FFmpeg drawtext = SECONDS (with decimals)

| Expression | Unit | Example |
|------------|------|---------|
| `t` | seconds | `t=2.5` means 2.5 seconds |
| `enable='between(t,0,3)'` | seconds | 0-3 seconds |
| `alpha='min(1,t/2)'` | seconds | fade over 2 seconds |

### Quick Conversion Table

| Seconds | Centiseconds (karaoke) | Milliseconds (animation) |
|---------|------------------------|--------------------------|
| 0.1s | 10 | 100 |
| 0.25s | 25 | 250 |
| 0.5s | 50 | 500 |
| 1.0s | 100 | 1000 |
| 2.0s | 200 | 2000 |

### Common Mistake Example

```ass
; WRONG - mixing units!
Dialogue: 0,0:00:00.00,0:00:02.00,Style,,0,0,0,,{\k100\t(0,100,...)}Word
; {\k100} = 1 second (centiseconds)
; \t(0,100,...) = 0-100ms = 0.1 seconds (milliseconds) - NOT THE SAME!

; CORRECT - consistent timing
Dialogue: 0,0:00:00.00,0:00:02.00,Style,,0,0,0,,{\k100\t(0,1000,...)}Word
; {\k100} = 1 second
; \t(0,1000,...) = 1 second - NOW THEY MATCH!
```

---

## Advanced Karaoke Timing Parameters (2026 Research)

### Optimal Karaoke Timing by Song Tempo

| BPM Range | Syllable Duration | Tag Value | Notes |
|-----------|-------------------|-----------|-------|
| 60-80 (Slow ballad) | 600-800ms | `\kf60-80` | Long, emotional |
| 80-100 (Moderate) | 400-600ms | `\kf40-60` | Standard pop |
| 100-120 (Upbeat) | 300-500ms | `\kf30-50` | Most common |
| 120-140 (Fast) | 250-400ms | `\kf25-40` | Energetic |
| 140+ (Rapid) | 200-300ms | `\kf20-30` | Rap, EDM |

### Karaoke Tag Selection Guide

Based on syllable/word duration and desired effect:

#### `\k` (Instant Fill) - Best For:
- **Very short syllables:** <120 centiseconds (1.2s)
- **Rap/hip-hop:** Fast lyric delivery
- **Staccato rhythm:** Percussive, sharp delivery

```ass
; Rap example (fast succession):
{\k25}Yo {\k20}this {\k15}is {\k30}rapid {\k25}fire {\k35}flow
```

#### `\kf` (Progressive Fill) - Best For:
- **Long syllables:** >120 centiseconds (1.2s)
- **Ballads:** Drawn-out emotional delivery
- **Smooth transitions:** Clean visual sweep

```ass
; Ballad example (sustained notes):
{\kf150}Loooooove {\kf120}yoooou {\kf180}foreeeever
```

**Recommended:** Use `\kf` for any syllable >100 centiseconds for smoothest visual effect.

#### `\ko` (Outline Reveal) - Best For:
- **High contrast:** Text that needs to "pop"
- **Neon/glow styles:** Outline-heavy fonts
- **Special emphasis:** Chorus, key phrases

```ass
; Neon karaoke style:
[V4+ Styles]
Style: NeonKaraoke,Arial,80,&H00000000,&H0000FF00,&H0000FF00,&H00000000,1,0,0,0,100,100,0,0,3,6,0,2,10,10,50,1

[Events]
Dialogue: 0,0:00:01.00,0:00:05.00,NeonKaraoke,,0,0,0,,{\ko50}Electric {\ko60}neon {\ko40}glow
```

### Multi-Color Karaoke Transitions

Create dynamic color changes during karaoke fill:

```ass
; Gradient karaoke: Yellow → Orange → Red
[V4+ Styles]
Style: GradientKaraoke,Impact,80,&H0000FFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,5,0,2,10,10,50,1
;                                   Primary^      Secondary^
;                                   Yellow(start) Red(filled)

; Add intermediate color transition with \t tags:
[Events]
Dialogue: 0,0:00:01.00,0:00:05.00,GradientKaraoke,,0,0,0,,{\kf80\t(0,400,\2c&H0000A5FF&)}Word1 {\kf100\t(0,500,\2c&H0000A5FF&)}Word2
;                                                                   ↑ Orange midpoint
```

**Color progression formula:**
```
Start: &H0000FFFF (Yellow)
Mid:   &H0000A5FF (Orange) - 50% through karaoke fill
End:   &H000000FF (Red)
```

### Per-Character Karaoke (Fine-Grained Control)

For very precise timing (character-by-character):

```ass
; Each character gets individual timing (manual, tedious)
{\k10}H{\k8}e{\k12}l{\k10}l{\k15}o {\k20}w{\k18}o{\k15}r{\k12}l{\k10}d

; Best practice: Use tools like Aegisub Karaoke Timer
; Manual character timing only for special effects
```

**When to use character-level karaoke:**
- Slow-motion word reveal
- Dramatic emphasis
- Non-linear character highlighting (e.g., every other letter)

---

## Advanced Text Animation Formulas (FFmpeg Drawtext)

### Spring Physics Implementation

Create natural bounce effects with exponential decay:

```bash
# Vertical spring bounce (decaying oscillation)
# Formula: y_offset = amplitude * e^(-decay*t) * sin(frequency*t)
-vf "drawtext=text='BOUNCE':fontsize=80:fontcolor=white:\
     x=(w-tw)/2:\
     y='(h-th)/2-30*exp(-t*2.5)*sin(t*15)'"

# Breakdown:
# -30*exp(-t*2.5) = amplitude decays from 30px to 0
# sin(t*15) = oscillates at 15 rad/s (≈2.4 Hz)
# Combines: bounces 2-3 times over ~1 second, settling at center
```

**Parameter tuning:**
- **Decay rate** (2.5): Higher = faster settling (3-4 for quick, 1-2 for slow)
- **Frequency** (15): Higher = more bounces (10-12 slow, 15-20 fast)
- **Amplitude** (30): Bounce height in pixels

### Elastic Overshoot Effect

Simulate elastic material with multiple overshoots:

```bash
# Elastic scale effect (rubber band)
# Overshoots target size multiple times before settling
-vf "drawtext=text='ELASTIC':fontsize='72*(1+0.4*exp(-t*3)*sin(t*20))':\
     fontcolor=yellow:x=(w-tw)/2:y=(h-th)/2"

# Scale oscillates: 72px → 101px → 65px → 80px → 70px → 72px (settled)
# Mathematical basis: e^(-3t) * sin(20t) creates damped oscillation
```

**Elastic parameters:**
- **Base fontsize:** 72 (target)
- **Overshoot:** 0.4 (40% maximum deviation) → 72 * 1.4 = 101px peak
- **Decay:** 3 (settles in ~1.5 seconds)
- **Frequency:** 20 (multiple small bounces)

### Bezier Curve Approximation (Ease-In-Out)

FFmpeg doesn't support bezier directly, but we can approximate with piecewise functions:

```bash
# Ease-out approximation (fast start, slow end)
# Cubic bezier (0, 0, 0.2, 1) approximation
-vf "drawtext=text='EASE OUT':\
     alpha='if(lt(t,0.5),1-exp(-t*6),1)':\
     fontsize=80:fontcolor=white:x=(w-tw)/2:y=(h-th)/2:\
     enable='lt(t,1)'"

# Ease-in approximation (slow start, fast end)
# Cubic bezier (0.8, 0, 1, 1) approximation
-vf "drawtext=text='EASE IN':\
     alpha='if(lt(t,0.5),exp(-(1-t)*6),0)':\
     fontsize=80:fontcolor=white:x=(w-tw)/2:y=(h-th)/2:\
     enable='between(t,1,2)'"

# Ease-in-out (S-curve) using sigmoid approximation
-vf "drawtext=text='SMOOTH':\
     alpha='1/(1+exp(-10*(t-0.5)))':\
     fontsize=80:fontcolor=white:x=(w-tw)/2:y=(h-th)/2:\
     enable='lt(t,1)'"
```

**Mathematical reasoning:**
- **Exponential ease:** `1 - e^(-kt)` creates natural deceleration
- **Sigmoid curve:** `1/(1+e^(-k(t-0.5)))` creates smooth S-curve (ease-in-out)
- **k parameter:** Controls transition sharpness (6-10 for subtle, 15-20 for pronounced)

### Wobble/Wiggle Effects

Create organic, unpredictable motion:

```bash
# Dual-frequency wobble (complex motion)
# Combines two sine waves at different frequencies for organic feel
-vf "drawtext=text='WOBBLE':fontsize=80:fontcolor=white:\
     x='(w-tw)/2+8*sin(t*7)+4*sin(t*17)':\
     y='(h-th)/2+6*cos(t*7)+3*cos(t*13)'"

# Breakdown:
# Primary wobble: 8*sin(t*7) = 8px amplitude, 7 rad/s (1.1 Hz)
# Secondary wobble: 4*sin(t*17) = 4px amplitude, 17 rad/s (2.7 Hz)
# Result: Complex, organic motion pattern

# Drunk/unstable effect (low frequency, large amplitude)
-vf "drawtext=text='UNSTABLE':fontsize=80:fontcolor=white:\
     x='(w-tw)/2+20*sin(t*2.5)+10*sin(t*6.3)':\
     y='(h-th)/2+15*cos(t*3.1)+8*cos(t*7.2)'"
```

**Wobble design principles:**
- Use **two frequencies** (primary + secondary) for natural randomness
- **Prime number ratios** (e.g., 7 and 17) prevent pattern repetition
- **Amplitude ratio 2:1** (primary twice the secondary) for balanced motion

### Pulse with Variable Intensity

Create heartbeat or alarm-style pulsing:

```bash
# Heartbeat pulse (two quick beats, pause)
# Pattern: THUMP-thump ... pause ... THUMP-thump
-vf "drawtext=text='♥ HEARTBEAT ♥':\
     fontsize='80+25*max(0,sin(t*15)*exp(-mod(t,1.2)*10))':\
     fontcolor=red:x=(w-tw)/2:y=(h-th)/2"

# Breakdown:
# sin(t*15) = rapid oscillation
# exp(-mod(t,1.2)*10) = decay envelope every 1.2 seconds
# max(0, ...) = only positive pulses
# Result: Pulse decays quickly, resets every 1.2s

# Alarm pulse (constant urgent rhythm)
-vf "drawtext=text='⚠ ALERT ⚠':\
     fontsize='80+20*abs(sin(t*8))':\
     fontcolor=yellow:x=(w-tw)/2:y=(h-th)/2"

# abs(sin(t*8)) creates continuous pulsing at 8 rad/s (1.3 Hz)
```

### Text Reveal Animations (Wipe Effects)

#### Horizontal Wipe (Left to Right)

```bash
# Clip text progressively from left
# Uses drawbox mask to reveal text over time
-filter_complex "\
  [0:v]drawtext=text='REVEALED':fontsize=100:fontcolor=white:\
       x=(w-tw)/2:y=(h-th)/2[txt];\
  [txt]drawbox=x=0:y=0:w='min(w,t*500)':h=h:c=black@0:t=fill:replace=1[v]" \
  -map "[v]"

# Breakdown:
# w='min(w,t*500)' = width grows at 500 pixels/second
# Creates left-to-right reveal effect
```

#### Vertical Wipe (Bottom to Top)

```bash
# Text rises from bottom
-vf "drawtext=text='RISING':fontsize=100:fontcolor=white:\
     x=(w-tw)/2:\
     y='if(lt(t,1),h-t*h,0)'"

# y position: starts at h (bottom), moves to 0 (top) over 1 second
```

### Countdown Timer Variations

#### Animated Countdown with Anticipation

```bash
# Countdown that pulses on each second change
-vf "drawtext=text='%{eif\\:10-floor(t)\\:d}':\
     fontsize='200+50*abs(sin(floor(t)*50))*exp(-(t-floor(t))*8)':\
     fontcolor=white:x=(w-tw)/2:y=(h-th)/2"

# Breakdown:
# %{eif\\:10-floor(t)\\:d} = countdown number (10, 9, 8, ...)
# abs(sin(floor(t)*50)) = trigger pulse on integer seconds
# exp(-(t-floor(t))*8) = decay within each second
# Result: Number "pops" at each second change
```

#### Split-Flap Display (Mechanical)

```bash
# Simulates old-school flip counter with vertical offset
-vf "drawtext=text='%{eif\\:10-floor(t)\\:d}':\
     fontsize=200:fontcolor=white:\
     x=(w-tw)/2:\
     y='(h-th)/2-(t-floor(t))*100*step(t-floor(t))'"

# y offset creates "flipping" motion at second boundaries
```

---

## Optimal Animation Timing by Content Type

### Music Video Karaoke

| Genre | Syllable Timing | Animation Style | Color Scheme |
|-------|----------------|-----------------|--------------|
| **Ballad** | 100-200 centiseconds | `\kf` smooth fill | White → Soft Blue |
| **Pop** | 40-80 centiseconds | `\kf` with bounce | White → Bright Pink |
| **Rap** | 15-40 centiseconds | `\k` instant | White → Red |
| **Rock** | 50-100 centiseconds | `\k` with shake | White → Orange |
| **EDM** | 30-60 centiseconds | `\ko` outline | Neon colors |

### Educational Content

```bash
# Slow, clear typewriter for learning
# 80ms per character = comfortable reading pace
-vf "drawtext=textfile=lesson.txt:\
     fontsize=48:fontcolor=white:\
     x=50:y=100:\
     enable='gte(n,eif(n/24,80))'"
# Each character appears every 80/24 ≈ 3.3 frames at 24fps
```

### Scrolling Credits Optimization

```bash
# Professional credits scroll
# Speed: 60-80 pixels/second for comfortable reading
-vf "drawtext=textfile=credits.txt:\
     fontsize=42:fontcolor=white:\
     x=(w-tw)/2:\
     y='h-60*t':\
     line_spacing=25"

# Calculation:
# 60 px/s at 42px font = ~1.4 lines/second
# For 50 lines: 50/1.4 = ~36 seconds total duration
```

**Credits readability formula:**
```
scroll_speed = font_size * 1.2 to 1.5  (pixels/second)
total_duration = (line_count * line_height) / scroll_speed

Example:
font_size = 42px
line_height = 42 + 25 (spacing) = 67px
scroll_speed = 42 * 1.4 = 59 px/s
50 lines = 50 * 67 = 3350 pixels
duration = 3350 / 59 = 56.8 seconds
```

---

## Sources

Enhanced with research from:
- [FFmpeg Drawtext Animation Exploration](https://www.braydenblackwell.com/blog/ffmpeg-text-rendering)
- [ASS Karaoke Tags Documentation](https://docs.karaokes.moe/contrib-guide/create-karaoke/karaoke/)
- [Advanced Aegisub Karaoke](https://docs.karaokes.moe/contrib-guide/create-karaoke/karaoke-advanced/)
- [Spring Physics for Animations](https://www.kvin.me/posts/effortless-ui-spring-animations)
- [Easing Functions Mathematical Reference](https://easings.net/)
- [FFmpeg Expression Evaluation](https://ffmpeg.org/ffmpeg-utils.html#Expression-Evaluation)

---

### Apply Karaoke ASS to Video

```bash
# Burn karaoke subtitles into video
ffmpeg -i input.mp4 \
  -vf "ass=karaoke.ass" \
  -c:v libx264 -crf 18 -c:a copy \
  output_karaoke.mp4

# With specific fonts directory
ffmpeg -i input.mp4 \
  -vf "ass=karaoke.ass:fontsdir=/path/to/fonts" \
  output.mp4
```

### Advanced ASS Karaoke Styles

```ass
[V4+ Styles]
; Gradient karaoke (yellow to red)
Style: KaraokeGradient,Impact,80,&H0000FFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,2,2,10,10,60,1

; Glow effect karaoke
Style: KaraokeGlow,Arial Black,72,&H00FFFFFF,&H00FF00FF,&H00FF00FF,&H00000000,1,0,0,0,100,100,0,0,4,0,20,2,10,10,50,1

; Outline only (neon style)
Style: KaraokeNeon,Arial,80,&H00000000,&H0000FF00,&H0000FF00,&H00000000,1,0,0,0,100,100,0,0,3,4,0,2,10,10,50,1

[Events]
; Word-by-word with effects
Dialogue: 0,0:00:01.00,0:00:05.00,KaraokeGradient,,0,0,0,,{\k50\fad(200,0)}Never {\k50}gonna {\k50}give {\k50}you {\k50}up
; With positioning
Dialogue: 0,0:00:05.00,0:00:09.00,KaraokeGlow,,0,0,0,,{\pos(960,900)\k50}Never {\k50}gonna {\k50}let {\k50}you {\k50}down
```

### ASS Color Format

ASS uses `&HAABBGGRR` format (Alpha, Blue, Green, Red):
- `&H00FFFFFF` = White (fully opaque)
- `&H000000FF` = Red
- `&H0000FF00` = Green
- `&H00FF0000` = Blue
- `&H80000000` = 50% transparent black

### Karaoke with Animation Effects

```ass
[Events]
; Bounce effect per word
Dialogue: 0,0:00:01.00,0:00:05.00,Karaoke,,0,0,0,,{\k50\t(0,500,\fry360)}Word1 {\k50\t(0,500,\fry360)}Word2

; Scale pop on highlight
Dialogue: 0,0:00:01.00,0:00:05.00,Karaoke,,0,0,0,,{\k50\t(0,100,\fscx120\fscy120)\t(100,200,\fscx100\fscy100)}Pop

; Color transition
Dialogue: 0,0:00:01.00,0:00:05.00,Karaoke,,0,0,0,,{\k100\t(0,1000,\c&H0000FF&)}Red {\k100\t(0,1000,\c&H00FF00&)}Green
```

### ASS Animation Tags Reference

| Tag | Effect |
|-----|--------|
| `\t(t1,t2,tags)` | Animate tags from t1 to t2 |
| `\move(x1,y1,x2,y2)` | Move text from point to point |
| `\fad(fadein,fadeout)` | Fade in/out (milliseconds) |
| `\fscx`, `\fscy` | Scale X/Y percentage |
| `\frx`, `\fry`, `\frz` | Rotate on axis |
| `\pos(x,y)` | Position text |
| `\an1-9` | Alignment (numpad positions) |

## Scrolling Credits

### Vertical Scroll (Bottom to Top)

```bash
# Basic scrolling credits
ffmpeg -i input.mp4 \
  -vf "drawtext=textfile=credits.txt:\
       fontfile=/path/to/font.ttf:\
       fontsize=48:\
       fontcolor=white:\
       x=(w-tw)/2:\
       y=h-80*t" \
  -c:v libx264 -crf 18 output.mp4

# y=h-80*t: Start at bottom (h), move up at 80 pixels/second
```

### credits.txt Format

```
DIRECTED BY
John Smith

PRODUCED BY
Jane Doe

STARRING
Actor One
Actor Two
Actor Three

MUSIC BY
Composer Name

SPECIAL THANKS
Everyone
```

### Scrolling Credits with Sections

```bash
# Multi-speed credits (slower for names)
ffmpeg -i input.mp4 \
  -vf "drawtext=textfile=credits.txt:\
       fontsize=48:\
       fontcolor=white:\
       x=(w-tw)/2:\
       y='h-60*t':\
       line_spacing=20" \
  output.mp4
```

### Horizontal Scrolling (News Ticker)

```bash
# Right to left scroll
ffmpeg -i input.mp4 \
  -vf "drawtext=text='BREAKING NEWS... This is a scrolling ticker message':\
       fontsize=36:\
       fontcolor=white:\
       y=h-50:\
       x='w-mod(t*150,w+tw)'" \
  ticker.mp4

# x='w-mod(t*150,w+tw)': Continuous scroll at 150 pixels/second
```

### Looping Horizontal Scroll

```bash
# Seamless looping ticker
ffmpeg -i input.mp4 \
  -vf "drawtext=text='   LIVE NEWS     BREAKING STORY     UPDATES   ':\
       fontsize=40:\
       fontcolor=yellow:\
       y=h-60:\
       x='w-mod(t*200\\,w+tw)':\
       box=1:boxcolor=red@0.8:boxborderw=10" \
  news_ticker.mp4
```

## Typewriter Effect

### Character-by-Character Reveal

```bash
# Typewriter effect using enable
ffmpeg -f lavfi -i "color=c=black:s=1920x1080:d=10" \
  -vf "\
    drawtext=text='H':x=100:y=500:fontsize=72:fontcolor=white:enable='gte(t,0.0)',\
    drawtext=text='e':x=150:y=500:fontsize=72:fontcolor=white:enable='gte(t,0.1)',\
    drawtext=text='l':x=200:y=500:fontsize=72:fontcolor=white:enable='gte(t,0.2)',\
    drawtext=text='l':x=250:y=500:fontsize=72:fontcolor=white:enable='gte(t,0.3)',\
    drawtext=text='o':x=300:y=500:fontsize=72:fontcolor=white:enable='gte(t,0.4)'" \
  typewriter.mp4
```

### Typewriter with Cursor

```bash
# Blinking cursor during typing
ffmpeg -f lavfi -i "color=c=black:s=1920x1080:d=5" \
  -vf "\
    drawtext=text='Hello':fontsize=72:fontcolor=white:x=100:y=500:\
             enable='gte(t,0)':alpha='min(1,(t-0)/0.5)',\
    drawtext=text='|':fontsize=72:fontcolor=white:\
             x='100+72*min(5,floor(t/0.1))':y=500:\
             alpha='lt(mod(t,0.5),0.25)'" \
  typewriter_cursor.mp4
```

## Text Fade Effects

### Fade In

```bash
# Simple fade in
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Title':fontsize=100:fontcolor=white:\
       x=(w-tw)/2:y=(h-th)/2:\
       alpha='if(lt(t,2),t/2,1)'" \
  fade_in.mp4

# Explanation: alpha goes from 0 to 1 over 2 seconds
```

### Fade Out

```bash
# Fade out (assuming 10 second video)
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Goodbye':fontsize=100:fontcolor=white:\
       x=(w-tw)/2:y=(h-th)/2:\
       alpha='if(gt(t,8),1-(t-8)/2,1)'" \
  fade_out.mp4
```

### Fade In and Out

```bash
# Title card with fade in/out
ffmpeg -f lavfi -i "color=c=black:s=1920x1080:d=6" \
  -vf "drawtext=text='Chapter One':fontsize=120:fontcolor=white:\
       x=(w-tw)/2:y=(h-th)/2:\
       alpha='if(lt(t,1),t,if(gt(t,5),1-(t-5),1))'" \
  title_card.mp4
```

## Moving Text

### Bouncing Text

```bash
# Vertical bounce
ffmpeg -i input.mp4 \
  -vf "drawtext=text='BOUNCE':fontsize=80:fontcolor=yellow:\
       x=(w-tw)/2:\
       y='(h-th)/2+50*sin(t*5)'" \
  bounce.mp4

# Horizontal bounce
ffmpeg -i input.mp4 \
  -vf "drawtext=text='PING PONG':fontsize=60:fontcolor=cyan:\
       x='(w-tw)/2+200*sin(t*3)':\
       y=(h-th)/2" \
  horizontal_bounce.mp4
```

### Circular Motion

```bash
# Text moving in circle
ffmpeg -i input.mp4 \
  -vf "drawtext=text='ORBIT':fontsize=60:fontcolor=white:\
       x='(w/2)+200*cos(t*2)-tw/2':\
       y='(h/2)+200*sin(t*2)-th/2'" \
  orbit.mp4
```

### Enter from Side

```bash
# Slide in from right
ffmpeg -i input.mp4 \
  -vf "drawtext=text='SLIDE IN':fontsize=80:fontcolor=white:\
       x='if(lt(t,1),w-tw*(t),w-tw)':\
       y=(h-th)/2" \
  slide_in.mp4

# Slide in from left
ffmpeg -i input.mp4 \
  -vf "drawtext=text='FROM LEFT':fontsize=80:fontcolor=white:\
       x='if(lt(t,1),-tw+tw*t,0)':\
       y=(h-th)/2" \
  slide_left.mp4
```

## Kinetic Typography

### Word Pop Effect

```bash
# Words appearing with scale
ffmpeg -f lavfi -i "color=c=black:s=1920x1080:d=8" \
  -vf "\
    drawtext=text='THIS':fontsize='72*(1+0.3*exp(-3*(t-1)))':fontcolor=white:\
             x=(w-tw)/2:y=h/2-100:enable='gte(t,1)',\
    drawtext=text='IS':fontsize='72*(1+0.3*exp(-3*(t-2)))':fontcolor=white:\
             x=(w-tw)/2:y=h/2:enable='gte(t,2)',\
    drawtext=text='KINETIC':fontsize='72*(1+0.3*exp(-3*(t-3)))':fontcolor=red:\
             x=(w-tw)/2:y=h/2+100:enable='gte(t,3)'" \
  kinetic_pop.mp4
```

### Shake Effect

```bash
# Shaking text (impact effect)
ffmpeg -i input.mp4 \
  -vf "drawtext=text='IMPACT':fontsize=120:fontcolor=white:\
       x='(w-tw)/2+10*sin(t*50)*exp(-t*2)':\
       y='(h-th)/2+10*cos(t*50)*exp(-t*2)'" \
  shake.mp4
```

### Rotation Animation

```bash
# Spinning text (requires recent FFmpeg)
# Note: drawtext doesn't support rotation natively
# Use ASS subtitles for rotation:

# Create spinning.ass
cat << 'EOF' > spinning.ass
[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Style: Spin,Arial,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,5,0,0,0,1

[Events]
Dialogue: 0,0:00:00.00,0:00:05.00,Spin,,0,0,0,,{\an5\pos(960,540)\t(0,5000,\frz1080)}SPINNING
EOF

ffmpeg -i input.mp4 -vf "ass=spinning.ass" output.mp4
```

## Lower Thirds

### Basic Lower Third

```bash
# Name and title lower third
ffmpeg -i input.mp4 \
  -vf "\
    drawbox=x=50:y=h-150:w=500:h=100:c=blue@0.7:t=fill,\
    drawtext=text='John Smith':fontsize=36:fontcolor=white:\
             x=70:y=h-140,\
    drawtext=text='CEO, Company Inc.':fontsize=24:fontcolor=white@0.8:\
             x=70:y=h-100" \
  lower_third.mp4
```

### Animated Lower Third

```bash
# Slide-in lower third
ffmpeg -i input.mp4 \
  -vf "\
    drawbox=x='if(lt(t,0.5),-500+1000*t,50)':\
            y=h-150:w=500:h=100:c=blue@0.7:t=fill:\
            enable='between(t,0,8)',\
    drawtext=text='John Smith':fontsize=36:fontcolor=white:\
             x='if(lt(t,0.5),-430+1000*t,70)':y=h-140:\
             alpha='min(1,(t-0.3)/0.3)':\
             enable='between(t,0.3,8)',\
    drawtext=text='CEO, Company Inc.':fontsize=24:fontcolor=white:\
             x='if(lt(t,0.5),-430+1000*t,70)':y=h-100:\
             alpha='min(1,(t-0.5)/0.3)':\
             enable='between(t,0.5,8)'" \
  animated_lower_third.mp4
```

## Countdown Timer

### Simple Countdown

```bash
# 10 second countdown
ffmpeg -f lavfi -i "color=c=black:s=1920x1080:d=10" \
  -vf "drawtext=text='%{eif\\:10-t\\:d}':fontsize=200:fontcolor=white:\
       x=(w-tw)/2:y=(h-th)/2" \
  countdown.mp4
```

### Countdown with Animation

```bash
# Pulsing countdown
ffmpeg -f lavfi -i "color=c=black:s=1920x1080:d=10" \
  -vf "drawtext=text='%{eif\\:10-t\\:d}':\
       fontsize='200+30*sin(t*10)*exp(-mod(t,1)*3)':\
       fontcolor=white:\
       x=(w-tw)/2:y=(h-th)/2" \
  pulsing_countdown.mp4
```

### Stopwatch/Timer

```bash
# Count up timer (MM:SS)
ffmpeg -f lavfi -i "color=c=black:s=1920x1080:d=120" \
  -vf "drawtext=text='%{eif\\:floor(t/60)\\:d\\:2}\\:%{eif\\:mod(t,60)\\:d\\:2}':\
       fontsize=100:fontcolor=green:\
       x=(w-tw)/2:y=(h-th)/2" \
  stopwatch.mp4
```

## Dynamic Text from Variables

### Frame Number Display

```bash
# Show frame number
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Frame\\: %{frame_num}':\
       fontsize=24:fontcolor=white:\
       x=10:y=10" \
  frame_numbers.mp4
```

### Timecode Display

```bash
# Show timecode
ffmpeg -i input.mp4 \
  -vf "drawtext=text='%{pts\\:hms}':\
       fontsize=24:fontcolor=white:\
       x=10:y=10" \
  timecode.mp4

# With milliseconds
ffmpeg -i input.mp4 \
  -vf "drawtext=text='%{pts}':\
       fontsize=24:fontcolor=white:\
       x=10:y=10" \
  timecode_ms.mp4
```

### File Metadata Display

```bash
# Show filename
ffmpeg -i input.mp4 \
  -vf "drawtext=text='%{metadata\\:title}':\
       fontsize=24:fontcolor=white:\
       x=10:y=h-40" \
  metadata.mp4
```

## Multi-Line Text

### Centered Multi-Line

```bash
# Multi-line centered text
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Line One\nLine Two\nLine Three':\
       fontsize=48:fontcolor=white:\
       x=(w-tw)/2:y=(h-th)/2:\
       line_spacing=20" \
  multiline.mp4
```

### Text File Input

```bash
# Use text file for long text
ffmpeg -i input.mp4 \
  -vf "drawtext=textfile=message.txt:\
       fontsize=36:fontcolor=white:\
       x=50:y=50:\
       line_spacing=10" \
  from_file.mp4
```

## Expression Reference

### Useful Time Expressions

| Expression | Result |
|------------|--------|
| `t` | Current time in seconds |
| `t*100` | Speed factor |
| `mod(t,5)` | Loop every 5 seconds |
| `sin(t*3)` | Oscillate 3 times/second |
| `exp(-t)` | Exponential decay |
| `if(lt(t,2),expr1,expr2)` | Conditional |
| `min(a,b)` / `max(a,b)` | Min/max |
| `floor(t)` / `ceil(t)` | Round down/up |

### Useful Variables

| Variable | Meaning |
|----------|---------|
| `w` | Video width |
| `h` | Video height |
| `tw` | Text width |
| `th` | Text height |
| `n` | Frame number |
| `frame_num` | Same as n |

### Common Patterns

```bash
# Appear after 2 seconds
enable='gte(t,2)'

# Visible between 2-5 seconds
enable='between(t,2,5)'

# Fade in over 1 second
alpha='min(1,t)'

# Center horizontally
x='(w-tw)/2'

# Center vertically
y='(h-th)/2'

# Loop position
x='mod(t*100,w)'

# Smooth oscillation
y='h/2+50*sin(t*3)'

# Decay animation
fontsize='100+50*exp(-t*2)'
```

This guide covers FFmpeg karaoke and animated text. For basic subtitles see `ffmpeg-captions-subtitles`, for shapes see `ffmpeg-shapes-graphics`.
