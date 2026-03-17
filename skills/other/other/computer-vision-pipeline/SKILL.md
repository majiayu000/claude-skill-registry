---
name: computer-vision-pipeline
description: Build production computer vision pipelines for object detection, tracking, and video analysis. Handles drone footage, wildlife monitoring, and real-time detection. Supports YOLO, Detectron2, TensorFlow, PyTorch. Use for archaeological surveys, conservation, security. Activate on "object detection", "video analysis", "YOLO", "tracking", "drone footage". NOT for simple image filters, photo editing, or face recognition APIs.
allowed-tools: Read,Write,Edit,Bash(python*,pip*,ffmpeg*)
---

# Computer Vision Pipeline

Expert in building production-ready computer vision systems for object detection, tracking, and video analysis.

## When to Use

✅ **Use for**:
- Drone footage analysis (archaeological surveys, conservation)
- Wildlife monitoring and tracking
- Real-time object detection systems
- Video preprocessing and analysis
- Custom model training and inference
- Multi-object tracking (MOT)

❌ **NOT for**:
- Simple image filters (use Pillow/PIL)
- Photo editing (use Photoshop/GIMP)
- Face recognition APIs (use AWS Rekognition)
- Basic OCR (use Tesseract)

---

## Technology Selection

### Object Detection Models

| Model | Speed (FPS) | Accuracy (mAP) | Use Case |
|-------|-------------|----------------|----------|
| YOLOv8 | 140 | 53.9% | Real-time detection |
| Detectron2 | 25 | 58.7% | High accuracy, research |
| EfficientDet | 35 | 55.1% | Mobile deployment |
| Faster R-CNN | 10 | 42.0% | Legacy systems |

**Timeline**:
- 2015: Faster R-CNN (two-stage detection)
- 2016: YOLO v1 (one-stage, real-time)
- 2020: YOLOv5 (PyTorch, production-ready)
- 2023: YOLOv8 (state-of-the-art)
- 2024: YOLOv8 is industry standard for real-time

**Decision tree**:
```
Need real-time (&gt;30 FPS)? → YOLOv8
Need highest accuracy? → Detectron2 Mask R-CNN
Need mobile deployment? → YOLOv8-nano or EfficientDet
Need instance segmentation? → Detectron2 or YOLOv8-seg
Need custom objects? → Fine-tune YOLOv8
```

---

## Common Anti-Patterns

### Anti-Pattern 1: Not Preprocessing Frames Before Detection

**Novice thinking**: "Just run detection on raw video frames"

**Problem**: Poor detection accuracy, wasted GPU cycles.

**Wrong approach**:
```python
# ❌ No preprocessing - poor results
import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('drone_footage.mp4')

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Raw frame detection - no normalization, no resizing
    results = model(frame)
    # Poor accuracy, slow inference
```

**Why wrong**:
- Video resolution too high (4K = 8.3 megapixels per frame)
- No normalization (pixel values 0-255 instead of 0-1)
- Aspect ratio not maintained
- GPU memory overflow on high-res frames

**Correct approach**:
```python
# ✅ Proper preprocessing pipeline
import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('drone_footage.mp4')

# Model expects 640x640 input
TARGET_SIZE = 640

def preprocess_frame(frame):
    # Resize while maintaining aspect ratio
    h, w = frame.shape[:2]
    scale = TARGET_SIZE / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)

    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Pad to square
    pad_w = (TARGET_SIZE - new_w) // 2
    pad_h = (TARGET_SIZE - new_h) // 2

    padded = cv2.copyMakeBorder(
        resized,
        pad_h, TARGET_SIZE - new_h - pad_h,
        pad_w, TARGET_SIZE - new_w - pad_w,
        cv2.BORDER_CONSTANT,
        value=(114, 114, 114)  # Gray padding
    )

    # Normalize to 0-1 (if model expects it)
    # normalized = padded.astype(np.float32) / 255.0

    return padded, scale

while True:
    ret, frame = video.read()
    if not ret:
        break

    preprocessed, scale = preprocess_frame(frame)
    results = model(preprocessed)

    # Scale bounding boxes back to original coordinates
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = x1/scale, y1/scale, x2/scale, y2/scale
```

**Performance comparison**:
- Raw 4K frames: 5 FPS, 72% mAP
- Preprocessed 640x640: 45 FPS, 89% mAP

**Timeline context**:
- 2015: Manual preprocessing required
- 2020: YOLOv5 added auto-resize
- 2023: YOLOv8 has smart preprocessing but explicit control is better

---

### Anti-Pattern 2: Processing Every Frame in Video

**Novice thinking**: "Run detection on every single frame"

**Problem**: 99% of frames are redundant, wasting compute.

**Wrong approach**:
```python
# ❌ Process every frame (30 FPS video = 1800 frames/min)
import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('drone_footage.mp4')

detections = []

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Run detection on EVERY frame
    results = model(frame)
    detections.append(results)

# 10-minute video = 18,000 inferences (15 minutes on GPU)
```

**Why wrong**:
- Adjacent frames are nearly identical
- Wasting 95% of compute on duplicate work
- Slow processing time
- Massive storage for results

**Correct approach 1**: Frame sampling
```python
# ✅ Sample every Nth frame
import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('drone_footage.mp4')

SAMPLE_RATE = 30  # Process 1 frame per second (if 30 FPS video)

frame_count = 0
detections = []

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_count += 1

    # Only process every 30th frame
    if frame_count % SAMPLE_RATE == 0:
        results = model(frame)
        detections.append({
            'frame': frame_count,
            'timestamp': frame_count / 30.0,
            'results': results
        })

# 10-minute video = 600 inferences (30 seconds on GPU)
```

**Correct approach 2**: Adaptive sampling with scene change detection
```python
# ✅ Only process when scene changes significantly
import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('drone_footage.mp4')

def scene_changed(prev_frame, curr_frame, threshold=0.3):
    """Detect scene change using histogram comparison"""
    if prev_frame is None:
        return True

    # Convert to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    # Calculate histograms
    prev_hist = cv2.calcHist([prev_gray], [0], None, [256], [0, 256])
    curr_hist = cv2.calcHist([curr_gray], [0], None, [256], [0, 256])

    # Compare histograms
    correlation = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_CORREL)

    return correlation < (1 - threshold)

prev_frame = None
detections = []

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Only run detection if scene changed
    if scene_changed(prev_frame, frame):
        results = model(frame)
        detections.append(results)

    prev_frame = frame.copy()

# Adapts to video content - static shots skip frames, action scenes process more
```

**Savings**:
- Every frame: 18,000 inferences
- Sample 1 FPS: 600 inferences (97% reduction)
- Adaptive: ~1,200 inferences (93% reduction)

---

### Anti-Pattern 3: Not Using Batch Inference

**Novice thinking**: "Process one image at a time"

**Problem**: GPU sits idle 80% of the time waiting for data.

**Wrong approach**:
```python
# ❌ Sequential processing - GPU underutilized
import cv2
from ultralytics import YOLO
import time

model = YOLO('yolov8n.pt')

# 100 images to process
image_paths = [f'frame_{i:04d}.jpg' for i in range(100)]

start = time.time()

for path in image_paths:
    frame = cv2.imread(path)
    results = model(frame)  # Process one at a time
    # GPU utilization: ~20%

elapsed = time.time() - start
print(f"Processed {len(image_paths)} images in {elapsed:.2f}s")
# Output: 45 seconds
```

**Why wrong**:
- GPU has to wait for CPU to load each image
- No parallelization
- GPU utilization ~20%
- Slow throughput

**Correct approach**:
```python
# ✅ Batch inference - GPU fully utilized
import cv2
from ultralytics import YOLO
import time

model = YOLO('yolov8n.pt')

image_paths = [f'frame_{i:04d}.jpg' for i in range(100)]

BATCH_SIZE = 16  # Process 16 images at once

start = time.time()

for i in range(0, len(image_paths), BATCH_SIZE):
    batch_paths = image_paths[i:i+BATCH_SIZE]

    # Load batch
    frames = [cv2.imread(path) for path in batch_paths]

    # Batch inference (single GPU call)
    results = model(frames)  # Pass list of images
    # GPU utilization: ~85%

elapsed = time.time() - start
print(f"Processed {len(image_paths)} images in {elapsed:.2f}s")
# Output: 8 seconds (5.6x faster!)
```

**Performance comparison**:
| Method | Time (100 images) | GPU Util | Throughput |
|--------|-------------------|----------|------------|
| Sequential | 45s | 20% | 2.2 img/s |
| Batch (16) | 8s | 85% | 12.5 img/s |
| Batch (32) | 6s | 92% | 16.7 img/s |

**Batch size tuning**:
```python
# Find optimal batch size for your GPU
import torch

def find_optimal_batch_size(model, image_size=(640, 640)):
    for batch_size in [1, 2, 4, 8, 16, 32, 64]:
        try:
            dummy_input = torch.randn(batch_size, 3, *image_size).cuda()

            start = time.time()
            with torch.no_grad():
                _ = model(dummy_input)
            elapsed = time.time() - start

            throughput = batch_size / elapsed
            print(f"Batch {batch_size}: {throughput:.1f} img/s")
        except RuntimeError as e:
            print(f"Batch {batch_size}: OOM (out of memory)")
            break

# Find optimal batch size before production
find_optimal_batch_size(model)
```

---

### Anti-Pattern 4: Ignoring Non-Maximum Suppression (NMS) Tuning

**Problem**: Duplicate detections, missed objects, slow post-processing.

**Wrong approach**:
```python
# ❌ Use default NMS settings for everything
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

# Default settings (iou_threshold=0.45, conf_threshold=0.25)
results = model('crowded_scene.jpg')

# Result: 50 bounding boxes, 30 are duplicates!
```

**Why wrong**:
- Default IoU=0.45 is too permissive for dense objects
- Default conf=0.25 includes low-quality detections
- No adaptation to use case

**Correct approach**:
```python
# ✅ Tune NMS for your use case
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

# Sparse objects (dolphins in ocean)
sparse_results = model(
    'ocean_footage.jpg',
    iou=0.5,    # Higher IoU = allow closer boxes
    conf=0.4    # Higher confidence = fewer false positives
)

# Dense objects (crowd, flock of birds)
dense_results = model(
    'crowded_scene.jpg',
    iou=0.3,    # Lower IoU = suppress more duplicates
    conf=0.5    # Higher confidence = filter noise
)

# High precision needed (legal evidence)
precise_results = model(
    'evidence.jpg',
    iou=0.5,
    conf=0.7,   # Very high confidence
    max_det=50  # Limit max detections
)
```

**NMS parameter guide**:
| Use Case | IoU | Conf | Max Det |
|----------|-----|------|---------|
| Sparse objects (wildlife) | 0.5 | 0.4 | 100 |
| Dense objects (crowd) | 0.3 | 0.5 | 300 |
| High precision (evidence) | 0.5 | 0.7 | 50 |
| Real-time (speed priority) | 0.45 | 0.3 | 100 |

---

### Anti-Pattern 5: No Tracking Between Frames

**Novice thinking**: "Run detection on each frame independently"

**Problem**: Can't count unique objects, track movement, or build trajectories.

**Wrong approach**:
```python
# ❌ Independent frame detection - no object identity
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('dolphins.mp4')

detections = []

while True:
    ret, frame = video.read()
    if not ret:
        break

    results = model(frame)
    detections.append(results)

# Result: Can't tell if frame 10 dolphin is same as frame 20 dolphin
# Can't count unique dolphins
# Can't track trajectories
```

**Why wrong**:
- No object identity across frames
- Can't count unique objects
- Can't analyze movement patterns
- Can't build trajectories

**Correct approach**: Use tracking (ByteTrack)
```python
# ✅ Multi-object tracking with ByteTrack
from ultralytics import YOLO
import cv2

# YOLO with tracking
model = YOLO('yolov8n.pt')
video = cv2.VideoCapture('dolphins.mp4')

# Track objects across frames
tracks = {}

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Run detection + tracking
    results = model.track(
        frame,
        persist=True,     # Maintain IDs across frames
        tracker='bytetrack.yaml'  # ByteTrack algorithm
    )

    # Each detection now has persistent ID
    for box in results[0].boxes:
        track_id = int(box.id[0])  # Unique ID across frames
        x1, y1, x2, y2 = box.xyxy[0]

        # Store trajectory
        if track_id not in tracks:
            tracks[track_id] = []

        tracks[track_id].append({
            'frame': len(tracks[track_id]),
            'bbox': (x1, y1, x2, y2),
            'conf': box.conf[0]
        })

# Now we can analyze:
print(f"Unique dolphins detected: {len(tracks)}")

# Trajectory analysis
for track_id, trajectory in tracks.items():
    if len(trajectory) > 30:  # Only long tracks
        print(f"Dolphin {track_id} appeared in {len(trajectory)} frames")
        # Calculate movement, speed, etc.
```

**Tracking benefits**:
- Count unique objects (not just detections per frame)
- Build trajectories and movement patterns
- Analyze behavior over time
- Filter out brief false positives

**Tracking algorithms**:
| Algorithm | Speed | Robustness | Occlusion Handling |
|-----------|-------|------------|---------------------|
| ByteTrack | Fast | Good | Excellent |
| SORT | Very Fast | Fair | Fair |
| DeepSORT | Medium | Excellent | Good |
| BotSORT | Medium | Excellent | Excellent |

---

## Production Checklist

```
□ Preprocess frames (resize, pad, normalize)
□ Sample frames intelligently (1 FPS or scene change detection)
□ Use batch inference (16-32 images per batch)
□ Tune NMS thresholds for your use case
□ Implement tracking if analyzing video
□ Log inference time and GPU utilization
□ Handle edge cases (empty frames, corrupted video)
□ Save results in structured format (JSON, CSV)
□ Visualize detections for debugging
□ Benchmark on representative data
```

---

## When to Use vs Avoid

| Scenario | Appropriate? |
|----------|--------------|
| Analyze drone footage for archaeology | ✅ Yes - custom object detection |
| Track wildlife in video | ✅ Yes - detection + tracking |
| Count people in crowd | ✅ Yes - dense object detection |
| Real-time security camera | ✅ Yes - YOLOv8 real-time |
| Filter vacation photos | ❌ No - use photo management apps |
| Face recognition login | ❌ No - use AWS Rekognition API |
| Read license plates | ❌ No - use specialized OCR |

---

## References

- `/references/yolo-guide.md` - YOLOv8 setup, training, inference patterns
- `/references/video-processing.md` - Frame extraction, scene detection, optimization
- `/references/tracking-algorithms.md` - ByteTrack, SORT, DeepSORT comparison

## Scripts

- `scripts/video_analyzer.py` - Extract frames, run detection, generate timeline
- `scripts/model_trainer.py` - Fine-tune YOLO on custom dataset, export weights

---

**This skill guides**: Computer vision | Object detection | Video analysis | YOLO | Tracking | Drone footage | Wildlife monitoring
