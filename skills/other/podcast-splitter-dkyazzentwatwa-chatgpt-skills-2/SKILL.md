---
name: podcast-splitter
description: Split audio files by detecting silence gaps. Auto-segment podcasts into chapters, remove long silences, and export individual clips.
---

# Podcast Splitter

Automatically split audio files into segments based on silence detection. Perfect for dividing podcasts into chapters, creating clips from long recordings, or removing dead air.

## Quick Start

```python
from scripts.podcast_splitter import PodcastSplitter

# Auto-split by silence
splitter = PodcastSplitter("podcast_episode.mp3")
segments = splitter.split_by_silence()
splitter.export_segments("./chapters/")

# Remove long silences
splitter = PodcastSplitter("raw_recording.mp3")
splitter.remove_silence(min_length=2000)  # Remove silences > 2 seconds
splitter.save("clean_recording.mp3")
```

## Features

- **Silence Detection**: Configurable threshold and duration
- **Auto-Split**: Divide audio at natural breaks
- **Silence Removal**: Remove or shorten long pauses
- **Chapter Export**: Save individual segments as files
- **Preview Mode**: List detected silences without splitting
- **Batch Processing**: Process multiple files

## API Reference

### Initialization

```python
splitter = PodcastSplitter("audio.mp3")

# With custom settings
splitter = PodcastSplitter(
    "audio.mp3",
    silence_thresh=-40,    # dBFS threshold
    min_silence_len=1000,  # Minimum silence length (ms)
    keep_silence=300       # Silence to keep at segment edges (ms)
)
```

### Silence Detection

```python
# Detect silence regions
silences = splitter.detect_silence()
# Returns: [(start_ms, end_ms), (start_ms, end_ms), ...]

# Print silence summary
splitter.print_silence_report()
```

### Splitting

```python
# Split at all detected silences
segments = splitter.split_by_silence()

# Split at silences longer than threshold
segments = splitter.split_by_silence(min_silence_len=3000)

# Limit number of segments
segments = splitter.split_by_silence(max_segments=10)
```

### Silence Removal

```python
# Remove silences longer than threshold
splitter.remove_silence(min_length=2000)  # Remove >2s silences

# Shorten silences to max length
splitter.shorten_silence(max_length=500)  # Cap at 500ms

# Remove leading/trailing silence only
splitter.strip_silence()
```

### Export

```python
# Export all segments
splitter.export_segments(
    output_dir="./chapters/",
    prefix="chapter",       # chapter_01.mp3, chapter_02.mp3
    format="mp3",
    bitrate=192
)

# Export specific segments
splitter.export_segment(0, "intro.mp3")
splitter.export_segment(3, "conclusion.mp3")

# Save modified audio
splitter.save("output.mp3")
```

## CLI Usage

```bash
# Split podcast into chapters
python podcast_splitter.py --input episode.mp3 --output-dir ./chapters/

# Detect and list silences (no splitting)
python podcast_splitter.py --input episode.mp3 --detect-only

# Remove long silences
python podcast_splitter.py --input raw.mp3 --output clean.mp3 --remove-silence 2000

# Custom sensitivity
python podcast_splitter.py --input episode.mp3 --output-dir ./chapters/ \
    --threshold -35 --min-silence 2000 --keep-silence 500
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input audio file | Required |
| `--output` | Output file (for silence removal) | - |
| `--output-dir` | Output directory for segments | - |
| `--detect-only` | Only detect/report silences | False |
| `--threshold` | Silence threshold (dBFS) | -40 |
| `--min-silence` | Minimum silence to detect (ms) | 1000 |
| `--keep-silence` | Silence to keep at edges (ms) | 300 |
| `--max-segments` | Maximum segments to create | None |
| `--remove-silence` | Remove silences longer than (ms) | - |
| `--shorten-silence` | Cap silence length at (ms) | - |
| `--prefix` | Output filename prefix | segment |
| `--format` | Output format | mp3 |
| `--bitrate` | Output bitrate (kbps) | 192 |

## Examples

### Split Interview into Q&A Segments

```python
splitter = PodcastSplitter(
    "interview.mp3",
    silence_thresh=-35,     # Less sensitive (louder threshold)
    min_silence_len=2000,   # Only split on 2+ second pauses
    keep_silence=400        # Keep some silence for natural feel
)

segments = splitter.split_by_silence()
print(f"Found {len(segments)} segments")

splitter.export_segments("./questions/", prefix="qa")
```

### Remove Dead Air from Recording

```python
splitter = PodcastSplitter("raw_recording.mp3")

# Show what would be removed
splitter.print_silence_report()

# Remove silences longer than 3 seconds
splitter.remove_silence(min_length=3000)

# Cap remaining silences at 1 second
splitter.shorten_silence(max_length=1000)

splitter.save("clean_recording.mp3")
```

### Create Highlight Clips

```python
splitter = PodcastSplitter("episode.mp3")
segments = splitter.split_by_silence(min_silence_len=5000)

# Export only segments longer than 30 seconds
for i, segment in enumerate(segments):
    duration = segment['end'] - segment['start']
    if duration > 30000:  # > 30 seconds
        splitter.export_segment(i, f"highlight_{i+1}.mp3")
```

### Batch Process Episodes

```python
import os
from scripts.podcast_splitter import PodcastSplitter

episodes_dir = "./raw_episodes/"
output_dir = "./processed/"

for filename in os.listdir(episodes_dir):
    if filename.endswith('.mp3'):
        filepath = os.path.join(episodes_dir, filename)
        splitter = PodcastSplitter(filepath)

        # Remove long silences
        splitter.remove_silence(min_length=2000)

        # Save cleaned version
        output_path = os.path.join(output_dir, filename)
        splitter.save(output_path)
        print(f"Processed: {filename}")
```

### Preview Silence Detection

```python
splitter = PodcastSplitter("episode.mp3")

# Get detailed silence info
silences = splitter.detect_silence()

print("Detected Silences:")
for i, (start, end) in enumerate(silences):
    duration = (end - start) / 1000
    start_time = start / 1000
    print(f"  {i+1}. {start_time:.1f}s - {duration:.1f}s silence")

# Print summary
splitter.print_silence_report()
```

## Detection Settings Guide

| Audio Type | Threshold | Min Silence | Notes |
|-----------|-----------|-------------|-------|
| Quiet studio | -50 dBFS | 500ms | Very sensitive |
| Normal podcast | -40 dBFS | 1000ms | Default |
| Noisy recording | -35 dBFS | 1500ms | Less sensitive |
| Music with breaks | -30 dBFS | 2000ms | For spoken breaks |

### Adjusting Sensitivity

- **More splits**: Lower threshold (e.g., -50), shorter min_silence
- **Fewer splits**: Higher threshold (e.g., -30), longer min_silence
- **Natural feel**: Longer keep_silence (500-1000ms)
- **Tight edits**: Shorter keep_silence (100-200ms)

## Dependencies

```
pydub>=0.25.0
```

**Note**: Requires FFmpeg installed on system.

## Limitations

- Works best with speech content (not music)
- Very noisy recordings may need threshold adjustment
- Long files use significant memory
- No automatic chapter naming (manual rename needed)
