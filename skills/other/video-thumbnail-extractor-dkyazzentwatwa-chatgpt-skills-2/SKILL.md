---
name: video-thumbnail-extractor
description: Extract frames from videos at specific timestamps or intervals, find best frames, and generate thumbnail grids for previews.
---

# Video Thumbnail Extractor

Extract frames and create thumbnails from videos.

## Features

- **Frame Extraction**: Extract at timestamps or intervals
- **Best Frame Detection**: Find sharpest/brightest frames
- **Grid Previews**: Contact sheet thumbnails
- **Batch Processing**: Process multiple videos
- **Multiple Formats**: PNG, JPG output

## CLI Usage

```bash
python video_thumbnail_extractor.py --input video.mp4 --time 00:01:30 --output thumb.jpg
python video_thumbnail_extractor.py --input video.mp4 --grid 4x4 --output preview.jpg
```

## Dependencies

- moviepy>=1.0.3
- pillow>=10.0.0
- numpy>=1.24.0
