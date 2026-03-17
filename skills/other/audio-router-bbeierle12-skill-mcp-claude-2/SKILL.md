---
name: audio-router
description: Router for audio domain including playback, analysis, and audio-reactive visuals. Use when implementing any audio functionality including music, sound effects, visualizers, or audio-driven animations. Routes to 3 specialized skills.
---

# Audio Router

Routes to 3 specialized skills based on audio requirements.

## Routing Protocol

1. **Classify** — Identify audio task from user request
2. **Match** — Apply signal matching rules below
3. **Combine** — Audio-visual projects need 2-3 skills together
4. **Load** — Read matched SKILL.md files before implementation

## Quick Route

### Tier 1: Core Skills
| Need | Skill | Signals |
|------|-------|---------|
| Playing audio, music, SFX | `audio-playback` | play, load, music, sound, mp3, transport, player, loop |
| Extracting audio data | `audio-analysis` | FFT, frequency, spectrum, amplitude, waveform, beat detection |
| Visual-audio connection | `audio-reactive` | visualizer, reactive, respond to audio, sync, pulse, beat-driven |

## Signal Matching

### Primary Signals

**audio-playback**:
- "play audio", "load music", "sound effect"
- "Tone.js", "Player", "transport"
- "loop", "crossfade", "volume"
- "schedule", "timing", "sync to beat"
- "background music", "ambient sound"

**audio-analysis**:
- "FFT", "frequency", "spectrum"
- "beat detection", "amplitude"
- "waveform", "audio data"
- "frequency bands", "bass", "treble"
- "analyze", "extract", "measure"

**audio-reactive**:
- "visualizer", "audio reactive"
- "respond to music", "sync visuals"
- "pulse on beat", "frequency to color"
- "music driven", "audio visualization"
- "bloom on bass", "particles on beat"

### Confidence Scoring

- **High (3+ signals)** — Route directly to matched skill
- **Medium (1-2 signals)** — Route with supporting skills
- **Low (0 signals)** — Start with `audio-playback`

## Common Combinations

### Simple Audio Player (1 skill)
```
audio-playback → Load and play audio files
```

### Audio Visualizer (3 skills)
```
audio-playback → Load and control audio
audio-analysis → Extract frequency/beat data
audio-reactive → Map data to visual properties
```

### Background Music (1-2 skills)
```
audio-playback → Looping, crossfade, volume
audio-analysis → Optional: beat sync features
```

### Beat-Synced Animation (2-3 skills)
```
audio-analysis → Beat detection
audio-reactive → Trigger animations on beat
audio-playback → Control playback
```

## Decision Table

| Task | Primary Skill | Supporting Skills |
|------|---------------|-------------------|
| Play music file | playback | - |
| Loop ambient sound | playback | - |
| Create visualizer | reactive | playback + analysis |
| Detect beats | analysis | playback |
| Pulse on bass | reactive | analysis + playback |
| Frequency spectrum display | analysis | playback |
| Sound effects | playback | - |
| Audio-reactive particles | reactive | analysis + playback |
| Volume meter | analysis | playback |

## Integration with Other Domains

### With Post-Processing (postfx-*)
```
audio-analysis → Bass/high frequency data
audio-reactive → Mapping strategy
postfx-bloom → Audio-reactive glow intensity
postfx-effects → Audio-reactive chromatic aberration
```
Audio drives post-processing parameters.

### With Particles (particles-*)
```
audio-analysis → Beat detection, energy levels
audio-reactive → Emission rate mapping
particles-systems → Particle emitter configuration
```
Beats trigger particle bursts, energy controls speed.

### With GSAP (gsap-*)
```
audio-analysis → Beat detection
audio-reactive → Timeline control
gsap-sequencing → Beat-synced timeline
```
Audio events trigger or scrub GSAP timelines.

### With R3F (r3f-*)
```
audio-playback → Audio context in React
audio-analysis → Data extraction
audio-reactive → Update Three.js objects
r3f-fundamentals → Scene/mesh setup
```
Audio data animates 3D scene properties.

### With Shaders (shaders-*)
```
audio-analysis → Frequency uniforms
audio-reactive → Uniform update strategy
shaders-uniforms → Pass audio data to shaders
```
FFT data becomes shader uniforms for custom effects.

## Workflow Patterns

### Visualizer Development
```
1. audio-playback → Set up player and audio context
2. audio-analysis → Configure analyzers and band extraction
3. audio-reactive → Map frequencies to visual properties
```

### Beat-Reactive Experience
```
1. audio-playback → Load audio
2. audio-analysis → Configure beat detection
3. audio-reactive → Define beat response animations
```

### Ambient Soundscape
```
1. audio-playback → Looping players, crossfade
   (Single skill usually sufficient)
```

## Temporal Collapse Stack

For the New Year countdown audio experience:
```
audio-playback → Cosmic ambient loop, countdown ticks, celebration
audio-analysis → Beat detection, bass/mid/high extraction
audio-reactive → Map to bloom, particles, digit glow, vignette
```

Key features:
- Background cosmic ambient audio (looped)
- Tick sound per second (intensifies in final 10)
- Beat detection for particle bursts
- Bass → bloom intensity
- High frequencies → chromatic aberration
- Celebration music at zero

## Quick Reference

### Task → Skills

| Task | Skills Needed |
|------|---------------|
| "Play background music" | playback |
| "Loop ambient sound" | playback |
| "Crossfade between tracks" | playback |
| "Show frequency spectrum" | analysis + playback |
| "Detect beats in music" | analysis + playback |
| "Make visuals react to audio" | reactive + analysis + playback |
| "Pulse element on beat" | reactive + analysis |
| "Audio-reactive bloom" | reactive + analysis |
| "Sound effects on events" | playback |

### Audio Library Quick Reference

| Library | Use Case |
|---------|----------|
| Tone.js | Full audio synthesis, analysis, effects |
| Howler.js | Simple playback, sprites, mobile |
| Web Audio API | Low-level, custom processing |

### Common Frequency Bands

| Band | Range | Visual Use |
|------|-------|------------|
| Sub-bass | 20-60 Hz | Deep pulses, rumble |
| Bass | 60-250 Hz | Scale, intensity, beat |
| Low-mid | 250-500 Hz | Background motion |
| Mid | 500-2000 Hz | General energy |
| High-mid | 2000-4000 Hz | Detail, sparkle |
| High | 4000+ Hz | Shimmer, aberration |

## Fallback Behavior

- **No specific signals** → Start with `audio-playback`
- **"Visualizer" mentioned** → Full stack: all three skills
- **"React to music"** → `audio-reactive` + `audio-analysis`
- **Just playing audio** → `audio-playback` only
- **Performance concerns** → Focus on `audio-analysis` optimization

## Performance Priority

When performance is critical:
1. `audio-analysis` — Use smaller FFT size (64-128)
2. `audio-reactive` — Apply smoothing to reduce jitter
3. `audio-playback` — Preload audio, reuse players
