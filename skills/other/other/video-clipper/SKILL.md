---
name: video-clipper
description: Cut video segments by timestamp, split videos into chunks, trim start/end, and extract specific scenes with precise frame control.
---

# Video Clipper

Cut and trim video segments with precise timestamp control.

## Features

- **Timestamp Clipping**: Cut segments by start/end times
- **Multi-Segment**: Extract multiple clips from one video
- **Split by Duration**: Auto-split into equal chunks
- **Trim**: Remove start/end portions
- **Format Preservation**: Maintain quality and format

## CLI Usage

```bash
python video_clipper.py --input video.mp4 --start 00:01:00 --end 00:02:30 --output clip.mp4
python video_clipper.py --input video.mp4 --split 60 --output clips/
```

## Dependencies

- moviepy>=1.0.3
- ffmpeg-python>=0.2.0
