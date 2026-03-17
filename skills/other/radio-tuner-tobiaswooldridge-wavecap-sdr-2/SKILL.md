---
name: radio-tuner
description: Adjust SDR radio settings (frequency, gain, squelch, bandwidth, filters, AGC) in WaveCap-SDR. Use when changing tuning parameters, optimizing reception, or configuring channels.
---

# Radio Tuner for WaveCap-SDR

This skill provides tools to adjust SDR radio settings including frequency, gain, squelch, bandwidth, filters, and AGC parameters.

## When to Use This Skill

Use this skill when:
- Changing the tuned frequency
- Adjusting gain for optimal signal level
- Setting squelch threshold to eliminate noise
- Configuring channel bandwidth
- Enabling/disabling filters (deemphasis, notch, etc.)
- Adjusting AGC parameters
- Changing demodulation mode

## Available Settings

### Capture Settings (SDR-level)
| Setting | Description | Range |
|---------|-------------|-------|
| `centerHz` | Center frequency | 1 MHz - 6 GHz |
| `sampleRate` | Sample rate | Device-dependent |
| `gain` | RF gain | -100 to 100 dB |
| `bandwidth` | IF bandwidth | 0 to sample_rate |
| `ppm` | Frequency correction | -1000 to 1000 |
| `antenna` | Antenna port | Device-dependent |

### Channel Settings (Demodulator-level)
| Setting | Description | Range |
|---------|-------------|-------|
| `mode` | Demodulation mode | wbfm, nbfm, am, ssb, raw, p25, dmr |
| `offsetHz` | Offset from capture center | -50 MHz to +50 MHz |
| `squelchDb` | Squelch threshold | -120 to 0 dB |
| `audioRate` | Output audio rate | 8000 to 192000 Hz |

### Filter Settings
| Setting | Description | Default |
|---------|-------------|---------|
| `enableDeemphasis` | FM de-emphasis filter | true (WBFM) |
| `deemphasisTauUs` | De-emphasis time constant | 75 µs (US), 50 µs (EU) |
| `enableAgc` | Automatic gain control | true |
| `agcTargetDb` | AGC target level | -20 dB |
| `agcAttackMs` | AGC attack time | 10 ms |
| `agcReleaseMs` | AGC release time | 500 ms |
| `notchFrequencies` | Notch filter frequencies | [] |

## Usage Instructions

### Step 1: List Current Settings

Get current capture and channel settings:

```bash
# Get capture settings
curl http://127.0.0.1:8087/api/v1/captures/c1 | jq

# Get channel settings
curl http://127.0.0.1:8087/api/v1/channels/ch1 | jq
```

Or use the helper script:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/radio-tuner/adjust_settings.py \
  --capture c1 --show
```

### Step 2: Adjust Capture Settings

Change frequency:
```bash
curl -X PATCH http://127.0.0.1:8087/api/v1/captures/c1 \
  -H "Content-Type: application/json" \
  -d '{"centerHz": 90300000}'
```

Change gain:
```bash
curl -X PATCH http://127.0.0.1:8087/api/v1/captures/c1 \
  -H "Content-Type: application/json" \
  -d '{"gain": 35.0}'
```

Or use the helper script:
```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/radio-tuner/adjust_settings.py \
  --capture c1 \
  --frequency 90.3 \
  --gain 35
```

### Step 3: Adjust Channel Settings

Change squelch:
```bash
curl -X PATCH http://127.0.0.1:8087/api/v1/channels/ch1 \
  -H "Content-Type: application/json" \
  -d '{"squelchDb": -50}'
```

Change mode:
```bash
curl -X PATCH http://127.0.0.1:8087/api/v1/channels/ch1 \
  -H "Content-Type: application/json" \
  -d '{"mode": "nbfm"}'
```

Enable/disable AGC:
```bash
curl -X PATCH http://127.0.0.1:8087/api/v1/channels/ch1 \
  -H "Content-Type: application/json" \
  -d '{"enableAgc": true, "agcTargetDb": -20, "agcAttackMs": 10, "agcReleaseMs": 500}'
```

### Step 4: Add Notch Filters

Remove interference at specific frequencies:
```bash
curl -X PATCH http://127.0.0.1:8087/api/v1/channels/ch1 \
  -H "Content-Type: application/json" \
  -d '{"notchFrequencies": [1000, 2000, 3000]}'
```

## Helper Script Reference

```bash
# Show current settings
python adjust_settings.py --capture c1 --show

# Change frequency (MHz)
python adjust_settings.py --capture c1 --frequency 90.3

# Change gain (dB)
python adjust_settings.py --capture c1 --gain 35

# Change bandwidth (Hz)
python adjust_settings.py --capture c1 --bandwidth 200000

# Change squelch (dB)
python adjust_settings.py --channel ch1 --squelch -50

# Change mode
python adjust_settings.py --channel ch1 --mode nbfm

# Multiple settings at once
python adjust_settings.py --capture c1 --frequency 90.3 --gain 35 --bandwidth 200000
```

## Demodulation Modes

| Mode | Description | Typical Use |
|------|-------------|-------------|
| `wbfm` | Wide-band FM (200 kHz) | FM broadcast radio |
| `nbfm` | Narrow-band FM (12.5-25 kHz) | Two-way radio, amateur |
| `am` | Amplitude modulation | Aviation, AM broadcast |
| `ssb` | Single sideband | Amateur radio, marine |
| `raw` | No demodulation | Digital modes, ISM |
| `p25` | Project 25 digital | Public safety |
| `dmr` | Digital Mobile Radio | Commercial two-way |

## Optimal Settings by Application

### FM Broadcast Radio
```json
{
  "sampleRate": 1024000,
  "bandwidth": 200000,
  "mode": "wbfm",
  "enableDeemphasis": true,
  "deemphasisTauUs": 75,
  "squelchDb": -60
}
```

### VHF Marine / Aviation
```json
{
  "sampleRate": 2000000,
  "bandwidth": 25000,
  "mode": "nbfm",
  "squelchDb": -50,
  "enableAgc": true
}
```

### Amateur Radio SSB
```json
{
  "mode": "ssb",
  "ssbMode": "usb",
  "enableSsbBandpass": true,
  "ssbBandpassLowHz": 300,
  "ssbBandpassHighHz": 3000,
  "squelchDb": -60
}
```

## Configuration Warnings

WaveCap-SDR automatically detects problematic configurations and displays warnings in the UI. Check `configWarnings` in capture API responses to see current warnings.

### Check Current Warnings

```bash
curl -s http://127.0.0.1:8087/api/v1/captures/c1 | jq '.configWarnings'
```

### Warning Types

| Code | Severity | Description | Resolution |
|------|----------|-------------|------------|
| `rtl_unstable_sample_rate` | warning | RTL-SDR sample rate <900kHz causes IQ overflows | Use 1.024 MHz, 2.048 MHz, or 2.4 MHz |
| `bandwidth_exceeds_sample_rate` | warning | Bandwidth > sample rate violates Nyquist | Reduce bandwidth or increase sample rate |
| `bandwidth_near_sample_rate` | info | Bandwidth >90% of sample rate causes edge aliasing | Use bandwidth ≤80% of sample rate |
| `sdrplay_high_sample_rate` | info | SDRplay >8 MHz may cause USB issues | Lower sample rate if experiencing dropouts |
| `zero_gain` | info | Gain set to 0 dB | Increase gain if signals are weak |

### Best Practices to Avoid Warnings

1. **RTL-SDR Sample Rates**: Use 1.024 MHz, 2.048 MHz, or 2.4 MHz
   ```bash
   curl -X PATCH http://127.0.0.1:8087/api/v1/captures/c1 \
     -H "Content-Type: application/json" \
     -d '{"sampleRate": 1024000}'
   ```

2. **Bandwidth/Sample Rate Ratio**: Keep bandwidth ≤80% of sample rate
   ```bash
   # For 2 MHz sample rate, use ≤1.6 MHz bandwidth
   curl -X PATCH http://127.0.0.1:8087/api/v1/captures/c1 \
     -H "Content-Type: application/json" \
     -d '{"sampleRate": 2000000, "bandwidth": 1600000}'
   ```

3. **SDRplay Sample Rates**: Stay ≤8 MHz for reliable USB throughput
   ```bash
   curl -X PATCH http://127.0.0.1:8087/api/v1/captures/c1 \
     -H "Content-Type: application/json" \
     -d '{"sampleRate": 6000000}'
   ```

## Common Issues

### Issue: Audio Too Quiet
**Solutions**:
- Increase `gain` on capture
- Increase `agcTargetDb` (e.g., -15 instead of -20)
- Check antenna connection

### Issue: Audio Distorted
**Solutions**:
- Reduce `gain` on capture
- Lower `agcTargetDb` (e.g., -25 instead of -20)
- Enable de-emphasis for FM

### Issue: Too Much Background Noise
**Solutions**:
- Increase `squelchDb` (less negative, e.g., -40 instead of -60)
- Add notch filters for specific interference
- Enable noise blanker

### Issue: Signal Cutting In/Out
**Solutions**:
- Lower `squelchDb` (more negative)
- Adjust AGC attack/release times
- Check if frequency offset is correct

### Issue: IQ Overflows (RTL-SDR)
**Solutions**:
- Use stable sample rate (1.024 MHz, 2.048 MHz, or 2.4 MHz)
- Avoid sample rates below 900 kHz
- Check USB connection quality

### Issue: Aliasing at Spectrum Edges
**Solutions**:
- Reduce bandwidth to ≤80% of sample rate
- Increase sample rate if wider bandwidth needed
- Use appropriate IF filter settings

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `adjust_settings.py`: Helper script for adjusting radio settings
