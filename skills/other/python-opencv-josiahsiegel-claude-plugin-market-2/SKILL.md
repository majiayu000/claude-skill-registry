---
name: python-opencv
description: Complete OpenCV computer vision system for Python. PROACTIVELY activate for: (1) Image loading with cv2.imread (BGR format gotcha), (2) Video capture with cv2.VideoCapture, (3) Color space conversion (BGR to RGB, HSV, grayscale), (4) Image filtering (GaussianBlur, medianBlur, bilateralFilter), (5) Edge detection (Canny), (6) Contour detection with cv2.findContours, (7) Image resizing with interpolation methods, (8) Template matching, (9) Feature detection (SIFT, ORB, AKAZE), (10) Drawing functions (rectangle, circle, text), (11) Video writing with cv2.VideoWriter, (12) Morphological operations, (13) Deep learning with cv2.dnn module, (14) GPU acceleration with cv2.cuda, (15) Coordinate system (x,y vs row,col) gotchas. Provides: Image processing patterns, video capture/writing, memory management, performance optimization, Jupyter notebook workarounds. Ensures correct BGR handling and memory-safe OpenCV usage.
---

## Quick Reference

| Function | Purpose | Gotcha |
|----------|---------|--------|
| `cv2.imread(path)` | Load image | Returns `None` if path invalid (no error!) |
| `cv2.imwrite(path, img)` | Save image | Expects BGR, not RGB |
| `cv2.cvtColor(img, code)` | Color conversion | BGR is default, not RGB |
| `cv2.VideoCapture(src)` | Video/camera input | Always check `isOpened()` and `release()` |
| `cv2.VideoWriter(...)` | Save video | Expects BGR frames, codec matters |
| `cv2.resize(img, (w, h))` | Resize image | Size is (width, height), not (height, width) |

| Coordinate System | Order | Usage |
|-------------------|-------|-------|
| NumPy indexing | `img[row, col]` = `img[y, x]` | Pixel access |
| Image shape | `(height, width, channels)` | Shape is (rows, cols, ch) |
| OpenCV functions | `(x, y)` | Drawing functions |
| Resize/ROI | `(width, height)` | Size parameters |

| Color Conversion | Code | Note |
|------------------|------|------|
| BGR to RGB | `cv2.COLOR_BGR2RGB` | For Matplotlib display |
| BGR to Gray | `cv2.COLOR_BGR2GRAY` | Single channel output |
| BGR to HSV | `cv2.COLOR_BGR2HSV` | H: 0-179, S/V: 0-255 |

| Interpolation | Best For | Speed |
|---------------|----------|-------|
| `INTER_NEAREST` | Speed, pixelated OK | Fastest |
| `INTER_LINEAR` | General purpose (default) | Fast |
| `INTER_AREA` | Downscaling | Medium |
| `INTER_CUBIC` | Upscaling quality | Slow |
| `INTER_LANCZOS4` | Best upscaling | Slowest |

## When to Use This Skill

Use for **computer vision and image processing**:
- Loading, displaying, and saving images
- Video capture from cameras or files
- Image filtering and transformations
- Edge and contour detection
- Object detection and template matching
- Feature detection and matching
- Deep learning inference with DNN module

**Related skills:**
- For NumPy arrays: see `python-fundamentals-313`
- For async processing: see `python-asyncio`
- For type hints: see `python-type-hints`

---

# OpenCV Python Complete Guide (2025)

## Overview

OpenCV (Open Source Computer Vision Library) is the most popular computer vision library. Python bindings (`opencv-python`) provide access to all functionality through NumPy arrays. OpenCV uses **BGR** color format by default, which is a critical gotcha.

## Installation

```bash
# CPU-only (most common)
pip install opencv-python

# With contrib modules (SIFT, SURF, extra features)
pip install opencv-contrib-python

# Headless (no GUI, for servers)
pip install opencv-python-headless

# Verify installation
python -c "import cv2; print(cv2.__version__)"
```

## Critical Gotchas

### 1. BGR vs RGB Color Format

**The #1 source of OpenCV bugs.** OpenCV uses BGR, not RGB.

```python
import cv2
import numpy as np
from matplotlib import pyplot as plt

# OpenCV reads images in BGR format
img_bgr = cv2.imread("image.jpg")  # BGR!

# WRONG: Display BGR directly with Matplotlib
# plt.imshow(img_bgr)  # Colors will be wrong!

# CORRECT: Convert to RGB for Matplotlib
img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.show()

# CORRECT: Save with OpenCV (expects BGR)
cv2.imwrite("output.jpg", img_bgr)  # Correct colors

# WRONG: Save RGB with OpenCV
# cv2.imwrite("output.jpg", img_rgb)  # Colors will be wrong!
```

**PIL/Pillow Integration:**

```python
from PIL import Image
import cv2
import numpy as np

# PIL uses RGB, OpenCV uses BGR
pil_image = Image.open("image.jpg")  # RGB
cv_image = np.array(pil_image)       # Still RGB!
cv_image_bgr = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)  # Now BGR

# Going back to PIL
cv_result = cv2.GaussianBlur(cv_image_bgr, (5, 5), 0)
cv_result_rgb = cv2.cvtColor(cv_result, cv2.COLOR_BGR2RGB)
pil_result = Image.fromarray(cv_result_rgb)
```

### 2. Coordinate System Confusion (x,y vs row,col)

```python
import cv2
import numpy as np

img = cv2.imread("image.jpg")

# Shape returns (height, width, channels) = (rows, cols, channels)
height, width, channels = img.shape
print(f"Image: {width}x{height}")  # width x height for display

# NumPy indexing: img[row, col] = img[y, x]
pixel = img[100, 200]  # Row 100, Column 200 = y=100, x=200

# OpenCV drawing functions use (x, y)
cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
cv2.circle(img, (center_x, center_y), radius, color, thickness)
cv2.putText(img, "text", (x, y), font, scale, color)

# ROI slicing: img[y1:y2, x1:x2]
roi = img[100:200, 150:300]  # rows 100-200, cols 150-300
```

### 3. imread Returns None on Failure

```python
import cv2

# DANGEROUS: No error raised, just returns None!
img = cv2.imread("nonexistent.jpg")
# img is None, but no exception!

# ALWAYS check the result
img = cv2.imread("image.jpg")
if img is None:
    raise FileNotFoundError(f"Could not load image: image.jpg")

# Better: Use pathlib to check first
from pathlib import Path

def load_image(path: str) -> np.ndarray:
    """Load image with proper error handling."""
    if not Path(path).exists():
        raise FileNotFoundError(f"Image file not found: {path}")

    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Could not decode image: {path}")

    return img
```

### 4. VideoCapture Memory Leaks

```python
import cv2

# ALWAYS release VideoCapture resources
cap = cv2.VideoCapture(0)  # or video file path

try:
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame...
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()

# OR use context manager pattern
class VideoCapture:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {source}")

    def __enter__(self):
        return self.cap

    def __exit__(self, *args):
        self.cap.release()

# Usage
with VideoCapture(0) as cap:
    ret, frame = cap.read()
```

### 5. Data Type Issues

```python
import cv2
import numpy as np

# OpenCV expects uint8 (0-255) for most operations
img = cv2.imread("image.jpg")  # dtype: uint8

# Arithmetic can overflow!
result = img + 50  # WRONG: overflow wraps around
result = cv2.add(img, 50)  # CORRECT: saturates at 255

# Float operations need conversion
img_float = img.astype(np.float32) / 255.0  # Normalize to 0-1
# ... do operations ...
img_uint8 = (img_float * 255).astype(np.uint8)  # Convert back

# Some functions require specific dtypes
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # uint8
edges = cv2.Canny(gray, 100, 200)  # Requires uint8 input
```

## Image I/O

### Loading Images

```python
import cv2
import numpy as np

# Basic load (BGR, 8-bit)
img = cv2.imread("image.jpg")

# Load with flags
img_gray = cv2.imread("image.jpg", cv2.IMREAD_GRAYSCALE)
img_unchanged = cv2.imread("image.jpg", cv2.IMREAD_UNCHANGED)  # Preserves alpha
img_color = cv2.imread("image.jpg", cv2.IMREAD_COLOR)  # Force BGR

# Load from URL (using urllib)
import urllib.request
def load_from_url(url: str) -> np.ndarray:
    resp = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)

# Load from bytes
def load_from_bytes(data: bytes) -> np.ndarray:
    arr = np.frombuffer(data, dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)
```

### Saving Images

```python
import cv2

# Basic save (auto-detects format from extension)
cv2.imwrite("output.jpg", img)
cv2.imwrite("output.png", img)

# JPEG quality (0-100, default 95)
cv2.imwrite("output.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])

# PNG compression (0-9, default 3)
cv2.imwrite("output.png", img, [cv2.IMWRITE_PNG_COMPRESSION, 9])

# Encode to bytes (for API responses, etc.)
success, encoded = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])
if success:
    image_bytes = encoded.tobytes()
```

## Video Capture and Writing

### Capturing from Camera

```python
import cv2

cap = cv2.VideoCapture(0)  # Default camera

# Set properties BEFORE reading frames
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)

# Check if properties were set (not all cameras support all settings)
actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_fps = cap.get(cv2.CAP_PROP_FPS)

if not cap.isOpened():
    raise RuntimeError("Cannot open camera")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Process frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
```

### Capturing from Video File

```python
import cv2

cap = cv2.VideoCapture("video.mp4")

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Video: {width}x{height} @ {fps}fps, {frame_count} frames")

# Read all frames
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()

# Seek to specific frame
cap = cv2.VideoCapture("video.mp4")
cap.set(cv2.CAP_PROP_POS_FRAMES, 100)  # Jump to frame 100
ret, frame = cap.read()
cap.release()
```

### Writing Video

```python
import cv2

# FourCC codec codes
# 'XVID' - MPEG-4 (good compatibility)
# 'mp4v' - MPEG-4 (for .mp4)
# 'MJPG' - Motion JPEG
# 'X264' - H.264 (if available)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))

if not out.isOpened():
    raise RuntimeError("Cannot open video writer")

try:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Ensure frame size matches writer
        frame = cv2.resize(frame, (640, 480))

        # Write frame (must be BGR!)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    out.release()
```

## Color Space Conversions

### Common Conversions

```python
import cv2

img = cv2.imread("image.jpg")

# BGR to RGB (for Matplotlib, PIL, etc.)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# BGR to Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# BGR to HSV (Hue, Saturation, Value)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# HSV ranges in OpenCV:
#   H: 0-179 (not 0-360!)
#   S: 0-255
#   V: 0-255

# BGR to LAB (perceptual color space)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# BGR to YCrCb
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
```

### HSV Color Detection

```python
import cv2
import numpy as np

img = cv2.imread("image.jpg")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define range for blue color
# Note: H is 0-179 in OpenCV, not 0-360!
lower_blue = np.array([100, 50, 50])   # H, S, V
upper_blue = np.array([130, 255, 255])

# Create mask
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Apply mask
result = cv2.bitwise_and(img, img, mask=mask)

# Common color ranges (approximate):
# Red: (0-10, 50-255, 50-255) OR (170-179, 50-255, 50-255)
# Orange: (10-25, 50-255, 50-255)
# Yellow: (25-35, 50-255, 50-255)
# Green: (35-85, 50-255, 50-255)
# Blue: (85-130, 50-255, 50-255)
# Purple: (130-170, 50-255, 50-255)
```

## Image Filtering

### Blurring/Smoothing

```python
import cv2

img = cv2.imread("image.jpg")

# Box filter (averaging) - fast but blocky
blur_box = cv2.blur(img, (5, 5))

# Gaussian blur - smooth, natural looking
blur_gaussian = cv2.GaussianBlur(img, (5, 5), 0)
# Kernel size must be odd: (3,3), (5,5), (7,7), etc.
# sigmaX=0 auto-calculates from kernel size

# Median blur - best for salt-and-pepper noise
blur_median = cv2.medianBlur(img, 5)  # Single odd value, not tuple

# Bilateral filter - edge-preserving smoothing (slower)
blur_bilateral = cv2.bilateralFilter(img, 9, 75, 75)
# d=9: diameter of pixel neighborhood
# sigmaColor=75: filter sigma in color space
# sigmaSpace=75: filter sigma in coordinate space
```

### Edge Detection

```python
import cv2
import numpy as np

img = cv2.imread("image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny edge detection (most common)
edges = cv2.Canny(gray, 100, 200)
# threshold1=100: lower threshold
# threshold2=200: upper threshold
# Ratio of 1:2 or 1:3 recommended

# With Gaussian blur first (reduces noise)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

# Sobel edge detection
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel = cv2.magnitude(sobelx, sobely)

# Laplacian
laplacian = cv2.Laplacian(gray, cv2.CV_64F)
```

### Morphological Operations

```python
import cv2
import numpy as np

# Create kernel
kernel = np.ones((5, 5), np.uint8)
# Or use getStructuringElement for different shapes
kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))

# Erosion - shrinks white regions
eroded = cv2.erode(img, kernel, iterations=1)

# Dilation - expands white regions
dilated = cv2.dilate(img, kernel, iterations=1)

# Opening - erosion followed by dilation (removes noise)
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Closing - dilation followed by erosion (fills holes)
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

# Gradient - dilation minus erosion (edge detection)
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

# Top hat - original minus opening
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

# Black hat - closing minus original
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
```

## Contour Detection

### Finding Contours

```python
import cv2
import numpy as np

img = cv2.imread("image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold or use Canny for edge detection
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours
contours, hierarchy = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,    # Retrieval mode
    cv2.CHAIN_APPROX_SIMPLE  # Contour approximation
)

# Retrieval modes:
# RETR_EXTERNAL - only outermost contours
# RETR_LIST - all contours, no hierarchy
# RETR_CCOMP - two-level hierarchy
# RETR_TREE - full hierarchy

# Approximation methods:
# CHAIN_APPROX_NONE - all points
# CHAIN_APPROX_SIMPLE - compress horizontal, vertical, diagonal segments

# Draw contours
cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
# -1 draws all contours, or specify index

# Draw single contour
cv2.drawContours(img, contours, 0, (0, 255, 0), 2)
```

### Contour Properties

```python
import cv2
import numpy as np

# For each contour
for cnt in contours:
    # Area
    area = cv2.contourArea(cnt)

    # Perimeter (arc length)
    perimeter = cv2.arcLength(cnt, closed=True)

    # Bounding rectangle (upright)
    x, y, w, h = cv2.boundingRect(cnt)

    # Rotated bounding rectangle
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Minimum enclosing circle
    (cx, cy), radius = cv2.minEnclosingCircle(cnt)

    # Fit ellipse (requires at least 5 points)
    if len(cnt) >= 5:
        ellipse = cv2.fitEllipse(cnt)

    # Convex hull
    hull = cv2.convexHull(cnt)

    # Centroid using moments
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

    # Approximate polygon
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(cnt, epsilon, closed=True)
```

## Image Resizing and Transformations

### Resizing

```python
import cv2

img = cv2.imread("image.jpg")

# Resize to specific dimensions
# Note: (width, height) not (height, width)!
resized = cv2.resize(img, (640, 480))

# Resize by scale factor
scaled = cv2.resize(img, None, fx=0.5, fy=0.5)

# With interpolation method
# INTER_NEAREST - fastest, blocky
# INTER_LINEAR - default, good balance
# INTER_AREA - best for shrinking
# INTER_CUBIC - better quality for enlarging
# INTER_LANCZOS4 - best quality for enlarging

# Downscaling - use INTER_AREA
small = cv2.resize(img, (320, 240), interpolation=cv2.INTER_AREA)

# Upscaling - use INTER_CUBIC or INTER_LANCZOS4
large = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_CUBIC)
```

### Rotation and Flipping

```python
import cv2
import numpy as np

img = cv2.imread("image.jpg")
h, w = img.shape[:2]

# Flip
flipped_h = cv2.flip(img, 1)   # Horizontal
flipped_v = cv2.flip(img, 0)   # Vertical
flipped_both = cv2.flip(img, -1)  # Both

# Rotate 90, 180, 270 degrees
rot_90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
rot_180 = cv2.rotate(img, cv2.ROTATE_180)
rot_270 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

# Rotate by arbitrary angle
angle = 45
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, scale=1.0)
rotated = cv2.warpAffine(img, M, (w, h))

# Rotate and expand canvas to fit
def rotate_bound(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    new_w = int((h * sin) + (w * cos))
    new_h = int((h * cos) + (w * sin))

    M[0, 2] += (new_w / 2) - center[0]
    M[1, 2] += (new_h / 2) - center[1]

    return cv2.warpAffine(image, M, (new_w, new_h))
```

### Perspective Transform

```python
import cv2
import numpy as np

img = cv2.imread("document.jpg")

# Define source points (corners of object in image)
src_pts = np.float32([
    [100, 200],   # top-left
    [500, 180],   # top-right
    [550, 400],   # bottom-right
    [80, 420]     # bottom-left
])

# Define destination points (where they should map to)
dst_pts = np.float32([
    [0, 0],
    [400, 0],
    [400, 300],
    [0, 300]
])

# Get perspective transform matrix
M = cv2.getPerspectiveTransform(src_pts, dst_pts)

# Apply transform
warped = cv2.warpPerspective(img, M, (400, 300))
```

## Template Matching

```python
import cv2
import numpy as np

img = cv2.imread("image.jpg")
template = cv2.imread("template.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

h, w = gray_template.shape

# Match template
result = cv2.matchTemplate(gray_img, gray_template, cv2.TM_CCOEFF_NORMED)

# Methods:
# TM_SQDIFF, TM_SQDIFF_NORMED - min value is best match
# TM_CCORR, TM_CCORR_NORMED - max value is best match
# TM_CCOEFF, TM_CCOEFF_NORMED - max value is best match (recommended)

# Find best match location
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# For TM_CCOEFF_NORMED, use max_loc
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

# Draw rectangle around match
cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

# Multiple matches with thresholding
threshold = 0.8
loc = np.where(result >= threshold)
for pt in zip(*loc[::-1]):  # Note: loc is (y, x), zip reverses
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
```

## Feature Detection and Matching

### ORB Features (Fast, Free)

```python
import cv2

img1 = cv2.imread("image1.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("image2.jpg", cv2.IMREAD_GRAYSCALE)

# Create ORB detector
orb = cv2.ORB_create(nfeatures=500)

# Detect keypoints and compute descriptors
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Create BFMatcher with Hamming distance (for binary descriptors)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors
matches = bf.match(des1, des2)

# Sort by distance
matches = sorted(matches, key=lambda x: x.distance)

# Draw matches
result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:20], None,
                         flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
```

### SIFT Features (Requires opencv-contrib)

```python
import cv2

img1 = cv2.imread("image1.jpg", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("image2.jpg", cv2.IMREAD_GRAYSCALE)

# Create SIFT detector
sift = cv2.SIFT_create()

# Detect and compute
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# Use FLANN matcher for SIFT (faster for large datasets)
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# KNN match
matches = flann.knnMatch(des1, des2, k=2)

# Apply Lowe's ratio test
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)
```

## DNN Module (Deep Learning Inference)

```python
import cv2
import numpy as np

# Load model
# TensorFlow (.pb)
net = cv2.dnn.readNetFromTensorflow("model.pb", "config.pbtxt")

# ONNX
net = cv2.dnn.readNetFromONNX("model.onnx")

# Darknet/YOLO
net = cv2.dnn.readNetFromDarknet("yolov3.cfg", "yolov3.weights")

# Caffe
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "model.caffemodel")

# Set backend and target
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
# Or for GPU: DNN_TARGET_CUDA

# Prepare input blob
img = cv2.imread("image.jpg")
blob = cv2.dnn.blobFromImage(
    img,
    scalefactor=1/255.0,   # Normalize to 0-1
    size=(416, 416),       # Network input size
    mean=(0, 0, 0),        # Subtract mean
    swapRB=True,           # BGR to RGB!
    crop=False
)

# Run inference
net.setInput(blob)
output = net.forward()
# Or get specific layers: net.forward(["layer1", "layer2"])
```

## Displaying Images (GUI)

### OpenCV Windows

```python
import cv2

img = cv2.imread("image.jpg")

# Create window
cv2.namedWindow("Window", cv2.WINDOW_NORMAL)  # Resizable
# cv2.WINDOW_AUTOSIZE - fixed size

# Show image
cv2.imshow("Window", img)

# Wait for key press
key = cv2.waitKey(0)  # 0 = wait forever
# key = cv2.waitKey(1)  # 1ms, for video loops

# Clean up
cv2.destroyAllWindows()
# cv2.destroyWindow("Window")  # Specific window

# Note: waitKey returns -1 if no key pressed, or ASCII value
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

### Jupyter Notebook Workaround

**cv2.imshow() doesn't work well in Jupyter notebooks!**

```python
import cv2
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display, Image as IPImage
import io

# Method 1: Use Matplotlib (recommended)
def show_image(img, title="Image"):
    """Display image in Jupyter using Matplotlib."""
    if len(img.shape) == 3:
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img

    plt.figure(figsize=(10, 8))
    plt.imshow(img_rgb, cmap='gray' if len(img.shape) == 2 else None)
    plt.title(title)
    plt.axis('off')
    plt.show()

# Method 2: Use IPython display
def show_image_ipython(img):
    """Display image using IPython display."""
    _, encoded = cv2.imencode('.png', img)
    display(IPImage(data=encoded.tobytes()))

# Method 3: Use cv2_imshow from google.colab (in Colab)
# from google.colab.patches import cv2_imshow
# cv2_imshow(img)
```

## Performance Tips

### Memory Management

```python
import cv2
import numpy as np

# 1. Reuse arrays instead of creating new ones
frame = np.empty((480, 640, 3), dtype=np.uint8)
cap = cv2.VideoCapture(0)
while True:
    ret = cap.read(frame)  # Reuses frame array
    if not ret:
        break

# 2. Use views instead of copies when possible
roi = img[100:200, 100:200]  # This is a view, not a copy
roi_copy = img[100:200, 100:200].copy()  # This creates a copy

# 3. Process in-place when possible
cv2.GaussianBlur(img, (5, 5), 0, dst=img)  # In-place

# 4. Use appropriate data types
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # uint8
# Don't convert to float64 unless necessary

# 5. Pre-allocate for batch processing
results = np.empty((num_images, h, w, 3), dtype=np.uint8)
for i, img_path in enumerate(paths):
    results[i] = process(cv2.imread(img_path))
```

### Vectorized Operations

```python
import cv2
import numpy as np

# BAD: Using loops
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img[i, j] = img[i, j] * 2

# GOOD: Vectorized with NumPy/OpenCV
img = img * 2  # NumPy broadcasting
# or
img = cv2.multiply(img, 2)  # OpenCV (handles overflow)

# Use OpenCV functions over NumPy when available
# OpenCV is optimized with SIMD, multi-threading

# OpenCV (faster)
result = cv2.countNonZero(mask)

# NumPy (slower for this)
result = np.count_nonzero(mask)
```

### GPU Acceleration (CUDA)

```python
import cv2

# Check CUDA availability
print(cv2.cuda.getCudaEnabledDeviceCount())

if cv2.cuda.getCudaEnabledDeviceCount() > 0:
    # Upload image to GPU
    gpu_img = cv2.cuda_GpuMat()
    gpu_img.upload(img)

    # GPU operations
    gpu_gray = cv2.cuda.cvtColor(gpu_img, cv2.COLOR_BGR2GRAY)
    gpu_blur = cv2.cuda.createGaussianFilter(
        cv2.CV_8UC1, cv2.CV_8UC1, (5, 5), 0
    ).apply(gpu_gray)

    # Download back to CPU
    result = gpu_blur.download()
else:
    # Fallback to CPU
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.GaussianBlur(gray, (5, 5), 0)
```

## Drawing Functions

```python
import cv2
import numpy as np

img = np.zeros((500, 500, 3), dtype=np.uint8)

# Colors are BGR!
blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
white = (255, 255, 255)

# Line
cv2.line(img, (0, 0), (500, 500), green, thickness=2)

# Rectangle
cv2.rectangle(img, (50, 50), (200, 200), blue, thickness=2)
cv2.rectangle(img, (250, 50), (400, 200), red, thickness=-1)  # Filled

# Circle
cv2.circle(img, (250, 250), 100, green, thickness=2)
cv2.circle(img, (250, 350), 50, red, thickness=-1)  # Filled

# Ellipse
cv2.ellipse(img, (250, 250), (100, 50), 45, 0, 360, white, 2)

# Polygon
pts = np.array([[100, 300], [200, 400], [150, 450]], np.int32)
pts = pts.reshape((-1, 1, 2))
cv2.polylines(img, [pts], isClosed=True, color=green, thickness=2)
cv2.fillPoly(img, [pts], color=blue)

# Text
cv2.putText(img, "OpenCV", (50, 450),
            cv2.FONT_HERSHEY_SIMPLEX, 1, white, 2, cv2.LINE_AA)

# Get text size (for positioning)
text = "OpenCV"
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
thickness = 2
(text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
```

## Additional References

For advanced topics beyond this guide, see:

- **[OpenCV Advanced Patterns](references/opencv-advanced-patterns.md)** - Background subtraction, object tracking, camera calibration, stereo vision, optical flow, image stitching, face detection, ArUco markers
