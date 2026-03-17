---
name: ffmpeg-animation-timing-reference
description: Definitive reference for FFmpeg and ASS/SSA animation timing units, optimal durations, and best practices. PROACTIVELY activate for: (1) Animation timing questions, (2) ASS subtitle timing, (3) Karaoke timing tags, (4) Caption duration calculation, (5) Transition duration selection, (6) Fade/zoom timing, (7) Frame rate considerations, (8) Platform-specific timing (TikTok/Shorts/Reels), (9) Readability formulas, (10) Audio-video sync tolerances. Provides: Complete time unit reference tables, optimal duration guidelines, psychology-based timing recommendations, caption readability formulas, and platform-specific timing profiles.
---

## CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

---

# FFmpeg Animation Timing Reference (2025-2026)

## Quick Reference Card

| Context | Unit | Example |
|---------|------|---------|
| FFmpeg filters (fade, xfade, drawtext) | **Seconds** | `duration=1.5` |
| FFmpeg zoompan `d=` parameter | **Frames** | `d=150` (150 frames) |
| FFmpeg time variable `t` | **Seconds** | `enable='gte(t,2)'` |
| ASS karaoke tags (\k, \kf, \ko) | **Centiseconds** | `{\k100}` = 1 second |
| ASS animation tags (\t, \fad, \move) | **Milliseconds** | `\t(0,500,...)` = 0.5s |
| ASS dialogue timestamps | **H:MM:SS.CC** | `0:00:05.50` |

---

# CRITICAL: ASS Has TWO Different Time Units!

**This is the most common source of confusion in subtitle animations.**

## ASS/SSA Time Unit Disambiguation

| Tag Type | Unit | Conversion | Example |
|----------|------|------------|---------|
| **Karaoke tags** (\k, \kf, \ko, \K) | **Centiseconds** (1/100s) | × 100 | `{\k50}` = 0.5 seconds |
| **Animation tags** (\t) | **Milliseconds** (1/1000s) | × 1000 | `\t(0,200,...)` = 0.2 seconds |
| **Fade tags** (\fad) | **Milliseconds** | × 1000 | `\fad(300,0)` = 0.3s fade in |
| **Move tags** (\move) | **Milliseconds** | × 1000 | `\move(x1,y1,x2,y2,0,500)` = 0.5s |
| **Dialogue timestamps** | **H:MM:SS.CC** | Centiseconds | `0:00:01.50` = 1.5 seconds |

### Example: Same Duration, Different Units

```ass
; Both animations last 0.5 seconds but use DIFFERENT UNITS:

; Karaoke: 50 CENTISECONDS = 0.5 seconds
{\k50}Word

; Animation: 500 MILLISECONDS = 0.5 seconds
{\t(0,500,\fscx120)}Word
```

---

# Section 1: FFmpeg Time Units (All Filters)

## Complete FFmpeg Time Unit Reference

| Filter/Context | Parameter | Unit | Example | Notes |
|----------------|-----------|------|---------|-------|
| `fade` | `duration` (d) | Seconds | `fade=t=in:d=2` | Floating point |
| `fade` | `start_time` (st) | Seconds | `fade=st=5:d=2` | When fade begins |
| `afade` | `duration` (d) | Seconds | `afade=d=3` | Audio fade |
| `xfade` | `duration` | Seconds | `duration=1.5` | Transition length |
| `xfade` | `offset` | Seconds | `offset=4` | When transition starts |
| `acrossfade` | `duration` (d) | Seconds | `acrossfade=d=1` | Audio crossfade |
| `drawtext` | `t` variable | Seconds | `enable='gte(t,5)'` | Time since start |
| `drawtext` | `alpha` | 0-1 scale | `alpha='min(1,t/2)'` | Opacity over time |
| `zoompan` | `d` | **Frames** | `d=150` | Duration in frames |
| `zoompan` | `t` variable | Seconds | `z='1+0.1*t'` | Time in expressions |
| `fps` | `fps` | Frames/second | `fps=30` | Frame rate |
| `trim` | `start`, `end` | Seconds | `trim=start=2:end=10` | Cut points |
| `setpts` | `PTS` | Timestamps | `setpts=PTS-STARTPTS` | Presentation timestamps |

## Frame Rate Conversion

| Frame Rate | 1 Frame Duration | 30 Frames | 60 Frames |
|------------|------------------|-----------|-----------|
| 24 fps | 41.67 ms | 1.25 s | 2.5 s |
| 25 fps | 40 ms | 1.2 s | 2.4 s |
| **30 fps** | **33.33 ms** | **1 s** | **2 s** |
| 50 fps | 20 ms | 0.6 s | 1.2 s |
| **60 fps** | **16.67 ms** | **0.5 s** | **1 s** |

### Zoompan Duration Calculation

```bash
# zoompan d= parameter is in FRAMES, not seconds!

# For 2-second zoom at 30fps:
ffmpeg -i input.mp4 -vf "zoompan=z='1.2':d=60:s=1080x1920" output.mp4
# d=60 frames ÷ 30fps = 2 seconds

# For 2-second zoom at 60fps:
ffmpeg -i input.mp4 -vf "zoompan=z='1.2':d=120:s=1080x1920" output.mp4
# d=120 frames ÷ 60fps = 2 seconds

# Formula: frames = seconds × fps
```

### Viral Video Timing Optimizations (2025-2026)

Based on the **1.3-second attention threshold** research, hook animations must be fast and dramatic:

| Effect Type | FPS | Effect Duration | Frame Count | `d=` Parameter |
|-------------|-----|-----------------|-------------|----------------|
| Hook zoom punch | 60 | 0.4-0.5s | 24-30 frames | `d=1` (use time conditional) |
| Hook flash | 60 | 0.2-0.3s | 12-18 frames | `d=1` (use time conditional) |
| Continuous zoom | 30 | Entire video | N/A | `d=1` (recalc per frame) |
| Text animations | 60 | 0.3-0.5s | 18-30 frames | `d=1` (use time conditional) |

**Important:** Always use `d=1` for continuous per-frame processing. Limit effect duration using time conditionals like `if(lt(t,0.5),effect,1)` rather than setting `d=` to a frame count (which would freeze the video after that many frames).

**Critical Rule:** Hook animations MUST complete within **0.5 seconds** to fit in the 1.3-second attention window with room for text/content.

### Optimal Zoom Parameters by Platform

| Platform | Hook Zoom | Hook Duration | Continuous Zoom | Recommended FPS |
|----------|-----------|---------------|-----------------|-----------------|
| **TikTok** | 1.5x (50%) | 0.4-0.5s | +0.2%/sec | 60fps for hooks |
| **YouTube Shorts** | 1.5x (50%) | 0.5-0.6s | +0.15%/sec | 60fps throughout |
| **Instagram Reels** | 1.4x (40%) | 0.5-0.6s | +0.18%/sec | 60fps for hooks |

### Optimized Hook Effect Formulas

```bash
# 1.5x zoom punch over 0.5s at 60fps (RECOMMENDED):
# Always use d=1 for continuous processing; time conditional limits effect duration
fps=60,zoompan=z='if(lt(t,0.5),1.5-t,1)':d=1:s=1080x1920

# 8% zoom pulse at ~2Hz for 1.5s (sin(t*12) = 12 rad/s = 1.91 Hz):
fps=60,zoompan=z='if(lt(t,1.5),1+0.08*sin(t*12),1)':d=1:s=1080x1920

# Subtle continuous zoom for TikTok (0.2%/sec - minimum perceptible):
zoompan=z='1+0.002*t':d=1:s=1080x1920

# Subtle continuous zoom for YouTube Shorts (0.15%/sec - larger screens):
zoompan=z='1+0.0015*t':d=1:s=1080x1920
```

---

# Section 2: ASS/SSA Subtitle Timing

## Karaoke Tags (Centiseconds)

| Tag | Name | Unit | Effect |
|-----|------|------|--------|
| `\k` | Karaoke | Centiseconds | Instant highlight (no fill) |
| `\kf` | Karaoke Fill | Centiseconds | Progressive fill left-to-right |
| `\ko` | Karaoke Outline | Centiseconds | Outline wipe effect |
| `\K` | Karaoke (alt) | Centiseconds | Same as \k |

### Karaoke Timing Examples

```ass
; Each word highlights for the specified duration
; Values are in CENTISECONDS (100 = 1 second)

; 0.5 second per word:
{\k50}This {\k50}is {\k50}a {\k50}test

; Variable timing matching speech:
{\k30}The {\k25}quick {\k40}brown {\k35}fox

; Karaoke fill (progressive highlight):
{\kf100}Slowly {\kf150}highlighting {\kf80}each {\kf120}word
```

### Conversion Table: Centiseconds

| Centiseconds | Seconds | Common Use |
|--------------|---------|------------|
| 10 | 0.1s | Very fast syllable |
| 25 | 0.25s | Quick word |
| 50 | 0.5s | Normal word |
| 100 | 1.0s | Long word/pause |
| 150 | 1.5s | Extended emphasis |
| 200 | 2.0s | Dramatic pause |

## Animation Tags (Milliseconds)

| Tag | Format | Unit | Effect |
|-----|--------|------|--------|
| `\t` | `\t(t1,t2,tags)` | Milliseconds | Animate between t1 and t2 |
| `\fad` | `\fad(in,out)` | Milliseconds | Fade in/out duration |
| `\move` | `\move(x1,y1,x2,y2,t1,t2)` | Milliseconds | Move from t1 to t2 |

### Animation Timing Examples

```ass
; Animation over 300 milliseconds (0.3 seconds):
{\t(0,300,\fscx120\fscy120)}Pop effect

; Scale animation: 0-200ms scale up, 200-400ms scale down
{\fscx80\fscy80\t(0,200,\fscx110\fscy110)\t(200,400,\fscx100\fscy100)}Bounce

; Fade in over 500ms, no fade out:
{\fad(500,0)}Fade in text

; Move over 800ms:
{\move(0,1920,540,960,0,800)}Slide in from bottom
```

### Conversion Table: Milliseconds

| Milliseconds | Seconds | Common Use |
|--------------|---------|------------|
| 50 | 0.05s | Instant flash |
| 100 | 0.1s | Very fast animation |
| 200 | 0.2s | Quick pop/snap |
| 300 | 0.3s | Standard UI animation |
| 500 | 0.5s | Smooth transition |
| 800 | 0.8s | Noticeable movement |
| 1000 | 1.0s | Slow, deliberate |
| 2000 | 2.0s | Very slow, dramatic |

## Dialogue Timestamps (H:MM:SS.CC)

```ass
; Format: Hours:Minutes:Seconds.Centiseconds
; Dialogue line from 1.5s to 5.0s:
Dialogue: 0,0:00:01.50,0:00:05.00,Default,,0,0,0,,Your text here

; Examples:
0:00:00.00  = 0 seconds (start)
0:00:01.50  = 1.5 seconds
0:00:10.00  = 10 seconds
0:01:00.00  = 60 seconds (1 minute)
0:05:30.25  = 5 minutes, 30.25 seconds
```

---

# Section 3: Optimal Animation Durations

## Human Perception Thresholds

| Timing | Brain Response | Application |
|--------|----------------|-------------|
| **<16ms** | Sub-perceptual | Cannot perceive (below 60fps frame) |
| **16-50ms** | Preattentive | Flash effects, subliminal |
| **50-100ms** | Motion detection | Pattern interrupts, glitches |
| **100-200ms** | Conscious recognition | Quick animations, snappy UI |
| **200-400ms** | Attention capture | Standard animations |
| **400-800ms** | Processing time | Complex transitions |
| **800ms-2s** | Contemplation | Dramatic, emotional effects |
| **>2s** | Extended focus | Deliberate, artistic pacing |

## Recommended Durations by Effect Type

### Text Animations

| Effect | Fast | Standard | Slow | Notes |
|--------|------|----------|------|-------|
| Word pop (scale) | 100-150ms | 150-250ms | 250-400ms | Material Design: 200ms |
| Fade in | 200-300ms | 300-500ms | 500-800ms | Smooth appearance |
| Fade out | 150-250ms | 200-400ms | 400-600ms | Slightly faster than fade in |
| Slide in | 200-300ms | 300-500ms | 500-800ms | Distance affects perception |
| Bounce | 300-400ms | 400-600ms | 600-800ms | Needs overshoot time |
| Typewriter | 30-50ms/char | 50-80ms/char | 80-120ms/char | Per character |

### Video Transitions (xfade)

| Transition | Fast | Standard | Slow | Best For |
|------------|------|----------|------|----------|
| Fade/Dissolve | 0.3-0.5s | 0.8-1.2s | 1.5-2.5s | Universal |
| Wipe | 0.2-0.4s | 0.5-0.8s | 1.0-1.5s | Directional energy |
| Slide | 0.3-0.5s | 0.6-1.0s | 1.2-2.0s | Dynamic movement |
| Circle/Iris | 0.5-0.8s | 1.0-1.5s | 2.0-3.0s | Dramatic reveal |
| Zoom | 0.4-0.6s | 0.8-1.2s | 1.5-2.5s | Impact, intensity |
| Pixelize | 0.3-0.5s | 0.5-0.8s | 1.0-1.5s | Glitch aesthetic |

### Hook Effects (First 1-3 Seconds)

| Hook Type | Effect Duration | Total Hook | Timing Pattern |
|-----------|----------------|------------|----------------|
| Pattern Interrupt | 50-150ms | 0.5-1.5s | Instant grab |
| Flash/Brightness | 80-200ms | 0.3-0.8s | Quick pulse |
| Zoom Punch | 200-400ms | 1-2s | Fast zoom-in, hold |
| Glitch | 100-300ms | 0.5-1.5s | Multiple bursts |
| Text Slam | 150-250ms | 1-2s | Quick appear, hold |

### Karaoke/Caption Animations

| Content | Duration Formula | Example |
|---------|------------------|---------|
| Single word | Word length × 50-100ms | "Hello" = 250-500ms |
| Short phrase | 1-2 seconds | "Check this out" |
| Sentence | Words ÷ 3 per second | 9 words = 3 seconds |
| Reading captions | See readability formula | Based on WPM |

---

# Section 4: Caption Readability Formula

## Reading Speed Standards

| Audience | Words Per Minute (WPM) | Use Case |
|----------|------------------------|----------|
| Slow readers | 120-140 WPM | Accessibility, elderly |
| **Average** | **160-180 WPM** | **Recommended default** |
| Fast readers | 200-220 WPM | Experienced viewers |
| Skim reading | 250-300 WPM | Not recommended for video |

## Caption Duration Calculation

### Formula

```python
# Basic formula:
caption_duration = (word_count / words_per_minute) * 60

# With minimum duration (accessibility):
minimum_duration = 1.5  # seconds - WCAG recommendation
duration = max(minimum_duration, caption_duration)

# Conservative formula (recommended):
duration = max(1.5, (word_count / 160) * 60)
```

### Quick Reference Table

| Word Count | @ 160 WPM | @ 180 WPM | Recommended |
|------------|-----------|-----------|-------------|
| 1-2 words | 0.75s | 0.67s | **1.5s** (minimum) |
| 3 words | 1.13s | 1.0s | **1.5s** (minimum) |
| 4 words | 1.5s | 1.33s | **1.5s** |
| 5 words | 1.88s | 1.67s | **1.9s** |
| 6 words | 2.25s | 2.0s | **2.3s** |
| 8 words | 3.0s | 2.67s | **3.0s** |
| 10 words | 3.75s | 3.33s | **3.8s** |
| 15 words | 5.63s | 5.0s | **5.6s** |

### Python Implementation

```python
def calculate_caption_duration(text: str, wpm: int = 160) -> float:
    """
    Calculate optimal caption display duration.

    Args:
        text: Caption text
        wpm: Words per minute (default 160 for comfortable reading)

    Returns:
        Duration in seconds
    """
    word_count = len(text.split())
    calculated = (word_count / wpm) * 60

    # WCAG minimum: 1.5 seconds for any caption
    minimum = 1.5

    # Add 0.5s buffer for cognitive processing
    buffer = 0.5

    return max(minimum, calculated + buffer)

# Examples:
print(calculate_caption_duration("Hello"))           # 1.5s (minimum)
print(calculate_caption_duration("This is a test")) # 2.0s
print(calculate_caption_duration("Check out this incredible transformation")) # 2.88s
```

## Accessibility Guidelines (WCAG 2.2)

| Guideline | Requirement |
|-----------|-------------|
| Minimum duration | 1.5 seconds for any caption |
| Maximum reading speed | 200 WPM (3.3 words/second) |
| Character limit | 42 characters per line (readability) |
| Lines per caption | Maximum 2 lines |
| Persistence | Caption visible for full duration |

---

# Section 5: Platform-Specific Timing

## TikTok (Fast, Energetic)

| Element | Timing | Notes |
|---------|--------|-------|
| Cut/transition | 0.5-1.5s between clips | Fast pacing |
| Text animation | 100-200ms | Snappy, punchy |
| Hook window | 1-1.5s | Immediate grab |
| Caption duration | 0.8-1.5s per phrase | Short, readable |
| Zoom effects | 200-400ms | Quick, impactful |
| Optimal video length | 15-30s (sweet spot) | Completion rate focus |

## YouTube Shorts (Medium-Fast)

| Element | Timing | Notes |
|---------|--------|-------|
| Cut/transition | 1-2s between clips | Slightly slower than TikTok |
| Text animation | 150-300ms | Smooth but quick |
| Hook window | 2-3s | Slightly more time |
| Caption duration | 1.2-2s per phrase | More readable |
| Zoom effects | 300-600ms | Noticeable but smooth |
| Optimal video length | 50-60s | Algorithm favored |

## Instagram Reels (Aesthetic, Polished)

| Element | Timing | Notes |
|---------|--------|-------|
| Cut/transition | 1.5-2.5s between clips | More polished |
| Text animation | 150-250ms | Stylish timing |
| Hook window | 2-3s | Visual-first platform |
| Caption duration | 1-1.8s per phrase | Instagram style |
| Zoom effects | 400-800ms | Cinematic feel |
| Optimal video length | 15-30s (trending) | Engagement focused |

## Professional/Broadcast

| Element | Timing | Notes |
|---------|--------|-------|
| Cut/transition | 2-4s between clips | Deliberate pacing |
| Text animation | 300-500ms | Smooth, professional |
| Lower third entrance | 400-600ms | Broadcast standard |
| Caption duration | 2-4s per phrase | Full readability |
| Zoom effects | 800-1500ms | Subtle, cinematic |
| Typical segment | 30-90s | Standard TV timing |

---

# Section 6: Easing Functions and Natural Motion

## Material Design Timing Standards

| Animation Type | Duration | Easing | Use Case |
|----------------|----------|--------|----------|
| Small (icon, button) | 100ms | ease-out | Micro-interactions |
| Medium (card, dialog) | 200-300ms | ease-in-out | Standard UI |
| Large (page, panel) | 300-500ms | ease-out | Major transitions |
| Complex (multi-element) | 400-700ms | ease-in-out | Choreographed |

## FFmpeg Easing Expressions

### Ease Out (Deceleration) - Elements Entering

```bash
# Ease out: fast start, slow finish
# Good for: Elements appearing, sliding in
-vf "drawtext=text='Hello':alpha='1-exp(-t*5)':fontsize=48:fontcolor=white:x=(w-tw)/2:y=(h-th)/2"
```

### Ease In (Acceleration) - Elements Leaving

```bash
# Ease in: slow start, fast finish
# Good for: Elements disappearing, sliding out
-vf "drawtext=text='Goodbye':alpha='exp(-(5-t)*5)':fontsize=48:fontcolor=white:x=(w-tw)/2:y=(h-th)/2:enable='lt(t,5)'"
```

### Bounce Effect

```bash
# Bounce: overshoot then settle
# Duration: 400-600ms recommended
-vf "drawtext=text='Bounce':y='h/2-50+50*exp(-t*3)*sin(t*15)':fontsize=48:fontcolor=white:x=(w-tw)/2"
```

### Elastic Effect

```bash
# Elastic: spring-like oscillation
# Duration: 600-1000ms recommended
-vf "drawtext=text='Elastic':fontsize='48*(1+0.3*exp(-t*2)*sin(t*10))':fontcolor=white:x=(w-tw)/2:y=(h-th)/2"
```

### Smooth Oscillation (Continuous)

```bash
# Pulse/float effect
# Period: 2-4 seconds per cycle
-vf "drawtext=text='Float':y='h/2+20*sin(t*2)':fontsize=48:fontcolor=white:x=(w-tw)/2"
```

## Recommended Easing by Context

| Context | Function | Duration |
|---------|----------|----------|
| Element appearing | `1-exp(-t*5)` | 200-400ms |
| Element disappearing | `exp(-t*5)` | 150-300ms |
| Emphasis/attention | `1+0.2*sin(t*6)` | Continuous |
| Bounce entrance | `exp(-t*3)*sin(t*15)` | 400-600ms |
| Smooth transition | Linear (no easing) | Any |

---

# Section 10: Mathematical Animation Formula Reference

## Complete Easing Function Formulas

Based on standard animation libraries (CSS, anime.js, React Spring) and adapted for FFmpeg.

### Linear (No Easing)

```
f(t) = t
```

**FFmpeg:** `alpha='t'` or `x='t*100'`

Use for: Constant speed motion, mechanical effects

### Quadratic Easing

**Ease In (Acceleration):**
```
f(t) = t²
```

**FFmpeg:** `alpha='t*t'`

**Ease Out (Deceleration):**
```
f(t) = 1 - (1-t)²
```

**FFmpeg:** `alpha='1-(1-t)*(1-t)'`

**Ease In-Out:**
```
f(t) = if(t < 0.5, 2*t², 1 - 2*(1-t)²)
```

**FFmpeg:** `alpha='if(lt(t,0.5),2*t*t,1-2*(1-t)*(1-t))'`

### Cubic Easing

**Ease In:**
```
f(t) = t³
```

**FFmpeg:** `alpha='t*t*t'`

**Ease Out:**
```
f(t) = 1 - (1-t)³
```

**FFmpeg:** `alpha='1-(1-t)*(1-t)*(1-t)'`

**Ease In-Out (Material Design Default):**
```
f(t) = if(t < 0.5, 4*t³, 1 - 4*(1-t)³)
```

**FFmpeg:** `alpha='if(lt(t,0.5),4*t*t*t,1-4*(1-t)*(1-t)*(1-t))'`

### Exponential Easing

**Ease In:**
```
f(t) = 2^(10*(t-1))
```

**FFmpeg:** `alpha='exp(10*(t-1)*0.693)'`
(Note: `2^x = e^(x*ln(2))` where `ln(2) ≈ 0.693`)

**Ease Out (Recommended for text appearing):**
```
f(t) = 1 - 2^(-10*t)
```

**FFmpeg:** `alpha='1-exp(-10*t*0.693)'`

### Sine Easing (Smooth, Gentle)

**Ease In:**
```
f(t) = 1 - cos(t*π/2)
```

**FFmpeg:** `alpha='1-cos(t*1.571)'`
(Note: `π/2 ≈ 1.571`)

**Ease Out:**
```
f(t) = sin(t*π/2)
```

**FFmpeg:** `alpha='sin(t*1.571)'`

**Ease In-Out:**
```
f(t) = -(cos(π*t) - 1)/2
```

**FFmpeg:** `alpha='-(cos(3.1416*t)-1)/2'`

### Circular Easing (Sharp Curve)

**Ease In:**
```
f(t) = 1 - sqrt(1 - t²)
```

**FFmpeg:** `alpha='1-sqrt(1-t*t)'`

**Ease Out:**
```
f(t) = sqrt(1 - (1-t)²)
```

**FFmpeg:** `alpha='sqrt(1-(1-t)*(1-t))'`

### Elastic Easing (Overshoot with Oscillation)

**Ease Out (Most Common):**
```
f(t) = 2^(-10*t) * sin((t*10 - 0.75)*2π/3) + 1
```

**FFmpeg approximation:**
```bash
alpha='exp(-10*t*0.693)*sin((t*10-0.75)*2.094)+1'
```
(Note: `2π/3 ≈ 2.094`)

**Ease In:**
```
f(t) = -2^(10*(t-1)) * sin((t*10 - 10.75)*2π/3)
```

**FFmpeg:**
```bash
alpha='-exp(10*(t-1)*0.693)*sin((t*10-10.75)*2.094)'
```

### Bounce Easing (Multiple Bounces)

**Ease Out (Complex, piecewise):**

For FFmpeg, simplified bounce approximation:
```bash
# Single bounce (easier implementation):
alpha='if(lt(t,0.4),
         7.5625*t*t,
         if(lt(t,0.8),
            7.5625*(t-0.6)*(t-0.6)+0.75,
            7.5625*(t-0.9)*(t-0.9)+0.9375))'
```

**Simplified damped oscillation bounce:**
```bash
# More natural, continuous bounce:
alpha='1-abs(cos(t*4.5*3.1416))*exp(-t*6)'
```

### Back Easing (Overshoot)

**Ease Out (Slight overshoot then settle):**
```
f(t) = 1 + c3 * (t-1)³ + c1 * (t-1)²
where c1 = 1.70158, c3 = c1 + 1
```

**FFmpeg approximation:**
```bash
# Simplified overshoot (10% beyond target):
alpha='if(lt(t,0.7),t*1.3,1+(1-t)*0.3)'
```

---

## Spring Physics Mathematical Reference

### Standard Spring System (Mass-Spring-Damper)

**Differential equation:**
```
m * x''(t) + c * x'(t) + k * x(t) = 0

Where:
m = mass
c = damping coefficient
k = spring stiffness (Hooke's constant)
x(t) = position at time t
x'(t) = velocity
x''(t) = acceleration
```

### Key Parameters

**Natural frequency:**
```
ω_n = sqrt(k/m)
```

**Damping ratio:**
```
ζ = c / (2 * sqrt(k * m))
```

### Damping Cases

**Under-damped (0 < ζ < 1) - Bouncy, overshoots:**
```
x(t) = e^(-ζ*ω_n*t) * [A*cos(ω_d*t) + B*sin(ω_d*t)]

Where:
ω_d = ω_n * sqrt(1 - ζ²)  (damped frequency)
```

**Critically damped (ζ = 1) - No overshoot, fastest settle:**
```
x(t) = (A + B*t) * e^(-ω_n*t)
```

**Over-damped (ζ > 1) - Slow, sluggish:**
```
x(t) = A*e^(r1*t) + B*e^(r2*t)
Where r1, r2 are real roots
```

### Simplified Spring for UI Animation

**Two-parameter approach (bounce + duration):**

```python
# Convert bounce and duration to spring parameters
mass = 1  # Normalized
stiffness = (2*π / duration)²

if bounce >= 0:
    damping = (1 - bounce) * 4*π / duration
else:
    damping = 4*π / (duration * (1 + bounce))
```

**Bounce parameter mapping:**
- `bounce = 0`: Critically damped (no overshoot)
- `0 < bounce < 1`: Under-damped (1 = undamped oscillation)
- `bounce < 0`: Over-damped (negative = slower settling)

### FFmpeg Spring Implementation

**Basic under-damped spring (stiffness=100, damping=10, mass=1):**

```bash
# Calculate natural frequency and damping ratio:
# ω_n = sqrt(100/1) = 10
# ζ = 10 / (2*sqrt(100*1)) = 10/20 = 0.5 (under-damped)
# ω_d = 10 * sqrt(1 - 0.5²) = 10 * 0.866 = 8.66

# Position formula:
-vf "drawtext=text='SPRING':\
     y='(h-th)/2-50*exp(-5*t)*cos(8.66*t)':\
     fontsize=80:fontcolor=white:x=(w-tw)/2"

# Breakdown:
# -50 = initial displacement (50px below center)
# exp(-5*t) = exponential decay (damping term: ζ*ω_n = 0.5*10 = 5)
# cos(8.66*t) = oscillation at damped frequency
```

**Tunable spring parameters for FFmpeg:**

```bash
# Low bounce (ζ=0.8, quick settle):
y='(h-th)/2+amplitude*exp(-8*t)*sin(10*t)'

# Medium bounce (ζ=0.5, balanced):
y='(h-th)/2+amplitude*exp(-5*t)*sin(12*t)'

# High bounce (ζ=0.3, very bouncy):
y='(h-th)/2+amplitude*exp(-3*t)*sin(14*t)'

# Critical damping (ζ=1, no overshoot):
y='(h-th)/2+amplitude*exp(-10*t)*(1+10*t)'
```

---

## Oscillation and Wave Formulas

### Basic Trigonometric Functions

**Sine wave (smooth oscillation):**
```
y = A * sin(ω*t + φ)

Where:
A = amplitude (peak height)
ω = angular frequency (rad/s)
t = time (seconds)
φ = phase offset (radians)
```

**Frequency conversion:**
```
ω = 2πf
where f = frequency in Hz (cycles/second)

Examples:
1 Hz = 6.28 rad/s (ω = 2π * 1)
2 Hz = 12.56 rad/s (ω = 2π * 2)
3 Hz = 18.85 rad/s (ω = 2π * 3)
```

**FFmpeg examples:**
```bash
# 2 Hz oscillation (2 cycles/second):
y='50*sin(12.56*t)'

# 1 Hz with phase offset (starts at peak):
y='50*sin(6.28*t+1.571)'  # φ = π/2 = 1.571

# Cosine (90° phase shifted sine):
y='50*cos(6.28*t)'  # equivalent to sin(t + π/2)
```

### Amplitude Modulation (AM)

**Variable amplitude sine wave:**
```
y = A(t) * sin(ω*t)
```

**FFmpeg decaying oscillation:**
```bash
# Exponential amplitude decay:
y='50*exp(-2*t)*sin(10*t)'

# Linear amplitude decay:
y='50*max(0,1-t)*sin(10*t)'

# Pulsing amplitude (low frequency modulates high frequency):
y='(30+20*sin(2*t))*sin(20*t)'
#    ↑ envelope     ↑ carrier wave
```

### Frequency Modulation (FM)

**Variable frequency sine wave:**
```
y = A * sin(ω(t)*t)
```

**FFmpeg examples:**
```bash
# Accelerating oscillation (siren effect):
y='50*sin(5*t*t)'  # frequency increases linearly

# Decelerating oscillation:
y='50*sin(20*t-5*t*t)'  # frequency decreases

# Vibrato (musical wobble):
y='50*sin(10*t+2*sin(3*t))'
#          ↑ base  ↑ vibrato modulation
```

### Lissajous Curves (2D Parametric Motion)

**Circular motion:**
```
x = r * cos(ω*t)
y = r * sin(ω*t)
```

**FFmpeg circular orbit:**
```bash
-vf "drawtext=text='○':\
     x='(w/2)+200*cos(2*t)':\
     y='(h/2)+200*sin(2*t)':\
     fontsize=40:fontcolor=white"
```

**Elliptical motion:**
```bash
# a=200 (horizontal radius), b=100 (vertical radius)
x='(w/2)+200*cos(2*t)'
y='(h/2)+100*sin(2*t)'
```

**Figure-8 motion (Lissajous 1:2 ratio):**
```bash
x='(w/2)+150*sin(1*t)'
y='(h/2)+150*sin(2*t)'
```

---

## Noise and Randomness Functions

### Pseudo-Random with Sine

FFmpeg doesn't have true random(), but we can approximate:

```bash
# Pseudo-random using high-frequency sine:
'10*sin(t*137.5)'  # 137.5 is irrational, appears random

# Multi-layered pseudo-random:
'5*sin(t*137.5)+3*sin(t*241.3)+2*sin(t*89.7)'
```

### Perlin-like Noise (Smooth Random)

```bash
# Smooth noise using multiple sine waves:
noise = 'sin(t*2.3)+0.5*sin(t*5.1)+0.25*sin(t*11.7)'

# Normalized to 0-1 range:
normalized_noise = '(sin(t*2.3)+0.5*sin(t*5.1)+0.25*sin(t*11.7)+1.75)/3.5'
```

### Jitter/Shake Effects

**Continuous shake:**
```bash
# High frequency, small amplitude:
x='(w-tw)/2+5*sin(t*50)'
y='(h-th)/2+5*cos(t*47)'  # Different freq for 2D randomness
```

**Decaying shake (impact):**
```bash
# Shake that settles over time:
x='(w-tw)/2+10*exp(-t*3)*sin(t*50)'
y='(h-th)/2+10*exp(-t*3)*cos(t*47)'
```

**Triggered shake (specific moments):**
```bash
# Shake only between t=2s and t=2.5s:
x='(w-tw)/2+if(between(t,2,2.5),15*sin(t*60),0)'
```

---

## Practical Animation Cookbook

### Fade Transitions

**Fade in (0 to 1 over duration):**
```bash
# Linear: alpha='min(1,t/duration)'
alpha='min(1,t/0.5)'  # 0.5s fade in

# Ease out: alpha='1-exp(-k*t)'
alpha='1-exp(-5*t)'  # Smooth fade in

# Cubic: alpha='min(1,t/duration)^3'
alpha='min(1,(t/0.5)*(t/0.5)*(t/0.5))'
```

**Fade out (1 to 0):**
```bash
# Assuming video duration = 10s, fade out in last 2s:
alpha='if(gt(t,8),1-(t-8)/2,1)'

# Exponential fade out:
alpha='if(gt(t,8),exp(-(t-8)*3),1)'
```

**Fade in and out:**
```bash
# Fade in 0-1s, hold 1-9s, fade out 9-10s:
alpha='if(lt(t,1),t,if(gt(t,9),10-t,1))'
```

### Scale Animations

**Pop in (scale 0 to 100%):**
```bash
# FFmpeg drawtext (no scale support, use ASS instead)

# ASS:
{\fscx0\fscy0\t(0,300,\fscx100\fscy100)}Text
```

**Pulse (continuous breathing):**
```bash
# ASS:
fontsize='72+8*sin(t*6.28)'  # 1 Hz pulse, ±8px

# ASS pulse with hold:
{\t(0,300,\fscx110\fscy110)\t(300,600,\fscx100\fscy100)}
```

**Bounce scale:**
```bash
# ASS overshoot bounce:
{\fscx50\fscy50\t(0,150,\fscx115\fscy115)\t(150,300,\fscx95\fscy95)\t(300,450,\fscx100\fscy100)}
```

### Position Animations

**Slide in from right:**
```bash
x='if(lt(t,1),w-(w-target_x)*t,target_x)'
# Example: target_x = (w-tw)/2 (center)
x='if(lt(t,1),w-((w-(w-tw)/2)*t),(w-tw)/2)'
```

**Slide in with ease-out:**
```bash
x='if(lt(t,1),w-((w-(w-tw)/2)*(1-exp(-5*t))),(w-tw)/2)'
```

**Bounce in from bottom:**
```bash
# ASS:
{\move(540,1920,540,960,0,400)\t(0,150,\fscy115)\t(150,300,\fscy95)\t(300,400,\fscy100)}
```

**Circular path:**
```bash
x='(w/2)+radius*cos(speed*t)'
y='(h/2)+radius*sin(speed*t)'
```

### Rotation Animations

**FFmpeg drawtext doesn't support rotation. Use ASS:**

```ass
; Continuous spin (360° over 2 seconds):
{\t(0,2000,\frz360)}Text

; Wobble rotation:
{\t(0,200,\frz15)\t(200,400,\frz-10)\t(400,600,\frz5)\t(600,800,\frz0)}
```

---

## Timing Psychology and Perception

### Human Perception Thresholds

| Threshold | Duration | Perception | Use Case |
|-----------|----------|------------|----------|
| **Flicker fusion** | 16-20ms | Below this: perceived as continuous | 60fps = 16.67ms/frame |
| **Preattentive** | 20-50ms | Detected but not consciously processed | Subliminal cues |
| **Attention capture** | 50-100ms | Minimum for conscious recognition | Flash effects |
| **Pattern interrupt** | 100-200ms | Breaks expectation, grabs attention | Hook effects |
| **Comfortable transition** | 200-400ms | Natural UI timing | Standard animations |
| **Deliberate motion** | 400-800ms | Noticeable, purposeful | Dramatic emphasis |
| **Sustained attention** | 800ms-2s | Holds focus | Title cards, captions |
| **Cognitive processing** | 2-5s | Complex information | Infographic reveals |

### Animation Duration Guidelines by Distance

**Relationship between distance and duration for perceived constant speed:**

```
duration = sqrt(distance) * k

Where:
distance = pixels traveled
k = speed constant (typically 5-15)

Example:
100px move: duration = sqrt(100) * 10 = 100ms
400px move: duration = sqrt(400) * 10 = 200ms
(Appears same speed despite 4x distance)
```

**FFmpeg implementation:**
```bash
# Move text 500px in 224ms (sqrt(500)*10):
-vf "drawtext=text='MOVE':\
     x='if(lt(t,0.224),(w-500)+500*t/0.224,w)':\
     y=(h-th)/2:fontsize=80:fontcolor=white"
```

### Biological Rhythms

**Natural timing that feels "right":**

| Rhythm | Rate | Use Case |
|--------|------|----------|
| **Resting heartbeat** | 60-80 BPM (1-1.3 Hz) | Calm, meditative pulse |
| **Walking pace** | 100-120 BPM (1.7-2 Hz) | Comfortable, steady rhythm |
| **Excited/anxious** | 120-160 BPM (2-2.7 Hz) | Energetic, urgent feeling |
| **Breathing** | 12-20/min (0.2-0.33 Hz) | Slow, natural oscillation |

**FFmpeg examples:**
```bash
# Heartbeat pulse (70 BPM = 1.17 Hz):
fontsize='72+6*max(0,sin(t*7.33))'

# Walking pace pulse (110 BPM = 1.83 Hz):
fontsize='72+4*abs(sin(t*11.5))'

# Breathing (15 breaths/min = 0.25 Hz):
fontsize='72+10*sin(t*1.57)'
```

---

## Sources

This comprehensive timing reference compiled from:
- [FFmpeg Expression Evaluation Documentation](https://ffmpeg.org/ffmpeg-utils.html#Expression-Evaluation)
- [Spring Physics for UI Animations](https://www.kvin.me/posts/effortless-ui-spring-animations)
- [Easing Functions Mathematical Reference](https://easings.net/)
- [Material Design Motion Guidelines](https://m3.material.io/styles/motion/overview)
- [React Spring Physics Documentation](https://www.react-spring.dev/docs/advanced/spring-configs)
- [ASS Subtitle Format Specification](https://aegisub.org/docs/latest/ass_tags/)
- [WCAG 2.2 Animation Accessibility](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions)
- [Human Perception Studies - Accessible Animations](https://www.a11y-collective.com/blog/wcag-animation/)

---

# Section 7: Audio-Video Sync Tolerances

## Synchronization Thresholds

| Sync Type | Maximum Tolerance | Recommended | Notes |
|-----------|-------------------|-------------|-------|
| Lip sync | ±80ms | ±40ms | Human perception limit |
| Music beat sync | ±50ms | ±20ms | Musical precision |
| Karaoke lyrics | ±100ms | ±30ms | Comfortable singing |
| Sound effects | ±30ms | ±10ms | Impact synchronization |
| Transition + audio | ±100ms | ±50ms | Cross-fade sync |

## Practical Guidelines

### Lip Sync

```
Tolerance: ±80ms (audio can lead or lag video by 80ms)
Recommendation: Keep within ±40ms for professional quality

Audio Leading (negative offset): Less noticeable, up to -80ms acceptable
Audio Lagging (positive offset): More noticeable, keep under +40ms
```

### Music Sync

```bash
# Calculate beat timing:
# 120 BPM = 2 beats/second = 500ms per beat
# 140 BPM = 2.33 beats/second = 429ms per beat

# Align transitions to beat:
# At 120 BPM, beats fall at: 0ms, 500ms, 1000ms, 1500ms, 2000ms...
```

### Karaoke Timing

```
Word highlight should START when word begins (not before)
Early highlight: Confusing, breaks immersion
Late highlight: Frustrating for singers

Recommendation: Highlight 0-50ms AFTER word starts (slight lag preferred)
```

---

# Section 8: Frame Rate Considerations

## Timing Precision Limits

| Frame Rate | Frame Duration | Precision Limit |
|------------|----------------|-----------------|
| 24 fps | 41.67ms | ~40ms increments |
| 25 fps | 40ms | 40ms increments |
| 30 fps | 33.33ms | ~33ms increments |
| 60 fps | 16.67ms | ~17ms increments |

## Implications

### Animation Smoothness

```
For smooth animation, use durations that are multiples of frame duration:

30fps:
- 100ms = 3 frames (smooth)
- 200ms = 6 frames (smooth)
- 333ms = 10 frames (smooth)
- 150ms = 4.5 frames (may stutter)

60fps:
- 100ms = 6 frames (smooth)
- 200ms = 12 frames (smooth)
- 167ms = 10 frames (smooth)
```

### Minimum Visible Duration

```
Animation duration must be at least 2-3 frames to be perceived:
- 30fps minimum: ~67-100ms
- 60fps minimum: ~33-50ms

Very short effects (<50ms) may not render consistently
```

## Frame-Safe Duration Table

| Desired Duration | 30fps Safe | 60fps Safe |
|------------------|------------|------------|
| ~100ms | 100ms (3f) | 100ms (6f) |
| ~150ms | 167ms (5f) | 150ms (9f) |
| ~200ms | 200ms (6f) | 200ms (12f) |
| ~250ms | 233ms (7f) | 250ms (15f) |
| ~300ms | 300ms (9f) | 300ms (18f) |
| ~500ms | 500ms (15f) | 500ms (30f) |

---

# Section 9: Quick Copy-Paste Reference

## FFmpeg Common Timing Patterns

```bash
# 2-second fade in:
-vf "fade=t=in:d=2"

# Text visible from 1s to 5s:
-vf "drawtext=text='Hello':enable='between(t,1,5)':..."

# 1.5s xfade starting at 4s:
-filter_complex "[0:v][1:v]xfade=duration=1.5:offset=4"

# 2-second zoom at 30fps (60 frames):
-vf "zoompan=z='1.5':d=60:s=1080x1920"

# Fade text in over 0.5s, hold, fade out over 0.3s:
-vf "drawtext=text='Hello':alpha='if(lt(t,0.5),t/0.5,if(lt(t,4.7),1,(5-t)/0.3))':enable='lt(t,5)':..."
```

## ASS Common Timing Patterns

```ass
; Word karaoke (centiseconds): 0.5s + 0.4s + 0.6s + 0.5s
{\k50}This {\k40}is {\k60}the {\k50}test

; 200ms pop animation (milliseconds):
{\fscx80\fscy80\t(0,200,\fscx100\fscy100)}Pop

; 500ms slide + 300ms fade:
{\move(0,1920,540,960,0,500)\fad(300,0)}Slide in

; Bounce: 150ms up, 100ms overshoot, 150ms settle (total 400ms)
{\fscx90\fscy90\t(0,150,\fscx110\fscy110)\t(150,250,\fscx95\fscy95)\t(250,400,\fscx100\fscy100)}Bounce
```

## Duration Cheat Sheet

| Duration | Use For |
|----------|---------|
| 50-100ms | Glitch, flash |
| 100-200ms | Quick UI feedback |
| 200-300ms | Standard animation |
| 300-500ms | Smooth transition |
| 500-800ms | Noticeable movement |
| 800-1500ms | Dramatic effect |
| 1.5-3s | Caption display |
| 3-5s | Long text reading |

---

## Related Skills

- `ffmpeg-karaoke-animated-text` - Karaoke subtitle creation
- `viral-video-animated-captions` - CapCut-style animations
- `ffmpeg-transitions-effects` - Video transitions
- `viral-video-hook-templates` - Hook timing patterns
- `ffmpeg-captions-subtitles` - Subtitle fundamentals
