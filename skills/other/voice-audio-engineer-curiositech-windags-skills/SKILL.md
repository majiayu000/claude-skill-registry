---
name: voice-audio-engineer
description: Expert in voice synthesis, TTS, voice cloning, podcast production, speech processing, and voice UI design via ElevenLabs integration. Specializes in vocal clarity, loudness standards (LUFS), de-essing, dialogue mixing, and voice transformation. Activate on 'TTS', 'text-to-speech', 'voice clone', 'voice synthesis', 'ElevenLabs', 'podcast', 'voice recording', 'speech-to-speech', 'voice UI', 'audiobook', 'dialogue'. NOT for spatial audio (use sound-engineer), music production (use DAW tools), game audio middleware (use sound-engineer), sound effects generation (use sound-engineer with ElevenLabs SFX), or live concert audio.
allowed-tools: Read,Write,Edit,Bash,mcp__firecrawl__firecrawl_search,WebFetch,mcp__ElevenLabs__text_to_speech,mcp__ElevenLabs__speech_to_speech,mcp__ElevenLabs__voice_clone,mcp__ElevenLabs__search_voices,mcp__ElevenLabs__speech_to_text,mcp__ElevenLabs__isolate_audio,mcp__ElevenLabs__create_agent
category: Design & Creative
tags:
  - voice
  - tts
  - elevenlabs
  - podcast
  - synthesis
pairs-with:
  - skill: sound-engineer
    reason: Full audio production pipeline
  - skill: speech-pathology-ai
    reason: Clinical voice applications
---

# Voice & Audio Engineer: Voice Synthesis, TTS & Speech Processing

Expert in voice synthesis, speech processing, and vocal production using ElevenLabs and professional audio techniques. Specializes in TTS, voice cloning, podcast production, and voice UI design.

## When to Use This Skill

✅ **Use for:**
- Text-to-speech (TTS) generation
- Voice cloning and voice design
- Speech-to-speech voice transformation
- Podcast production and editing
- Audiobook production
- Voice UI/conversational AI audio
- Dialogue mixing and processing
- Loudness normalization (LUFS)
- Voice quality enhancement (de-essing, compression)
- Transcription and speech-to-text

❌ **Do NOT use for:**
- Spatial audio (HRTF, Ambisonics) → **sound-engineer**
- Sound effects generation → **sound-engineer** (ElevenLabs SFX)
- Game audio middleware (Wwise, FMOD) → **sound-engineer**
- Music composition/production → DAW tools
- Live concert/event audio → specialized domain

## MCP Integrations

| MCP Tool | Purpose |
|----------|---------|
| `text_to_speech` | Generate speech from text with voice selection |
| `speech_to_speech` | Transform voice recordings to different voices |
| `voice_clone` | Create instant voice clones from audio samples |
| `search_voices` | Find voices in ElevenLabs library |
| `speech_to_text` | Transcribe audio with speaker diarization |
| `isolate_audio` | Separate voice from background noise |
| `create_agent` | Build conversational AI agents with voice |

## Expert vs Novice Shibboleths

| Topic | Novice | Expert |
|-------|--------|--------|
| **TTS quality** | "Any voice works" | Matches voice to brand; considers emotion, pace, style |
| **Voice cloning** | "Upload any audio" | Knows 30s-3min of clean, varied speech needed; single speaker |
| **Loudness** | "Make it loud" | Targets -16 to -19 LUFS for podcasts; -14 for streaming |
| **De-essing** | "Doesn't matter" | Knows sibilance lives at 5-8kHz; frequency-selective compression |
| **Compression** | "Squash it" | Uses 3:1-4:1 for dialogue; slow attack (10-20ms) to preserve transients |
| **High-pass** | "Never use it" | Always HPF at 80-100Hz for voice; removes rumble, plosives |
| **True peak** | "Peak is peak" | Knows intersample peaks exceed 0dBFS; targets -1 dBTP |
| **ElevenLabs models** | "Use default" | `eleven_multilingual_v2` for quality; `eleven_flash_v2_5` for speed |

## Common Anti-Patterns

### Anti-Pattern: Uploading Noisy Audio for Voice Cloning
**What it looks like**: Voice clone from phone recording with background noise, echo
**Why it's wrong**: Clone learns the noise; output has artifacts
**What to do instead**: Use `isolate_audio` first; record in quiet space; provide 1-3 min of varied speech

### Anti-Pattern: Ignoring Loudness Standards
**What it looks like**: Podcast at -6 LUFS, then normalized by platform → crushed dynamics
**Why it's wrong**: Each platform normalizes differently; too loud = distortion, too quiet = inaudible
**What to do instead**: Master to -16 LUFS for podcasts; -14 LUFS for streaming; always check true peak < -1 dBTP

### Anti-Pattern: TTS Without Voice Matching
**What it looks like**: Using default robotic voice for premium product
**Why it's wrong**: Voice IS brand; wrong voice = wrong emotional connection
**What to do instead**: `search_voices` to find matching tone; consider custom clone for brand consistency

### Anti-Pattern: No De-essing on Processed Voice
**What it looks like**: "SSSSibilant" speech after compression and EQ boost
**Why it's wrong**: Compression brings up sibilance; EQ boost at 3-5kHz makes it worse
**What to do instead**: De-ess at 5-8kHz before compression; use frequency-selective compression

### Anti-Pattern: Single Take, No Editing
**What it looks like**: Podcast with 20 "ums", breath sounds, long pauses
**Why it's wrong**: Listeners fatigue; unprofessional; reduces engagement
**What to do instead**: Edit out filler words; gate or manually cut breaths; tighten pacing

## Evolution Timeline

### Pre-2020: Robotic TTS
- Concatenative synthesis (spliced recordings)
- Obvious robotic quality
- Limited voice options

### 2020-2022: Neural TTS Emerges
- Tacotron, WaveNet improve naturalness
- Still detectable as synthetic
- Voice cloning requires hours of data

### 2023-2024: AI Voice Revolution
- ElevenLabs instant voice cloning (30 seconds)
- Near-human quality in TTS
- Real-time voice transformation
- Voice agents for customer service

### 2025+: Current Best Practices
- Emotional TTS (control tone, pace, emotion)
- Cross-lingual voice cloning
- Real-time voice transformation in apps
- Personalized voice agents
- Voice authentication integration

## Core Concepts

### ElevenLabs Voice Selection

**Model comparison:**
| Model | Quality | Latency | Languages | Use Case |
|-------|---------|---------|-----------|----------|
| `eleven_multilingual_v2` | Best | Higher | 29 | Production, quality-critical |
| `eleven_flash_v2_5` | Good | Lowest | 32 | Real-time, voice UI |
| `eleven_turbo_v2_5` | Better | Low | 32 | Balanced |

**Voice parameters:**
```python
# Stability: 0-1 (lower = more expressive, higher = more consistent)
# Similarity boost: 0-1 (higher = closer to original voice)
# Style: 0-1 (higher = more exaggerated style)

# For natural speech:
stability = 0.5       # Balanced expression
similarity = 0.75     # Close to voice but natural
style = 0.0           # Neutral (increase for dramatic)
```

### Voice Cloning Best Practices

**Audio requirements:**
- Duration: 1-3 minutes (more = better, diminishing returns after 3min)
- Quality: Clean, no background noise, no reverb
- Content: Varied speech (questions, statements, emotions)
- Format: WAV/MP3, 44.1kHz or higher

**Cloning workflow:**
1. `isolate_audio` to clean source material
2. `voice_clone` with cleaned audio
3. Test with varied prompts
4. Adjust stability/similarity for output quality

### Voice Processing Chain

**Standard voice chain (order matters!):**
```
[Raw Recording]
    ↓
[High-Pass Filter @ 80Hz]  ← Remove rumble, plosives
    ↓
[De-esser @ 5-8kHz]        ← Before compression!
    ↓
[Compressor 3:1, 10ms/100ms] ← Smooth dynamics
    ↓
[EQ: +2dB @ 3kHz presence] ← Clarity boost
    ↓
[Limiter -1 dBTP]          ← Prevent clipping
    ↓
[Loudness Norm -16 LUFS]   ← Target loudness
```

### Loudness Standards

| Platform/Format | Target LUFS | True Peak |
|-----------------|-------------|-----------|
| Podcast | -16 to -19 | -1 dBTP |
| Audiobook (ACX) | -18 to -23 RMS | -3 dBFS |
| YouTube | -14 | -1 dBTP |
| Spotify/Apple Music | -14 | -1 dBTP |
| Broadcast (EBU R128) | -23 ±1 | -1 dBTP |

**Measurement:**
- LUFS = Loudness Units Full Scale (integrated)
- True Peak = Maximum level including intersample peaks
- Always measure with K-weighting (ITU-R BS.1770)

### Conversational AI Agents

**ElevenLabs agent configuration:**
```python
create_agent(
    name="Support Agent",
    first_message="Hi, how can I help you today?",
    system_prompt="You are a helpful customer support agent...",
    voice_id="your_voice_id",
    language="en",
    llm="gemini-2.0-flash-001",  # Fast for conversation
    temperature=0.5,
    asr_quality="high",          # Speech recognition quality
    turn_timeout=7,              # Seconds before agent responds
    max_duration_seconds=300     # 5 minute call limit
)
```

**Voice UI considerations:**
- Use fast model (`eleven_flash_v2_5`) for real-time
- Keep responses concise (< 30 seconds)
- Add pauses for natural conversation flow
- Handle interruptions gracefully

## Quick Reference

### Voice Selection Decision Tree
- **Brand/professional content?** → Custom clone or curated voice
- **Real-time/interactive?** → `eleven_flash_v2_5` model
- **Quality-critical?** → `eleven_multilingual_v2` model
- **Multiple languages?** → Check language support per voice

### Processing Decision Tree
- **Voice sounds muddy?** → HPF at 80Hz, boost 3kHz
- **Sibilance harsh?** → De-ess at 5-8kHz
- **Inconsistent volume?** → Compress 3:1, then limit
- **Too quiet?** → Normalize to target LUFS
- **Background noise?** → Use `isolate_audio` first

### Common Settings
```
De-esser: 5-8kHz, -6dB reduction, Q=2
Compressor: 3:1 ratio, -20dB threshold, 10ms attack, 100ms release
EQ presence: +2-3dB shelf at 3kHz
HPF: 80-100Hz, 12dB/oct
Limiter: -1 dBTP ceiling
```

## Working With Speech Disfluencies

### Cluttering vs Stuttering

| Type | Characteristics | ASR Impact |
|------|-----------------|------------|
| **Stuttering** | Repetitions ("I-I-I"), prolongations ("wwwant"), blocks (silent pauses) | Word boundaries confused; repetitions misrecognized |
| **Cluttering** | Irregular rate, collapsed syllables, filler overload, tangential speech | Words merged; rate changes confuse timing |

### ASR Challenges with Disfluent Speech

Most ASR models trained on fluent speech. Disfluencies cause:
- Word boundary detection errors
- Repetitions transcribed literally ("I I I want" vs "I want")
- Collapsed syllables missed entirely
- Timing models confused by irregular pace

### Solutions & Workarounds

**1. Model selection (best to worst for disfluencies):**
- **Whisper large-v3** - Most robust to disfluencies
- **ElevenLabs speech_to_text** - Good with varied speech
- **Google Speech-to-Text** - Decent with enhanced models
- **Fast/lightweight models** - Usually worst

**2. Pre-processing:**
```python
# Normalize speech rate before ASR
# Use librosa to stretch irregular segments toward target rate
import librosa
y, sr = librosa.load("disfluent.wav")
y_stretched = librosa.effects.time_stretch(y, rate=0.9)  # Slow down
```

**3. Post-processing:**
- Remove duplicate words: "I I I want" → "I want"
- Filter common fillers: "um", "uh", "like", "you know"
- Use LLM to clean transcripts while preserving meaning

**4. Fine-tuning Whisper (advanced):**
```python
# Fine-tune on disfluent speech dataset
# Datasets: FluencyBank, UCLASS, SEP-28k (stuttering)
from transformers import WhisperForConditionalGeneration, WhisperProcessor

model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3")
# Fine-tune on your speech samples with corrected transcripts
# Training loop with disfluent audio → fluent transcript pairs
```

**5. ElevenLabs voice cloning approach:**
- Clone your voice from fluent segments
- Use TTS for fluent output with your voice
- Great for pre-recorded content, not live

### Accessibility Considerations

- Always provide manual transcript correction option
- Consider hybrid: ASR + human review
- For voice UI: longer timeout, confirmation prompts
- Test with actual users from target population

## Performance Targets

| Operation | Typical Time |
|-----------|--------------|
| TTS (100 words) | 2-5 seconds |
| Voice clone creation | 10-30 seconds |
| Speech-to-speech | 3-8 seconds |
| Transcription (1 min audio) | 5-15 seconds |
| Audio isolation | 5-20 seconds |

## Integrates With

- **sound-engineer** - For spatial audio, game audio, procedural SFX
- **native-app-designer** - Voice UI implementation in apps
- **vr-avatar-engineer** - Avatar voice integration

---

**For detailed implementations**: See `/references/implementations.md`

**Remember**: Voice is intimate—it speaks directly to the listener's brain. Match voice to brand, process for clarity not loudness, and always respect the platform's loudness standards. With ElevenLabs, you have instant access to professional voice synthesis; use it thoughtfully.
