---
name: video-processing
description: This skill provides guidance for video analysis and processing tasks using computer vision techniques. It should be used when analyzing video frames, detecting motion or events, tracking objects, extracting temporal data (e.g., identifying specific frames like takeoff/landing moments), or performing frame-by-frame processing with OpenCV or similar libraries.
---

# Video Processing

## Overview

This skill provides structured approaches for video analysis tasks involving frame extraction, motion detection, event identification, and temporal analysis. It emphasizes visualization-first debugging, systematic parameter tuning, and robust validation strategies to avoid common pitfalls in video processing workflows.

## Core Workflow

### Phase 1: Establish Ground Truth Before Implementation

Before writing any detection algorithms:

1. **Manual frame inspection**: Extract key frames and manually identify the expected results (e.g., "takeoff appears around frame 90-100")
2. **Create validation targets**: Document specific frame numbers or ranges to validate against
3. **Understand video properties**: Check FPS, resolution, codec, and total frame count
4. **Identify reference frames**: Determine which frames can serve as baselines (e.g., empty background, starting position)

```python
import cv2

cap = cv2.VideoCapture('video.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"FPS: {fps}, Frames: {frame_count}, Resolution: {width}x{height}")
```

### Phase 2: Build Visualization Infrastructure Early

Create visualization capabilities before implementing detection logic:

1. **Frame export function**: Save individual frames with annotations for manual review
2. **Debug video output**: Generate annotated videos showing detection overlays
3. **Data logging**: Output CSV/JSON with per-frame metrics for analysis

```python
def save_debug_frame(frame, frame_num, detections, output_dir):
    """Save annotated frame for visual verification."""
    annotated = frame.copy()
    for det in detections:
        cv2.rectangle(annotated, det['bbox'][:2], det['bbox'][2:], (0, 255, 0), 2)
        cv2.putText(annotated, f"y={det['lowest_y']}",
                    (det['bbox'][0], det['bbox'][1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imwrite(f"{output_dir}/frame_{frame_num:04d}.png", annotated)
```

### Phase 3: Implement Detection with Parameterization

Avoid hardcoded magic numbers. Make all thresholds configurable:

```python
class VideoAnalyzerConfig:
    blur_kernel_size: tuple = (21, 21)      # Document why this size
    binary_threshold: int = 25               # Threshold for foreground detection
    dilation_iterations: int = 2             # Morphological operations
    min_contour_area: int = 500              # Minimum detection size in pixels
    smoothing_window: int = 5                # Temporal smoothing for metrics
```

### Phase 4: Handle Detection Gaps and Edge Cases

Common scenarios requiring explicit handling:

1. **Subject not visible in reference frame**: Verify assumptions about background frames
2. **Detection gaps**: When subject temporarily undetectable, use interpolation or secondary metrics
3. **Multiple motion sources**: Filter by expected position, size, or motion characteristics
4. **Partial visibility**: Handle frames where subject enters/exits frame boundaries
5. **Lighting changes**: Consider adaptive thresholding or histogram equalization

```python
def handle_detection_gap(frame_data, gap_start, gap_end):
    """Interpolate or use secondary metrics during detection gaps."""
    # Option 1: Linear interpolation of position
    # Option 2: Use motion magnitude as proxy
    # Option 3: Flag gap for manual review
    pass
```

## Verification Strategies

### Strategy 1: Visual Verification Checkpoints

At each major algorithm step, output visual proof:

```python
# After background subtraction
cv2.imwrite("debug/01_background_diff.png", diff_frame)

# After thresholding
cv2.imwrite("debug/02_thresholded.png", thresh_frame)

# After morphological operations
cv2.imwrite("debug/03_morphed.png", morph_frame)

# After contour detection
cv2.imwrite("debug/04_contours.png", contour_frame)
```

### Strategy 2: Sanity Check Assertions

Add runtime validation for expected conditions:

```python
def validate_detection(detection, frame_num, video_props):
    """Verify detection makes physical sense."""
    assert detection['area'] > 0, f"Zero area detection at frame {frame_num}"
    assert 0 <= detection['center_x'] <= video_props['width']
    assert 0 <= detection['center_y'] <= video_props['height']

    # Domain-specific checks
    if frame_num > 0:
        max_reasonable_movement = video_props['fps'] * 50  # pixels per frame
        assert abs(detection['center_x'] - prev_x) < max_reasonable_movement
```

### Strategy 3: Metric Continuity Analysis

Plot metrics over time to identify anomalies:

```python
import matplotlib.pyplot as plt

def plot_metrics(frame_data, output_path):
    """Visualize metrics for anomaly detection."""
    frames = [d['frame'] for d in frame_data]
    y_positions = [d.get('lowest_y', None) for d in frame_data]
    motion = [d.get('motion_magnitude', None) for d in frame_data]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    axes[0].plot(frames, y_positions, 'b-', label='Y Position')
    axes[0].set_ylabel('Y Position (pixels)')
    axes[1].plot(frames, motion, 'r-', label='Motion')
    axes[1].set_ylabel('Motion Magnitude')
    plt.savefig(output_path)
```

## Common Pitfalls

### Pitfall 1: Coordinate System Confusion

Image coordinates have origin at top-left, with Y increasing downward:
- Lower Y value = higher position in frame
- When tracking jumps: minimum Y = maximum height

```python
# CORRECT: Finding highest point (lowest Y value)
peak_frame = min(detections, key=lambda d: d['lowest_y'])

# WRONG: Assuming higher Y = higher position
# peak_frame = max(detections, key=lambda d: d['lowest_y'])
```

### Pitfall 2: Numpy Type Serialization

Convert numpy types before JSON/TOML serialization:

```python
# WRONG: Will fail with "Object of type int64 is not JSON serializable"
result = {'frame': detection['frame'], 'y': detection['y']}

# CORRECT: Explicit conversion
result = {'frame': int(detection['frame']), 'y': int(detection['y'])}
```

### Pitfall 3: Bounding Box vs Actual Position

Bounding box coordinates may not reflect actual body position:
- During jumps, leg extension changes bounding box without changing body center
- Use center of mass or specific keypoint detection for accuracy

### Pitfall 4: Single-Video Overfitting

Thresholds tuned on one video may fail on others:
- Test on multiple videos with varying conditions
- Use relative thresholds based on video statistics (e.g., mean + 2*std)
- Document assumptions about video characteristics

### Pitfall 5: Incomplete Heredoc/Script Writes

When writing analysis scripts via heredoc or Write tool:
- Verify the complete script was written (check for truncation)
- Test syntax before running (e.g., `python -m py_compile script.py`)
- Watch for missing spaces in string concatenation

## Motion Detection Approaches

### Approach 1: Frame Differencing

Best for: Static camera, moving subject against stationary background

```python
def frame_difference(frame1, frame2, threshold=25):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    return thresh
```

### Approach 2: Background Subtraction

Best for: Longer videos, gradual lighting changes

```python
# MOG2 handles lighting changes better
bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500, varThreshold=16, detectShadows=True
)

# KNN for more stable backgrounds
bg_subtractor = cv2.createBackgroundSubtractorKNN(
    history=500, dist2Threshold=400.0, detectShadows=True
)
```

### Approach 3: Optical Flow

Best for: Tracking motion direction and magnitude

```python
def compute_optical_flow(prev_gray, curr_gray):
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None,
        pyr_scale=0.5, levels=3, winsize=15,
        iterations=3, poly_n=5, poly_sigma=1.2, flags=0
    )
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    return magnitude, angle
```

## Event Detection Pattern

For detecting specific events (e.g., takeoff, landing, collisions):

```python
def detect_event(frame_data, event_type='takeoff'):
    """
    Detect event using multiple signals for robustness.

    Returns: frame_number, confidence_score, supporting_evidence
    """
    candidates = []

    for i, data in enumerate(frame_data):
        signals = {
            'y_derivative': compute_y_velocity(frame_data, i),
            'motion_spike': data['motion'] > motion_threshold,
            'position_threshold': data['y'] < y_threshold,
            'acceleration': compute_acceleration(frame_data, i)
        }

        # Require multiple confirming signals
        confidence = sum(signals.values()) / len(signals)
        if confidence > 0.6:
            candidates.append({
                'frame': data['frame'],
                'confidence': confidence,
                'signals': signals
            })

    # Return highest confidence candidate
    return max(candidates, key=lambda c: c['confidence'])
```

## Output Requirements

When producing analysis results:

1. **Include confidence scores**: Indicate certainty of detections
2. **Provide frame ranges**: For events, give a range (e.g., "takeoff: 93-97, most likely 95")
3. **Export debug artifacts**: Save annotated frames for human verification
4. **Document assumptions**: List what conditions the analysis assumes
5. **Handle errors gracefully**: Write partial results if processing fails mid-video

```python
result = {
    'takeoff_frame': int(takeoff),
    'takeoff_confidence': 0.85,
    'takeoff_range': [93, 97],
    'landing_frame': int(landing),
    'landing_confidence': 0.92,
    'landing_range': [112, 116],
    'assumptions': [
        'First frame contains no subject',
        'Single subject in frame',
        'Camera is stationary'
    ],
    'debug_frames_exported': True
}
```
