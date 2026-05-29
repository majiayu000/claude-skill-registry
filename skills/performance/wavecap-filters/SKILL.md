---
name: wavecap-filters
description: Tune WaveCap audio filters and AGC settings. Use when the user wants to adjust highpass/lowpass filters, automatic gain control, de-emphasis, or improve audio quality for transcription.
---

# WaveCap Audio Filter Tuning Skill

Use this skill to tune audio pre-processing filters that improve speech intelligibility before transcription.

## Configuration Location

Audio filter settings are in the `whisper:` section of the config file:
- **User config:** `/Users/thw/Projects/WaveCap/state/config.yaml`
- **Default config:** `/Users/thw/Projects/WaveCap/backend/default-config.yaml`

## Filter Parameters

### Highpass Filter (removes low-frequency rumble)

```yaml
whisper:
  highpassCutoffHz: 250  # Default: 250 Hz
```

| Value | Effect |
|-------|--------|
| 80-150 Hz | Preserves bass, some rumble may remain |
| 200-300 Hz | Balanced for emergency radio (default) |
| 400-500 Hz | Aggressive rumble removal, may thin voice |

**When to adjust:**
- Increase if you hear wind noise, engine rumble, or low-frequency hum
- Decrease if voices sound thin or tinny

### Lowpass Filter (removes high-frequency hiss)

```yaml
whisper:
  lowpassCutoffHz: 3800  # Default: 3800 Hz
```

| Value | Effect |
|-------|--------|
| 3000-3500 Hz | More aggressive hiss removal, slightly muffled |
| 3800-4000 Hz | Balanced for radio speech intelligibility (default) |
| 4500-6000 Hz | Preserves more clarity, but keeps more hiss |

**When to adjust:**
- Decrease if there's persistent high-frequency hiss or static
- Increase if speech sounds muffled or lacks clarity

### De-emphasis (compensates for radio pre-emphasis)

```yaml
whisper:
  deemphasisTimeConstantMicros: 75  # Default: 75 microseconds
```

| Value | Effect |
|-------|--------|
| 50 μs | Less treble reduction (North American FM standard) |
| 75 μs | Moderate treble reduction (default, good for most radio) |
| 100-150 μs | More treble reduction (European FM standard) |

**When to adjust:**
- If audio sounds too bright/harsh, increase the value
- If audio sounds too dull, decrease the value

### Automatic Gain Control (AGC)

```yaml
whisper:
  agcTargetRms: 0.04  # Default: 0.04 (4% of full scale)
```

| Value | Effect |
|-------|--------|
| null | AGC disabled (use raw audio levels) |
| 0.02-0.03 | Light normalization, preserves dynamics |
| 0.04-0.05 | Moderate normalization (default) |
| 0.06-0.08 | Aggressive boost for very quiet sources |

**When to adjust:**
- Increase if audio is too quiet and Whisper misses words
- Decrease if audio clips or sounds distorted
- Set to `null` if source audio is already well-normalized

## View Current Settings

```bash
grep -A20 "whisper:" /Users/thw/Projects/WaveCap/state/config.yaml | grep -E "(highpass|lowpass|deemphasis|agc)"
```

## Common Tuning Scenarios

### Noisy Environment (wind, engines, background noise)
```yaml
whisper:
  highpassCutoffHz: 350      # More aggressive low-cut
  lowpassCutoffHz: 3500      # Reduce hiss
  agcTargetRms: 0.05         # Boost speech above noise
```

### Clean Studio/Dispatch Audio
```yaml
whisper:
  highpassCutoffHz: 150      # Preserve natural bass
  lowpassCutoffHz: 4500      # Keep clarity
  agcTargetRms: 0.03         # Light normalization
```

### Weak/Distant Radio Signal
```yaml
whisper:
  highpassCutoffHz: 300      # Remove noise floor
  lowpassCutoffHz: 3800      # Standard
  agcTargetRms: 0.07         # Aggressive boost
```

### Broadcastify/Web Streams (already processed)
```yaml
whisper:
  highpassCutoffHz: 200      # Light filtering
  lowpassCutoffHz: 4000      # Preserve quality
  agcTargetRms: 0.04         # Standard
```

## Apply Changes

After editing `state/config.yaml`, restart the service:

```bash
launchctl stop com.wavecap.server && sleep 2 && launchctl start com.wavecap.server
```

## Analyze Current Audio Quality

Check RMS levels of recent recordings to inform AGC tuning:

```bash
cd /Users/thw/Projects/WaveCap/backend && source .venv/bin/activate && python3 << 'EOF'
import numpy as np
from pathlib import Path
import struct

def get_wav_rms(filepath):
    with open(filepath, 'rb') as f:
        f.read(44)  # Skip header
        data = f.read()
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
        return np.sqrt(np.mean(samples**2))

recordings = sorted(Path("/Users/thw/Projects/WaveCap/state/recordings").glob("*.wav"),
                   key=lambda x: x.stat().st_mtime, reverse=True)[:10]
print("Recent recordings RMS levels:")
for r in recordings:
    rms = get_wav_rms(r)
    print(f"  {r.name}: {rms:.4f} ({rms*100:.1f}%)")
EOF
```

## Tips

- Start with default values and make small adjustments (10-20% changes)
- Test with a variety of recordings before committing to changes
- AGC is the most impactful setting for quiet/loud sources
- Highpass filter is most important for outdoor/mobile radio
- Keep notes on what works for different stream sources
