---
name: Voice Synthesis
tier: 3
load_policy: task-specific
description: Generate voice audio using Google Cloud TTS with enhancement
version: 1.0.0
parent_skill: production-operations
---

# Voice Synthesis Skill

> **The Voice Is the Heart of the Journey**

This skill handles converting SSML scripts to voice audio with psychoacoustic enhancement.

---

## Purpose

Generate high-quality, hypnotic voice audio from SSML scripts using Google Cloud Text-to-Speech.

---

## Production Voice Standard

**Always use**: `en-US-Neural2-H` (bright female)

| Parameter | Value |
|-----------|-------|
| Voice ID | `en-US-Neural2-H` |
| Speaking Rate | 0.88x (applied by TTS engine) |
| Pitch | 0 semitones (base) |
| Enhancement | Always enabled |

---

## Canonical Command

```bash
python3 scripts/core/generate_voice.py \
    sessions/{session}/working_files/script_voice_clean.ssml \
    sessions/{session}/output
```

This automatically:
- Uses production voice (`en-US-Neural2-H`)
- Applies 0.88x speaking rate baseline
- Generates both raw and enhanced output
- Outputs `voice.mp3` and `voice_enhanced.mp3`

---

## Voice Options Reference

### Female Voices (Recommended for Hypnosis)

| Voice ID | Character | Best For |
|----------|-----------|----------|
| `en-US-Neural2-H` | Bright, clear | **Production standard** |
| `en-US-Neural2-E` | Deep, resonant | Darker themes, shadow work |
| `en-US-Neural2-C` | Soft, gentle | Very gentle sessions |
| `en-US-Neural2-F` | Clear, articulate | Educational content |
| `en-US-Neural2-G` | Warm, approachable | Confidence, empowerment |

### Male Voices

| Voice ID | Character | Best For |
|----------|-----------|----------|
| `en-US-Neural2-D` | Deep, authoritative | Guided pathworkings |
| `en-US-Neural2-I` | Warm, compassionate | Healing journeys |
| `en-US-Neural2-J` | Rich, mature | Wisdom, elder guidance |

**Note**: `en-US-Neural2-A` is MALE, not female.

---

## Output Files

| File | Purpose | Use For |
|------|---------|---------|
| `voice.mp3` | Raw TTS output | Never use directly |
| `voice_enhanced.mp3` | Production voice | **Always use this** |
| `voice_enhanced.wav` | Lossless for mixing | Audio mixing input |

---

## Voice Enhancement

The `generate_voice.py` script applies these enhancements:

| Enhancement | Effect |
|-------------|--------|
| Tape Warmth | Analog saturation (25% drive) |
| De-essing | Sibilance reduction (4-8 kHz) |
| Room Tone | Gentle reverb (4% wet) |
| EQ Shaping | Presence boost, rumble cut |

---

## Chunking System

Large scripts are automatically chunked:

1. **Detection**: Script exceeds API byte limit
2. **Splitting**: At natural break points (`<break time="3s"/>` or greater)
3. **Generation**: Each chunk processed separately
4. **Concatenation**: Final output seamlessly joined

---

## Duration Verification

After generation, verify duration matches target:

```bash
# Check duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \
    sessions/{session}/output/voice_enhanced.mp3
```

| Target Duration | Expected | Acceptable Range |
|-----------------|----------|------------------|
| 25 minutes | 25:00 | 23:00 - 27:00 |
| 30 minutes | 30:00 | 28:00 - 32:00 |
| 45 minutes | 45:00 | 42:00 - 48:00 |

If duration is off:
1. Adjust `<break>` durations in SSML
2. Add/remove content as needed
3. Regenerate voice

---

## Prerequisites

Before running voice synthesis:

1. **Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Google Cloud Auth**:
   ```bash
   echo $GOOGLE_APPLICATION_CREDENTIALS
   # Should show path to credentials JSON
   ```

3. **SSML Validation**:
   ```bash
   python3 scripts/utilities/validate_ssml.py sessions/{session}/working_files/script_voice_clean.ssml
   ```

4. **SFX Stripped**:
   ```bash
   grep -c "\[SFX:" sessions/{session}/working_files/script_voice_clean.ssml
   # Should return 0
   ```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "Authentication failed" | Missing credentials | Check `GOOGLE_APPLICATION_CREDENTIALS` |
| Robotic sound | Using slow rate in SSML | Use `rate="1.0"`, breaks for pacing |
| TTS reads "[SFX:..." | SFX markers not stripped | Use `script_voice_clean.ssml` |
| Chunking errors | Break points too far apart | Add `<break time="3s"/>` every few paragraphs |
| Duration too short | Not enough content | Add more script content |
| Duration too long | Too much content | Trim or reduce break times |

---

## Integration with Pipeline

**Before** (dependencies):
- SSML script validated
- SFX markers stripped

**After** (next steps):
- Audio mixing with binaural and SFX
- Hypnotic post-processing

---

## Quality Checklist

Before proceeding to mixing:

- [ ] `voice_enhanced.mp3` exists
- [ ] Duration within acceptable range
- [ ] No clipping (peak < 0 dB)
- [ ] No artifacts or glitches
- [ ] Pacing sounds natural
- [ ] All words clearly articulated

---

## Related Resources

- **Skill**: `tier3-production/ssml-generation/` (input)
- **Skill**: `tier3-production/audio-mixing/` (next step)
- **Serena Memory**: `audio_production_methodology`
- **Script**: `scripts/core/generate_voice.py`
