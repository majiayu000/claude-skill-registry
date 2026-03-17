---
name: timelapse-creator
description: Create timelapse videos from image sequences with frame rate control, transitions, and quality optimization.
---

# Timelapse Creator

Create timelapse videos from image sequences.

## Features

- **Image Sequence**: Combine images into video
- **Frame Rate Control**: Custom FPS settings
- **Transitions**: Crossfade between frames
- **Sorting**: Auto-sort by timestamp/filename
- **Quality Control**: Resolution and codec options
- **Text Overlays**: Add timestamps/labels

## CLI Usage

```bash
python timelapse_creator.py --input images/ --output timelapse.mp4 --fps 30
```

## Dependencies

- moviepy>=1.0.3
- pillow>=10.0.0
- numpy>=1.24.0
