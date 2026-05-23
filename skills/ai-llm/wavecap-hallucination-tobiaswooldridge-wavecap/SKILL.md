---
name: wavecap-hallucination
description: Configure WaveCap hallucination detection and prevention. Use when Whisper outputs gibberish, repeated phrases, or phantom text on silent audio.
---

# WaveCap Hallucination Prevention Skill

Use this skill to detect and filter out Whisper hallucinations - false transcriptions generated when there's no actual speech.

## What Are Hallucinations?

Whisper sometimes generates plausible-sounding text when fed:
- Silent audio or white noise
- Background music or tones
- Very low-quality speech

Common hallucination patterns:
- "Thank you for watching"
- "Transcription by CastingWords"
- Repeated phrases like "the the the the"
- Random punctuation or symbols

## Configuration Location

Hallucination settings are in the `whisper:` section:
- **User config:** `/Users/thw/Projects/WaveCap/state/config.yaml`

## Silence Hallucination Phrases

Phrases that indicate Whisper hallucinated rather than transcribed:

```yaml
whisper:
  silenceHallucinationPhrases:
    - "thank you"
    - "thanks for watching"
    - "transcription by castingwords"
    - "casting words"
    - "all right here we go"
    - "alright here we go"
    - "all right let's go"
    - "alright let's go"
    - "you"
    - "bye"
    - "uh"
    - "hmm"
```

When these phrases appear on low-energy audio, the transcription is discarded.

### Add Custom Hallucination Phrases

If you notice recurring false phrases, add them:

```bash
# View current phrases
grep -A20 "silenceHallucinationPhrases:" /Users/thw/Projects/WaveCap/state/config.yaml
```

## Segment Repetition Detection

Detects when Whisper outputs the same phrase repeatedly (a common failure mode):

```yaml
whisper:
  segmentRepetitionMinCharacters: 16  # Min chars to check for repetition
  segmentRepetitionMaxAllowedConsecutiveRepeats: 4  # Max allowed repeats
```

| Parameter | Default | Effect |
|-----------|---------|--------|
| segmentRepetitionMinCharacters | 16 | Phrases shorter than this are ignored |
| segmentRepetitionMaxAllowedConsecutiveRepeats | 4 | More than this = discard |

Example: "test test test test test" (5 repeats) would be discarded if max is 4.

## Blank Audio Detection

Configure when to emit `[BLANK_AUDIO]` tokens instead of attempting transcription:

```yaml
whisper:
  blankAudioMinDurationSeconds: 3.0  # Min duration to check
  blankAudioMinActiveRatio: 0.05     # Max 5% active samples
  blankAudioMinRms: 0.01             # Min RMS to consider "active"
```

| Parameter | Default | Effect |
|-----------|---------|--------|
| blankAudioMinDurationSeconds | null | Minimum chunk duration to evaluate |
| blankAudioMinActiveRatio | null | If active ratio below this, mark blank |
| blankAudioMinRms | null | RMS threshold for "active" audio |

Set to `null` to disable blank audio detection.

## View Current Settings

```bash
grep -E "(hallucination|repetition|blank)" /Users/thw/Projects/WaveCap/state/config.yaml
```

## Diagnose Hallucination Issues

### Find potential hallucinations in transcriptions

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(
    (.text | test("thank you|thanks for|transcription by|casting"; "i")) or
    (.text | test("^(uh|um|hmm|bye|you)$"; "i"))
  )] | .[:10] | .[] | {id, text, confidence}'
```

### Find repeated phrase patterns

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.text | test("(\\b\\w{4,}\\b).*\\1.*\\1.*\\1"))] |
      .[:10] | .[] | {id, text: (.text | .[0:100])}'
```

### Count BLANK_AUDIO tokens

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.text == "[BLANK_AUDIO]")] | length'
```

### Find low-confidence + short transcriptions (likely noise)

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.confidence < 0.6 and (.text | length) < 20)] |
      .[:10] | .[] | {id, text, confidence}'
```

## Tuning Scenarios

### Aggressive Hallucination Filtering
```yaml
whisper:
  silenceHallucinationPhrases:
    - "thank you"
    - "thanks for watching"
    - "transcription by castingwords"
    - "you"
    - "bye"
    - "uh"
    - "um"
    - "hmm"
    - "okay"
  segmentRepetitionMinCharacters: 12
  segmentRepetitionMaxAllowedConsecutiveRepeats: 3
  blankAudioMinDurationSeconds: 2.0
  blankAudioMinActiveRatio: 0.08
  blankAudioMinRms: 0.015
```

### Conservative (keep more transcriptions)
```yaml
whisper:
  silenceHallucinationPhrases:
    - "transcription by castingwords"
    - "casting words"
  segmentRepetitionMinCharacters: 20
  segmentRepetitionMaxAllowedConsecutiveRepeats: 5
  blankAudioMinDurationSeconds: null  # Disabled
```

### Radio with Music/Tones (e.g., hold music)
```yaml
whisper:
  silenceHallucinationPhrases:
    - "thank you"
    - "music"
    - "playing"
  blankAudioMinActiveRatio: 0.15  # Higher threshold due to tones
```

## Apply Changes

```bash
launchctl stop com.wavecap.server && sleep 2 && launchctl start com.wavecap.server
```

## Analyze Audio Energy for Tuning

Check if hallucinations correlate with low-energy audio:

```bash
cd /Users/thw/Projects/WaveCap/backend && source .venv/bin/activate && python3 << 'EOF'
import numpy as np
from pathlib import Path
import json
import urllib.request

# Get recent transcriptions
with urllib.request.urlopen("http://localhost:8000/api/transcriptions/export") as r:
    transcriptions = json.loads(r.read())

RECORDINGS = Path("/Users/thw/Projects/WaveCap/state/recordings")

def get_rms(filepath):
    try:
        with open(filepath, 'rb') as f:
            f.read(44)
            data = f.read()
            samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            return np.sqrt(np.mean(samples**2))
    except:
        return None

print("Low-confidence transcriptions with audio RMS:")
print("-" * 70)
low_conf = [t for t in transcriptions if t.get('confidence', 1) < 0.7 and t.get('recordingUrl')][:10]
for t in low_conf:
    filename = t['recordingUrl'].split('/')[-1]
    filepath = RECORDINGS / filename
    rms = get_rms(filepath)
    rms_str = f"{rms:.4f}" if rms else "N/A"
    print(f"conf={t['confidence']:.2f} rms={rms_str} text={t['text'][:50]}")
EOF
```

## Tips

- Add phrases you see repeatedly on silent chunks to the hallucination list
- Lower `segmentRepetitionMaxAllowedConsecutiveRepeats` if you see stuttering output
- Use `blankAudioMinRms` to catch very quiet segments before Whisper processes them
- Monitor `[BLANK_AUDIO]` count - too many may indicate overly aggressive filtering
- Hallucination phrases are case-insensitive and matched as substrings
