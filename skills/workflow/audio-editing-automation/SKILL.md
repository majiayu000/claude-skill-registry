---
name: audio-editing-automation
description: FFmpeg audio processing, batch editing, normalization, mixing, and automated audio production workflows. Use when processing audio at scale, automating editing tasks, or building audio pipelines.
---

# Audio Editing Automation

## FFmpeg Audio Operations

### Extract Audio from Video

```bash
ffmpeg -i input.mp4 -vn -acodec copy audio.aac
# -vn: no video
# -acodec copy: no re-encoding
```

### Audio Format Conversion

```bash
# WAV to MP3
ffmpeg -i input.wav -c:a libmp3lame -b:a 192k output.mp3

# MP3 to AAC
ffmpeg -i input.mp3 -c:a aac -b:a 192k output.m4a
```

### Volume Normalization

```bash
# Increase volume by 10dB
ffmpeg -i input.mp3 -af "volume=10dB" output.mp3

# Normalize using loudnorm filter
ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.wav
```

### Audio Mixing

```bash
# Mix two audio files
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex amix=inputs=2:duration=longest output.mp3

# Voice + background music (ducking)
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex \
  "[1:a]volume=0.3[bg];[0:a][bg]amix=inputs=2:duration=first"  output.mp3
```

### Batch Processing

```python
import subprocess
from pathlib import Path

def normalize_audio_batch(input_dir, output_dir):
    for audio in Path(input_dir).glob("*.mp3"):
        output = Path(output_dir) / audio.name

        subprocess.run([
            'ffmpeg', '-i', str(audio),
            '-af', 'loudnorm=I=-16:TP=-1.5',
            str(output)
        ])
```

## Audio Quality Standards

### Podcast Export

```
Format: MP3
Bitrate: 128-192kbps
Sample Rate: 44.1kHz
Loudness: -16 LUFS
Peak: -1dB
```

### Audiobook (ACX)

```
Format: MP3, 192kbps CBR
Sample Rate: 44.1kHz
Peak: -3dB
RMS: -18dB to -23dB
Noise Floor: -60dB
```

### YouTube/Video

```
Format: AAC
Bitrate: 192kbps
Sample Rate: 48kHz
Loudness: -14 LUFS
```

## Automation Workflow

```python
def audio_production_pipeline(voice_file, music_file):
    # 1. Normalize voice
    normalize_audio(voice_file, 'voice_normalized.mp3')

    # 2. Mix with music
    mix_audio('voice_normalized.mp3', music_file, 'mixed.mp3')

    # 3. Final loudness normalization
    final_normalize('mixed.mp3', 'final.mp3', target_lufs=-16)

    # 4. Export for platforms
    export_for_podcast('final.mp3')
    export_for_youtube('final.mp3')
```

## Resources

- FFmpeg Audio Documentation
- Loudness Standards (LUFS)
- Audio Mastering Best Practices
