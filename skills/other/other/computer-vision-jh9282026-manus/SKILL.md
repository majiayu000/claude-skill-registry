---
name: computer-vision
description: "Build computer vision systems using CNNs and modern architectures. Use for image classification, object detection (YOLO, Faster R-CNN), image segmentation, face recognition, and visual analysis tasks."
---

# Computer Vision

Build computer vision systems for image classification, object detection, and visual analysis.

## Overview

Computer vision enables machines to interpret and understand visual information. This skill covers CNNs, object detection, segmentation, and modern vision architectures.

## Quick Reference

| Scenario | Recommended Approach | Reference File |
|----------|---------------------|----------------|
| Image classification | CNNs (ResNet, EfficientNet, ViT) | `/references/classification.md` |
| Object detection and localization | YOLO, Faster R-CNN, RetinaNet | `/references/object-detection.md` |
| Pixel-level segmentation | U-Net, Mask R-CNN, DeepLab | `/references/segmentation.md` |

## Core Principles

1. **Convolutional Layers** - Extract spatial features hierarchically
2. **Transfer Learning** - Use pre-trained models on ImageNet
3. **Data Augmentation** - Increase robustness through transformations
4. **Multi-Scale Processing** - Detect objects at different sizes
5. **End-to-End Learning** - Train entire pipeline jointly

## Key Tasks

### Image Classification
Assign label to entire image.

**Architectures:**
- ResNet: Residual connections for deep networks
- EfficientNet: Optimal scaling
- Vision Transformers: Attention-based

**Approach:**
- Use pre-trained model
- Fine-tune on target dataset
- Data augmentation

### Object Detection
Locate and classify objects in images.

**Methods:**
- YOLO: Single-stage, real-time
- Faster R-CNN: Two-stage, accurate
- RetinaNet: Focal loss for imbalance

**Components:**
- Backbone: Feature extraction
- Neck: Feature fusion
- Head: Detection and classification

### Image Segmentation
Classify each pixel.

**Types:**
- Semantic: Class per pixel
- Instance: Separate object instances
- Panoptic: Semantic + instance

**Architectures:**
- U-Net: Encoder-decoder with skip connections
- Mask R-CNN: Instance segmentation
- DeepLab: Atrous convolutions

## Using the Reference Files

**`/references/classification.md`** — CNN architectures, transfer learning, fine-tuning strategies, data augmentation, and evaluation metrics.

**`/references/object-detection.md`** — YOLO, Faster R-CNN, anchor boxes, non-maximum suppression, evaluation (mAP), and real-time detection.

**`/references/segmentation.md`** — U-Net, Mask R-CNN, semantic vs instance segmentation, loss functions, and post-processing.

## Best Practices

- Use pre-trained models (ImageNet weights)
- Apply data augmentation (crop, flip, color jitter)
- Normalize inputs (ImageNet mean/std)
- Use appropriate image size for model
- Monitor for overfitting
- Evaluate on diverse test set
- Consider inference speed requirements
- Handle class imbalance

## Common Pitfalls to Avoid

- Not using pre-trained weights
- Insufficient data augmentation
- Wrong input normalization
- Inappropriate image resolution
- Ignoring class imbalance
- Not considering inference speed
- Overfitting to small datasets
- Poor anchor box design (object detection)

