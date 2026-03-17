---
name: ffmpeg-opencv-integration
description: Complete FFmpeg + OpenCV + Python integration guide for video processing pipelines. PROACTIVELY activate for: (1) FFmpeg to OpenCV frame handoff, (2) cv2.VideoCapture vs ffmpeg subprocess, (3) BGR/RGB color format conversion gotchas, (4) Frame dimension order img[y,x] vs img[x,y], (5) ffmpegcv GPU-accelerated video I/O, (6) VidGear multi-threaded streaming, (7) Decord batch video loading for ML, (8) PyAV frame-level processing, (9) Audio stream preservation with video filters, (10) Memory-efficient frame generators, (11) OpenCV + FFmpeg + Modal parallel processing, (12) Pipe frames between FFmpeg and OpenCV. Provides: Color format conversion patterns, coordinate system gotchas, library selection guide, memory management, subprocess pipe patterns, GPU-accelerated alternatives to cv2.VideoCapture. Ensures: Correct integration between FFmpeg and OpenCV without color/coordinate bugs. See also: ffmpeg-python-integration-reference for type-safe parameter mappings.
---

## Quick Reference

| Task | Best Library | Why |
|------|--------------|-----|
| Simple video read | OpenCV `cv2.VideoCapture` | Built-in, easy API |
| GPU video I/O | ffmpegcv | NVDEC/NVENC, OpenCV-compatible API |
| Multi-threaded streaming | VidGear | RTSP/RTMP, camera capture |
| ML batch loading | Decord | 2x faster than OpenCV, batch GPU decode |
| Frame-level precision | PyAV | Direct libav access, precise seeking |
| Complex filter graphs | ffmpeg-python subprocess | Full FFmpeg power |

| Color Format | Library | Conversion |
|--------------|---------|------------|
| BGR | OpenCV (cv2) | `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` |
| RGB | FFmpeg, PIL, PyAV | `cv2.cvtColor(img, cv2.COLOR_RGB2BGR)` |
| YUV | FFmpeg internal | Convert to RGB/BGR for processing |

## When to Use This Skill

Use for **FFmpeg + OpenCV combined workflows**:
- Reading video with FFmpeg, processing frames with OpenCV
- Piping frames between FFmpeg and OpenCV processes
- GPU-accelerated video I/O with OpenCV processing
- Fixing color format mismatches (BGR vs RGB)
- Memory-efficient processing of large videos
- Parallel frame processing on Modal.com

---

# FFmpeg + OpenCV Integration Guide

Complete guide to combining FFmpeg's video I/O power with OpenCV's image processing capabilities.

## Critical Gotchas (Must Know!)

### 1. Color Format Mismatch (BGR vs RGB)

**The #1 source of bugs in FFmpeg + OpenCV pipelines.**

```python
import cv2
import numpy as np

# OpenCV uses BGR by default
img_bgr = cv2.imread("image.jpg")  # BGR format!

# FFmpeg outputs RGB by default (in most configs)
# PyAV outputs RGB
# PIL/Pillow uses RGB

# WRONG: Using FFmpeg RGB output directly with OpenCV
# Colors will be swapped (red becomes blue)

# CORRECT: Always convert explicitly
def bgr_to_rgb(frame: np.ndarray) -> np.ndarray:
    """Convert OpenCV BGR to RGB for FFmpeg/PIL/ML."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def rgb_to_bgr(frame: np.ndarray) -> np.ndarray:
    """Convert RGB (FFmpeg/PyAV/PIL) to OpenCV BGR."""
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

# When piping FFmpeg to OpenCV:
def read_ffmpeg_frame_for_opencv(raw_bytes: bytes, width: int, height: int) -> np.ndarray:
    """Read FFmpeg raw frame and convert to OpenCV BGR."""
    # FFmpeg rawvideo is RGB by default
    frame_rgb = np.frombuffer(raw_bytes, dtype=np.uint8).reshape(height, width, 3)
    # Convert to BGR for OpenCV
    frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
    return frame_bgr
```

### 2. Frame Dimension Order (y, x) vs (x, y)

**OpenCV and NumPy use (row, col) = (y, x), not (x, y).**

```python
import cv2
import numpy as np

img = cv2.imread("image.jpg")
print(img.shape)  # (height, width, channels) = (y, x, c)

# WRONG: Accessing pixel at x=100, y=200
# pixel = img[100, 200]  # This gets row=100, col=200 = (y=100, x=200)

# CORRECT: Accessing pixel at x=100, y=200
pixel = img[200, 100]  # row=200 (y), col=100 (x)

# WRONG: Creating image with width=1920, height=1080
# img = np.zeros((1920, 1080, 3))  # Creates 1920 rows × 1080 cols!

# CORRECT: Creating 1920×1080 image
img = np.zeros((1080, 1920, 3), dtype=np.uint8)  # (height, width, channels)

# When reading frame dimensions:
cap = cv2.VideoCapture("video.mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # x dimension
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # y dimension

# NumPy array will be: frame.shape = (height, width, 3)
```

### 3. Audio Stream Loss with FFmpeg Filters

**Video filters drop audio by default in ffmpeg-python.**

```python
import ffmpeg

# WRONG: Audio is silently dropped
(
    ffmpeg
    .input('input.mp4')
    .filter('scale', 1280, 720)
    .output('output.mp4')
    .run()
)

# CORRECT: Explicitly handle both streams
input_file = ffmpeg.input('input.mp4')
video = input_file.video.filter('scale', 1280, 720)
audio = input_file.audio  # Preserve audio stream
(
    ffmpeg
    .output(video, audio, 'output.mp4')
    .overwrite_output()
    .run()
)

# CORRECT: For complex pipelines
input_file = ffmpeg.input('input.mp4')
video = (
    input_file.video
    .filter('scale', 1280, 720)
    .filter('fps', fps=30)
)
audio = input_file.audio.filter('loudnorm')
ffmpeg.output(video, audio, 'output.mp4', vcodec='libx264', acodec='aac').run()
```

### 4. Memory Leaks with VideoCapture

**Always release VideoCapture and destroy windows.**

```python
import cv2

# WRONG: No cleanup
cap = cv2.VideoCapture("video.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Frame", frame)
# Memory leak!

# CORRECT: Use try/finally
cap = cv2.VideoCapture("video.mp4")
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()

# CORRECT: Use context manager pattern
class VideoReader:
    def __init__(self, path: str):
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise IOError(f"Cannot open video: {path}")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cap.release()

    def frames(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            yield frame

# Usage
with VideoReader("video.mp4") as reader:
    for frame in reader.frames():
        # Process frame...
        pass
```

---

## Pattern 1: Pipe FFmpeg to OpenCV

For complex input handling (network streams, unusual formats), use FFmpeg to decode and pipe raw frames to OpenCV.

```python
import subprocess
import numpy as np
import cv2

def ffmpeg_to_opencv_pipe(input_path: str, width: int, height: int):
    """Read video with FFmpeg, process frames with OpenCV."""

    # FFmpeg command to output raw BGR24 frames
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',  # BGR for OpenCV!
        '-s', f'{width}x{height}',
        '-'  # Output to stdout
    ]

    # Start FFmpeg process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,  # Suppress FFmpeg logs
        bufsize=10**8  # Large buffer for video
    )

    frame_size = width * height * 3

    try:
        while True:
            raw_frame = process.stdout.read(frame_size)
            if len(raw_frame) != frame_size:
                break

            # Convert to NumPy array (already BGR for OpenCV)
            frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape(height, width, 3)

            # Process with OpenCV
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)

            yield edges
    finally:
        process.stdout.close()
        process.wait()

# Get video dimensions first
def get_video_dimensions(path: str) -> tuple[int, int]:
    """Get video width and height using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    width, height = map(int, result.stdout.strip().split(','))
    return width, height

# Usage
width, height = get_video_dimensions("input.mp4")
for edge_frame in ffmpeg_to_opencv_pipe("input.mp4", width, height):
    cv2.imshow("Edges", edge_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

---

## Pattern 2: OpenCV to FFmpeg Pipe

Process frames with OpenCV, encode output with FFmpeg.

```python
import subprocess
import numpy as np
import cv2

def opencv_to_ffmpeg_pipe(
    input_path: str,
    output_path: str,
    process_frame: callable,
    fps: float = 30.0
):
    """Process video frames with OpenCV, encode with FFmpeg."""

    # Open input with OpenCV
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # FFmpeg command to receive raw BGR frames
    cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{width}x{height}',
        '-pix_fmt', 'bgr24',  # OpenCV BGR format
        '-r', str(fps),
        '-i', '-',  # Read from stdin
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        output_path
    ]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process frame with user function
            processed = process_frame(frame)

            # Write to FFmpeg
            process.stdin.write(processed.tobytes())
    finally:
        cap.release()
        process.stdin.close()
        process.wait()

# Example usage
def add_blur(frame: np.ndarray) -> np.ndarray:
    return cv2.GaussianBlur(frame, (15, 15), 0)

opencv_to_ffmpeg_pipe("input.mp4", "blurred.mp4", add_blur)
```

---

## Pattern 3: Bidirectional Pipe (FFmpeg ↔ OpenCV ↔ FFmpeg)

For full control over input/output codecs while processing with OpenCV.

```python
import subprocess
import numpy as np
import cv2
from concurrent.futures import ThreadPoolExecutor

def ffmpeg_opencv_ffmpeg_pipeline(
    input_path: str,
    output_path: str,
    process_frame: callable,
    preserve_audio: bool = True
):
    """Complete pipeline: FFmpeg decode → OpenCV process → FFmpeg encode."""

    # Get video info
    probe_cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,r_frame_rate',
        '-of', 'csv=p=0',
        input_path
    ]
    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
    parts = probe_result.stdout.strip().split(',')
    width, height = int(parts[0]), int(parts[1])
    fps_parts = parts[2].split('/')
    fps = int(fps_parts[0]) / int(fps_parts[1])

    # FFmpeg decode command (output BGR24 for OpenCV)
    decode_cmd = [
        'ffmpeg',
        '-i', input_path,
        '-f', 'rawvideo',
        '-pix_fmt', 'bgr24',
        '-'
    ]

    # FFmpeg encode command
    encode_cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-s', f'{width}x{height}',
        '-pix_fmt', 'bgr24',
        '-r', str(fps),
        '-i', '-',
    ]

    # Add audio from original file if preserving
    if preserve_audio:
        encode_cmd.extend(['-i', input_path, '-map', '0:v', '-map', '1:a', '-c:a', 'copy'])

    encode_cmd.extend([
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-pix_fmt', 'yuv420p',
        output_path
    ])

    # Start processes
    decoder = subprocess.Popen(
        decode_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    encoder = subprocess.Popen(
        encode_cmd,
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

    frame_size = width * height * 3

    try:
        while True:
            raw_frame = decoder.stdout.read(frame_size)
            if len(raw_frame) != frame_size:
                break

            # Convert to NumPy, process, convert back
            frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape(height, width, 3)
            processed = process_frame(frame)
            encoder.stdin.write(processed.tobytes())
    finally:
        decoder.stdout.close()
        decoder.wait()
        encoder.stdin.close()
        encoder.wait()

# Usage
def detect_edges(frame: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    # Convert back to BGR for encoding
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

ffmpeg_opencv_ffmpeg_pipeline("input.mp4", "edges.mp4", detect_edges)
```

---

## ffmpegcv: GPU-Accelerated Video I/O

**ffmpegcv** provides an OpenCV-compatible API with GPU acceleration (NVDEC/NVENC).

### Installation

```bash
pip install ffmpegcv
```

### Basic Usage

```python
import ffmpegcv

# Read video (uses NVDEC if available)
cap = ffmpegcv.VideoCapture("video.mp4")

# CPU-only reading
cap = ffmpegcv.VideoCapture("video.mp4", gpu=-1)

# Force GPU 0
cap = ffmpegcv.VideoCapture("video.mp4", gpu=0)

# Read frames (returns BGR like OpenCV!)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # frame is BGR NumPy array, just like cv2.VideoCapture
    print(frame.shape)  # (height, width, 3)

cap.release()
```

### GPU Video Writing

```python
import ffmpegcv
import cv2
import numpy as np

# GPU-accelerated writing with NVENC
writer = ffmpegcv.VideoWriter(
    "output.mp4",
    codec="h264_nvenc",  # NVIDIA GPU encoding
    fps=30,
    frameSize=(1920, 1080)
)

# Write frames
for i in range(300):
    frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    writer.write(frame)  # Accepts BGR like OpenCV

writer.release()
```

### Read Specific Range

```python
import ffmpegcv

# Read frames 100-200 only (efficient seeking)
cap = ffmpegcv.VideoCapture("video.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)

for i in range(100):
    ret, frame = cap.read()
    if not ret:
        break
    # Process frame...

cap.release()
```

### Integration with OpenCV Processing

```python
import ffmpegcv
import cv2
import numpy as np

def process_with_ffmpegcv(input_path: str, output_path: str):
    """GPU decode → OpenCV process → GPU encode."""

    # GPU reader
    cap = ffmpegcv.VideoCapture(input_path, gpu=0)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # GPU writer
    writer = ffmpegcv.VideoWriter(
        output_path,
        codec="h264_nvenc",
        fps=fps,
        frameSize=(width, height)
    )

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # OpenCV processing (CPU)
            processed = cv2.GaussianBlur(frame, (5, 5), 0)
            processed = cv2.Canny(processed, 100, 200)
            processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

            writer.write(processed)
    finally:
        cap.release()
        writer.release()

process_with_ffmpegcv("input.mp4", "processed.mp4")
```

---

## VidGear: Multi-Threaded Video I/O

**VidGear** provides multi-threaded, high-performance video streaming with OpenCV integration.

### Installation

```bash
pip install vidgear[core]
```

### CamGear: High-Performance Capture

```python
from vidgear.gears import CamGear
import cv2

# Multi-threaded video reading (faster than cv2.VideoCapture)
stream = CamGear(source="video.mp4").start()

while True:
    frame = stream.read()
    if frame is None:
        break

    # frame is BGR like OpenCV
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stream.stop()
cv2.destroyAllWindows()
```

### RTSP/Network Streaming

```python
from vidgear.gears import CamGear

# RTSP stream capture
options = {
    "THREADED_QUEUE_MODE": True,
    "CAP_PROP_FRAME_WIDTH": 1920,
    "CAP_PROP_FRAME_HEIGHT": 1080,
}

stream = CamGear(
    source="rtsp://192.168.1.100:554/stream",
    stream_mode=True,
    **options
).start()

while True:
    frame = stream.read()
    if frame is None:
        break
    # Process frame...

stream.stop()
```

### WriteGear: FFmpeg-Backed Writing

```python
from vidgear.gears import WriteGear
import cv2
import numpy as np

# High-performance writing with FFmpeg backend
output_params = {
    "-vcodec": "libx264",
    "-crf": 23,
    "-preset": "fast",
    "-pix_fmt": "yuv420p",
}

writer = WriteGear(output="output.mp4", **output_params)

# Generate and write frames
for i in range(300):
    frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    writer.write(frame)

writer.close()
```

### GPU-Accelerated WriteGear

```python
from vidgear.gears import WriteGear

# NVENC GPU encoding
output_params = {
    "-vcodec": "h264_nvenc",
    "-preset": "p4",
    "-rc": "vbr",
    "-cq": 23,
    "-pix_fmt": "yuv420p",
}

writer = WriteGear(output="output.mp4", **output_params)
# ... write frames ...
writer.close()
```

---

## Decord: ML Batch Loading

**Decord** provides 2x faster video loading than OpenCV, optimized for deep learning.

### Installation

```bash
pip install decord
```

### Basic Usage

```python
from decord import VideoReader, cpu, gpu
import numpy as np

# CPU video reader
vr = VideoReader("video.mp4", ctx=cpu(0))

# Get video info
print(f"Total frames: {len(vr)}")
print(f"FPS: {vr.get_avg_fps()}")

# Read single frame (returns RGB!)
frame = vr[0]
print(frame.shape)  # (height, width, 3) - RGB format!

# CRITICAL: Decord returns RGB, not BGR
# Convert for OpenCV:
frame_bgr = frame[:, :, ::-1]  # RGB to BGR
# Or use cv2:
import cv2
frame_bgr = cv2.cvtColor(frame.asnumpy(), cv2.COLOR_RGB2BGR)
```

### Batch Loading for ML

```python
from decord import VideoReader, cpu
import numpy as np

vr = VideoReader("video.mp4", ctx=cpu(0))

# Load batch of frames (very efficient!)
frame_indices = [0, 10, 20, 30, 40]
batch = vr.get_batch(frame_indices)
print(batch.shape)  # (5, height, width, 3) - batch of RGB frames

# Load every 10th frame
all_frames = vr.get_batch(range(0, len(vr), 10))

# Convert batch to PyTorch tensor
import torch
tensor = torch.from_numpy(batch.asnumpy())
tensor = tensor.permute(0, 3, 1, 2)  # NHWC → NCHW for PyTorch
tensor = tensor.float() / 255.0  # Normalize
```

### GPU Decoding

```python
from decord import VideoReader, gpu

# GPU video reader (NVDEC)
vr = VideoReader("video.mp4", ctx=gpu(0))

# Batch read with GPU
frames = vr.get_batch([0, 1, 2, 3, 4])
# frames is on GPU, can be used directly with PyTorch
```

### Decord with OpenCV Processing

```python
from decord import VideoReader, cpu
import cv2
import numpy as np

def process_video_with_decord(path: str, batch_size: int = 32):
    """Efficient batch processing with Decord and OpenCV."""

    vr = VideoReader(path, ctx=cpu(0))
    total_frames = len(vr)

    results = []
    for start in range(0, total_frames, batch_size):
        end = min(start + batch_size, total_frames)
        batch = vr.get_batch(range(start, end))

        for frame_rgb in batch.asnumpy():
            # Convert RGB (Decord) to BGR (OpenCV)
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

            # OpenCV processing
            gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)

            results.append(edges)

    return results
```

---

## PyAV: Frame-Level Precision

**PyAV** provides direct access to libav for precise frame-level control.

### Installation

```bash
pip install av
```

### Basic Usage

```python
import av
import numpy as np

# Open video
container = av.open("video.mp4")

for frame in container.decode(video=0):
    # frame.to_ndarray() returns RGB by default!
    img_rgb = frame.to_ndarray(format="rgb24")

    # Convert to BGR for OpenCV
    import cv2
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    print(img_bgr.shape)  # (height, width, 3)

container.close()
```

### Precise Seeking

```python
import av

container = av.open("video.mp4")
stream = container.streams.video[0]

# Get frame at timestamp
target_pts = 10.0  # 10 seconds
container.seek(int(target_pts * av.time_base))

for frame in container.decode(video=0):
    # Process frame at approximately 10 seconds
    img = frame.to_ndarray(format="rgb24")
    break

container.close()
```

### Efficient Frame Extraction

```python
import av
import numpy as np
from typing import Generator

def extract_frames_pyav(
    path: str,
    fps: float = None
) -> Generator[np.ndarray, None, None]:
    """Extract frames with PyAV (yields BGR for OpenCV)."""

    container = av.open(path)
    stream = container.streams.video[0]

    # Set frame rate if specified
    if fps:
        stream.codec_context.framerate = fps

    for frame in container.decode(stream):
        # Get RGB array
        img_rgb = frame.to_ndarray(format="rgb24")
        # Convert to BGR for OpenCV
        img_bgr = img_rgb[:, :, ::-1]
        yield img_bgr

    container.close()

# Usage
for frame_bgr in extract_frames_pyav("video.mp4"):
    # Direct OpenCV processing
    edges = cv2.Canny(frame_bgr, 100, 200)
```

### Write Video with PyAV

```python
import av
import numpy as np

def write_video_pyav(frames: list, output_path: str, fps: float = 30.0):
    """Write frames to video with PyAV."""

    height, width = frames[0].shape[:2]

    container = av.open(output_path, mode='w')
    stream = container.add_stream('libx264', rate=fps)
    stream.width = width
    stream.height = height
    stream.pix_fmt = 'yuv420p'
    stream.options = {'crf': '23', 'preset': 'fast'}

    for frame_bgr in frames:
        # Convert BGR to RGB for PyAV
        frame_rgb = frame_bgr[:, :, ::-1]

        # Create VideoFrame
        av_frame = av.VideoFrame.from_ndarray(frame_rgb, format='rgb24')

        # Encode
        for packet in stream.encode(av_frame):
            container.mux(packet)

    # Flush encoder
    for packet in stream.encode():
        container.mux(packet)

    container.close()
```

---

## Modal.com Integration: FFmpeg + OpenCV + GPU

Deploy FFmpeg + OpenCV pipelines on Modal's serverless infrastructure.

### Image Configuration

```python
import modal

# Complete image with FFmpeg, OpenCV, and GPU libraries
video_image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install(
        "ffmpeg",           # FFmpeg CLI
        "libsm6",           # OpenCV dependencies
        "libxext6",
        "libgl1",
        "libglib2.0-0",
    )
    .pip_install(
        "opencv-python-headless",  # No GUI for server
        "ffmpeg-python",
        "numpy",
        "Pillow",
    )
)

# GPU image with additional libraries
gpu_video_image = (
    modal.Image.debian_slim(python_version="3.12")
    .apt_install("ffmpeg", "libsm6", "libxext6", "libgl1", "libglib2.0-0")
    .pip_install(
        "opencv-python-headless",
        "ffmpeg-python",
        "numpy",
        "torch",
        "decord",
        "ffmpegcv",
    )
)

app = modal.App("ffmpeg-opencv-pipeline", image=video_image)
```

### Basic Frame Processing on Modal

```python
import modal

app = modal.App("opencv-processing")

image = (
    modal.Image.debian_slim()
    .apt_install("ffmpeg", "libsm6", "libxext6", "libgl1")
    .pip_install("opencv-python-headless", "numpy")
)

@app.function(image=image)
def process_frame(frame_bytes: bytes) -> bytes:
    """Process single frame with OpenCV on Modal."""
    import cv2
    import numpy as np

    # Decode image (PNG or JPEG)
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # BGR

    # OpenCV processing
    processed = cv2.GaussianBlur(frame, (15, 15), 0)

    # Encode back to PNG
    _, encoded = cv2.imencode('.png', processed)
    return encoded.tobytes()

@app.function(image=image, timeout=600)
def extract_and_process(video_bytes: bytes) -> list[bytes]:
    """Extract frames with FFmpeg, process with OpenCV."""
    import subprocess
    import tempfile
    from pathlib import Path
    import cv2
    import numpy as np

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.mp4"
        input_path.write_bytes(video_bytes)

        # Extract frames with FFmpeg
        subprocess.run([
            "ffmpeg", "-i", str(input_path),
            "-vf", "fps=1",  # 1 frame per second
            f"{tmpdir}/frame_%04d.png"
        ], check=True, capture_output=True)

        # Process each frame with OpenCV
        results = []
        for frame_path in sorted(Path(tmpdir).glob("frame_*.png")):
            frame = cv2.imread(str(frame_path))

            # Apply edge detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)

            # Encode result
            _, encoded = cv2.imencode('.png', edges)
            results.append(encoded.tobytes())

        return results

@app.local_entrypoint()
def main():
    video_bytes = Path("input.mp4").read_bytes()
    processed_frames = extract_and_process.remote(video_bytes)

    for i, frame_bytes in enumerate(processed_frames):
        Path(f"output/frame_{i:04d}.png").write_bytes(frame_bytes)
```

### Parallel Frame Processing with map()

```python
import modal
from pathlib import Path

app = modal.App("parallel-opencv")

image = (
    modal.Image.debian_slim()
    .apt_install("ffmpeg", "libsm6", "libxext6", "libgl1")
    .pip_install("opencv-python-headless", "numpy")
)

@app.function(image=image)
def extract_frames(video_bytes: bytes) -> list[bytes]:
    """Extract all frames from video."""
    import subprocess
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.mp4"
        input_path.write_bytes(video_bytes)

        subprocess.run([
            "ffmpeg", "-i", str(input_path),
            "-vsync", "0",
            f"{tmpdir}/frame_%06d.png"
        ], check=True, capture_output=True)

        frames = []
        for path in sorted(Path(tmpdir).glob("frame_*.png")):
            frames.append(path.read_bytes())

        return frames

@app.function(image=image)
def process_single_frame(frame_data: tuple[int, bytes]) -> tuple[int, bytes]:
    """Process a single frame."""
    import cv2
    import numpy as np

    frame_idx, frame_bytes = frame_data

    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Heavy OpenCV processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    dilated = cv2.dilate(edges, None, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on original frame
    result = frame.copy()
    cv2.drawContours(result, contours, -1, (0, 255, 0), 2)

    _, encoded = cv2.imencode('.png', result)
    return frame_idx, encoded.tobytes()

@app.function(image=image, timeout=600)
def combine_frames(processed_frames: list[tuple[int, bytes]], fps: float) -> bytes:
    """Combine processed frames back into video."""
    import subprocess
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        # Sort by frame index and write
        for idx, frame_bytes in sorted(processed_frames):
            path = Path(tmpdir) / f"frame_{idx:06d}.png"
            path.write_bytes(frame_bytes)

        output_path = Path(tmpdir) / "output.mp4"

        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", f"{tmpdir}/frame_%06d.png",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ], check=True, capture_output=True)

        return output_path.read_bytes()

@app.local_entrypoint()
def main():
    video_bytes = Path("input.mp4").read_bytes()

    # Extract frames (single container)
    frames = extract_frames.remote(video_bytes)
    print(f"Extracted {len(frames)} frames")

    # Process frames in parallel (many containers!)
    inputs = [(i, frame) for i, frame in enumerate(frames)]
    processed = list(process_single_frame.map(inputs))
    print(f"Processed {len(processed)} frames")

    # Combine back into video
    output = combine_frames.remote(processed, fps=30.0)
    Path("output.mp4").write_bytes(output)
    print("Done!")
```

### GPU-Accelerated Pipeline with ffmpegcv

```python
import modal

app = modal.App("gpu-video-pipeline")

# GPU image with ffmpegcv
gpu_image = (
    modal.Image.from_registry("nvidia/cuda:12.4.0-runtime-ubuntu22.04", add_python="3.12")
    .apt_install("ffmpeg", "libsm6", "libxext6", "libgl1", "libglib2.0-0")
    .pip_install("opencv-python-headless", "numpy", "ffmpegcv")
)

@app.function(image=gpu_image, gpu="T4")
def gpu_video_processing(video_bytes: bytes) -> bytes:
    """GPU-accelerated video processing with ffmpegcv."""
    import cv2
    import numpy as np
    import ffmpegcv
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.mp4"
        output_path = Path(tmpdir) / "output.mp4"
        input_path.write_bytes(video_bytes)

        # GPU reader (NVDEC)
        cap = ffmpegcv.VideoCapture(str(input_path), gpu=0)
        fps = cap.fps
        width = int(cap.width)
        height = int(cap.height)

        # GPU writer (NVENC)
        writer = ffmpegcv.VideoWriter(
            str(output_path),
            codec="h264_nvenc",
            fps=fps,
            frameSize=(width, height)
        )

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # OpenCV processing (CPU - can't avoid this)
                processed = cv2.bilateralFilter(frame, 9, 75, 75)

                writer.write(processed)
        finally:
            cap.release()
            writer.release()

        return output_path.read_bytes()

@app.local_entrypoint()
def main():
    video = Path("input.mp4").read_bytes()
    result = gpu_video_processing.remote(video)
    Path("output.mp4").write_bytes(result)
```

---

## Common Patterns Summary

### Color Conversion Cheat Sheet

```python
import cv2
import numpy as np

# OpenCV BGR → RGB (for FFmpeg, PIL, PyTorch)
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
rgb = bgr[:, :, ::-1]  # Faster, pure NumPy

# RGB → BGR (for OpenCV from FFmpeg, PyAV, Decord)
bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
bgr = rgb[:, :, ::-1]  # Faster

# Grayscale
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
bgr_from_gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

# HSV (for color filtering)
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
```

### Library Selection Decision Tree

```
Need video I/O?
├── Simple local file?
│   └── cv2.VideoCapture (built-in, easy)
├── Need GPU acceleration?
│   └── ffmpegcv (NVDEC/NVENC, OpenCV-compatible)
├── Network streaming (RTSP/RTMP)?
│   └── VidGear CamGear (multi-threaded)
├── ML batch training?
│   └── Decord (2x faster, batch GPU decode)
├── Frame-level precision/seeking?
│   └── PyAV (direct libav access)
└── Complex filters/formats?
    └── FFmpeg subprocess with pipes
```

### Memory-Efficient Generators

```python
def frame_generator(path: str, batch_size: int = 1):
    """Memory-efficient frame generator."""
    cap = cv2.VideoCapture(path)
    try:
        batch = []
        while True:
            ret, frame = cap.read()
            if not ret:
                if batch:
                    yield batch
                break
            batch.append(frame)
            if len(batch) == batch_size:
                yield batch
                batch = []
    finally:
        cap.release()

# Usage - never loads entire video into memory
for batch in frame_generator("large_video.mp4", batch_size=32):
    # Process batch of 32 frames
    pass
```

---

## Related Skills

- **`ffmpeg-python-integration-reference`** - Type-safe Python-FFmpeg parameter mappings, color conversions, time units
- `ffmpeg-fundamentals-2025` - Core FFmpeg operations
- `ffmpeg-captions-subtitles` - Subtitle processing with Python

## References

- [OpenCV Documentation](https://docs.opencv.org/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [ffmpegcv GitHub](https://github.com/chenxinfeng4/ffmpegcv)
- [VidGear Documentation](https://abhitronix.github.io/vidgear/)
- [Decord GitHub](https://github.com/dmlc/decord)
- [PyAV Documentation](https://pyav.org/docs/stable/)
- [Modal.com Documentation](https://modal.com/docs)
