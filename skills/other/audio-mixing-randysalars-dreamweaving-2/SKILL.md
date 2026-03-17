---
name: Audio Mixing & Mastering
tier: 3
load_policy: task-specific
description: Mix voice, binaural, and SFX stems into final master
version: 1.0.0
parent_skill: production-operations
---

# Audio Mixing Skill

> **The Mix Is Where Magic Happens**

This skill handles combining voice, binaural beats, and sound effects into a cohesive, hypnotic audio experience.

---

## Purpose

Mix multiple audio stems at correct levels and apply hypnotic post-processing for production masters.

---

## Standard Stem Levels

**CRITICAL**: Always use these exact levels.

| Stem | Level | Rationale |
|------|-------|-----------|
| Voice | -6 dB | Reference level, prevents clipping |
| Binaural | -6 dB | Audible but not distracting |
| SFX | 0 dB | Full impact for transitions |

---

## Canonical Mix Command

```bash
ffmpeg -y \
  -i sessions/{session}/output/voice_enhanced.wav \
  -i sessions/{session}/output/binaural_dynamic.wav \
  -i sessions/{session}/output/sfx_track.wav \
  -filter_complex \
    "[0:a]volume=-6dB[voice]; \
     [1:a]volume=-6dB[bin]; \
     [2:a]volume=0dB[sfx]; \
     [voice][bin][sfx]amix=inputs=3:duration=longest:normalize=0[mixed]" \
  -map "[mixed]" \
  -acodec pcm_s16le \
  sessions/{session}/output/session_mixed.wav
```

**Important**: Use `normalize=0` to prevent unpredictable level changes.

---

## Input Stems

| Stem | File | Required |
|------|------|----------|
| Voice | `voice_enhanced.wav` | Yes |
| Binaural | `binaural_dynamic.wav` | Yes |
| SFX | `sfx_track.wav` | Optional |

**Never use** `voice.mp3` - always use the enhanced version.

---

## Hypnotic Post-Processing (MANDATORY)

After mixing, apply psychoacoustic mastering:

```bash
python3 scripts/core/hypnotic_post_process.py --session sessions/{session}/
```

### Triple-Layer Hypnotic Presence

| Layer | Enhancement | Level | Effect |
|-------|-------------|-------|--------|
| 1 | Whisper Overlay | -22 dB | Ethereal presence |
| 2 | Subharmonic | -12 dB | Grounding presence |
| 3 | Double-Voice | -14 dB, 8ms delay | Subliminal presence |

### Additional Enhancements

| Enhancement | Description | Default |
|-------------|-------------|---------|
| Tape Warmth | Analog saturation | 25% drive |
| De-essing | Sibilance reduction | 4-8 kHz |
| Room Tone | Gentle reverb | 4% wet |
| Cuddle Waves | Amplitude modulation | 0.05 Hz, ±1.5 dB |
| Echo | Subtle depth | 180ms, 25% decay |

---

## Output Files

| File | Purpose |
|------|---------|
| `session_mixed.wav` | Pre-master mix (intermediate) |
| `{session}_MASTER.mp3` | **Final deliverable** (320 kbps) |
| `{session}_MASTER.wav` | Archive master (24-bit) |

---

## Two-Stem Mix (No SFX)

When no SFX track is needed:

```bash
ffmpeg -y \
  -i sessions/{session}/output/voice_enhanced.wav \
  -i sessions/{session}/output/binaural_dynamic.wav \
  -filter_complex \
    "[0:a]volume=-6dB[voice]; \
     [1:a]volume=-6dB[bin]; \
     [voice][bin]amix=inputs=2:duration=longest:normalize=0[mixed]" \
  -map "[mixed]" \
  -acodec pcm_s16le \
  sessions/{session}/output/session_mixed.wav
```

---

## Level Verification

After mixing, check levels:

```bash
# Check peak level (should be < 0 dB)
ffmpeg -i session_mixed.wav -af "volumedetect" -f null /dev/null 2>&1 | grep max_volume

# Check LUFS (target: -14 LUFS)
ffmpeg -i session_mixed.wav -af "loudnorm=print_format=json" -f null /dev/null 2>&1
```

### Target Levels

| Metric | Target | Acceptable Range |
|--------|--------|------------------|
| Integrated LUFS | -14 LUFS | -16 to -12 LUFS |
| True Peak | -1.5 dBTP | < -1.0 dBTP |
| Peak | -3 dB | < 0 dB |

---

## Binaural Beat Standards

| Brainwave State | Frequency Range | Use For |
|-----------------|-----------------|---------|
| Beta | 13-30 Hz | Alert, focused |
| Alpha | 8-12 Hz | Relaxed, light trance |
| Theta | 4-7 Hz | Deep trance, meditation |
| Delta | 0.5-3 Hz | Very deep, sleep-adjacent |

### Typical Journey Curve

```
0:00  - Alpha (10 Hz) - Induction
5:00  - Theta (7 Hz)  - Deepening
15:00 - Deep Theta (4 Hz) - Journey core
25:00 - Theta (7 Hz)  - Integration
28:00 - Alpha (10 Hz) - Emergence
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Clipping/distortion | Levels too hot | Check stem levels, use -6 dB |
| Binaural inaudible | Level too low | Should be -6 dB (not -12 dB) |
| Voice buried | Binaural too loud | Verify -6 dB on binaural |
| Muddy mix | Sample rate mismatch | All stems same rate (44100 or 48000) |
| SFX too harsh | Level too high | Try -3 dB for gentler SFX |
| Silent output | normalize=1 issue | Use `normalize=0` in amix |

---

## Quality Checklist

Before video assembly:

- [ ] `{session}_MASTER.mp3` exists
- [ ] No clipping or distortion
- [ ] Binaural beats audible but not intrusive
- [ ] Voice clear and present
- [ ] SFX properly timed (if used)
- [ ] LUFS within target range
- [ ] Duration matches expected

---

## Integration with Pipeline

**Before** (dependencies):
- Voice synthesis complete (`voice_enhanced.wav`)
- Binaural generated (`binaural_dynamic.wav`)
- SFX track if needed (`sfx_track.wav`)

**After** (next steps):
- Video assembly
- YouTube packaging

---

## Related Resources

- **Skill**: `tier3-production/voice-synthesis/` (input)
- **Skill**: `tier3-production/video-assembly/` (next step)
- **Serena Memory**: `audio_production_methodology`
- **Script**: `scripts/core/hypnotic_post_process.py`
