---
name: audio-trimmer
description: Cut, trim, and edit audio segments with fade effects, speed control, concatenation, and basic audio manipulations.
---

# Audio Trimmer

Edit audio files with precise cutting, trimming, and effects. Extract segments, add fades, adjust speed, concatenate clips, and apply basic audio manipulations.

## Quick Start

```python
from scripts.audio_trimmer import AudioTrimmer

# Trim to segment
trimmer = AudioTrimmer("podcast.mp3")
trimmer.trim(start="00:05:30", end="00:10:00")
trimmer.save("segment.mp3")

# Add fades and save
trimmer = AudioTrimmer("song.mp3")
trimmer.fade_in(3000).fade_out(5000).save("song_faded.mp3")

# Concatenate multiple files
AudioTrimmer.concatenate(["intro.mp3", "main.mp3", "outro.mp3"], "full_episode.mp3")
```

## Features

- **Precise Trimming**: Cut segments by timestamp or milliseconds
- **Fade Effects**: Fade in/out with customizable duration
- **Speed Control**: Speed up or slow down audio
- **Concatenation**: Join multiple audio files
- **Basic Effects**: Reverse, loop, overlay
- **Silence Operations**: Add silence, remove silence
- **Volume Adjustment**: Gain control, normalization

## API Reference

### Initialization

```python
trimmer = AudioTrimmer("audio.mp3")
```

### Trimming

```python
# By timestamp (HH:MM:SS or MM:SS)
trimmer.trim(start="01:30", end="05:00")

# By milliseconds
trimmer.trim(start_ms=90000, end_ms=300000)

# From start to timestamp
trimmer.trim(end="02:00")

# From timestamp to end
trimmer.trim(start="10:00")
```

### Fade Effects

```python
# Fade in at start (milliseconds)
trimmer.fade_in(3000)  # 3 second fade in

# Fade out at end
trimmer.fade_out(5000)  # 5 second fade out

# Crossfade (for concatenation)
AudioTrimmer.concatenate_with_crossfade(files, output, crossfade_ms=2000)
```

### Speed Control

```python
# Speed up (1.5x)
trimmer.speed(1.5)

# Slow down (0.75x)
trimmer.speed(0.75)
```

### Effects

```python
# Reverse audio
trimmer.reverse()

# Loop audio N times
trimmer.loop(3)

# Overlay another audio
trimmer.overlay("background.mp3", position_ms=0, volume=-6)
```

### Volume

```python
# Adjust volume (dB)
trimmer.gain(6)   # Increase by 6 dB
trimmer.gain(-3)  # Decrease by 3 dB

# Normalize to target level
trimmer.normalize(-3)  # Normalize to -3 dBFS
```

### Silence Operations

```python
# Add silence at start
trimmer.add_silence_start(2000)  # 2 seconds

# Add silence at end
trimmer.add_silence_end(1000)

# Strip leading/trailing silence
trimmer.strip_silence(threshold=-50)  # dBFS threshold
```

### Concatenation

```python
# Simple concatenation
AudioTrimmer.concatenate(
    ["file1.mp3", "file2.mp3", "file3.mp3"],
    "output.mp3"
)

# With crossfade
AudioTrimmer.concatenate_with_crossfade(
    ["intro.mp3", "main.mp3", "outro.mp3"],
    "output.mp3",
    crossfade_ms=2000
)
```

### Save

```python
# Save to file (format from extension)
trimmer.save("output.mp3")

# Explicit format and quality
trimmer.save("output.mp3", format="mp3", bitrate=320)
```

## CLI Usage

```bash
# Trim segment
python audio_trimmer.py --input podcast.mp3 --output segment.mp3 --start 05:30 --end 10:00

# Add fades
python audio_trimmer.py --input song.mp3 --output faded.mp3 --fade-in 3000 --fade-out 5000

# Speed up
python audio_trimmer.py --input lecture.mp3 --output fast.mp3 --speed 1.5

# Concatenate files
python audio_trimmer.py --concat file1.mp3 file2.mp3 file3.mp3 --output merged.mp3

# Extract multiple segments
python audio_trimmer.py --input podcast.mp3 --segments "00:00-05:00,10:00-15:00,20:00-25:00" --output-dir ./clips/
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input audio file | Required |
| `--output` | Output file path | Required |
| `--start` | Start timestamp (HH:MM:SS or MM:SS) | - |
| `--end` | End timestamp | - |
| `--fade-in` | Fade in duration (ms) | - |
| `--fade-out` | Fade out duration (ms) | - |
| `--speed` | Speed multiplier | 1.0 |
| `--gain` | Volume adjustment (dB) | 0 |
| `--reverse` | Reverse audio | False |
| `--normalize` | Normalize to dBFS level | - |
| `--concat` | Files to concatenate | - |
| `--crossfade` | Crossfade duration for concat (ms) | 0 |
| `--segments` | Multiple segments to extract | - |

## Examples

### Extract Podcast Segment

```python
trimmer = AudioTrimmer("episode_42.mp3")
trimmer.trim(start="15:30", end="22:45")
trimmer.fade_in(1000)
trimmer.fade_out(2000)
trimmer.save("highlight_clip.mp3")
```

### Create Ringtone

```python
trimmer = AudioTrimmer("song.mp3")
trimmer.trim(start="01:15", end="01:45")  # 30-second segment
trimmer.fade_in(500)
trimmer.fade_out(1000)
trimmer.normalize(-3)
trimmer.save("ringtone.mp3", bitrate=192)
```

### Speed Up Lecture

```python
trimmer = AudioTrimmer("lecture.mp3")
trimmer.speed(1.25)  # 25% faster
trimmer.normalize(-16)  # Podcast-friendly level
trimmer.save("lecture_fast.mp3")
```

### Build Episode from Segments

```python
# With crossfades between segments
AudioTrimmer.concatenate_with_crossfade(
    files=[
        "intro_music.mp3",
        "sponsor_read.mp3",
        "main_content.mp3",
        "outro_music.mp3"
    ],
    output="full_episode.mp3",
    crossfade_ms=1500
)
```

### Extract Multiple Highlights

```python
# Extract several segments from a long recording
trimmer = AudioTrimmer("meeting_recording.mp3")

segments = [
    ("00:05:00", "00:08:30", "intro"),
    ("00:25:00", "00:32:00", "discussion"),
    ("01:15:00", "01:20:00", "conclusion")
]

for start, end, name in segments:
    t = AudioTrimmer("meeting_recording.mp3")
    t.trim(start=start, end=end)
    t.fade_in(500)
    t.fade_out(500)
    t.save(f"{name}.mp3")
```

### Add Background Music

```python
# Overlay quiet background music
trimmer = AudioTrimmer("podcast.mp3")
trimmer.overlay(
    "ambient_music.mp3",
    position_ms=0,
    volume=-15,  # 15 dB quieter
    loop=True    # Loop to fill duration
)
trimmer.save("podcast_with_music.mp3")
```

## Time Format Reference

The trimmer accepts these timestamp formats:

| Format | Example | Meaning |
|--------|---------|---------|
| `MM:SS` | `05:30` | 5 minutes 30 seconds |
| `HH:MM:SS` | `01:30:00` | 1 hour 30 minutes |
| `SS` | `90` | 90 seconds |
| `SS.ms` | `90.500` | 90.5 seconds |

## Dependencies

```
pydub>=0.25.0
```

**Note**: Requires FFmpeg installed on system.

## Limitations

- Speed adjustment may affect pitch (no pitch preservation)
- Very large files may consume significant memory
- Crossfade works best with similar audio levels
