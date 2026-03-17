---
name: signal-monitor
description: Get real-time signal quality metrics (RSSI, SNR, S-meter) from WaveCap-SDR channels. Use when checking signal strength, monitoring reception quality, or debugging weak signals.
---

# Signal Monitor for WaveCap-SDR

This skill provides real-time signal quality metrics from SDR channels, including RSSI, SNR, signal power, and S-meter readings.

## When to Use This Skill

Use this skill when:
- Checking signal strength of a tuned station
- Monitoring reception quality over time
- Debugging weak or noisy signals
- Comparing signal quality between antennas
- Verifying that a channel is receiving properly
- Getting S-meter readings (ham radio style)

## Available Metrics

| Metric | Description | Range |
|--------|-------------|-------|
| RSSI (dB) | Received Signal Strength Indicator | -100 to 0 dB |
| SNR (dB) | Signal-to-Noise Ratio | 0 to 60+ dB |
| Signal Power (dB) | Audio output power level | -80 to 0 dB |
| S-Units | Ham radio S-meter reading | S0 to S9+60 |
| Squelch State | Whether squelch is open/closed | true/false |

## Usage Instructions

### Step 1: Get Channel Metrics

Use the helper script to get signal metrics:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/signal-monitor/get_signal_stats.py \
  --channel ch1 \
  --port 8087
```

Or use curl directly:

```bash
# Get extended metrics for a channel
curl http://127.0.0.1:8087/api/v1/channels/ch1/metrics/extended | jq

# Example output:
{
  "channelId": "ch1",
  "rssiDb": -45.2,
  "snrDb": 28.5,
  "signalPowerDb": -22.1,
  "sUnits": "S8",
  "squelchOpen": true,
  "streamSubscribers": 1,
  "streamDropsPerSec": 0.0,
  "captureState": "running",
  "timestamp": 1700000000.0
}
```

### Step 2: Monitor Signal Over Time

Monitor signal quality continuously:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/signal-monitor/get_signal_stats.py \
  --channel ch1 \
  --monitor \
  --interval 1.0 \
  --duration 60
```

### Step 3: Get Spectrum Snapshot

Get a single FFT spectrum snapshot (without WebSocket):

```bash
curl http://127.0.0.1:8087/api/v1/captures/c1/spectrum/snapshot | jq '.centerHz, .sampleRate'
```

## Interpreting S-Meter Readings

| S-Units | Signal Quality | Typical Use |
|---------|---------------|-------------|
| S0-S2 | Very weak | Marginal reception |
| S3-S5 | Weak | Usable with noise |
| S6-S7 | Moderate | Good reception |
| S8-S9 | Strong | Excellent reception |
| S9+10 | Very strong | Local/powerful station |
| S9+20+ | Extremely strong | Possible overload |

## API Reference

### GET /channels/{chan_id}/metrics/extended

Returns extended signal metrics including S-meter reading.

**Response:**
```json
{
  "channelId": "ch1",
  "rssiDb": -45.2,
  "snrDb": 28.5,
  "signalPowerDb": -22.1,
  "sUnits": "S8",
  "squelchOpen": true,
  "streamSubscribers": 1,
  "streamDropsPerSec": 0.0,
  "captureState": "running",
  "timestamp": 1700000000.0
}
```

### GET /captures/{cid}/spectrum/snapshot

Returns single FFT spectrum snapshot.

**Response:**
```json
{
  "power": [-80.1, -78.5, ...],
  "freqs": [90000000, 90000122, ...],
  "centerHz": 90300000,
  "sampleRate": 250000,
  "timestamp": 1700000000.0
}
```

### GET /channels/{chan_id}/metrics/history?seconds=60

Returns time-series of metrics (currently single point).

## Common Issues

### Issue: No Signal / Low RSSI
**Symptoms**: RSSI below -90 dB, S0-S1 readings
**Solutions**:
- Check antenna connection
- Verify frequency is correct
- Increase gain in capture settings
- Check for interference

### Issue: Low SNR Despite Good RSSI
**Symptoms**: RSSI is good but SNR is poor (<10 dB)
**Solutions**:
- Reduce gain (may be overloading)
- Check for nearby interference
- Try different antenna
- Enable noise blanker

### Issue: Squelch Always Closed
**Symptoms**: squelchOpen is always false
**Solutions**:
- Lower squelch threshold (more negative dB)
- Check if signal is actually present
- Verify channel offset is correct

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `get_signal_stats.py`: Helper script for fetching and displaying signal metrics
