---
name: wavecap-silence
description: Tune WaveCap silence detection and voice activity settings. Use when the user wants to adjust chunk boundaries, reduce clipping, tune VAD sensitivity, or optimize latency vs accuracy trade-offs.
---

# WaveCap Silence Detection & Chunking Skill

Use this skill to tune how WaveCap detects speech boundaries and groups audio into chunks for transcription.

## Configuration Location

Silence/chunking settings are in the `whisper:` section:
- **User config:** `/Users/thw/Projects/WaveCap/state/config.yaml`
- **Default config:** `/Users/thw/Projects/WaveCap/backend/default-config.yaml`

## Core Parameters

### Silence Threshold (amplitude floor for speech detection)

```yaml
whisper:
  silenceThreshold: 0.015  # RMS amplitude (0.0-1.0)
```

| Value | Effect |
|-------|--------|
| 0.005-0.01 | Very sensitive, detects quiet speech, may trigger on noise |
| 0.015-0.02 | Balanced for most radio sources |
| 0.025-0.04 | Less sensitive, ignores background noise, may miss soft speech |

**Symptoms & Fixes:**
- Speech cut off at start → Lower threshold (e.g., 0.015 → 0.01)
- False triggers on noise → Raise threshold (e.g., 0.015 → 0.025)

### Silence Hold Seconds (wait before cutting)

```yaml
whisper:
  silenceHoldSeconds: 1.8  # Seconds of silence before flush
```

| Value | Effect |
|-------|--------|
| 0.5-0.8 | Fast updates, may clip trailing words |
| 1.0-1.5 | Balanced latency vs completeness |
| 1.8-2.5 | Safer for complete sentences, higher latency |

**Symptoms & Fixes:**
- Words cut off at end → Increase (e.g., 1.2 → 1.8)
- Updates feel slow → Decrease (e.g., 1.8 → 1.2)

### Silence Lookback Seconds (evaluation window)

```yaml
whisper:
  silenceLookbackSeconds: 3.0  # Window for silence detection
```

| Value | Effect |
|-------|--------|
| 1.0-2.0 | Responsive but may trigger on brief pauses |
| 3.0-4.0 | More stable, requires sustained silence |
| 5.0+ | Very stable, may delay chunk boundaries |

### Active Samples Percentage (VAD sensitivity)

```yaml
whisper:
  activeSamplesInLookbackPct: 0.10  # 10% of samples must be active
```

| Value | Effect |
|-------|--------|
| 0.05 (5%) | Very sensitive, keeps chunks open longer |
| 0.10 (10%) | Balanced default |
| 0.20 (20%) | Requires more sustained speech to keep chunk open |

### Chunk Length (maximum chunk duration)

```yaml
whisper:
  chunkLength: 20  # Maximum seconds before forced flush
```

| Value | Effect |
|-------|--------|
| 10-15 | Low latency, may break mid-sentence |
| 20-30 | Balanced for real-time monitoring |
| 45-60 | Better sentence structure, higher latency |

### Minimum Chunk Duration

```yaml
whisper:
  minChunkDurationSeconds: 12  # Minimum before silence triggers flush
```

| Value | Effect |
|-------|--------|
| 4-8 | Frequent small updates |
| 10-15 | Balanced, avoids tiny fragments |
| 15-20 | Fewer but larger chunks |

### Context Overlap (between chunks)

```yaml
whisper:
  contextSeconds: 1.5  # Overlap for Whisper context
```

| Value | Effect |
|-------|--------|
| 0.5 | Low latency, may lose speech at boundaries |
| 1.0-2.0 | Balanced overlap for boundary recovery |
| 3.0-5.0 | Maximum safety, more redundant processing |

## View Current Settings

```bash
grep -E "(silence|chunk|context|active)" /Users/thw/Projects/WaveCap/state/config.yaml
```

## Diagnose Clipping Issues

### Check for premature clipping (speech cut at start)

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.text | startswith("..."))] | length' | \
  xargs -I{} echo "Transcriptions starting with '...': {}"
```

### Check for late clipping (speech cut at end)

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.text | test("[a-z]$"))] | length' | \
  xargs -I{} echo "Transcriptions ending mid-word: {}"
```

### Analyze audio amplitude at boundaries

```bash
cd /Users/thw/Projects/WaveCap/backend && source .venv/bin/activate && python3 << 'EOF'
import numpy as np
from pathlib import Path

RECORDINGS = Path("/Users/thw/Projects/WaveCap/state/recordings")

def analyze_boundaries(filepath):
    with open(filepath, 'rb') as f:
        f.read(44)
        data = f.read()
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        if len(samples) < 1600:
            return None
        first_50ms = np.sqrt(np.mean(samples[:800]**2))
        last_50ms = np.sqrt(np.mean(samples[-800:]**2))
        return first_50ms, last_50ms

print("Boundary analysis (high RMS at start/end = potential clipping):")
print("-" * 70)
files = sorted(RECORDINGS.glob("*.wav"), key=lambda x: x.stat().st_mtime, reverse=True)[:15]
clip_start = clip_end = 0
for f in files:
    result = analyze_boundaries(f)
    if result:
        first, last = result
        issues = []
        if first > 0.06: issues.append("HIGH_START"); clip_start += 1
        if last > 0.06: issues.append("HIGH_END"); clip_end += 1
        status = ", ".join(issues) if issues else "OK"
        print(f"{f.name[-45:]}: start={first:.4f} end={last:.4f} [{status}]")
print("-" * 70)
print(f"Summary: {clip_start} potential start clips, {clip_end} potential end clips")
EOF
```

## Tuning Scenarios

### Reduce Clipping (speech being cut off)
```yaml
whisper:
  silenceThreshold: 0.012        # More sensitive
  silenceHoldSeconds: 2.0        # Wait longer before cutting
  silenceLookbackSeconds: 3.5    # Larger evaluation window
  contextSeconds: 2.0            # More overlap
  activeSamplesInLookbackPct: 0.08  # Keep chunks open easier
```

### Lower Latency (faster updates)
```yaml
whisper:
  silenceThreshold: 0.025        # Less sensitive
  silenceHoldSeconds: 0.8        # Cut quickly on silence
  silenceLookbackSeconds: 1.5    # Smaller window
  chunkLength: 15                # Shorter max chunks
  minChunkDurationSeconds: 6     # Allow smaller chunks
  contextSeconds: 0.5            # Minimal overlap
```

### Noisy Environment (false triggers)
```yaml
whisper:
  silenceThreshold: 0.035        # Ignore low-level noise
  silenceHoldSeconds: 1.0        # Quick silence detection
  activeSamplesInLookbackPct: 0.20  # Require 20% active
```

### Quiet Environment (soft speakers)
```yaml
whisper:
  silenceThreshold: 0.008        # Very sensitive
  silenceHoldSeconds: 2.0        # Patient with pauses
  activeSamplesInLookbackPct: 0.05  # 5% is enough
```

## Apply Changes

```bash
launchctl stop com.wavecap.server && sleep 2 && launchctl start com.wavecap.server
```

## Latency vs Accuracy Trade-offs

| Priority | chunkLength | minChunk | silenceHold | context |
|----------|-------------|----------|-------------|---------|
| Low latency | 15 | 6 | 0.8 | 0.5 |
| Balanced | 20 | 12 | 1.5 | 1.5 |
| High accuracy | 45 | 20 | 2.5 | 3.0 |

## Tips

- Changes take effect on service restart
- Test with live audio after changes
- Monitor clipping rates over 50+ transcriptions before final tuning
- `silenceThreshold` and `silenceHoldSeconds` have the biggest impact
- Higher `contextSeconds` helps but adds processing overhead
