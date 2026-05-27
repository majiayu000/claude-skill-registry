---
name: channel-optimizer
description: Auto-tune channel parameters to find optimal offset, squelch, and AGC settings for best audio quality. Use when setting up new channels, improving weak signals, or finding the sweet spot for demodulation settings.
---

# Channel Optimizer for WaveCap-SDR

This skill automatically finds optimal channel parameters by testing combinations and measuring audio quality.

## When to Use This Skill

Use this skill when:
- Setting up channels for new frequencies
- Audio quality is poor but signal is present
- Need to find exact frequency offset
- Tuning squelch threshold
- Optimizing AGC parameters
- Finding best demodulation settings

## How It Works

The optimizer:
1. Creates test channel with initial parameters
2. Captures audio samples
3. Measures quality metrics (RMS, SNR, distortion)
4. Adjusts parameters (offset, squelch, AGC)
5. Repeats until optimal settings found

## Usage

Optimize channel offset:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/channel-optimizer/optimize_channel.py \
  --capture cap_abc123 \
  --frequency 90.3e6 \
  --optimize offset \
  --port 8087
```

Optimize squelch:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/channel-optimizer/optimize_channel.py \
  --capture cap_abc123 \
  --offset 0 \
  --optimize squelch \
  --port 8087
```

Parameters:
- `--capture`: Capture ID
- `--frequency`: Target frequency (Hz)
- `--offset`: Initial offset (Hz)
- `--optimize`: What to optimize (offset, squelch, agc)
- `--port`: Server port

## Optimization Strategies

### Offset Optimization
Search range ±10 kHz around initial offset
- Test offsets: -10k, -5k, 0, +5k, +10k
- Measure RMS level for each
- Select offset with highest RMS

### Squelch Optimization
Find threshold that:
- Opens for signal
- Closes for noise
- Minimizes false triggers

### AGC Optimization
Find attack/release/target that:
- Maintains consistent output level
- Minimizes pumping artifacts
- Preserves dynamics

## Files in This Skill

- `SKILL.md`: This file
- `optimize_channel.py`: Channel optimization script
