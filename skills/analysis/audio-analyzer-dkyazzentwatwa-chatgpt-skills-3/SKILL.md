---
name: audio-analyzer
description: Comprehensive audio analysis with waveform visualization, spectrogram, BPM detection, key detection, frequency analysis, and loudness metrics.
---

# Audio Analyzer

A comprehensive toolkit for analyzing audio files. Extract detailed information about audio including tempo, musical key, frequency content, loudness metrics, and generate professional visualizations.

## Quick Start

```python
from scripts.audio_analyzer import AudioAnalyzer

# Analyze an audio file
analyzer = AudioAnalyzer("song.mp3")
analyzer.analyze()

# Get all analysis results
results = analyzer.get_results()
print(f"BPM: {results['tempo']['bpm']}")
print(f"Key: {results['key']['key']} {results['key']['mode']}")

# Generate visualizations
analyzer.plot_waveform("waveform.png")
analyzer.plot_spectrogram("spectrogram.png")

# Full report
analyzer.save_report("analysis_report.json")
```

## Features

- **Tempo/BPM Detection**: Accurate beat tracking with confidence score
- **Key Detection**: Musical key and mode (major/minor) identification
- **Frequency Analysis**: Spectrum, dominant frequencies, frequency bands
- **Loudness Metrics**: RMS, peak, LUFS, dynamic range
- **Waveform Visualization**: Multi-channel waveform plots
- **Spectrogram**: Time-frequency visualization with customization
- **Chromagram**: Pitch class visualization for harmonic analysis
- **Beat Grid**: Visual beat markers overlaid on waveform
- **Export Formats**: JSON report, PNG/SVG visualizations

## API Reference

### Initialization

```python
# From file
analyzer = AudioAnalyzer("audio.mp3")

# With custom sample rate
analyzer = AudioAnalyzer("audio.wav", sr=44100)
```

### Analysis Methods

```python
# Run full analysis
analyzer.analyze()

# Individual analyses
analyzer.analyze_tempo()      # BPM and beat positions
analyzer.analyze_key()        # Musical key detection
analyzer.analyze_loudness()   # RMS, peak, LUFS
analyzer.analyze_frequency()  # Spectrum analysis
analyzer.analyze_dynamics()   # Dynamic range
```

### Results Access

```python
# Get all results as dict
results = analyzer.get_results()

# Individual results
tempo = analyzer.get_tempo()        # {'bpm': 120, 'confidence': 0.85, 'beats': [...]}
key = analyzer.get_key()            # {'key': 'C', 'mode': 'major', 'confidence': 0.72}
loudness = analyzer.get_loudness()  # {'rms_db': -14.2, 'peak_db': -0.5, 'lufs': -14.0}
freq = analyzer.get_frequency()     # {'dominant_freq': 440, 'spectrum': [...]}
```

### Visualization Methods

```python
# Waveform
analyzer.plot_waveform(
    output="waveform.png",
    figsize=(12, 4),
    color="#1f77b4",
    show_rms=True
)

# Spectrogram
analyzer.plot_spectrogram(
    output="spectrogram.png",
    figsize=(12, 6),
    cmap="magma",           # viridis, plasma, inferno, magma
    freq_scale="log",       # linear, log, mel
    max_freq=8000           # Hz
)

# Chromagram (pitch classes)
analyzer.plot_chromagram(
    output="chromagram.png",
    figsize=(12, 4)
)

# Onset strength / beat grid
analyzer.plot_beats(
    output="beats.png",
    figsize=(12, 4),
    show_strength=True
)

# Combined dashboard
analyzer.plot_dashboard(
    output="dashboard.png",
    figsize=(14, 10)
)
```

### Export

```python
# JSON report with all analysis
analyzer.save_report("report.json")

# Summary text
summary = analyzer.get_summary()
print(summary)
```

## Analysis Details

### Tempo Detection

Uses beat tracking algorithm to detect:
- **BPM**: Beats per minute (tempo)
- **Beat positions**: Timestamps of detected beats
- **Confidence**: Reliability score (0-1)

```python
tempo = analyzer.get_tempo()
# {
#     'bpm': 128.0,
#     'confidence': 0.89,
#     'beats': [0.0, 0.469, 0.938, 1.406, ...],  # seconds
#     'beat_count': 256
# }
```

### Key Detection

Analyzes harmonic content to identify:
- **Key**: Root note (C, C#, D, etc.)
- **Mode**: Major or minor
- **Confidence**: Detection confidence
- **Key profile**: Correlation with each key

```python
key = analyzer.get_key()
# {
#     'key': 'A',
#     'mode': 'minor',
#     'confidence': 0.76,
#     'profile': {'C': 0.12, 'C#': 0.08, ...}
# }
```

### Loudness Metrics

Comprehensive loudness analysis:
- **RMS dB**: Root mean square level
- **Peak dB**: Maximum sample level
- **LUFS**: Integrated loudness (broadcast standard)
- **Dynamic Range**: Difference between loud and quiet sections

```python
loudness = analyzer.get_loudness()
# {
#     'rms_db': -14.2,
#     'peak_db': -0.3,
#     'lufs': -14.0,
#     'dynamic_range_db': 12.5,
#     'crest_factor': 8.2
# }
```

### Frequency Analysis

Spectrum analysis including:
- **Dominant frequency**: Strongest frequency component
- **Frequency bands**: Energy in bass, mid, treble
- **Spectral centroid**: "Brightness" of audio
- **Spectral rolloff**: Frequency below which 85% of energy exists

```python
freq = analyzer.get_frequency()
# {
#     'dominant_freq': 440.0,
#     'spectral_centroid': 2150.3,
#     'spectral_rolloff': 4200.5,
#     'bands': {
#         'sub_bass': -28.5,      # 20-60 Hz
#         'bass': -18.2,          # 60-250 Hz
#         'low_mid': -12.1,       # 250-500 Hz
#         'mid': -10.8,           # 500-2000 Hz
#         'high_mid': -14.3,      # 2000-4000 Hz
#         'high': -22.1           # 4000-20000 Hz
#     }
# }
```

## CLI Usage

```bash
# Full analysis with all visualizations
python audio_analyzer.py --input song.mp3 --output-dir ./analysis/

# Just tempo and key
python audio_analyzer.py --input song.mp3 --analyze tempo key --output report.json

# Generate specific visualization
python audio_analyzer.py --input song.mp3 --plot spectrogram --output spec.png

# Dashboard view
python audio_analyzer.py --input song.mp3 --dashboard --output dashboard.png

# Batch analyze directory
python audio_analyzer.py --input-dir ./songs/ --output-dir ./reports/
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input audio file | Required |
| `--input-dir` | Directory of audio files | - |
| `--output` | Output file path | - |
| `--output-dir` | Output directory | `.` |
| `--analyze` | Analysis types: tempo, key, loudness, frequency, all | `all` |
| `--plot` | Plot type: waveform, spectrogram, chromagram, beats, dashboard | - |
| `--format` | Output format: json, txt | `json` |
| `--sr` | Sample rate for analysis | `22050` |

## Examples

### Song Analysis

```python
analyzer = AudioAnalyzer("track.mp3")
analyzer.analyze()

print(f"Tempo: {analyzer.get_tempo()['bpm']:.1f} BPM")
print(f"Key: {analyzer.get_key()['key']} {analyzer.get_key()['mode']}")
print(f"Loudness: {analyzer.get_loudness()['lufs']:.1f} LUFS")

analyzer.plot_dashboard("track_analysis.png")
```

### Podcast Quality Check

```python
analyzer = AudioAnalyzer("podcast.mp3")
analyzer.analyze_loudness()

loudness = analyzer.get_loudness()
if loudness['lufs'] > -16:
    print("Warning: Audio may be too loud for podcast standards")
elif loudness['lufs'] < -20:
    print("Warning: Audio may be too quiet")
else:
    print("Loudness is within podcast standards (-16 to -20 LUFS)")
```

### Batch Analysis

```python
import os
from scripts.audio_analyzer import AudioAnalyzer

results = []
for filename in os.listdir("./songs"):
    if filename.endswith(('.mp3', '.wav', '.flac')):
        analyzer = AudioAnalyzer(f"./songs/{filename}")
        analyzer.analyze()
        results.append({
            'file': filename,
            'bpm': analyzer.get_tempo()['bpm'],
            'key': f"{analyzer.get_key()['key']} {analyzer.get_key()['mode']}",
            'lufs': analyzer.get_loudness()['lufs']
        })

# Sort by BPM for DJ set
results.sort(key=lambda x: x['bpm'])
```

## Supported Formats

Input formats (via librosa/soundfile):
- MP3
- WAV
- FLAC
- OGG
- M4A/AAC
- AIFF

Output formats:
- JSON (analysis report)
- PNG (visualizations)
- SVG (visualizations)
- TXT (summary)

## Dependencies

```
librosa>=0.10.0
soundfile>=0.12.0
matplotlib>=3.7.0
numpy>=1.24.0
scipy>=1.10.0
```

## Limitations

- Key detection works best with melodic content (less accurate for drums/percussion)
- BPM detection may struggle with free-tempo or complex time signatures
- Very short clips (<5 seconds) may have reduced accuracy
- LUFS calculation is simplified (not full ITU-R BS.1770-4)
