---
name: sound-effects-generator
description: Generate audio tones, noise, DTMF signals, and simple sound effects programmatically. Export to WAV or MP3 format.
---

# Sound Effects Generator

Generate programmatic audio: pure tones, noise types, DTMF signals, and simple sound effects. Perfect for testing, alerts, audio cues, and placeholder sounds.

## Quick Start

```python
from scripts.sfx_generator import SoundEffectsGenerator

# Generate a tone
sfx = SoundEffectsGenerator()
sfx.tone(440, duration=1000).save("a440.wav")

# Generate white noise
sfx.noise("white", duration=2000).save("whitenoise.wav")

# Create a beep sequence
sfx.beep_sequence([440, 880, 440], durations=200, gap=100).save("alert.wav")
```

## Features

- **Tones**: Sine, square, sawtooth, triangle waveforms
- **Noise**: White, pink, brown/red noise
- **DTMF**: Phone dial tones
- **Sequences**: Multi-tone patterns
- **Effects**: Fade, volume control
- **Export**: WAV, MP3

## API Reference

### Initialization

```python
sfx = SoundEffectsGenerator(sample_rate=44100)
```

### Tone Generation

```python
# Pure sine wave
sfx.tone(frequency=440, duration=1000)

# Different waveforms
sfx.tone(440, duration=1000, waveform="sine")      # Default
sfx.tone(440, duration=1000, waveform="square")
sfx.tone(440, duration=1000, waveform="sawtooth")
sfx.tone(440, duration=1000, waveform="triangle")

# With volume (0.0 to 1.0)
sfx.tone(440, duration=1000, volume=0.5)
```

### Noise Generation

```python
# White noise (equal energy all frequencies)
sfx.noise("white", duration=2000)

# Pink noise (1/f, natural sounding)
sfx.noise("pink", duration=2000)

# Brown noise (1/f^2, deeper)
sfx.noise("brown", duration=2000)

# With volume
sfx.noise("white", duration=1000, volume=0.3)
```

### DTMF Tones

```python
# Single digit
sfx.dtmf("5", duration=200)

# Sequence (phone number)
sfx.dtmf_sequence("5551234", tone_duration=150, gap=50)
```

### Beep Sequences

```python
# Single beep
sfx.beep(frequency=800, duration=200)

# Multiple beeps (same frequency)
sfx.beep_sequence([800, 800, 800], durations=100, gap=100)

# Melody (different frequencies)
sfx.beep_sequence([523, 659, 784, 1047], durations=200, gap=50)

# Varying durations
sfx.beep_sequence(
    frequencies=[440, 880],
    durations=[300, 500],
    gap=100
)
```

### Silence

```python
# Generate silence
sfx.silence(duration=1000)
```

### Effects

```python
# Fade in/out
sfx.tone(440, 2000).fade_in(200).fade_out(500)

# Volume adjustment
sfx.tone(440, 1000).volume(0.5)
```

### Chaining

```python
# Combine multiple sounds
sfx.tone(440, 500) \
   .silence(200) \
   .tone(880, 500) \
   .save("two_tones.wav")
```

### Save

```python
# Save to WAV
sfx.save("output.wav")

# Save to MP3 (requires pydub)
sfx.save("output.mp3", bitrate=192)
```

## CLI Usage

```bash
# Generate tone
python sfx_generator.py --tone 440 --duration 1000 --output tone.wav

# Generate noise
python sfx_generator.py --noise white --duration 2000 --output noise.wav

# Generate DTMF
python sfx_generator.py --dtmf "5551234" --output phone.wav

# Generate beep pattern
python sfx_generator.py --beeps "800,800,800" --duration 100 --gap 100 --output alert.wav

# With waveform
python sfx_generator.py --tone 440 --waveform square --duration 1000 --output square.wav
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--tone` | Frequency in Hz | - |
| `--noise` | Noise type (white, pink, brown) | - |
| `--dtmf` | DTMF digits | - |
| `--beeps` | Comma-separated frequencies | - |
| `--duration` | Duration in ms | 1000 |
| `--gap` | Gap between sounds (ms) | 100 |
| `--waveform` | Tone waveform | sine |
| `--volume` | Volume (0.0-1.0) | 0.8 |
| `--sample-rate` | Sample rate | 44100 |
| `--output` | Output file | Required |

## Examples

### Alert Sound

```python
sfx = SoundEffectsGenerator()
sfx.beep_sequence(
    frequencies=[880, 1100, 880, 1100],
    durations=150,
    gap=50
)
sfx.fade_out(100)
sfx.save("alert.wav")
```

### Notification Chime

```python
sfx = SoundEffectsGenerator()

# C-E-G chord progression
notes = [523, 659, 784]  # C5, E5, G5
for freq in notes:
    sfx.tone(freq, 200)
    sfx.silence(50)

sfx.fade_out(200)
sfx.save("chime.wav")
```

### White Noise Background

```python
sfx = SoundEffectsGenerator()
sfx.noise("brown", duration=60000)  # 1 minute
sfx.volume(0.3)  # Quiet
sfx.fade_in(2000)
sfx.fade_out(2000)
sfx.save("background.mp3", bitrate=128)
```

### DTMF Phone Number

```python
sfx = SoundEffectsGenerator()
sfx.dtmf_sequence("18005551234", tone_duration=180, gap=80)
sfx.save("phone_dial.wav")
```

### Test Tone Sweep

```python
sfx = SoundEffectsGenerator()

# Generate tones from 100Hz to 1000Hz
for freq in range(100, 1001, 100):
    sfx.tone(freq, 200)
    sfx.silence(50)

sfx.save("sweep.wav")
```

## Common Frequencies

| Name | Frequency (Hz) |
|------|----------------|
| A4 (Concert pitch) | 440 |
| Middle C (C4) | 261.63 |
| C5 | 523.25 |
| Standard dial tone | 350 + 440 |
| Busy signal | 480 + 620 |

### Musical Notes (A4 = 440Hz)

| Note | Frequency |
|------|-----------|
| C4 | 261.63 |
| D4 | 293.66 |
| E4 | 329.63 |
| F4 | 349.23 |
| G4 | 392.00 |
| A4 | 440.00 |
| B4 | 493.88 |
| C5 | 523.25 |

## Dependencies

```
numpy>=1.24.0
scipy>=1.10.0
soundfile>=0.12.0
```

**Optional**: pydub (for MP3 export)

## Limitations

- No complex synthesis (no ADSR envelopes)
- No stereo panning
- Limited to basic waveforms
- MP3 export requires pydub + FFmpeg
