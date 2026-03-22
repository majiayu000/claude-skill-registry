---
name: analyzing-wav
description: Analyze WAV audio files for debugging TTS and audio pipelines. Use when checking audio quality, validating WAV format, inspecting waveform patterns, or diagnosing generated speech issues.
---

# WAV Audio Analysis Skill

## Description

Analyze WAV audio files to debug audio generation pipelines. Provides statistical analysis, format validation, and quality metrics for diagnosing issues with generated speech.

**Triggers:** wav, audio, waveform, samples, amplitude, audio analysis, sound quality, audio debug

## Analysis Capabilities

### Basic Statistics

- Sample count and duration
- Min/max amplitude
- Standard deviation (expected ~3000-8000 for speech)
- Near-silent sample percentage

### Quality Indicators

- Zero crossing rate (speech typically 50-200 per 1000 samples)
- Clipping detection (samples at ±32767)
- NaN/Inf detection (if processing raw floats)
- DC offset analysis

### Format Validation

- Sample rate verification (24kHz for Qwen3-Omni TTS)
- Bit depth check
- Channel count
- RIFF header validation

## Usage

To analyze a WAV file, provide the path and I'll run comprehensive diagnostics:

```python
import numpy as np

with open("audio.wav", "rb") as f:
    header = f.read(44)
    data = f.read()

samples = np.frombuffer(data, dtype=np.int16)
print(f"Samples: {len(samples)}")
print(f"Duration: {len(samples)/24000:.2f} sec")
print(f"Min/Max: {samples.min()} / {samples.max()}")
print(f"Std dev: {np.std(samples):.1f}")

# Quality check
near_silent = np.sum(np.abs(samples) < 100)
print(f"Near-silent: {100*near_silent/len(samples):.1f}%")

# Zero crossings (voice activity indicator)
if len(samples) > 1000:
    zc = np.sum(np.diff(np.sign(samples[:1000])) != 0)
    print(f"Zero crossings (first 1000): {zc}")
```

## Typical Values for Good Speech Audio

| Metric         | Expected Range | Meaning                  |
| -------------- | -------------- | ------------------------ |
| Std dev        | 3000-8000      | Audio energy level       |
| Near-silent    | <5%            | Minimal silent padding   |
| Zero crossings | 50-200/1000    | Voice frequency activity |
| Min/Max        | ±20000-32000   | Healthy amplitude range  |

## Common Issues

### 99% Near-Silent

- Cause: NaN values converted to zeros
- Fix: Check for numerical overflow in pipeline

### Low Std Dev (<1000)

- Cause: Values too quiet before output normalization
- Fix: Check gain stages, ensure proper scaling

### Constant Value Runs

- Cause: Chunked processing with context overlap issues
- Fix: Verify chunk stitching logic

### Clipping (values at ±32767)

- Cause: Overflow or missing tanh/clamp
- Fix: Add output clamping before int16 conversion
