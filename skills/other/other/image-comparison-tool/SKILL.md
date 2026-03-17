---
name: image-comparison-tool
description: Compare images with SSIM similarity scoring, pixel difference highlighting, and side-by-side visualization.
---

# Image Comparison Tool

Compare images with similarity scoring and difference visualization.

## Features

- **SSIM Similarity**: Structural similarity index
- **Pixel Differences**: Highlight changed areas
- **Side-by-Side**: Visual comparison layout
- **Diff Heatmap**: Color-coded differences
- **Batch Comparison**: Compare multiple image pairs
- **Threshold Detection**: Find significant changes

## CLI Usage

```bash
python image_comparison.py --image1 before.jpg --image2 after.jpg --output diff.png
```

## Dependencies

- opencv-python>=4.8.0
- scikit-image>=0.21.0
- pillow>=10.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
