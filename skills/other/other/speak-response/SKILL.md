---
name: speak-response
description: Vocalize Claude's last response using local Qwen3-TTS. Default voice is the Oracle (deep, resonant Dune narrator). Use --preset for emotion-controlled preset speakers.
argument-hint: [sentences|"text"|--preset mood:warm]
disable-model-invocation: true
---

# Speak Response

Vocalize text using local Qwen3-TTS. Default voice is the **Oracle** (cloned from a Dune narrator with deep, resonant, prophetic quality).

## Quick Examples

| Command | Effect |
|---------|--------|
| `/speak` | Last 2 sentences with Oracle voice |
| `/speak 5` | Last 5 sentences with Oracle voice |
| `/speak "The sleeper must awaken."` | Specific text with Oracle voice |
| `/speak --preset mood:warm` | Last 2 sentences with preset speaker + emotion |
| `/speak --preset "Hello" speaker:Vivian voice:"nurturing"` | Preset speaker with custom voice |

## Default: Oracle Voice

The oracle voice is a deep, resonant, prophetic voice cloned from a Dune narrator. It speaks all text with a sense of ancient wisdom and gravitas.

```bash
# Default usage - Oracle voice
scripts/speak.sh "The spice must flow."
scripts/speak.sh "He who controls the spice controls the universe."
```

### Limitation

The Oracle uses voice cloning (Base model), which does **not** support per-message instruction control. The voice characteristics are fixed. For emotion/mood control, use `--preset`.

## Preset Speakers (--preset)

For emotion and mood control, use `--preset` to switch to CustomVoice with adjustable instructions:

```bash
scripts/speak.sh --preset "<text>" [speaker] [instruction]
```

### Quick Preset Examples

```bash
# Calm therapeutic voice
scripts/speak.sh --preset "Take a deep breath." Vivian "calm, nurturing, gentle pace"

# Excited announcement
scripts/speak.sh --preset "We did it!" Ryan "joyful, excited, enthusiastic"

# Serious explanation
scripts/speak.sh --preset "This is important." Eric "serious, measured, emphatic"
```

### Custom Voice Instructions

The model understands rich natural language descriptions:

| Aspect | Examples |
|--------|----------|
| **Emotion** | joyful, melancholic, anxious, calm, excited, contemplative |
| **Pace** | slow and deliberate, rapid and energetic, measured, hesitant |
| **Intensity** | soft and gentle, loud and commanding, whispered, emphatic |
| **Style** | warm and nurturing, professional, playful, dramatic |
| **Prosody** | with dramatic pauses, rising intonation, emphatic on key words |

### Mood Presets (Shortcuts)

| Preset | Expands To |
|--------|------------|
| `calm` | "calm, soothing, gentle pace" |
| `warm` | "warm, empathetic, nurturing tone" |
| `excited` | "joyful, excited, enthusiastic" |
| `serious` | "serious, measured, authoritative" |
| `gentle` | "soft, gentle, whispered" |
| `encouraging` | "encouraging, uplifting, sincere" |
| `contemplative` | "thoughtful, slow pace, reflective" |

### Speakers

| Speaker | Best For |
|---------|----------|
| Ryan (default) | Professional, serious, authoritative |
| Vivian | Warm, nurturing, therapeutic |
| Serena | Calm, gentle, contemplative |
| Dylan | Friendly, casual, playful |
| Eric | Serious, dramatic, commanding |
| Aiden | Encouraging, uplifting, energetic |
| Uncle_Fu | Wise, measured |
| Ono_Anna | Soft, gentle |
| Sohee | Clear, professional |

## Workflow

1. Parse arguments for text and mode (default oracle vs --preset)
2. Extract text from last response if not provided
3. **Default mode**: Clone with Oracle voice
4. **Preset mode**: Generate with CustomVoice + instruction
5. Audio plays through macOS speakers

## Execution

```bash
# Oracle voice (default)
scripts/speak.sh "<text>"

# Preset speaker with instruction
scripts/speak.sh --preset "<text>" [speaker] [instruction]
```

## Voice Cloning (Custom Voices)

Clone any voice from a 3+ second audio sample:

```bash
# Get transcript first (use Whisper API)
curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@reference.mp3" -F model="whisper-1"

# Clone the voice
scripts/clone.sh "<text to speak>" "<audio_file>" "<transcript>"
```

## Voice Design (Create New Voices)

Design entirely new voices from natural language descriptions:

```bash
scripts/design-voice.sh "<sample_text>" "<voice_description>"

# Example: Create a warm guide voice
scripts/design-voice.sh \
  "Take a deep breath and feel this moment." \
  "warm, nurturing, gentle pace, empathetic, female"
```

Then clone the designed voice for reuse:

```bash
scripts/clone.sh "New text" designed-voice.wav "Original sample text"
```

See `references/moods.md` for more instruction examples.
