---
name: video-analysis-workflow
description: Guides video analysis for CMJ and drop jump. Use when processing athlete videos, debugging pose detection, troubleshooting analysis failures, or running kinemotion CLI commands.
allowed-tools: Bash(uv run kinemotion:*), Read, Glob
---

# Video Analysis Workflow

## Analysis Commands

```bash
# CMJ analysis
uv run kinemotion cmj-analyze <video> [--output debug.mp4]

# Drop Jump analysis
uv run kinemotion dropjump-analyze <video> [--output debug.mp4]

# Batch processing
uv run kinemotion cmj-analyze videos/*.mp4 --batch --workers 4
```

## Quality Presets

| Preset     | Use Case                     | Trade-off             |
| ---------- | ---------------------------- | --------------------- |
| `fast`     | Quick preview, large batches | Lower accuracy        |
| `balanced` | Default, most use cases      | Good accuracy/speed   |
| `accurate` | Validation, research         | Best accuracy, slower |

```bash
uv run kinemotion cmj-analyze video.mp4 --quality accurate
```

## Debug Output

Always use `--output debug.mp4` when:

- Metrics seem incorrect
- Troubleshooting pose detection
- Validating new videos
- Training coaches on video quality

The debug video shows:

- Skeleton overlay with joint angles
- Phase markers (takeoff, landing, peak)
- Real-time metrics display

## Camera Angle Recommendations

| Angle           | Recommendation  | Reason                                         |
| --------------- | --------------- | ---------------------------------------------- |
| **45° oblique** | Recommended     | Both legs clearly visible, accurate tracking   |
| 90° lateral     | Not recommended | MediaPipe confuses left/right feet (occlusion) |
| Front/back      | Not recommended | Depth ambiguity for sagittal plane motion      |

## Troubleshooting

### No Takeoff Detected

1. Verify video contains complete jump (before, during, after)
2. Check athlete is fully visible throughout
3. Try `--quality accurate` for stricter detection
4. Review debug video for landmark quality

### Invalid Metrics

1. Video may be too short (need full jump cycle)
2. Athlete may be partially occluded
3. Poor lighting affecting pose detection
4. Camera shake causing landmark jitter

### Jittery Landmarks

1. Check lighting conditions (avoid backlighting)
2. Ensure stable camera (tripod recommended)
3. Verify athlete clothing contrast with background
4. Try `--quality accurate` for better filtering

### Rotation Issues (Mobile Videos)

- Mobile videos often have rotation metadata
- kinemotion handles this automatically via `video_io.py`
- If issues persist, pre-process with: `ffmpeg -i input.mp4 -vf "transpose=1" output.mp4`

## Video Requirements

| Requirement | Specification              |
| ----------- | -------------------------- |
| Frame rate  | 30+ fps (60+ preferred)    |
| Resolution  | 720p minimum               |
| Duration    | Full jump cycle visible    |
| Lighting    | Even, front-lit preferred  |
| Background  | Contrasting with athlete   |
| Camera      | Stable, tripod recommended |

## Output Metrics

### CMJ Metrics

- `jump_height_cm`: Calculated from flight time
- `flight_time_ms`: Time in air
- `countermovement_depth_cm`: Lowest point before takeoff
- `takeoff_velocity_m_s`: Velocity at ground leave
- `triple_extension`: Hip, knee, ankle angles at takeoff

### Drop Jump Metrics

- `ground_contact_time_ms`: Time on ground after drop
- `flight_time_ms`: Time in air after contact
- `reactive_strength_index`: RSI = flight_time / contact_time
- `drop_height_cm`: Initial drop height (if detectable)

## Python API Alternative

```python
from kinemotion import process_cmj_video, process_dropjump_video

# CMJ
metrics = process_cmj_video("video.mp4", quality="balanced")

# Drop Jump
metrics = process_dropjump_video("video.mp4", quality="balanced")
```
