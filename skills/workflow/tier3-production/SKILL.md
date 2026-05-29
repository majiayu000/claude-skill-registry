---
name: Production Operations
tier: 3
load_policy: task-specific
description: Complete production pipeline for creating hypnotic audio/video sessions
version: 1.0.0
---

# Production Operations Skill (Tier 3)

> **This Is the Assembly Line of Dreamweaving**

This tier contains all operational skills for producing finished hypnotic sessions.

---

## Purpose

Execute the technical production pipeline from script to YouTube-ready package.

These skills are loaded based on the specific task being performed.

---

## Sub-Skills

| Skill | Location | Loads When |
|-------|----------|------------|
| **SSML Generation** | `ssml-generation/` | Script writing tasks |
| **Voice Synthesis** | `voice-synthesis/` | Audio generation tasks |
| **Audio Mixing** | `audio-mixing/` | Post-voice mixing tasks |
| **Video Assembly** | `video-assembly/` | Video creation tasks |
| **YouTube Packaging** | `youtube-packaging/` | Publication preparation |
| **Session Creation** | `session-creation/` | New session initialization |

---

## Pipeline Flow

```
Session Init → SSML Script → Voice TTS → Audio Mix → Video Assembly → YouTube Package
     │              │            │           │            │              │
     ▼              ▼            ▼           ▼            ▼              ▼
  session-      ssml-       voice-      audio-      video-        youtube-
  creation/   generation/  synthesis/   mixing/    assembly/     packaging/
```

---

## Production Standards

### Audio Quality

| Parameter | Standard |
|-----------|----------|
| Sample Rate | 44100 Hz or 48000 Hz |
| Bit Depth | 24-bit (processing), 16-bit (final) |
| LUFS | -14 LUFS integrated |
| True Peak | -1.5 dBTP maximum |
| Format | MP3 320kbps (delivery), WAV (masters) |

### Video Quality

| Parameter | Standard |
|-----------|----------|
| Resolution | 1920x1080 (Full HD) |
| Codec | H.264 |
| Frame Rate | 24 fps (cinematic) or 30 fps |
| Audio | AAC 320kbps |

### SSML Standards

| Parameter | Standard |
|-----------|----------|
| Speaking Rate | `rate="1.0"` (always) |
| Pacing | Via `<break>` tags only |
| Voice | `en-US-Neural2-H` (production) |
| Validation | Must pass `validate_ssml.py` |

---

## Integration with Other Tiers

| Tier | Relationship |
|------|--------------|
| **Tier 1** (Neural Core) | Content generation follows Tier 1 language/symbolic rules |
| **Tier 2** (Safety) | All output validated against safety constraints |
| **Tier 4** (Growth) | Analytics feed back to improve production |

---

## Quick Reference

### Full Build Command
```bash
/full-build {session}
```

### Individual Stages
```bash
/generate-script {session}   # SSML generation
/build-audio {session}       # Voice + mixing
/build-video {session}       # Video assembly
```

### Validation
```bash
python3 scripts/utilities/validate_ssml.py sessions/{session}/working_files/script.ssml
```

---

## Related Resources

- **Serena Memory**: `production_workflow_stages`
- **Serena Memory**: `audio_production_methodology`
- **Doc**: `docs/CANONICAL_WORKFLOW.md`
