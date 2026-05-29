---
name: audio-quality-checker
description: Analyze the WaveCap-SDR audio stream to assess tuning quality, detect silence, noise, proper audio, or distortion. Use when checking if SDR channels are properly configured or debugging audio issues.
---

# Audio Quality Checker for WaveCap-SDR

This skill helps analyze the audio stream from WaveCap-SDR channels to determine if they are properly tuned and producing usable audio.

## When to Use This Skill

Use this skill when:
- User asks to check if an SDR channel is "well tuned" or working properly
- User wants to verify audio quality or detect issues
- User asks if they're getting "real sound" vs "just noise" vs "nothing"
- Debugging why audio playback isn't working as expected
- Validating SDR configuration changes

## How It Works

The skill captures a sample of the audio stream and analyzes it to detect:

1. **Silence** - No signal, near-zero amplitude (broken/stopped channel)
2. **Noise** - Random signal with no structure (poor tuning, no carrier)
3. **Proper Audio** - Structured signal with meaningful content (well-tuned FM station)
4. **Clipping/Distortion** - Signal hitting limits (gain too high, overmodulation)

## Usage Instructions

### Step 1: Identify the Server and Channel

First, determine:
- Server port (default: 8087, check `backend/config/wavecapsdr.yaml` or environment variables)
- Channel ID to test (e.g., "ch1", "ch2", etc.)
- Server bind address (default: 127.0.0.1)

You can find active channels by checking:
```bash
curl http://127.0.0.1:8087/api/v1/captures | jq '.[] | .channels'
```

### Step 2: Capture Audio Sample

Use the provided `analyze_audio_stream.py` script to capture and analyze:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/audio-quality-checker/analyze_audio_stream.py \
  --port 8087 \
  --channel ch1 \
  --duration 3
```

Parameters:
- `--port`: Server port (default: 8087)
- `--channel`: Channel ID to test (default: ch1)
- `--duration`: Seconds of audio to capture (default: 3)
- `--host`: Server host (default: 127.0.0.1)
- `--format`: Audio format, pcm16 or f32 (default: pcm16)

### Step 3: Interpret Results

The script outputs a detailed analysis including:

**Signal Level Metrics:**
- RMS Level (dB): Overall signal strength (-inf = silence, -20 to 0 dB = good)
- Peak Level (dB): Maximum amplitude (near 0 dB may indicate clipping)
- Crest Factor: Peak-to-RMS ratio (high = dynamic, low = compressed/noise)

**Spectral Analysis:**
- Spectral Flatness: How "flat" the spectrum is (high = noise-like, low = tonal)
- Spectral Centroid: "Center of mass" of the spectrum in Hz
- Zero Crossing Rate: How often signal crosses zero (higher for noise/high-freq content)

**Signal Classification:**
The script will classify the signal as:
- **SILENCE**: RMS < -60 dB
- **NOISE**: High spectral flatness (> 0.7) and low RMS
- **CLIPPED**: Peak level > -0.5 dB
- **GOOD AUDIO**: Structured signal with moderate levels

### Step 4: Recommendations

Based on the results:

**If SILENCE detected:**
- Check if channel is started: `curl -X POST http://127.0.0.1:8087/api/v1/channels/{chan_id}/start`
- Verify capture is running
- Check SDR device connection

**If NOISE detected:**
- Adjust channel frequency (offset_hz) - may not be tuned to a station
- Check antenna connection
- Try different frequencies known to have active broadcasts
- Verify modulation mode matches the signal (wbfm, nbfm, am, ssb, p25, dmr supported)

**If CLIPPED detected:**
- Reduce SDR gain settings
- Check for overmodulation from the broadcaster
- Adjust RF gain in device configuration

**If GOOD AUDIO:**
- Channel is properly tuned and working correctly
- Can fine-tune squelch_db if needed to reduce noise during silent periods

## Example Workflow

```bash
# 1. Check what channels exist
curl http://127.0.0.1:8087/api/v1/captures | jq

# 2. Start a channel if needed
curl -X POST http://127.0.0.1:8087/api/v1/channels/ch1/start

# 3. Analyze the audio quality
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/audio-quality-checker/analyze_audio_stream.py \
  --channel ch1 --duration 3

# 4. If noise detected, try adjusting frequency
# (Update channel configuration and restart)
```

## Technical Details

**Audio Stream Format:**
- Endpoint: `GET /api/v1/stream/channels/{chan_id}.pcm?format=pcm16`
- Sample Rate: 48000 Hz (default, configurable)
- Channels: Mono (1 channel)
- Format: 16-bit signed little-endian PCM
- Streaming: Continuous, no headers

**Analysis Metrics:**

1. **RMS Level**: `20 * log10(sqrt(mean(signal^2)))`
   - Measures average signal power
   - Typical good audio: -20 to -6 dB

2. **Spectral Flatness**: Geometric mean / Arithmetic mean of power spectrum
   - Near 1.0 = white noise (flat spectrum)
   - Near 0.0 = tonal (structured frequencies)

3. **Zero Crossing Rate**: Count of sign changes / total samples
   - High ZCR = noisy or high-frequency content
   - Low ZCR = low-frequency or tonal content

4. **Crest Factor**: Peak / RMS
   - High (>4) = dynamic audio (speech, music)
   - Low (<3) = compressed or noise-like

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `analyze_audio_stream.py`: Python script to capture and analyze audio
- `requirements.txt`: Python dependencies (numpy, scipy, requests)

## Notes

- The skill uses the Python environment at `backend/.venv`
- Ensure the WaveCap-SDR server is running before analysis
- For best results, capture at least 2-3 seconds of audio
- The analysis is statistical and works best with steady signals
- Some transient issues may not be detected in short samples
