---
name: motion-sampler
description: Extracts frames at regular intervals from dashcam videos to create compact visual summaries of vehicle movement and location changes. This skill should be used when users need motion trajectory analysis, want to optimize dashcam storage by 90%+, need quick visual review of hours of footage, or want to create visual timelines of trips.
---

# Motion Sampler Skill

**Version:** 1.0
**Type:** Video Frame Extraction
**Purpose:** Extract representative frame samples from dashcam videos to understand motion and trajectory without storing full videos

## Overview

The Motion Sampler extracts frames at regular intervals from dashcam videos to create a compact visual summary of vehicle movement and location changes. This achieves **90-95% storage reduction** compared to keeping original videos while preserving spatial and temporal context.

## Use Cases

1. **Motion trajectory analysis** - Understand vehicle path through a sequence of locations
2. **Storage optimization** - Reduce dashcam archive size by 90%+ while retaining visual record
3. **Quick visual review** - Browse through hours of footage via representative frames
4. **Location identification** - Identify where vehicle was at specific times
5. **Event timeline** - Create visual timeline of trips without watching full videos

## Natural Language Interface

Use natural language to request frame extraction:

**Example Requests:**

```
Extract frames every 10 seconds from all Movie_F videos in the CARDV folder.

Sample frames from Movie_R dashcam videos, one frame every 15 seconds.

Create motion samples for all parking camera videos with 5-second intervals.

Extract representative frames from Movie_F and Movie_R for July 27-29, 2025.
```

## Parameters

### Required
- **camera** (string): Camera type to process
  - Options: `Movie_F`, `Movie_R`, `Park_F`, `Park_R`, or `all`
  - Default: `Movie_F`

- **source_dir** (path): Root directory containing camera folders
  - Example: `C:\Users\yousu\Desktop\CARDV`

### Optional
- **sample_interval** (float): Seconds between extracted frames
  - Range: 1.0 - 60.0
  - Default: 10.0
  - Examples: 5.0 (dense sampling), 15.0 (sparse sampling)

- **output_dir** (path): Where to save extracted frames
  - Default: `{source_dir}/MOTION_SAMPLES`

- **jpeg_quality** (int): JPEG compression quality
  - Range: 50 - 100
  - Default: 92 (visually lossless)
  - Lower = smaller files, slightly reduced quality

- **max_workers** (int): Parallel processing threads
  - Range: 1 - 8
  - Default: 4
  - Higher = faster but more CPU usage

- **date_filter** (string): Only process videos from specific date(s)
  - Format: `YYYYMMDD` or `YYYYMMDD-YYYYMMDD` (range)
  - Example: `20250727` or `20250727-20250729`

- **min_duration** (float): Skip videos shorter than this (seconds)
  - Default: 3.0

### Advanced (Future GPU Enhancement)
- **use_nvdec** (bool): Use NVIDIA hardware decoding
  - Default: false (CPU-only in v1.0)
  - Future: true for 3-5x speedup

- **gpu_id** (int): CUDA device ID if multiple GPUs
  - Default: 0

## Output Format

### Directory Structure
```
{output_dir}/
├── INDEX.csv                                      # Comprehensive metadata
├── 20250727150654_052278A_F001_001000ms.jpg      # Frame 1 at 1s
├── 20250727150654_052278A_F002_011000ms.jpg      # Frame 2 at 11s
├── 20250727150654_052278A_F003_021000ms.jpg      # Frame 3 at 21s
└── ...
```

### Filename Format
```
{YYYYMMDDHHMMSS}_{FILEIDA/B}_{POSITION}_{TIMESTAMP_MS}ms.jpg

Example: 20250727150654_052278A_F003_021000ms.jpg
         └─────┬─────┘ └──┬──┘  └┬┘   └───┬───┘
           Date/Time   FileID  Pos  Timestamp

Components:
- YYYYMMDDHHMMSS: Video start time
- FILEIDA/B: Camera file ID + suffix (A=front, B=rear)
- F###: Frame position (F001, F002, F003...)
- ######ms: Milliseconds into video
```

### INDEX.csv Schema
```csv
original_video,frame_file,camera,date,position,timestamp_ms,timestamp_s,frame_number,file_size_kb
20250727150654_052278A.MP4,20250727150654_052278A_F001_001000ms.jpg,Movie_F,20250727,F001,1000,1.0,24,1713.06
```

**Columns:**
- `original_video`: Source MP4 filename
- `frame_file`: Extracted JPEG filename
- `camera`: Camera type (Movie_F/Movie_R/Park_F/Park_R)
- `date`: YYYYMMDD
- `position`: Frame position (F001, F002...)
- `timestamp_ms`: Milliseconds into video
- `timestamp_s`: Seconds into video
- `frame_number`: Frame number in video (at 24fps)
- `file_size_kb`: JPEG file size in KB

## Performance Metrics

### Current (CPU-only v1.0)
- **Throughput**: 6-8 videos/second (4 workers, Intel i7/i9)
- **Speedup**: 4x with multi-threading
- **Memory**: ~500 MB
- **GPU Usage**: 0% (CPU-only)

### Projected (GPU-accelerated v2.0)
- **Throughput**: 20-30 videos/second (NVDEC + multi-threading)
- **Speedup**: 10-15x vs single-threaded CPU
- **Memory**: ~1-2 GB
- **GPU Usage**: 30-50% (NVDEC decoder only)

### Storage Examples

**Input:** 418 Movie_F/R videos, 60s avg, ~45 GB total

| Interval | Frames/Video | Total Frames | Storage | Reduction |
|----------|--------------|--------------|---------|-----------|
| 5s       | 12           | 5,016        | 9 GB    | 80%       |
| 10s      | 7            | 2,926        | 5 GB    | 89%       |
| 15s      | 5            | 2,090        | 3.7 GB  | 92%       |
| 30s      | 3            | 1,254        | 2.2 GB  | 95%       |

*Assumes 1.7 MB per frame average at 4K resolution*

## Algorithm Details

### Frame Sampling Strategy

For each video:
1. **Skip buffer zones**: Start at 1.0s, end at duration-1.0s (avoids black frames)
2. **Calculate sample timestamps**: Every N seconds starting from 1.0s
3. **Always include end frame**: Last frame at duration-1.0s
4. **Example for 60s video, 10s interval:**
   - F001: 1s, F002: 11s, F003: 21s, F004: 31s, F005: 41s, F006: 51s, F007: 59s

### Pseudo-code
```python
timestamps = []
current_time = 1.0  # start offset
while current_time < (duration - 1.0):
    timestamps.append(current_time)
    current_time += sample_interval
timestamps.append(duration - 1.0)  # always include end
```

## Error Handling

### Automatic Handling
- **Short videos (<3s)**: Skipped with warning
- **Corrupted files**: Logged as error, processing continues
- **Unreadable frames**: Frame skipped, next frame attempted
- **Disk full**: Graceful termination with partial results saved

### Error Messages
```
SKIP: video.MP4 too short (2.1s)
ERROR: Cannot open corrupted_video.MP4
WARNING: Failed to read frame 120 from video.MP4
```

## Example Usage

### Request 1: Standard Extraction
```
Use the motion-sampler skill to extract frames every 10 seconds from all Movie_F videos
in C:\Users\yousu\Desktop\CARDV. Save to MOTION_SAMPLES folder.
```

**Execution:**
- Camera: Movie_F
- Source: C:\Users\yousu\Desktop\CARDV\Movie_F\
- Output: C:\Users\yousu\Desktop\CARDV\MOTION_SAMPLES\
- Interval: 10.0s
- Quality: 92

### Request 2: Dense Sampling for Specific Date
```
Extract frames every 5 seconds from Movie_R videos on July 27, 2025.
```

**Execution:**
- Camera: Movie_R
- Date filter: 20250727
- Interval: 5.0s
- Only processes videos matching `20250727*.MP4`

### Request 3: Sparse Sampling for Long-term Archive
```
Create motion samples with 30-second intervals for all parking cameras (Park_F and Park_R)
to minimize storage while keeping a visual record.
```

**Execution:**
- Camera: Park_F, Park_R (both)
- Interval: 30.0s
- Expected: ~3 frames per 60s video
- Storage: Minimal (~1-2 GB for thousands of videos)

## Troubleshooting

### Issue: Processing Very Slow
**Solution:** Increase `max_workers` to 6-8 (if you have 8+ CPU cores)

### Issue: Large Output Size
**Solution:** Reduce `jpeg_quality` to 85 or increase `sample_interval` to 15-20s

### Issue: Missing Some Videos
**Cause:** Videos shorter than `min_duration` (default 3s) are skipped
**Solution:** Lower `min_duration` to 1.0s if you need very short clips

### Issue: Out of Memory
**Cause:** Too many parallel workers on low-RAM system
**Solution:** Reduce `max_workers` to 2

## Future Enhancements (v2.0 Roadmap)

### GPU Acceleration
- [ ] NVDEC hardware video decoding (5-10x speedup)
- [ ] GPU-accelerated JPEG encoding
- [ ] Multi-GPU support for massive archives
- [ ] Automatic GPU/CPU fallback

### Advanced Features
- [ ] Smart sampling (detect motion, skip static scenes)
- [ ] Face/person detection integration
- [ ] GPS overlay preservation
- [ ] Thumbnail strip generation
- [ ] Web viewer for browsing samples

### Optimization
- [ ] Incremental processing (skip already-processed videos)
- [ ] Resume from interruption
- [ ] S3/cloud storage output
- [ ] Real-time progress dashboard

## Technical Dependencies

### Required
- Python 3.8+
- opencv-python (cv2) >= 4.8
- numpy >= 1.24
- pandas >= 2.0 (for INDEX.csv)

### Optional (for future GPU support)
- cuda >= 11.0
- opencv-contrib-python (CUDA build)

## File Locations

```
G:\My Drive\PROJECTS\skills\motion-sampler\
├── skill.md                          # This file
├── README.md                         # Quick start guide
├── SKILL_MANIFEST.md                # File inventory & testing
├── scripts/
│   ├── extract_motion_samples.py    # Main extraction script
│   └── analyze_results.py           # Post-processing analysis
├── assets/
│   ├── config_template.json         # Default configuration
│   └── camera_mapping.json          # Camera ID mapping
└── references/
    ├── SAMPLING_ALGORITHM.md        # Detailed algorithm docs
    └── PERFORMANCE_BENCHMARKS.md    # Speed/storage benchmarks
```

## JSON API Contract

For programmatic invocation:

```json
{
  "camera": "Movie_F",
  "source_dir": "C:\\Users\\yousu\\Desktop\\CARDV",
  "output_dir": "C:\\Users\\yousu\\Desktop\\CARDV\\MOTION_SAMPLES",
  "sample_interval": 10.0,
  "jpeg_quality": 92,
  "max_workers": 4,
  "date_filter": null,
  "min_duration": 3.0,
  "use_nvdec": false
}
```

**Response:**
```json
{
  "status": "success",
  "videos_processed": 2146,
  "frames_extracted": 15022,
  "total_size_mb": 26750.5,
  "avg_frames_per_video": 7.0,
  "processing_time_s": 305.2,
  "throughput_videos_per_sec": 7.03,
  "output_dir": "C:\\Users\\yousu\\Desktop\\CARDV\\MOTION_SAMPLES",
  "index_file": "C:\\Users\\yousu\\Desktop\\CARDV\\MOTION_SAMPLES\\INDEX.csv"
}
```

## License & Attribution

Part of the dashcam analysis suite.
Designed for personal dashcam archive management and motion trajectory analysis.
