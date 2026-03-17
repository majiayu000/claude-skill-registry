---
name: stream-validator
description: Validate WebSocket and HTTP stream health for WaveCap-SDR channels. Use when debugging streaming issues, measuring latency or throughput, detecting packet loss, or verifying audio/spectrum delivery.
---

# Stream Validator for WaveCap-SDR

This skill helps validate WebSocket and HTTP streaming performance, measure metrics, and diagnose streaming issues.

## When to Use This Skill

Use this skill when:
- Audio playback is stuttering or cutting out
- Spectrum display not updating smoothly
- WebSocket connections frequently disconnecting
- Need to measure streaming latency or throughput
- Debugging "no data" or buffering issues
- Performance testing under load
- Verifying stream quality after infrastructure changes

## Stream Types in WaveCap-SDR

**Audio Streams:**
- HTTP: `GET /api/v1/stream/channels/{chan_id}.pcm?format=pcm16`
- WebSocket: `ws://server/api/v1/stream/channels/{chan_id}`
- Format: PCM16 (16-bit signed) or F32 (32-bit float)
- Rate: 48 kHz default (configurable)

**Spectrum Streams:**
- WebSocket: `ws://server/api/v1/stream/captures/{capture_id}/spectrum`
- Format: JSON messages with FFT bins
- Rate: Configurable FPS (typically 10-15)

**IQ Streams:**
- WebSocket: `ws://server/api/v1/stream/captures/{capture_id}.iq`
- Format: Complex IQ samples
- Rate: Full SDR sample rate (2+ MHz)

## Usage Instructions

### Step 1: Check Server Health

Before validating streams, check server health:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/stream-validator/validate_stream.py \
  --health-check \
  --port 8087
```

This shows:
- Server status (ok, degraded, error)
- Device count and status
- Capture count and status
- Channel count and status
- Streaming stats (subscriber count, zombie cleanup)

### Step 2: Identify Stream to Validate

Determine the stream endpoint:

```bash
# List captures
curl http://127.0.0.1:8087/api/v1/captures | jq

# List channels for a capture
curl http://127.0.0.1:8087/api/v1/captures/{capture_id} | jq '.channels'
```

### Step 3: Run Stream Validator

**Validate HTTP audio stream:**
```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/stream-validator/validate_stream.py \
  --type audio \
  --channel ch1 \
  --duration 10 \
  --port 8087
```

**Validate WebSocket audio stream:**
```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/stream-validator/validate_stream.py \
  --type audio_ws \
  --channel ch1 \
  --duration 10 \
  --port 8087
```

**Validate spectrum stream:**
```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/stream-validator/validate_stream.py \
  --type spectrum \
  --capture cap_abc123 \
  --duration 10 \
  --port 8087
```

**Full validation with verbose audio analysis:**
```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/stream-validator/validate_stream.py \
  --type audio \
  --channel ch1 \
  --duration 10 \
  --verbose \
  --health-check \
  --port 8087
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--type` | Stream type (audio, audio_ws, spectrum, iq) | audio |
| `--channel` | Channel ID for audio streams | ch1 |
| `--capture` | Capture ID for spectrum/IQ streams | (required for spectrum) |
| `--duration` | Seconds to monitor | 10 |
| `--host` | Server host | 127.0.0.1 |
| `--port` | Server port | 8087 |
| `--report` | Output JSON report | false |
| `--health-check` | Check server health first | false |
| `--verbose` | Include audio quality analysis | false |

### Step 4: Interpret Results

The validator outputs:

**Connection Metrics:**
- Connection time (time to establish WebSocket/HTTP)
- Connection success rate
- Reconnection attempts

**Data Metrics:**
- Throughput (bytes/sec, samples/sec, messages/sec)
- Latency (time from server to client)
- Packet loss or gaps
- Buffer underruns

**Quality Metrics:**
- Audio: RMS level, silence detection, clipping
- Spectrum: Update rate, FFT bin count
- IQ: Sample continuity, overflow detection

**Health Status:**
- HEALTHY: Stream working correctly (throughput >= 95%)
- DEGRADED: Issues detected but stream usable (throughput 80-95%)
- UNHEALTHY: Critical problems, stream unusable (throughput < 80%)

### Example Output

```
============================================================
STREAM VALIDATION RESULTS: AUDIO
============================================================

Status: ✓ HEALTHY

Connection:
  Connect time: 12.3 ms
  Duration: 10.02s

Throughput:
  Bytes received: 960,384
  Throughput: 93.75 KB/s
  Expected: 93.75 KB/s
  Ratio: 100.0%

Audio Analysis:
  RMS level: -18.5 dB
  Peak level: -3.2 dB

============================================================
```

## Common Issues and Solutions

### Issue: Low Throughput

**Expected throughput:**
- Audio PCM16: 96 KB/s (48 kHz × 2 bytes)
- Spectrum: 1-10 KB/s (depends on FFT size and FPS)
- IQ: 4-16 MB/s (depends on sample rate)

**Solutions:**
- Check network bandwidth
- Reduce stream quality (lower sample rate, smaller FFT)
- Check server CPU usage
- Verify no other bandwidth-intensive processes

### Issue: High Latency

**Expected latency:**
- Local network: <10 ms
- WiFi: 10-50 ms
- Remote: Varies by distance

**Solutions:**
- Use wired connection instead of WiFi
- Reduce buffering (if configurable)
- Check server processing time
- Verify network not congested

### Issue: Packet Loss

**Symptoms:**
- Audio glitches or pops
- Spectrum gaps or freezes
- Counters show dropped packets

**Solutions:**
- Check WiFi signal strength
- Reduce stream bandwidth
- Verify no network congestion
- Check for server overload

### Issue: Audio Appears Silent

**Symptoms:**
- RMS level < -50 dB
- Validator reports "Audio appears silent"

**Solutions:**
- Check channel is started and tuned correctly
- Verify frequency has active signal
- Check gain settings (may be too low)
- Use squelch threshold if monitoring quiet frequencies

### Issue: Audio is Clipping

**Symptoms:**
- Peak level > -0.5 dB
- Validator reports "Audio is clipping"

**Solutions:**
- Reduce RF gain
- Enable AGC in channel settings
- Check for nearby strong signals causing overload

## JSON Report Format

Use `--report` to get machine-readable output:

```json
{
  "type": "audio",
  "channel": "ch1",
  "url": "http://127.0.0.1:8087/api/v1/stream/channels/ch1.pcm?format=pcm16",
  "success": true,
  "status": "HEALTHY",
  "connect_time_ms": 12.3,
  "duration_seconds": 10.02,
  "bytes_received": 960384,
  "throughput_kbps": 93.75,
  "expected_throughput_kbps": 93.75,
  "samples_received": 480192,
  "throughput_ratio": 1.0,
  "audio_analysis": {
    "rms_db": -18.5,
    "peak_db": -3.2,
    "is_silent": false,
    "is_clipping": false
  }
}
```

## Files in This Skill

- `SKILL.md`: This file - instructions
- `validate_stream.py`: Stream validation and metrics script

## Dependencies

The validator requires:
- `requests` - HTTP streaming (included in WaveCap-SDR deps)
- `websockets` - WebSocket streaming (included in WaveCap-SDR deps)
- `numpy` - Audio analysis (included in WaveCap-SDR deps)
