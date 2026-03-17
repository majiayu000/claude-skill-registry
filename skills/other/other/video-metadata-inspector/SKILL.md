---
name: video-metadata-inspector
description: Use when asked to inspect video file metadata, get video duration, resolution, codec information, frame rate, or bitrate.
---

# Video Metadata Inspector

Extract and analyze comprehensive metadata from video files including duration, resolution, codec, frame rate, and technical specifications.

## Purpose

Video metadata inspection for:
- Format verification and compatibility checking
- Quality assessment and validation
- Transcoding planning and optimization
- Video library cataloging
- Technical specification reports

## Features

- **Basic Info**: Duration, resolution, frame rate, file size
- **Codec Details**: Video/audio codec, profile, bitrate
- **Technical Specs**: Aspect ratio, pixel format, sample rate
- **Metadata**: Title, artist, creation date, tags
- **Batch Analysis**: Process multiple files in one operation
- **Export Formats**: JSON, CSV, human-readable text

## Quick Start

```python
from video_metadata_inspector import VideoMetadataInspector

# Inspect single video
inspector = VideoMetadataInspector()
inspector.load('video.mp4')
metadata = inspector.get_metadata()
print(f"Duration: {metadata['duration_seconds']:.2f}s")
print(f"Resolution: {metadata['width']}x{metadata['height']}")
print(f"FPS: {metadata['fps']}")

# Export full report
inspector.export_report('report.json', format='json')

# Batch inspect directory
inspector.batch_inspect(
    input_files=['video1.mp4', 'video2.mkv'],
    output='metadata.csv',
    format='csv'
)
```

## CLI Usage

```bash
# Basic metadata
python video_metadata_inspector.py input.mp4

# Full technical details
python video_metadata_inspector.py input.mp4 --verbose

# Export to JSON
python video_metadata_inspector.py input.mp4 --output metadata.json --format json

# Batch inspect directory
python video_metadata_inspector.py *.mp4 --output metadata.csv --format csv

# Compare multiple videos
python video_metadata_inspector.py video1.mp4 video2.mp4 --compare
```

## API Reference

### VideoMetadataInspector

```python
class VideoMetadataInspector:
    def load(self, filepath: str) -> 'VideoMetadataInspector'
    def get_metadata(self) -> Dict[str, Any]
    def get_basic_info(self) -> Dict[str, Any]
    def get_video_info(self) -> Dict[str, Any]
    def get_audio_info(self) -> Dict[str, Any]
    def get_format_info(self) -> Dict[str, Any]
    def export_report(self, output: str, format: str = 'json') -> str
    def batch_inspect(self, input_files: List[str], output: str = None,
                     format: str = 'csv') -> pd.DataFrame
    def compare_videos(self, video_files: List[str]) -> pd.DataFrame
```

## Metadata Categories

### Basic Information
- Duration (seconds, formatted)
- Resolution (width × height)
- Frame rate (FPS)
- File size
- Aspect ratio

### Video Stream
- Video codec (H.264, H.265, VP9, etc.)
- Codec profile and level
- Bitrate (kbps)
- Pixel format (yuv420p, etc.)
- Color space and range

### Audio Stream
- Audio codec (AAC, MP3, Opus, etc.)
- Sample rate (Hz)
- Channels (mono, stereo, 5.1, etc.)
- Audio bitrate (kbps)

### Container Format
- Container type (MP4, MKV, AVI, etc.)
- Creation date
- Metadata tags (title, artist, description)
- Number of streams

## Use Cases

**Format Verification:**
```python
inspector.load('video.mp4')
info = inspector.get_video_info()
if info['codec'] == 'h264' and info['width'] >= 1920:
    print("✓ Meets requirements: 1080p H.264")
```

**Transcoding Planning:**
```python
# Check if transcoding needed
metadata = inspector.get_metadata()
if metadata['video_codec'] != 'h265' or metadata['bitrate_kbps'] > 5000:
    print("Transcode recommended")
```

**Quality Assessment:**
```python
# Analyze video quality metrics
info = inspector.get_metadata()
quality_score = (
    (info['width'] * info['height']) / 2073600 * 50 +  # Resolution score
    min(info['fps'] / 60, 1) * 25 +  # Frame rate score
    min(info['bitrate_kbps'] / 10000, 1) * 25  # Bitrate score
)
```

## Common Checks

**Is video 4K?**
```python
metadata['width'] >= 3840 and metadata['height'] >= 2160
```

**Is video HDR?**
```python
'hdr' in metadata.get('color_space', '').lower()
```

**Is audio stereo?**
```python
metadata['audio_channels'] == 2
```

**Is codec modern?**
```python
metadata['video_codec'] in ['h265', 'vp9', 'av1']
```

## Limitations

- Cannot extract corrupt/damaged video metadata
- Some proprietary formats may have limited support
- DRM-protected content cannot be analyzed
- Metadata extraction may be slow for very large files
- Requires FFmpeg/FFprobe for full codec details
