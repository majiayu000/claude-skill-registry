---
name: opencv
description: OpenCV computer vision library. Use for image processing.
---

# OpenCV

OpenCV is the fundamental library for Image Processing. v5.0 (2025) modernizes deep learning support and licensing.

## When to Use

- **Image Manipulation**: Resizing, cropping, color space conversion (BGR -> RGB).
- **Classic CV**: Edge detection (Canny), Feature matching (SIFT/ORB).
- **Video I/O**: Reading/Writing webcams or video files.

## Core Concepts

### BGR

OpenCV reads images as Blue-Green-Red (not RGB) by default. History quirks.

### `cv::Mat`

The core matrix structure (in C++). In Python, it's just a NumPy array.

### DNN Module

Running darknet/onnx models directly in OpenCV (lightweight inference).

## Best Practices (2025)

**Do**:

- **Use it for Preprocessing**: `cv2.resize()` is highly optimized.
- **Use `headless`**: `pip install opencv-python-headless` for server deployments (smaller, no GUI deps).

**Don't**:

- **Don't implement Deep Learning training**: Use PyTorch. Use OpenCV only for inference/preprocessing.

## References

- [OpenCV Documentation](https://opencv.org/)
