---
name: audio-converter
description: Convert audio files between formats (MP3, WAV, FLAC, OGG, M4A) with bitrate and sample rate control. Batch processing supported.
---

# Audio Converter

Convert audio files between popular formats with control over quality settings. Supports batch processing and maintains metadata where possible.

## Quick Start

```python
from scripts.audio_converter import AudioConverter

# Simple conversion
converter = AudioConverter("input.wav")
converter.convert("output.mp3")

# With quality settings
converter = AudioConverter("input.flac")
converter.bitrate(320).sample_rate(44100).convert("output.mp3")

# Batch convert directory
AudioConverter.batch_convert("./input_folder", "./output_folder", format="mp3", bitrate=192)
```

## Features

- **Format Support**: MP3, WAV, FLAC, OGG, M4A/AAC, AIFF
- **Quality Control**: Bitrate, sample rate, channels
- **Metadata Preservation**: Copy tags when possible
- **Batch Processing**: Convert entire directories
- **Normalization**: Optional volume normalization

## API Reference

### Initialization

```python
# From file
converter = AudioConverter("audio.wav")
```

### Settings

```python
converter.bitrate(192)        # kbps (for lossy formats)
converter.sample_rate(44100)  # Hz
converter.channels(2)         # 1=mono, 2=stereo
converter.normalize(True)     # Normalize volume
```

### Conversion

```python
# Convert to format (inferred from extension)
converter.convert("output.mp3")

# Explicit format
converter.convert("output", format="mp3")
```

### Batch Processing

```python
# Convert all files in directory
AudioConverter.batch_convert(
    input_dir="./wavs",
    output_dir="./mp3s",
    format="mp3",
    bitrate=320
)
```

## CLI Usage

```bash
# Simple conversion
python audio_converter.py --input song.wav --output song.mp3

# With quality settings
python audio_converter.py --input song.flac --output song.mp3 --bitrate 320 --sample-rate 44100

# Batch convert
python audio_converter.py --input-dir ./wavs --output-dir ./mp3s --format mp3 --bitrate 192

# Normalize during conversion
python audio_converter.py --input song.wav --output song.mp3 --normalize
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input audio file | Required |
| `--output` | Output file path | Required |
| `--input-dir` | Input directory for batch | - |
| `--output-dir` | Output directory for batch | - |
| `--format` | Output format | From extension |
| `--bitrate` | Bitrate in kbps | 192 |
| `--sample-rate` | Sample rate in Hz | Original |
| `--channels` | Number of channels | Original |
| `--normalize` | Normalize volume | False |

## Supported Formats

| Format | Extension | Type | Notes |
|--------|-----------|------|-------|
| MP3 | .mp3 | Lossy | Most compatible |
| WAV | .wav | Lossless | Large files |
| FLAC | .flac | Lossless | Compressed lossless |
| OGG | .ogg | Lossy | Open format |
| M4A | .m4a | Lossy | AAC codec |
| AIFF | .aiff | Lossless | Apple format |

## Examples

### Convert WAV to MP3

```python
converter = AudioConverter("recording.wav")
converter.bitrate(320).convert("recording.mp3")
```

### Convert FLAC to Multiple Formats

```python
source = AudioConverter("album.flac")

# High quality MP3
source.bitrate(320).convert("album_hq.mp3")

# Standard MP3
source.bitrate(192).convert("album_std.mp3")

# OGG for streaming
source.bitrate(128).convert("album.ogg")
```

### Batch Convert for Podcast

```python
# Convert all WAV recordings to MP3 with podcast settings
AudioConverter.batch_convert(
    input_dir="./raw_episodes",
    output_dir="./episodes",
    format="mp3",
    bitrate=128,
    sample_rate=44100,
    channels=1  # Mono for podcasts
)
```

## Dependencies

```
pydub>=0.25.0
soundfile>=0.12.0
```

**Note**: Requires FFmpeg installed on system for MP3/M4A support.

## Limitations

- Requires FFmpeg for MP3 and M4A formats
- Metadata transfer is best-effort
- Some format combinations may not preserve all tags
