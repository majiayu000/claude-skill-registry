---
name: wavecap-whisper
description: Tune WaveCap Whisper model settings. Use when the user wants to change model size, adjust decoding parameters, configure prompts, or optimize transcription accuracy vs speed.
---

# WaveCap Whisper Model Tuning Skill

Use this skill to tune the Whisper speech-to-text model for optimal transcription quality.

## Configuration Location

Whisper settings are in the `whisper:` section:
- **User config:** `/Users/thw/Projects/WaveCap/state/config.yaml`
- **Default config:** `/Users/thw/Projects/WaveCap/backend/default-config.yaml`

## Model Selection

### Primary Model

```yaml
whisper:
  model: large-v3-turbo  # Model checkpoint
```

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| tiny | 39M | Fastest | Low | Testing only |
| base | 74M | Very fast | Fair | CPU fallback |
| small | 244M | Fast | Good | Limited GPU |
| medium | 769M | Moderate | Very good | Balanced |
| large-v2 | 1.5B | Slow | Excellent | High accuracy |
| large-v3 | 1.5B | Slow | Best | Maximum accuracy |
| **large-v3-turbo** | 809M | Fast | Excellent | **Recommended** |

### Backend Selection

```yaml
whisper:
  backend: auto  # auto, mlx, faster-whisper
```

| Backend | Platform | Performance |
|---------|----------|-------------|
| auto | Any | Detects best option |
| mlx | Apple Silicon | 10-50x faster than CPU |
| faster-whisper | CUDA/CPU | Best for NVIDIA GPUs |

### CPU Fallback Model

```yaml
whisper:
  cpuFallbackModel: base  # Model when GPU unavailable
```

Set to `null` to use the primary model on CPU (slower but more accurate).

## Decoding Parameters

### Beam Size (search width)

```yaml
whisper:
  beamSize: 8  # 1-15, higher = more consistent
```

| Value | Effect |
|-------|--------|
| 1-3 | Fast, less consistent |
| 5-8 | Balanced (default) |
| 10-15 | More consistent, slower |

### Temperature (randomness)

```yaml
whisper:
  decodeTemperature: 0.0  # 0.0 = deterministic
  temperatureIncrementOnFallback: 0.2  # Boost on low confidence
```

| Temperature | Effect |
|-------------|--------|
| 0.0 | Deterministic, consistent output |
| 0.1-0.3 | Slight variation, may recover from errors |
| 0.5+ | More creative, not recommended for transcription |

### Condition on Previous Text

```yaml
whisper:
  conditionOnPreviousText: false
```

| Value | Effect |
|-------|--------|
| false | Each chunk independent (default) |
| true | Uses previous segment context, better punctuation consistency |

## Language Configuration

```yaml
whisper:
  language: en  # ISO 639-1 code
```

Common codes: `en` (English), `es` (Spanish), `fr` (French), `de` (German), `ja` (Japanese)

Per-stream override:
```yaml
streams:
  - id: spanish-feed
    language: es
```

## Initial Prompts (domain vocabulary)

### Global Prompt

```yaml
whisper:
  initialPrompt: >-
    Emergency radio dispatch. Key terms: Adelaide, SITREP, SAPOL, SES, CFS.
```

### Named Prompts (reusable)

```yaml
whisper:
  prompts:
    sa_emergency: >-
      South Australia emergency dispatch. Terms: Adelaide, Noarlunga, SAPOL, SES, CFS.
    marine_vhf: >-
      Marine VHF radio. Terms: mayday, pan-pan, sécurité, vessel, nautical miles.
```

### Assign to Stream

```yaml
streams:
  - id: broadcastify-2653
    initialPromptName: sa_emergency
```

## Concurrency

```yaml
whisper:
  maxConcurrentProcesses: 2  # Parallel transcription jobs
```

| Value | Effect |
|-------|--------|
| 1 | Sequential, lowest memory |
| 2-3 | Balanced for most systems |
| 4+ | High throughput, needs strong GPU |

## View Current Settings

```bash
grep -A30 "whisper:" /Users/thw/Projects/WaveCap/state/config.yaml | head -35
```

## Check Model Status

```bash
curl -s http://localhost:8000/api/health | jq
```

## Tuning Scenarios

### Maximum Accuracy (powerful hardware)
```yaml
whisper:
  model: large-v3
  backend: auto
  beamSize: 12
  decodeTemperature: 0.0
  conditionOnPreviousText: true
  maxConcurrentProcesses: 1
```

### Balanced Real-Time (recommended)
```yaml
whisper:
  model: large-v3-turbo
  backend: auto
  beamSize: 8
  decodeTemperature: 0.0
  conditionOnPreviousText: false
  maxConcurrentProcesses: 2
```

### Low Latency (weaker hardware)
```yaml
whisper:
  model: small
  backend: auto
  cpuFallbackModel: tiny
  beamSize: 5
  decodeTemperature: 0.0
  maxConcurrentProcesses: 1
```

### Apple Silicon Optimized
```yaml
whisper:
  model: large-v3-turbo
  backend: mlx
  cpuFallbackModel: null  # Use primary on CPU too
  beamSize: 8
  maxConcurrentProcesses: 2
```

## Prompt Engineering Tips

### Effective Prompts
- Include domain-specific terms that Whisper might misspell
- Use proper capitalization for names and acronyms
- Keep prompts under 200 words
- Include example phrases if helpful

### Example for Emergency Radio
```yaml
whisper:
  initialPrompt: >-
    Emergency services radio dispatch for South Australia.
    Common terms: Adelaide, Adelaide fire out, Noarlunga, Aldinga, Para Hills,
    SITREP (situation report), SAPOL (SA Police), SES (State Emergency Service),
    CFS (Country Fire Service), MFS (Metropolitan Fire Service).
    Station identifiers: Sturt, Gawler, Metro, Blackwood.
    Radio protocol: Roger, Wilco, Over, Out, Copy that.
```

## Apply Changes

```bash
launchctl stop com.wavecap.server && sleep 2 && launchctl start com.wavecap.server
```

## Monitor Transcription Quality

### Check confidence distribution
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.confidence | . * 10 | floor / 10) |
      map({confidence: (.[0].confidence | . * 10 | floor / 10), count: length}) |
      sort_by(.confidence)'
```

### Find low-confidence transcriptions
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.confidence < 0.7)] | sort_by(.confidence) | .[:5] | .[] | {confidence, text}'
```

## Tips

- `large-v3-turbo` offers the best speed/accuracy balance
- MLX backend on Apple Silicon is significantly faster
- Initial prompts help with domain-specific vocabulary
- Lower beam size for faster processing, higher for consistency
- Temperature 0.0 is best for transcription accuracy
- Monitor confidence scores to evaluate model performance
