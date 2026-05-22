---
name: cv-pipeline-builder
description: |
  Computer vision ML pipelines for image classification, object detection, semantic segmentation, and image generation. Activates for "computer vision", "image classification", "object detection", "CNN", "ResNet", "YOLO", "image segmentation", "image preprocessing", "data augmentation". Builds end-to-end CV pipelines with PyTorch/TensorFlow, integrated with SpecWeave increments.
---

# Computer Vision Pipeline Builder

## Overview

Specialized ML pipelines for computer vision tasks. Handles image preprocessing, data augmentation, CNN architectures, transfer learning, and deployment for production CV systems.

## CV Tasks Supported

### 1. Image Classification

```python
from specweave import CVPipeline

# Binary or multi-class classification
pipeline = CVPipeline(
    task="classification",
    num_classes=10,
    increment="0042"
)

# Automatically configures:
# - Image preprocessing (resize, normalize)
# - Data augmentation (rotation, flip, color jitter)
# - CNN architecture (ResNet, EfficientNet, ViT)
# - Transfer learning from ImageNet
# - Training loop with validation
# - Inference pipeline

pipeline.fit(train_images, train_labels)
```

### 2. Object Detection

```python
# Detect multiple objects in images
pipeline = CVPipeline(
    task="object_detection",
    classes=["person", "car", "dog", "cat"],
    increment="0042"
)

# Uses: YOLO, Faster R-CNN, or RetinaNet
# Returns: Bounding boxes + class labels + confidence scores
```

### 3. Semantic Segmentation

```python
# Pixel-level classification
pipeline = CVPipeline(
    task="segmentation",
    num_classes=21,
    increment="0042"
)

# Uses: U-Net, DeepLab, or SegFormer
# Returns: Segmentation mask for each pixel
```

## Best Practices for CV

### Data Augmentation

```python
from specweave import ImageAugmentation

aug = ImageAugmentation(increment="0042")

# Standard augmentations
aug.add_transforms([
    "random_rotation",  # ±15 degrees
    "random_flip_horizontal",
    "random_brightness",  # ±20%
    "random_contrast",  # ±20%
    "random_crop"
])

# Advanced augmentations
aug.add_advanced([
    "mixup",  # Mix two images
    "cutout",  # Random erasing
    "autoaugment"  # Learned augmentation
])
```

### Transfer Learning

```python
# Start from pre-trained ImageNet models
pipeline = CVPipeline(task="classification")

# Option 1: Feature extraction (freeze backbone)
pipeline.use_pretrained(
    model="resnet50",
    freeze_backbone=True
)

# Option 2: Fine-tuning (unfreeze after few epochs)
pipeline.use_pretrained(
    model="resnet50",
    freeze_backbone=False,
    fine_tune_after_epoch=3
)
```

### Model Selection

**Image Classification**:
- Small datasets (<10K): ResNet18, MobileNetV2
- Medium datasets (10K-100K): ResNet50, EfficientNet-B0
- Large datasets (>100K): EfficientNet-B3, Vision Transformer

**Object Detection**:
- Real-time (>30 FPS): YOLOv8, SSDLite
- High accuracy: Faster R-CNN, RetinaNet

**Segmentation**:
- Medical imaging: U-Net
- Scene segmentation: DeepLabV3, SegFormer

## Integration with SpecWeave

```python
# CV increment structure
.specweave/increments/0042-image-classifier/
├── spec.md
├── data/
│   ├── train/
│   ├── val/
│   └── test/
├── models/
│   ├── model-v1.pth
│   └── model-v2.pth
├── experiments/
│   ├── baseline-resnet18/
│   ├── resnet50-augmented/
│   └── efficientnet-b0/
└── deployment/
    ├── onnx_model.onnx
    └── inference.py
```

## Commands

```bash
/ml:cv-pipeline --task classification --model resnet50
/ml:cv-evaluate 0042  # Evaluate on test set
/ml:cv-deploy 0042    # Export to ONNX
```

Quick setup for CV projects with production-ready pipelines.
