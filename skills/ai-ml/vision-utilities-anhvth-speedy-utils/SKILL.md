---
name: 'vision-utilities'
description: 'Guide for using vision utilities in speedy_utils, including fast GPU image loading, memory-mapped datasets, and notebook visualization.'
---

# Vision Utilities Guide

This skill provides comprehensive guidance for using the vision utilities in `speedy_utils`.

## When to Use This Skill

Use this skill when you need to:
- Load images efficiently, leveraging GPU acceleration (NVIDIA DALI) when available.
- Create memory-mapped datasets (`ImageMmap`) for extremely fast random access training loops.
- Visualize batches of images in Jupyter notebooks with automatic grid layout.
- Handle various image formats (numpy, torch, file paths) uniformly.

## Prerequisites

- `speedy_utils` installed.
- `Pillow` and `numpy` (required).
- `matplotlib` (for plotting).
- `nvidia-dali-cuda110` or similar (optional, for GPU loading).
- `torch` (optional, for tensor support).

## Core Capabilities

### Fast Image Loading (`read_images`)
- Tries GPU (DALI) first, falls back to CPU (Pillow).
- Supports batch processing and resizing.
- Validates images to skip corrupted files.

### Memory-Mapped Datasets (`ImageMmap`, `ImageMmapDynamic`)
- **`ImageMmap`**: For fixed-size images. Pre-processes and resizes images once, then stores them in a single binary file for zero-copy access.
- **`ImageMmapDynamic`**: For variable-size images. Stores flattened images and metadata.
- Both support multi-process safe building with file locks.

### Notebook Visualization (`plot_images_notebook`)
- Automatically arranges images in a grid.
- Handles mixed inputs: paths, numpy arrays, torch tensors.
- Supports (H, W, C), (C, H, W), and (B, ...) formats.

## Usage Examples

### Example 1: Fast Image Loading
Load a batch of images, resizing them to 224x224.

```python
from vision_utils.io_utils import read_images

paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
# Returns dict: {path: np.ndarray}
images = read_images(paths, hw=(224, 224))
```

### Example 2: Creating a Mmap Dataset
Create a dataset that loads instantly on subsequent runs.

```python
from vision_utils.io_utils import ImageMmap

# First run: reads files, resizes, writes .cache/mmap_dataset_...
# Next runs: maps file directly
dataset = ImageMmap(paths, size=(224, 224))

# Access like a list/array
img = dataset[0]  # np.ndarray (224, 224, 3)
```

### Example 3: Visualizing Images
Plot a mix of tensors and paths in a notebook.

```python
from vision_utils.plot import plot_images_notebook
import torch
import numpy as np

images = [
    "img1.jpg",                  # Path
    np.random.rand(100, 100, 3), # Numpy
    torch.rand(3, 64, 64)        # Tensor (C, H, W)
]

plot_images_notebook(images, ncols=3, titles=["File", "Random", "Tensor"])
```

## Guidelines

1.  **GPU Loading**:
    - `read_images` is most effective for large batches. For single images, CPU overhead is lower.
    - Ensure DALI is installed for GPU speedup.

2.  **Mmap Datasets**:
    - Use `ImageMmap` for training pipelines where fixed size is required (e.g., ResNet).
    - Use `ImageMmapDynamic` if you need original resolutions (e.g., for object detection with variable size inputs).
    - The cache is stored in `.cache/` by default. Clear it if your source images change content but keep the same filenames (hashing is based on paths).

3.  **Plotting**:
    - `plot_images_notebook` is designed for *notebooks*. It uses `plt.show()`.
    - It automatically handles normalization (0-1 vs 0-255) for display.

## Limitations

- **DALI Installation**: Installing DALI can be complex depending on CUDA version. The code gracefully falls back to CPU if DALI is missing.
- **Disk Space**: Mmap datasets duplicate image data in uncompressed format (raw pixels). This takes significantly more disk space than JPEGs but offers much faster read speeds.
