---
name: pydub-automation
description: "Automate repetitive audio tasks with Python using PyDub for batch processing, format conversion, normalization, and content assembly. Use when: Processing large numbers of audio files consistently; Converting between audio formats at scale; Normalizing loudness across a batch of files; Assembling intros/outros automatically to episodes; Trimming silence or extracting segments programmatically"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# PyDub Audio Automation

> Automate repetitive audio tasks with Python using PyDub for batch processing, format conversion, normalization, and content assembly.

## When to Use This Skill

- Processing large numbers of audio files consistently
- Converting between audio formats at scale
- Normalizing loudness across a batch of files
- Assembling intros/outros automatically to episodes
- Trimming silence or extracting segments programmatically
- Building audio pipelines for content production

## Methodology Foundation

**Source**: PyDub Library (James Robert) + Python Audio Processing

**Core Principle**: "Audio operations that take hours manually can run in minutes with code." PyDub provides a high-level interface that abstracts FFmpeg's complexity, making common operations accessible to non-audio engineers.

**Why This Matters**: Content teams producing regular podcasts, courses, or video content spend significant time on repetitive audio tasks. Automation enables consistent quality at scale while freeing humans for creative work.


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## What This Skill Does

1. **Batch processes audio files** - Apply same operations to hundreds of files
2. **Converts formats** - MP3, WAV, FLAC, OGG, and more
3. **Normalizes loudness** - Consistent levels across episodes
4. **Assembles content** - Concatenate intros, content, outros
5. **Extracts segments** - Trim, split, and slice audio programmatically

## How to Use

### Generate Processing Script
```
Help me write a PyDub script to [describe task].
Input files: [format, location]
Output requirements: [format, specs]
```

### Create Batch Workflow
```
Create a Python script that processes all audio files in a folder:
- Input: [source folder, file type]
- Operations: [what to do]
- Output: [destination, naming convention]
```

### Debug Audio Script
```
This PyDub script isn't working as expected:
[paste code]
Expected: [what you want]
Actual: [what's happening]
```

## Instructions

When automating audio with PyDub, follow this methodology:

### Step 1: Setup and Prerequisites

```python
## Installation

# Install PyDub
pip install pydub

# FFmpeg is required (PyDub uses it under the hood)
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Windows:
# Download from ffmpeg.org, add to PATH
```

```python
## Basic Imports

from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pydub.silence import detect_silence, split_on_silence
import os
from pathlib import Path
```

---

### Step 2: Core Operations

```python
## Loading and Saving Audio

# Load audio file (format auto-detected from extension)
audio = AudioSegment.from_file("input.mp3")
audio = AudioSegment.from_file("input.wav", format="wav")

# Save audio file
audio.export("output.mp3", format="mp3", bitrate="192k")
audio.export("output.wav", format="wav")

# Export with metadata
audio.export(
    "output.mp3",
    format="mp3",
    bitrate="192k",
    tags={"artist": "Brand Name", "album": "Podcast"}
)
```

```python
## Basic Properties

print(f"Duration: {len(audio)} ms")
print(f"Channels: {audio.channels}")
print(f"Frame rate: {audio.frame_rate} Hz")
print(f"Sample width: {audio.sample_width} bytes")
print(f"dBFS: {audio.dBFS}")  # Volume level
```

---

### Step 3: Volume and Normalization

```python
## Volume Adjustments

# Increase volume by 6 dB
louder = audio + 6

# Decrease volume by 3 dB
quieter = audio - 3

# Normalize to target level (0 dB = maximum)
normalized = normalize(audio)

# Normalize to specific headroom
def normalize_to_target(audio, target_dBFS=-16):
    """Normalize audio to target loudness."""
    change_in_dBFS = target_dBFS - audio.dBFS
    return audio.apply_gain(change_in_dBFS)

normalized = normalize_to_target(audio, target_dBFS=-16)
```

```python
## Batch Normalization

def normalize_folder(input_dir, output_dir, target_dBFS=-16):
    """Normalize all audio files in a folder."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for file in input_path.glob("*.mp3"):
        audio = AudioSegment.from_file(file)
        normalized = normalize_to_target(audio, target_dBFS)

        output_file = output_path / file.name
        normalized.export(output_file, format="mp3", bitrate="192k")
        print(f"Processed: {file.name}")

# Usage
normalize_folder("raw_episodes/", "processed_episodes/", target_dBFS=-16)
```

---

### Step 4: Concatenation and Assembly

```python
## Basic Concatenation

intro = AudioSegment.from_file("intro.mp3")
content = AudioSegment.from_file("episode.mp3")
outro = AudioSegment.from_file("outro.mp3")

# Concatenate (+ operator)
full_episode = intro + content + outro

# Add silence between segments
silence = AudioSegment.silent(duration=2000)  # 2 seconds
full_episode = intro + silence + content + silence + outro

full_episode.export("final_episode.mp3", format="mp3")
```

```python
## Podcast Assembly Script

def assemble_episode(
    content_file,
    intro_file="assets/intro.mp3",
    outro_file="assets/outro.mp3",
    output_file=None,
    intro_fade_ms=500,
    outro_fade_ms=500
):
    """
    Assemble podcast episode with intro and outro.
    Includes crossfade for professional sound.
    """
    intro = AudioSegment.from_file(intro_file)
    content = AudioSegment.from_file(content_file)
    outro = AudioSegment.from_file(outro_file)

    # Apply fade out to intro, fade in to content
    intro = intro.fade_out(intro_fade_ms)
    content = content.fade_in(intro_fade_ms).fade_out(outro_fade_ms)
    outro = outro.fade_in(outro_fade_ms)

    # Crossfade join
    episode = intro.append(content, crossfade=intro_fade_ms)
    episode = episode.append(outro, crossfade=outro_fade_ms)

    # Generate output filename if not provided
    if output_file is None:
        output_file = content_file.replace(".mp3", "_final.mp3")

    episode.export(output_file, format="mp3", bitrate="192k")
    print(f"Assembled: {output_file} ({len(episode)/1000:.1f}s)")
    return output_file

# Usage
assemble_episode("episode_042_raw.mp3")
```

---

### Step 5: Trimming and Splitting

```python
## Time-Based Trimming

# Extract segment (milliseconds)
# audio[start:end]
first_30_seconds = audio[:30000]
last_minute = audio[-60000:]
middle_section = audio[60000:120000]

# Remove first 5 seconds (skip intro)
without_intro = audio[5000:]
```

```python
## Silence-Based Operations

from pydub.silence import detect_silence, split_on_silence

# Detect silence regions
# Returns list of [start, end] in milliseconds
silence_ranges = detect_silence(
    audio,
    min_silence_len=1000,  # Minimum 1 second silence
    silence_thresh=-40     # dB threshold for "silence"
)

# Split on silence (useful for chapter markers)
chunks = split_on_silence(
    audio,
    min_silence_len=500,
    silence_thresh=-40,
    keep_silence=250  # Keep 250ms of silence on each side
)

# Export chunks
for i, chunk in enumerate(chunks):
    chunk.export(f"segment_{i:03d}.mp3", format="mp3")
```

```python
## Trim Silence from Start/End

def trim_silence(audio, silence_thresh=-50, chunk_size=10):
    """Remove silence from beginning and end of audio."""

    # Find first non-silent moment
    start_trim = 0
    for i in range(0, len(audio), chunk_size):
        if audio[i:i+chunk_size].dBFS > silence_thresh:
            start_trim = max(0, i - 100)  # Keep 100ms before
            break

    # Find last non-silent moment
    end_trim = len(audio)
    for i in range(len(audio), 0, -chunk_size):
        if audio[i-chunk_size:i].dBFS > silence_thresh:
            end_trim = min(len(audio), i + 100)  # Keep 100ms after
            break

    return audio[start_trim:end_trim]
```

---

### Step 6: Format Conversion

```python
## Batch Format Conversion

def convert_folder(input_dir, output_dir, output_format="mp3", **export_kwargs):
    """
    Convert all audio files to specified format.

    Example kwargs for MP3:
        bitrate="192k"
    Example kwargs for WAV:
        parameters=["-ac", "1"]  # mono
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Supported input formats
    extensions = ["*.mp3", "*.wav", "*.flac", "*.ogg", "*.m4a"]

    for ext in extensions:
        for file in input_path.glob(ext):
            audio = AudioSegment.from_file(file)

            output_file = output_path / f"{file.stem}.{output_format}"
            audio.export(output_file, format=output_format, **export_kwargs)
            print(f"Converted: {file.name} → {output_file.name}")

# Usage: Convert WAVs to MP3
convert_folder("recordings/", "mp3_output/", output_format="mp3", bitrate="192k")

# Usage: Convert to mono WAV
convert_folder("stereo/", "mono/", output_format="wav", parameters=["-ac", "1"])
```

---

### Step 7: Complete Pipeline Example

```python
## Full Podcast Processing Pipeline

from pydub import AudioSegment
from pydub.effects import normalize
from pathlib import Path
import json
from datetime import datetime

class PodcastProcessor:
    """
    Complete podcast processing pipeline.

    Operations:
    1. Normalize loudness
    2. Trim silence
    3. Add intro/outro
    4. Export with metadata
    """

    def __init__(self, config_file="podcast_config.json"):
        with open(config_file) as f:
            self.config = json.load(f)

        self.intro = AudioSegment.from_file(self.config["intro_file"])
        self.outro = AudioSegment.from_file(self.config["outro_file"])

    def process_episode(self, input_file, episode_number, title):
        """Process a single episode through the full pipeline."""

        print(f"Processing Episode {episode_number}: {title}")

        # 1. Load and normalize
        audio = AudioSegment.from_file(input_file)
        target_db = self.config.get("target_loudness", -16)
        audio = self._normalize_to_target(audio, target_db)
        print(f"  ✓ Normalized to {target_db} dBFS")

        # 2. Trim silence
        audio = self._trim_silence(audio)
        print(f"  ✓ Trimmed silence (duration: {len(audio)/1000:.1f}s)")

        # 3. Add intro/outro with crossfade
        fade_ms = self.config.get("crossfade_ms", 500)
        intro = self.intro.fade_out(fade_ms)
        outro = self.outro.fade_in(fade_ms)
        audio = audio.fade_in(fade_ms).fade_out(fade_ms)

        final = intro.append(audio, crossfade=fade_ms)
        final = final.append(outro, crossfade=fade_ms)
        print(f"  ✓ Added intro/outro (total: {len(final)/1000:.1f}s)")

        # 4. Export with metadata
        output_dir = Path(self.config["output_dir"])
        output_dir.mkdir(exist_ok=True)

        filename = f"episode_{episode_number:03d}.mp3"
        output_path = output_dir / filename

        final.export(
            output_path,
            format="mp3",
            bitrate=self.config.get("bitrate", "192k"),
            tags={
                "title": f"Episode {episode_number}: {title}",
                "artist": self.config["podcast_name"],
                "album": self.config["podcast_name"],
                "track": episode_number,
                "date": datetime.now().strftime("%Y"),
            }
        )
        print(f"  ✓ Exported: {output_path}")

        return output_path

    def _normalize_to_target(self, audio, target_dBFS):
        change = target_dBFS - audio.dBFS
        return audio.apply_gain(change)

    def _trim_silence(self, audio, threshold=-50):
        # Simple trim - just first/last 100ms chunks
        chunk_size = 100
        start = 0
        for i in range(0, min(5000, len(audio)), chunk_size):
            if audio[i:i+chunk_size].dBFS > threshold:
                start = max(0, i - 100)
                break

        end = len(audio)
        for i in range(len(audio), max(0, len(audio)-5000), -chunk_size):
            if audio[i-chunk_size:i].dBFS > threshold:
                end = min(len(audio), i + 100)
                break

        return audio[start:end]


# Example config file (podcast_config.json):
"""
{
    "podcast_name": "Marketing Mastery",
    "intro_file": "assets/intro.mp3",
    "outro_file": "assets/outro.mp3",
    "output_dir": "processed_episodes/",
    "target_loudness": -16,
    "crossfade_ms": 500,
    "bitrate": "192k"
}
"""

# Usage:
# processor = PodcastProcessor("podcast_config.json")
# processor.process_episode("raw/ep42.mp3", 42, "The Power of Audio")
```

## Examples

### Example 1: Batch Normalize Podcast Backlog

**Context**: 50 podcast episodes with inconsistent loudness levels.

**Input**:
> Write a script to normalize all MP3 files in my episodes/ folder to -16 LUFS, keeping the originals as backup.

**Output**:

```python
#!/usr/bin/env python3
"""
Batch normalize podcast episodes to -16 dBFS.
Creates backups before processing.
"""

from pydub import AudioSegment
from pathlib import Path
import shutil

def batch_normalize(
    input_dir: str,
    target_dBFS: float = -16,
    create_backup: bool = True
):
    """
    Normalize all MP3 files in directory to target loudness.

    Args:
        input_dir: Folder containing MP3 files
        target_dBFS: Target loudness level
        create_backup: If True, saves originals to backup/ folder
    """
    input_path = Path(input_dir)

    # Create backup folder if needed
    if create_backup:
        backup_path = input_path / "backup"
        backup_path.mkdir(exist_ok=True)

    # Find all MP3 files
    mp3_files = list(input_path.glob("*.mp3"))
    print(f"Found {len(mp3_files)} MP3 files")

    for i, file in enumerate(mp3_files, 1):
        print(f"\n[{i}/{len(mp3_files)}] Processing: {file.name}")

        # Backup original
        if create_backup:
            shutil.copy(file, backup_path / file.name)

        # Load and check current level
        audio = AudioSegment.from_file(file)
        original_dBFS = audio.dBFS
        print(f"  Original level: {original_dBFS:.1f} dBFS")

        # Calculate adjustment needed
        adjustment = target_dBFS - original_dBFS

        if abs(adjustment) < 0.5:
            print(f"  Already at target, skipping")
            continue

        # Apply normalization
        normalized = audio.apply_gain(adjustment)

        # Export (overwrite original)
        normalized.export(file, format="mp3", bitrate="192k")
        print(f"  Normalized: {original_dBFS:.1f} → {target_dBFS} dBFS")

    print(f"\n✓ Complete! Processed {len(mp3_files)} files")
    if create_backup:
        print(f"  Backups saved to: {backup_path}")


if __name__ == "__main__":
    import sys

    input_dir = sys.argv[1] if len(sys.argv) > 1 else "episodes/"
    batch_normalize(input_dir, target_dBFS=-16)
```

**Usage**:
```bash
python normalize_episodes.py episodes/
```

---

### Example 2: Auto-Add Intro/Outro to New Episodes

**Context**: Weekly podcast needs intro/outro added to each new recording.

**Input**:
> Create a script that watches a folder for new recordings and automatically adds my standard intro and outro.

**Output**:

```python
#!/usr/bin/env python3
"""
Auto-assemble podcast episodes when new recordings are added.
Watch 'incoming/' folder, output to 'ready/' folder.
"""

from pydub import AudioSegment
from pathlib import Path
import time

# Configuration
WATCH_DIR = Path("incoming/")
OUTPUT_DIR = Path("ready/")
INTRO_FILE = Path("assets/intro.mp3")
OUTRO_FILE = Path("assets/outro.mp3")
CROSSFADE_MS = 500
TARGET_DBFS = -16

def assemble_episode(input_file: Path) -> Path:
    """Add intro/outro and normalize a podcast episode."""

    print(f"\nProcessing: {input_file.name}")

    # Load audio
    intro = AudioSegment.from_file(INTRO_FILE)
    content = AudioSegment.from_file(input_file)
    outro = AudioSegment.from_file(OUTRO_FILE)

    # Normalize content to target
    adjustment = TARGET_DBFS - content.dBFS
    content = content.apply_gain(adjustment)
    print(f"  Normalized: {content.dBFS:.1f} dBFS")

    # Apply fades
    intro = intro.fade_out(CROSSFADE_MS)
    content = content.fade_in(CROSSFADE_MS).fade_out(CROSSFADE_MS)
    outro = outro.fade_in(CROSSFADE_MS)

    # Assemble with crossfade
    episode = intro.append(content, crossfade=CROSSFADE_MS)
    episode = episode.append(outro, crossfade=CROSSFADE_MS)

    # Export
    output_file = OUTPUT_DIR / input_file.name
    episode.export(output_file, format="mp3", bitrate="192k")
    print(f"  Created: {output_file} ({len(episode)/1000/60:.1f} min)")

    return output_file


def watch_and_process():
    """Watch folder and process new files."""

    WATCH_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    processed = set()
    print(f"Watching {WATCH_DIR} for new recordings...")
    print(f"Output to: {OUTPUT_DIR}")
    print("Press Ctrl+C to stop\n")

    while True:
        for file in WATCH_DIR.glob("*.mp3"):
            if file.name not in processed:
                try:
                    assemble_episode(file)
                    processed.add(file.name)
                    # Move original to archive
                    archive = WATCH_DIR / "processed"
                    archive.mkdir(exist_ok=True)
                    file.rename(archive / file.name)
                except Exception as e:
                    print(f"  Error: {e}")

        time.sleep(5)  # Check every 5 seconds


if __name__ == "__main__":
    watch_and_process()
```

## Checklists & Templates

### PyDub Project Setup

```
## Requirements

□ Python 3.7+ installed
□ pip install pydub
□ FFmpeg installed and in PATH
□ Test: python -c "from pydub import AudioSegment; print('OK')"

## Project Structure

project/
├── scripts/
│   ├── normalize.py
│   ├── assemble.py
│   └── convert.py
├── assets/
│   ├── intro.mp3
│   └── outro.mp3
├── incoming/      # Raw recordings
├── processed/     # Final output
└── config.json    # Settings
```

---

### Common Operations Reference

```python
## Quick Reference

# Load
audio = AudioSegment.from_file("file.mp3")

# Save
audio.export("out.mp3", format="mp3", bitrate="192k")

# Volume
louder = audio + 6  # +6 dB
quieter = audio - 3  # -3 dB

# Trim
first_30s = audio[:30000]  # milliseconds
last_min = audio[-60000:]

# Concatenate
combined = audio1 + audio2 + audio3

# Fade
audio = audio.fade_in(500).fade_out(500)

# Crossfade
combined = audio1.append(audio2, crossfade=500)

# Normalize
from pydub.effects import normalize
normalized = normalize(audio)

# Silence
silence = AudioSegment.silent(duration=2000)

# Properties
print(len(audio))  # duration in ms
print(audio.dBFS)  # volume level
```

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## References

- PyDub. "GitHub Repository" (jiaaro/pydub) - Library documentation
- GeeksforGeeks. "Create an Audio Editor in Python Using PyDub"
- Real Python. "Working with Audio in Python"
- FFmpeg Documentation - Underlying encoder

## Related Skills

- [audio-editing](../audio-editing/) - Manual editing fundamentals
- [transcription-to-content](../transcription-to-content/) - Processing transcripts
- [podcast-production](../podcast-production/) - Full podcast workflow

---

## Skill Metadata (Internal Use)

```yaml
name: pydub-automation
category: audio
subcategory: automation
version: 1.0
author: MKTG Skills
source_expert: PyDub Library
source_work: jiaaro/pydub
difficulty: intermediate
estimated_value: Hours saved per batch (5-50 hours depending on scale)
tags: [python, automation, audio, batch-processing, pydub]
created: 2026-01-26
updated: 2026-01-26
```
