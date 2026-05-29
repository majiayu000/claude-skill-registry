---
name: audio-editing
description: "Master the essential audio post-production techniques—normalization, compression, EQ, and noise reduction—using the correct processing order to achieve professional-quality audio. Use when: Editing podcast episodes or video soundtracks; Cleaning up recorded voiceovers; Improving audio quality for marketing content; Preparing audio files for distribution; Troubleshooting common audio issues"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Audio Editing Fundamentals

> Master the essential audio post-production techniques—normalization, compression, EQ, and noise reduction—using the correct processing order to achieve professional-quality audio.

## When to Use This Skill

- Editing podcast episodes or video soundtracks
- Cleaning up recorded voiceovers
- Improving audio quality for marketing content
- Preparing audio files for distribution
- Troubleshooting common audio issues
- Standardizing audio levels across a project

## Methodology Foundation

**Source**: iZotope + Industry Best Practices

**Core Principle**: Audio processing must happen in the correct order—each step builds on the previous. "Noise reduction before compression prevents amplifying noise. Compression before EQ prevents undoing your level work." The goal is to serve the content, not showcase the processing.

**Why This Matters**: Poor audio editing is the most common reason otherwise good content sounds amateur. Understanding these fundamentals enables marketers to polish recordings themselves or effectively communicate with audio engineers.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Applies correct processing order** - Gain → Noise → Compression → EQ → Limiting
2. **Sets appropriate levels** - Normalization, loudness standards (LUFS), peak management
3. **Reduces noise intelligently** - Without introducing artifacts
4. **Balances dynamics** - Compression settings for voice and music
5. **Shapes tone** - EQ adjustments for clarity and warmth

## How to Use

### Fix Audio Problems
```
My audio has [describe problem: too quiet, noisy background, inconsistent levels, muddy sound].
Help me fix it using proper processing order.
```

### Prepare Audio for Platform
```
Help me prepare this audio for [podcast/YouTube/Spotify/broadcast].
Current state: [describe audio]
```

### Master Audio Workflow
```
Create an audio editing workflow for [content type].
Include settings for [software: Audacity/Audition/etc.]
```

## Instructions

When editing audio, follow this methodology:

### Step 1: The Processing Order

Always process in this sequence to avoid compounding problems.

```
## Correct Processing Order

1. GAIN STAGING
   ↓
2. NOISE REDUCTION
   ↓
3. COMPRESSION
   ↓
4. EQUALIZATION
   ↓
5. FINAL NORMALIZATION / LIMITING

Why this order:
- Noise reduction BEFORE compression: Prevents amplifying noise
- Compression BEFORE EQ: Prevents EQ changes affecting dynamics
- Limiting LAST: Sets final ceiling after all processing
```

---

### Step 2: Gain Staging

Set initial levels before any processing.

```
## Gain Staging Guidelines

**Recording (target during capture)**:
- Peaks at -12 to -6 dB
- Leaves headroom for processing

**Initial Normalization (start of editing)**:
- Normalize peaks to -6 dB
- Creates consistent starting point

**Two Types of Normalization**:

1. **Peak Normalization**
   - Adjusts based on loudest point
   - Use for: Initial gain staging
   - Does NOT change dynamic range

2. **RMS/Loudness Normalization**
   - Adjusts based on average level
   - Use for: Final delivery
   - Better for perceived loudness matching
```

**Tool-Specific**:
| Software | Normalize Function |
|----------|-------------------|
| Audacity | Effect → Normalize |
| Audition | Effects → Amplitude → Normalize |
| Logic Pro | Region → Normalize |

---

### Step 3: Noise Reduction

Remove unwanted background sound without artifacts.

```
## Noise Reduction Approach

**When to use**:
- Consistent background hiss/hum
- Air conditioning, computer fan noise
- Not for variable noise (traffic, voices)

**Method 1: Spectral Noise Reduction**
1. Find 2-3 seconds of "silence" (noise only)
2. Use as noise profile
3. Apply reduction to full track
4. Use conservative settings

**Settings Guide** (Audacity example):
- Noise Reduction: 6-12 dB (start low)
- Sensitivity: 4-6 (higher = more aggressive)
- Frequency Smoothing: 3-6 bands

**Method 2: Noise Gate**
- Sets threshold; audio below is silenced
- Better for breaths between speech
- Doesn't affect audio during speech

**Warning Signs of Over-Processing**:
- "Underwater" or "robotic" sound
- Swirling artifacts
- Unnatural silence between words

**Rule**: If choosing between slight noise or artifacts, keep the noise.
```

---

### Step 4: Compression

Even out dynamics—reduce loud parts, bring up quiet parts.

```
## Compression for Voice

**What It Does**:
- Reduces volume of sounds above threshold
- Results in more consistent, fuller sound

**Key Parameters**:

| Parameter | What It Does | Voice Setting |
|-----------|--------------|---------------|
| Threshold | Level where compression starts | -20 to -12 dB |
| Ratio | How much to reduce | 2:1 to 4:1 |
| Attack | How fast compression kicks in | 10-30 ms |
| Release | How fast compression stops | 100-300 ms |
| Makeup Gain | Boosts output after compression | To taste |

**Voice Compression Starting Point**:
- Threshold: -18 dB
- Ratio: 3:1
- Attack: 15 ms (fast enough for transients)
- Release: 150 ms
- Gain: +3-6 dB (compensate for reduction)

**Multi-Band Compression** (advanced):
- Different settings for different frequency ranges
- Useful for controlling low-end rumble without affecting highs
- Overkill for most marketing audio

**When NOT to Compress**:
- Already consistent audio (well-recorded)
- Music meant to be dynamic
- Over-compression sounds "squashed"
```

---

### Step 5: Equalization (EQ)

Shape the tone—cut problems, enhance clarity.

```
## EQ for Voice

**Philosophy**: Cut more than boost. Removing problems is safer than adding "goodness."

**Voice Frequency Guide**:

| Range | Frequency | Effect |
|-------|-----------|--------|
| Rumble | Below 80 Hz | Cut (high-pass filter) |
| Muddiness | 200-400 Hz | Cut if boomy |
| Body/Warmth | 150-250 Hz | Boost slightly for thin voice |
| Boxy/Nasal | 400-800 Hz | Cut if honky |
| Clarity/Presence | 2-4 kHz | Boost for intelligibility |
| Sibilance | 5-8 kHz | Cut if harsh "s" sounds |
| Air/Brightness | 8-12 kHz | Boost for expensive studio feel |

**Standard Voice EQ Recipe**:
1. High-pass filter at 80 Hz (removes rumble)
2. Cut 2-3 dB around 300 Hz (reduces muddiness)
3. Boost 2-3 dB around 3 kHz (adds clarity)
4. High-shelf boost at 10 kHz if needed (adds air)

**De-essing**:
- Tames harsh "s" and "sh" sounds
- Target: 5-8 kHz range
- Use de-esser plugin OR narrow EQ cut
```

---

### Step 6: Final Normalization / Limiting

Set output level for delivery platform.

```
## Loudness Standards by Platform

| Platform | Target | Measurement |
|----------|--------|-------------|
| Podcast (general) | -16 LUFS | Integrated loudness |
| Spotify/Apple Podcasts | -14 LUFS | May normalize further |
| YouTube | -14 LUFS | Recommended |
| Broadcast TV (US) | -24 LKFS | FCC regulation |
| ACX/Audiobooks | -23 to -18 dB RMS | Per chapter |

**Final Steps**:

1. **Loudness Normalization**
   - Match to platform standard (e.g., -16 LUFS)
   - Use loudness meter, not peak meter

2. **Limiting**
   - Prevents clipping
   - Set ceiling at -1 dB (leaves headroom for encoding)
   - Catches peaks that exceed ceiling

3. **Export Settings**
   - Podcast: 128-192 kbps MP3, stereo
   - Video: Match video project settings
   - Audiobook: 192 kbps MP3, 44.1 kHz, mono
```

## Examples

### Example 1: Fixing a Noisy Podcast Recording

**Context**: Recorded a remote podcast interview with audible background hum.

**Input**:
> My podcast guest recorded on their laptop mic. There's a consistent low hum and the levels are all over the place—sometimes quiet, sometimes too loud. How do I fix this?

**Output**:

## Podcast Rescue Workflow

### Assessment
- Problem 1: Low hum (likely electrical, 50/60 Hz)
- Problem 2: Inconsistent levels (no compression during recording)
- Problem 3: Probably laptop mic = thin, harsh sound

### Step-by-Step Fix

**1. Gain Staging**
- Normalize peaks to -6 dB
- This gives you headroom for processing

**2. Remove the Hum**

*If it's electrical hum (consistent pitch)*:
- Use a notch filter at 60 Hz (US) or 50 Hz (Europe)
- Also notch harmonics: 120 Hz, 180 Hz, 240 Hz
- Settings: Very narrow Q (high), deep cut (-12 to -20 dB)

*If it's broadband noise (hiss)*:
- Find 2 seconds of just the hum (between speech)
- Use as noise profile
- Apply noise reduction: 8-10 dB, sensitivity 5
- Listen for artifacts; reduce if robotic

**3. Even Out Levels**

Compression settings:
- Threshold: -18 dB
- Ratio: 4:1 (higher than normal because it's bad)
- Attack: 20 ms
- Release: 200 ms
- Makeup gain: +5 dB

**4. Fix the Thin Sound**

EQ adjustments:
- High-pass at 100 Hz (laptop mics have no good bass anyway)
- Boost 2 dB at 200 Hz (add body)
- Cut 3 dB at 500 Hz (reduce boxiness)
- Boost 2 dB at 3 kHz (clarity)
- Cut 2 dB at 6 kHz if harsh

**5. Final Output**
- Loudness normalize to -16 LUFS
- Limit peaks to -1 dB
- Export: 192 kbps MP3

### Before/After Check
- A/B compare with bypass
- Check it doesn't sound "processed"
- The best edit is invisible

---

### Example 2: Audio Settings by Content Type

**Context**: Setting up templates for different audio content.

**Input**:
> I produce three types of content: YouTube videos, podcast episodes, and Loom videos for sales. Can you give me processing templates for each?

**Output**:

## Audio Processing Templates

### Template 1: YouTube Videos

**Goal**: Clear voice over background music, sounds good on phone speakers and headphones

**Processing Chain**:
1. **Noise Gate**: Threshold -40 dB, removes room noise between speech
2. **High-pass Filter**: 100 Hz, removes rumble
3. **Compression**: Threshold -16 dB, Ratio 3:1
4. **EQ**:
   - Cut 3 dB at 350 Hz
   - Boost 3 dB at 3.5 kHz
   - High shelf +2 dB at 8 kHz
5. **De-esser**: Target 6 kHz, medium threshold
6. **Limiter**: Ceiling -1 dB

**Export**: -14 LUFS, stereo, match video codec

**Voice/Music Balance**: Voice at -12 dB, music at -20 to -24 dB (8-12 dB lower than voice)

---

### Template 2: Podcast Episodes

**Goal**: Intimate, consistent sound for headphone listening over long duration

**Processing Chain**:
1. **Normalize**: Peaks to -6 dB
2. **Noise Reduction**: Light (6 dB max)
3. **Compression**: Threshold -18 dB, Ratio 2.5:1, slower release (250 ms)
4. **EQ**:
   - High-pass at 80 Hz
   - Slight warmth boost at 200 Hz
   - Presence boost at 2.5 kHz
5. **Limiter**: Ceiling -1 dB

**Export**: -16 LUFS, 128-192 kbps MP3, stereo or mono

**Multi-Speaker**: Process each track separately, then balance (should be equal loudness when together)

---

### Template 3: Loom/Sales Videos

**Goal**: Professional but natural, focus on intelligibility, optimize for laptop speakers

**Processing Chain**:
1. **High-pass Filter**: 120 Hz (aggressive, laptop speakers can't reproduce below anyway)
2. **Compression**: Threshold -14 dB, Ratio 3.5:1 (consistent level for presentation)
3. **EQ**:
   - Cut 4 dB at 300-400 Hz (reduce muddy laptop sound)
   - Boost 3 dB at 2-4 kHz (cuts through small speakers)
4. **Limiter**: Ceiling -3 dB (accounts for Loom compression)

**Export**: -14 LUFS, optimize for file size (lower bitrate acceptable)

**Pro tip**: Test playback on laptop speakers, not studio monitors—that's how buyers will hear it

## Checklists & Templates

### Audio Editing Checklist

```
## Pre-Processing
□ Imported audio to project
□ Listened through once for problems
□ Noted specific issues (noise, pops, volume spikes)
□ Backed up original file

## Processing (in order)
□ 1. Gain staging: peaks at -6 dB
□ 2. Noise reduction applied (if needed)
□    - Used clean noise sample
□    - Checked for artifacts
□ 3. Compression applied
□    - Threshold set appropriately
□    - Gain reduction 3-6 dB typical
□ 4. EQ applied
□    - High-pass engaged
□    - Problem frequencies cut
□ 5. Final limiting
□    - Ceiling at -1 dB (or per platform)

## Quality Check
□ A/B comparison with bypass
□ Listened on headphones
□ Listened on different speakers
□ No artifacts or processing sounds
□ Loudness matches target spec
```

---

### Platform Cheat Sheet

```
## Quick Reference: Delivery Specs

PODCASTS
- Loudness: -16 LUFS
- Format: 128-192 kbps MP3
- Channels: Mono or Stereo

YOUTUBE
- Loudness: -14 LUFS
- Format: Match video settings
- Note: Will be normalized by platform

AUDIOBOOKS (ACX)
- RMS: -23 to -18 dB
- Peak: -3 dB max
- Noise floor: -60 dB
- Format: 192 kbps MP3, 44.1 kHz, mono

BROADCAST (US)
- Loudness: -24 LKFS
- True peak: -2 dB
- Note: FCC regulated

MUSIC STREAMING
- Loudness: -14 LUFS (Spotify reference)
- Platforms normalize, but masters are louder
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- iZotope. "Tips to Record Professional Quality Voice Over at Home"
- Riverside. "Complete Post Production Guide"
- Lower Street. "How to Edit a Podcast"
- MixingMonster. "Audio Post Production Guide"

## Related Skills

- [pydub-automation](../pydub-automation/) - Python scripts for batch processing
- [audiobook-production](../audiobook-production/) - ACX-compliant mastering
- [podcast-production](../podcast-production/) - Full podcast workflow
- [voiceover-direction](../voiceover-direction/) - Getting better raw recordings

---

## Skill Metadata (Internal Use)

```yaml
name: audio-editing
category: audio
subcategory: editing
version: 1.0
author: MKTG Skills
source_expert: iZotope, Industry Best Practices
source_work: Audio Engineering Standards
difficulty: beginner
estimated_value: $50-200 per hour (equivalent engineering time)
tags: [audio, editing, eq, compression, normalization, post-production]
created: 2026-01-26
updated: 2026-01-26
```
