---
name: audio-production
description: Professional audio production for music, podcasts, and sound design. Use when working with audio recording, mixing, mastering, or sound design for any medium.
---

# Audio Production

Comprehensive guide for professional audio production across music, podcasts, video, and interactive media.

## Audio Fundamentals

### The Audio Signal Chain

```
SOURCE → CAPTURE → PROCESS → OUTPUT

Detailed:
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ Source  │→→→│   Mic   │→→→│ Preamp  │→→→│Interface│
│(voice,  │   │         │   │         │   │  (A/D)  │
│ instr.) │   │         │   │         │   │         │
└─────────┘   └─────────┘   └─────────┘   └────┬────┘
                                               │
                                               ▼
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│Speakers │←←←│  (D/A)  │←←←│   Mix   │←←←│   DAW   │
│Headphone│   │Interface│   │  Master │   │Recording│
└─────────┘   └─────────┘   └─────────┘   └─────────┘
```

### Key Audio Concepts

| Concept           | Definition                   | Standard                        |
| ----------------- | ---------------------------- | ------------------------------- |
| **Sample Rate**   | Samples per second           | 44.1kHz, 48kHz, 96kHz           |
| **Bit Depth**     | Dynamic range resolution     | 16-bit, 24-bit, 32-bit float    |
| **Bit Rate**      | Data per second (compressed) | 128-320 kbps (MP3)              |
| **Dynamic Range** | Loudest to quietest          | ~96dB (16-bit), ~144dB (24-bit) |
| **Headroom**      | Space below 0 dBFS           | -6 to -18 dB typical            |

### Frequency Spectrum

```
20 Hz                                              20,000 Hz
├───────────────────────────────────────────────────────┤

SUB-BASS │  BASS  │  LOW-MID │  MID  │ HIGH-MID │ HIGH
20-60    │ 60-250 │ 250-500  │500-2k │  2k-6k   │ 6k-20k
         │        │          │       │          │
Rumble   │ Warmth │  Body    │ Pres- │ Presence │ Air
Feel     │ Punch  │  Muddiness│ ence  │ Harshness│ Sibilance
```

### Decibel Reference Points

```
dBFS (Full Scale):
 0 dBFS  ████████████  Digital maximum (clipping)
-3 dBFS  ██████████    Peaks (leave headroom)
-6 dBFS  █████████     Recommended peak ceiling
-12 dBFS ███████       Average loud signal
-18 dBFS ██████        Recommended recording level
-24 dBFS ████          Conservative level
-60 dBFS █             Noise floor target
```

---

## Recording

### Microphone Types

| Type          | Principle        | Best For                        |
| ------------- | ---------------- | ------------------------------- |
| **Dynamic**   | Moving coil      | Loud sources, live, durable     |
| **Condenser** | Capacitor        | Studio vocals, acoustic, detail |
| **Ribbon**    | Thin metal strip | Vintage tone, smooth highs      |
| **USB**       | Built-in ADC     | Podcasts, convenience           |

### Polar Patterns

```
CARDIOID          FIGURE-8           OMNI
   ╭─────╮          ╭───╮           ╭─────╮
 ╭─┤     ├─╮      ╭─┤   ├─╮       ╭─┤     ├─╮
│  │     │  │    │  │   │  │     │  │     │  │
│  │  ●  │  │    │  │ ● │  │     │  │  ●  │  │
│  │     │  │    │  │   │  │     │  │     │  │
 ╰─┤     ├─╯      ╰─┤   ├─╯       ╰─┤     ├─╯
   ╰─────╯          ╰───╯           ╰─────╯
 Front pickup    Front + Back      All around
```

### Recording Levels

```
Target Peaks: -12 to -6 dBFS
Average Level: -18 to -12 dBFS

Why?
- Leaves headroom for processing
- Matches analog equipment sweet spot
- Prevents digital clipping
- 24-bit has plenty of resolution
```

### Recording Best Practices

- [ ] Set gain before recording (never during)
- [ ] Record at 24-bit minimum
- [ ] Use 48kHz for video, 44.1kHz for music
- [ ] Monitor with headphones
- [ ] Record a few seconds of room tone
- [ ] Check phase when using multiple mics
- [ ] Label takes immediately

---

## Essential Processing

### EQ (Equalization)

```
Types:
- High-pass filter (HPF): Removes low frequencies
- Low-pass filter (LPF): Removes high frequencies
- Bell/Peak: Boost or cut specific frequency
- Shelf: Boost or cut above/below frequency

Common Applications:
┌─────────────────────────────────────────┐
│ Vocal:                                  │
│ HPF at 80-100Hz (remove rumble)         │
│ Cut 200-300Hz (reduce mud)              │
│ Boost 3-5kHz (presence)                 │
│ Shelf boost 10kHz+ (air)                │
├─────────────────────────────────────────┤
│ Kick Drum:                              │
│ Boost 50-80Hz (sub)                     │
│ Cut 300-400Hz (boxiness)                │
│ Boost 3-5kHz (attack/click)             │
├─────────────────────────────────────────┤
│ Electric Guitar:                        │
│ HPF at 80Hz                             │
│ Cut 400-600Hz if muddy                  │
│ Boost 2-4kHz (bite)                     │
└─────────────────────────────────────────┘
```

### Compression

```
Parameters:
┌────────────────────────────────────────────────┐
│ Threshold: Level where compression starts      │
│ Ratio: Amount of compression (4:1, 8:1, etc.) │
│ Attack: Time to engage (fast=punch, slow=body)│
│ Release: Time to disengage                     │
│ Knee: Hard (sudden) or soft (gradual)         │
│ Makeup Gain: Restore lost volume               │
└────────────────────────────────────────────────┘

Common Settings:
┌─────────────────────────────────────────┐
│ Vocals: 3:1-4:1, medium attack/release  │
│ Drums: 4:1-8:1, fast attack             │
│ Bass: 4:1, medium attack                │
│ Mix Bus: 2:1-3:1, slow attack, 1-3dB GR│
└─────────────────────────────────────────┘
```

### Reverb

| Type        | Character       | Use                 |
| ----------- | --------------- | ------------------- |
| **Room**    | Small, tight    | Natural ambience    |
| **Hall**    | Large, spacious | Orchestral, ballads |
| **Plate**   | Bright, smooth  | Vocals, snare       |
| **Spring**  | Vintage, boingy | Guitar, lo-fi       |
| **Chamber** | Warm, dense     | Natural depth       |

```
Key Parameters:
- Pre-delay: Time before reverb (50-100ms for vocals)
- Decay/RT60: How long it lasts
- Damping: High-frequency absorption
- Size: Room dimensions
- Mix/Wet-Dry: Balance with original
```

### Delay

| Type           | Application                    |
| -------------- | ------------------------------ |
| **Slapback**   | 50-150ms, rockabilly, presence |
| **Stereo**     | Different L/R times, width     |
| **Ping-pong**  | Alternating L/R, interest      |
| **Tempo-sync** | 1/4, 1/8 notes, rhythmic       |

---

## Mixing

### Gain Staging

```
Signal Flow Levels:
┌─────────────────────────────────────────┐
│ Input:     -18 dBFS (sweet spot)        │
│            ↓                            │
│ Plugin 1:  Output matches input level   │
│            ↓                            │
│ Plugin 2:  Output matches input level   │
│            ↓                            │
│ Fader:     Unity (0 dB) ideally         │
│            ↓                            │
│ Bus:       -12 to -6 dBFS peaks         │
│            ↓                            │
│ Master:    -6 dBFS peaks (before limit) │
└─────────────────────────────────────────┘
```

### Panning Guidelines

```
Stereo Field:
Hard L    L    L-C    CENTER    R-C    R    Hard R
  │       │     │        │        │     │       │
  │       │     │        │        │     │       │
Rhythm   Gtr1  Keys1   Vocal    Keys2  Gtr2   Rhythm
 Gtr            BVox1   Bass    BVox2          Gtr
                        Kick
                        Snare

Common Positions:
- Center (0): Lead vocal, bass, kick, snare
- Slight L/R: Main instruments, harmonies
- Wide L/R: Rhythm guitars, stereo keys
- Hard L/R: Doubled parts, effects
```

### Frequency Balancing

```
Making space (subtractive EQ approach):
┌────────────────────────────────────────────┐
│ Kick:  Boost 60Hz   │ Cut from Bass here   │
│ Bass:  Boost 80-100 │ Cut from Kick here   │
│ Gtr:   Owns 1-3kHz  │ Cut vocal slightly   │
│ Vocal: Boost 3-5kHz │ Cut guitar slightly  │
└────────────────────────────────────────────┘

Each element should have its own frequency "home"
```

### Mix Bus Processing

```
Typical Chain:
1. Subtle EQ (tonal shaping)
2. Light compression (2:1, 1-3dB GR)
3. Stereo enhancement (if needed)
4. Limiter (only for reference bounce)

Keep mix bus processing minimal!
Leave headroom for mastering.
```

---

## Mastering

### Mastering Goals

1. **Tonal Balance**: Even frequency response
2. **Dynamics**: Appropriate loudness/dynamics
3. **Stereo Image**: Width and mono compatibility
4. **Translation**: Sounds good everywhere
5. **Format**: Prepare for distribution

### Loudness Standards

| Platform           | Target         | Measurement |
| ------------------ | -------------- | ----------- |
| **Spotify**        | -14 LUFS       | Integrated  |
| **Apple Music**    | -16 LUFS       | Integrated  |
| **YouTube**        | -14 LUFS       | Integrated  |
| **Broadcast (US)** | -24 LUFS       | Integrated  |
| **Broadcast (EU)** | -23 LUFS       | Integrated  |
| **CD**             | -9 to -12 LUFS | Integrated  |

### Mastering Chain (Typical)

```
1. Reference Import
   └─→ Compare to commercial releases

2. EQ (Linear Phase)
   └─→ Broad adjustments only

3. Multiband Compression
   └─→ Control specific bands

4. Stereo Width
   └─→ Enhance or narrow

5. Limiting
   └─→ Final loudness, prevent clipping

6. Dither (if needed)
   └─→ 16-bit conversion only
```

---

## Podcast Production

### Recording Setup

```
Recommended Signal Chain:
Mic → Audio Interface → DAW

Equipment Tiers:
┌─────────────────────────────────────────┐
│ Budget:    USB Mic (Blue Yeti, AT2020)  │
│ Mid:       SM7B + Cloudlifter + Interface│
│ Pro:       Large diaphragm condenser    │
│            + high-end preamp            │
└─────────────────────────────────────────┘
```

### Podcast Processing Chain

```
1. Noise Reduction
   └─→ Remove room noise, hum

2. De-essing
   └─→ Tame harsh "s" sounds

3. Compression
   └─→ Even out volume (3:1-4:1)

4. EQ
   └─→ HPF at 80Hz, presence boost

5. Limiter
   └─→ Catch peaks, -1 dBFS ceiling

Target: -16 LUFS (mono), -19 LUFS (stereo)
True Peak: -1 dBTP
```

### Podcast Export Settings

```
Standard:
- Format: MP3 or AAC
- Bitrate: 128 kbps (mono), 192 kbps (stereo)
- Sample rate: 44.1 kHz

High Quality:
- Format: AAC
- Bitrate: 256 kbps
- Sample rate: 48 kHz

Chapters: Use ID3 tags for chapter markers
Artwork: 3000x3000 minimum, JPG or PNG
```

---

## Sound Design

### Creating Sounds

```
Approaches:
1. Recording: Capture real sounds (foley)
2. Synthesis: Create from oscillators
3. Sampling: Manipulate existing sounds
4. Processing: Transform through effects
5. Layering: Combine multiple sources
```

### Synthesis Types

| Type                  | Method               | Sound Character       |
| --------------------- | -------------------- | --------------------- |
| **Subtractive**       | Filter oscillators   | Classic analog        |
| **FM**                | Frequency modulation | Metallic, bells       |
| **Wavetable**         | Morphing waveforms   | Modern, evolving      |
| **Granular**          | Tiny sound particles | Texture, pads         |
| **Additive**          | Stack sine waves     | Precise, organs       |
| **Physical Modeling** | Simulate physics     | Realistic instruments |

### Layering Formula

```
Sound Design Stack:
┌─────────────────────────────────────┐
│ TOP: High frequencies (air, presence)│
│ MID: Character, tone                │
│ LOW: Foundation, weight             │
│ SUB: Felt, not heard (20-60Hz)      │
│ TRANSIENT: Attack, punch            │
└─────────────────────────────────────┘

Process each layer separately, combine at end.
```

---

## DAWs (Digital Audio Workstations)

| DAW              | Strengths                    | Platform |
| ---------------- | ---------------------------- | -------- |
| **Pro Tools**    | Industry standard, editing   | All      |
| **Logic Pro**    | Complete package, Apple      | macOS    |
| **Ableton Live** | Live performance, electronic | All      |
| **FL Studio**    | Beat making, workflow        | All      |
| **Reaper**       | Customizable, affordable     | All      |
| **Cubase**       | MIDI, composition            | All      |
| **Studio One**   | Modern workflow              | All      |
| **Audacity**     | Free, simple editing         | All      |

---

## File Formats

| Format   | Type         | Quality  | Use                 |
| -------- | ------------ | -------- | ------------------- |
| **WAV**  | Uncompressed | Lossless | Production, archive |
| **AIFF** | Uncompressed | Lossless | Mac production      |
| **FLAC** | Compressed   | Lossless | Archive, audiophile |
| **ALAC** | Compressed   | Lossless | Apple ecosystem     |
| **MP3**  | Compressed   | Lossy    | Distribution        |
| **AAC**  | Compressed   | Lossy    | Streaming, Apple    |
| **OGG**  | Compressed   | Lossy    | Games, open source  |

### Export Specifications

```
For Mastering:
- Format: WAV
- Bit depth: 24-bit (or 32-bit float)
- Sample rate: Match session (typically 44.1/48kHz)
- Headroom: -6 dBFS peaks

For Distribution:
- Format: WAV or FLAC (lossless)
- Bit depth: 16-bit (with dither)
- Sample rate: 44.1 kHz
- Loudness: Platform target LUFS
```

---

## Best Practices

### DO:

- Record at proper levels (-18 dBFS average)
- Use reference tracks
- Take breaks (ear fatigue is real)
- Check mono compatibility
- Use subtractive EQ first
- Process in series, not parallel (usually)
- Save project versions regularly
- Export stems for backup

### DON'T:

- Record with processing (usually)
- Mix at high volumes
- Over-compress everything
- Solo instruments too long
- Trust only one playback system
- Rush the mixing process
- Forget to dither (16-bit only)
- Master your own mixes (ideally)

---

## Quality Checklist

### Pre-Export

- [ ] Gain staging correct throughout
- [ ] No clipping or distortion
- [ ] Phase issues resolved
- [ ] Mono compatibility checked
- [ ] Low-end translation verified
- [ ] High frequencies not harsh

### Final Check

- [ ] Listen on multiple systems
- [ ] Check in car, phone, earbuds
- [ ] Verify format specifications
- [ ] Confirm LUFS target met
- [ ] True peak below -1 dBTP
- [ ] Metadata correctly embedded
