---
name: mediapipe-pose-detection
description: MediaPipe pose detection expertise. Use when debugging landmark tracking, adjusting confidence thresholds, fixing pose detection issues, working with pose.py and video_io.py, or validating pose detection with manual observation.
---

# MediaPipe Pose Detection

## Key Landmarks for Jump Analysis

### Lower Body (Primary for Jumps)

| Landmark | Left Index | Right Index | Use Case                    |
| -------- | ---------- | ----------- | --------------------------- |
| Hip      | 23         | 24          | Center of mass, jump height |
| Knee     | 25         | 26          | Triple extension, landing   |
| Ankle    | 27         | 28          | Ground contact detection    |
| Heel     | 29         | 30          | Takeoff/landing timing      |
| Toe      | 31         | 32          | Forefoot contact            |

### Upper Body (Secondary)

| Landmark | Left Index | Right Index | Use Case           |
| -------- | ---------- | ----------- | ------------------ |
| Shoulder | 11         | 12          | Arm swing tracking |
| Elbow    | 13         | 14          | Arm action         |
| Wrist    | 15         | 16          | Arm swing timing   |

### Reference Points

| Landmark  | Index | Use Case         |
| --------- | ----- | ---------------- |
| Nose      | 0     | Head position    |
| Left Eye  | 2     | Face orientation |
| Right Eye | 5     | Face orientation |

## Confidence Thresholds

### Default Settings

```python
min_detection_confidence = 0.5  # Initial pose detection
min_tracking_confidence = 0.5   # Frame-to-frame tracking
```

### Quality Presets (auto_tuning.py)

| Preset     | Detection | Tracking | Use Case                           |
| ---------- | --------- | -------- | ---------------------------------- |
| `fast`     | 0.3       | 0.3      | Quick processing, tolerates errors |
| `balanced` | 0.5       | 0.5      | Default, good accuracy             |
| `accurate` | 0.7       | 0.7      | Best accuracy, slower              |

### Tuning Guidelines

- **Increase thresholds** when: Jittery landmarks, false detections
- **Decrease thresholds** when: Missing landmarks, tracking loss
- **Typical adjustment**: ±0.1 increments

## Common Issues and Solutions

### Landmark Jitter

**Symptoms**: Landmarks jump erratically between frames

**Solutions**:

1. Apply Butterworth low-pass filter (cutoff 6-10 Hz)
2. Increase tracking confidence
3. Use One-Euro filter for real-time applications

```python
# Butterworth filter (filtering.py)
from kinemotion.core.filtering import butterworth_filter
smoothed = butterworth_filter(landmarks, cutoff=8.0, fps=30)

# One-Euro filter (smoothing.py)
from kinemotion.core.smoothing import one_euro_filter
smoothed = one_euro_filter(landmarks, min_cutoff=1.0, beta=0.007)
```

### Left/Right Confusion

**Symptoms**: MediaPipe swaps left and right landmarks mid-video

**Cause**: Occlusion at 90° lateral camera angle

**Solutions**:

1. Use 45° oblique camera angle (recommended)
2. Post-process to detect and correct swaps
3. Use single-leg tracking when possible

### Tracking Loss

**Symptoms**: Landmarks disappear for several frames

**Causes**:

- Athlete moves out of frame
- Fast motion blur
- Occlusion by equipment/clothing

**Solutions**:

1. Ensure full athlete visibility throughout video
2. Use higher frame rate (60+ fps)
3. Interpolate missing frames (up to 3-5 frames)

```python
# Simple linear interpolation for gaps
import numpy as np
def interpolate_gaps(landmarks, max_gap=5):
    # Fill NaN gaps with linear interpolation
    for i in range(landmarks.shape[1]):
        mask = np.isnan(landmarks[:, i])
        if mask.sum() > 0 and mask.sum() <= max_gap:
            landmarks[:, i] = np.interp(
                np.arange(len(landmarks)),
                np.where(~mask)[0],
                landmarks[~mask, i]
            )
    return landmarks
```

### Low Confidence Scores

**Symptoms**: Visibility scores consistently below threshold

**Causes**:

- Poor lighting (backlighting, shadows)
- Low contrast clothing vs background
- Partial occlusion

**Solutions**:

1. Improve lighting (front-lit, even)
2. Ensure clothing contrasts with background
3. Remove obstructions from camera view

## Video Processing (video_io.py)

### Rotation Handling

Mobile videos often have rotation metadata that must be handled:

```python
# video_io.py handles this automatically
# Reads EXIF rotation and applies correction
from kinemotion.core.video_io import read_video_frames

frames, fps, dimensions = read_video_frames("mobile_video.mp4")
# Frames are correctly oriented regardless of source
```

### Manual Rotation (if needed)

```bash
# FFmpeg rotation options
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4  # 90° clockwise
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4  # 90° counter-clockwise
ffmpeg -i input.mp4 -vf "hflip" output.mp4        # Horizontal flip
```

### Frame Dimensions

Always read actual frame dimensions from first frame, not metadata:

```python
# Correct approach
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
height, width = frame.shape[:2]

# Incorrect (may be wrong for rotated videos)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
```

## Coordinate Systems

### MediaPipe Output

- Normalized coordinates: (0.0, 0.0) to (1.0, 1.0)
- Origin: Top-left corner
- X: Left to right
- Y: Top to bottom
- Z: Depth (relative, camera-facing is negative)

### Conversion to Pixels

```python
def normalized_to_pixel(landmark, width, height):
    x = int(landmark.x * width)
    y = int(landmark.y * height)
    return x, y
```

### Visibility Score

Each landmark has a visibility score (0.0-1.0):

- > 0.5: Likely visible and accurate
- < 0.5: May be occluded or estimated
- = 0.0: Not detected

## Debug Overlay (debug_overlay.py)

### Skeleton Drawing

```python
# Key connections for jump visualization
POSE_CONNECTIONS = [
    (23, 25), (25, 27), (27, 29), (27, 31),  # Left leg
    (24, 26), (26, 28), (28, 30), (28, 32),  # Right leg
    (23, 24),                                  # Hips
    (11, 23), (12, 24),                       # Torso
]
```

### Color Coding

| Element        | Color (BGR)   | Meaning                   |
| -------------- | ------------- | ------------------------- |
| Skeleton       | (0, 255, 0)   | Green - normal tracking   |
| Low confidence | (0, 165, 255) | Orange - visibility < 0.5 |
| Key angles     | (255, 0, 0)   | Blue - measured angles    |
| Phase markers  | (0, 0, 255)   | Red - takeoff/landing     |

## Performance Optimization

### Reducing Latency

1. Use `model_complexity=0` for fastest inference
2. Process every Nth frame for batch analysis
3. Use GPU acceleration if available

```python
import mediapipe as mp

pose = mp.solutions.pose.Pose(
    model_complexity=0,      # 0=Lite, 1=Full, 2=Heavy
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    static_image_mode=False  # False for video (uses tracking)
)
```

### Memory Management

- Release pose estimator after processing: `pose.close()`
- Process videos in chunks for large files
- Use generators for frame iteration

## Integration with kinemotion

### File Locations

- Pose estimation: `src/kinemotion/core/pose.py`
- Video I/O: `src/kinemotion/core/video_io.py`
- Filtering: `src/kinemotion/core/filtering.py`
- Smoothing: `src/kinemotion/core/smoothing.py`
- Auto-tuning: `src/kinemotion/core/auto_tuning.py`

### Typical Pipeline

```text
Video → read_video_frames() → pose.process() → filter/smooth → analyze
```

## Manual Observation for Validation

During development, use manual frame-by-frame observation to establish ground truth and validate pose detection accuracy.

### When to Use Manual Observation

1. **Algorithm development**: Validating new phase detection methods
2. **Parameter tuning**: Comparing detected vs actual frames
3. **Debugging**: Investigating pose detection failures
4. **Ground truth collection**: Building validation datasets

### Ground Truth Data Collection Protocol

**Step 1: Generate Debug Video**

```bash
uv run kinemotion cmj-analyze video.mp4 --output debug.mp4
```

**Step 2: Manual Frame-by-Frame Analysis**

Open debug video in a frame-stepping tool (QuickTime, VLC with frame advance, or video editor).

**Step 3: Record Observations**

For each key phase, record the frame number where the event occurs:

```text
=== MANUAL OBSERVATION: PHASE DETECTION ===

Video: ________________________
FPS: _____ Total Frames: _____

PHASE DETECTION (frame numbers)
| Phase | Detected | Manual | Error | Notes |
|-------|----------|--------|-------|-------|
| Standing End | ___ | ___ | ___ | |
| Lowest Point | ___ | ___ | ___ | |
| Takeoff | ___ | ___ | ___ | |
| Peak Height | ___ | ___ | ___ | |
| Landing | ___ | ___ | ___ | |

LANDMARK QUALITY (per phase)
| Phase | Hip Visible | Knee Visible | Ankle Visible | Notes |
|-------|-------------|--------------|---------------|-------|
| Standing | Y/N | Y/N | Y/N | |
| Countermovement | Y/N | Y/N | Y/N | |
| Flight | Y/N | Y/N | Y/N | |
| Landing | Y/N | Y/N | Y/N | |
```

### Phase Detection Criteria

**Standing End**: Last frame before downward hip movement begins

- Look for: Hip starts descending, knees begin flexing

**Lowest Point**: Frame where hip reaches minimum height

- Look for: Deepest squat position, hip at lowest Y coordinate

**Takeoff**: First frame where both feet leave ground

- Look for: Toe/heel landmarks separate from ground plane
- Note: May be 1-2 frames after visible liftoff due to detection lag

**Peak Height**: Frame where hip reaches maximum height

- Look for: Hip at highest Y coordinate during flight

**Landing**: First frame where foot contacts ground

- Look for: Heel or toe landmark touches ground plane
- Note: Algorithm may detect 1-2 frames late (velocity-based)

### Landmark Quality Assessment

For each landmark, observe:

| Quality     | Criteria                                             |
| ----------- | ---------------------------------------------------- |
| **Good**    | Landmark stable, positioned correctly on body part   |
| **Jittery** | Landmark oscillates ±5-10 pixels between frames      |
| **Offset**  | Landmark consistently displaced from actual position |
| **Lost**    | Landmark missing or wildly incorrect                 |
| **Swapped** | Left/right landmarks switched                        |

### Recording Observations Format

When validating, provide structured data:

```text
## Ground Truth: [video_name]

**Video Info:**
- Frames: 215
- FPS: 60
- Duration: 3.58s
- Camera: 45° oblique

**Phase Detection Comparison:**

| Phase | Detected | Manual | Error (frames) | Error (ms) |
|-------|----------|--------|----------------|------------|
| Standing End | 64 | 64 | 0 | 0 |
| Lowest Point | 91 | 88 | +3 (late) | +50 |
| Takeoff | 104 | 104 | 0 | 0 |
| Landing | 144 | 142 | +2 (late) | +33 |

**Error Analysis:**
- Mean absolute error: 1.25 frames (21ms)
- Bias detected: Landing consistently late
- Accuracy: 2/4 perfect, 4/4 within ±3 frames

**Landmark Issues Observed:**
- Frame 87-92: Hip jitter during lowest point
- Frame 140-145: Ankle tracking unstable at landing
```

### Acceptable Error Thresholds

At 60fps (16.67ms per frame):

| Error Level | Frames | Time  | Interpretation                    |
| ----------- | ------ | ----- | --------------------------------- |
| Perfect     | 0      | 0ms   | Exact match                       |
| Excellent   | ±1     | ±17ms | Within human observation variance |
| Good        | ±2     | ±33ms | Acceptable for most metrics       |
| Acceptable  | ±3     | ±50ms | May affect precise timing metrics |
| Investigate | >3     | >50ms | Algorithm may need adjustment     |

### Bias Detection

Look for systematic patterns across multiple videos:

| Pattern              | Meaning                 | Action                   |
| -------------------- | ----------------------- | ------------------------ |
| Consistent +N frames | Algorithm detects late  | Adjust threshold earlier |
| Consistent -N frames | Algorithm detects early | Adjust threshold later   |
| Variable ±N frames   | Normal variance         | No action needed         |
| Increasing error     | Tracking degrades       | Check landmark quality   |

### Integration with basic-memory

Store ground truth observations:

```python
# Save validation results
write_note(
    title="CMJ Phase Detection Validation - [video_name]",
    content="[structured observation data]",
    folder="biomechanics"
)

# Search previous validations
search_notes("phase detection ground truth")

# Build context for analysis
build_context("memory://biomechanics/*")
```

### Example: CMJ Validation Study Reference

See basic-memory for complete validation study:

- `biomechanics/cmj-phase-detection-validation-45deg-oblique-view-ground-truth`
- `biomechanics/cmj-landing-detection-bias-root-cause-analysis`
- `biomechanics/cmj-landing-detection-impact-vs-contact-method-comparison`

Key findings from validation:

- Standing End: 100% accuracy (0 frame error)
- Takeoff: ~0.7 frame mean error (excellent)
- Lowest Point: ~2.3 frame mean error (variable)
- Landing: +1-2 frame consistent bias (investigate)
