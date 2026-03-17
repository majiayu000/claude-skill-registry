---
name: audio-normalizer
description: Use when asked to normalize audio volume, match loudness, or apply peak/RMS normalization to audio files.
---

# Audio Normalizer

Normalize audio volume levels using peak or RMS normalization to ensure consistent loudness across files.

## Purpose

Volume normalization for:
- Podcast episode consistency
- Music playlist leveling
- Speech recording standardization
- Broadcast loudness compliance

## Features

- **Peak Normalization**: Normalize to maximum peak level (dBFS)
- **RMS Normalization**: Normalize to average loudness level
- **Loudness Matching**: Match LUFS target for broadcast compliance
- **Batch Processing**: Normalize multiple files to same level
- **Format Preservation**: Maintain original audio format
- **Headroom Control**: Prevent clipping with configurable headroom

## Quick Start

```python
from audio_normalizer import AudioNormalizer

# Peak normalization to -1 dBFS
normalizer = AudioNormalizer()
normalizer.load('input.mp3')
normalizer.normalize_peak(target_dbfs=-1.0)
normalizer.save('normalized.mp3')

# RMS normalization for consistent average loudness
normalizer.normalize_rms(target_dbfs=-20.0)
normalizer.save('normalized_rms.mp3')

# Batch normalize all files to same level
normalizer.batch_normalize(
    input_files=['audio1.mp3', 'audio2.mp3'],
    output_dir='normalized/',
    method='rms',
    target_dbfs=-20.0
)
```

## CLI Usage

```bash
# Peak normalization
python audio_normalizer.py input.mp3 --output normalized.mp3 --method peak --target -1.0

# RMS normalization
python audio_normalizer.py input.mp3 --output normalized.mp3 --method rms --target -20.0

# Batch normalize directory
python audio_normalizer.py *.mp3 --output-dir normalized/ --method rms --target -20.0

# Show current levels without normalizing
python audio_normalizer.py input.mp3 --analyze-only
```

## API Reference

### AudioNormalizer

```python
class AudioNormalizer:
    def load(self, filepath: str) -> 'AudioNormalizer'
    def normalize_peak(self, target_dbfs: float = -1.0, headroom: float = 0.1) -> 'AudioNormalizer'
    def normalize_rms(self, target_dbfs: float = -20.0) -> 'AudioNormalizer'
    def analyze_levels(self) -> Dict[str, float]
    def save(self, output: str, format: str = None, bitrate: str = '192k') -> str
    def batch_normalize(self, input_files: List[str], output_dir: str,
                       method: str = 'rms', target_dbfs: float = -20.0) -> List[str]
```

## Normalization Methods

### Peak Normalization
- Scales audio so highest peak reaches target level
- Preserves dynamic range
- Good for preventing clipping
- Target: typically -1.0 to -3.0 dBFS

### RMS Normalization
- Scales audio so average level reaches target
- Better for perceived loudness matching
- Good for podcasts and speech
- Target: typically -20.0 to -23.0 dBFS

### LUFS Matching
- Integrated Loudness Units relative to Full Scale
- Broadcast standard (EBU R128, ITU BS.1770)
- Target: -23 LUFS (broadcast), -16 LUFS (streaming)

## Best Practices

**For Podcasts:**
```python
normalizer.normalize_rms(target_dbfs=-19.0)  # Speech clarity
```

**For Music:**
```python
normalizer.normalize_peak(target_dbfs=-1.0)  # Preserve dynamics
```

**For Broadcast:**
```python
normalizer.normalize_rms(target_dbfs=-23.0)  # EBU R128 compliance
```

## Use Cases

- **Podcast Production**: Consistent volume across episodes
- **Music Playlists**: Even loudness for continuous playback
- **Audiobooks**: Standardized narration levels
- **Conference Recordings**: Normalize different speakers
- **Video Production**: Match audio levels before mixing

## Limitations

- Does not apply dynamic compression (use separate compressor)
- Does not remove DC offset (pre-processing recommended)
- Peak normalization won't match perceived loudness
- Doesn't fix clipped audio (distortion is permanent)
