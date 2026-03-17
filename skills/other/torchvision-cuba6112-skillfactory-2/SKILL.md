---
name: torchvision
description: Computer vision library for PyTorch featuring pretrained models, advanced image transforms (v2), and utilities for handling complex data types like bounding boxes and masks. (torchvision, transforms, tvtensor, resnet, cutmix, mixup, pretrained models, vision transforms)
---

## Overview

TorchVision provides models, datasets, and transforms for computer vision. It has recently transitioned to "v2" transforms, which support more complex data types like bounding boxes and masks alongside images, using a unified API.

## When to Use

Use TorchVision for standard CV tasks like classification, detection, or segmentation. Use the v2 transforms for performance-critical pipelines or when applying augmentations like MixUp/CutMix that require batch-level processing.

## Decision Tree

1. Are you starting a new project?
   - YES: Use `torchvision.transforms.v2`.
2. Do you need a pretrained model?
   - YES: Use the `weights` parameter (e.g., `ResNet50_Weights.DEFAULT`).
3. Do you have bounding boxes that need to move with the image?
   - YES: Use `TVTensors` for automatic coordinate transformation.

## Workflows

1. **Standard Inference with Pretrained Models**
   1. Select a model and its specific weights (e.g., `ResNet50_Weights.DEFAULT`).
   2. Initialize the model with those weights and set to `.eval()`.
   3. Extract the required preprocessing from the weights using `weights.transforms()`.
   4. Apply the transform to the input image and run the forward pass.

2. **Advanced Data Augmentation with MixUp**
   1. Import `MixUp` and `CutMix` from `torchvision.transforms.v2`.
   2. Incorporate them into the training loop logic (they act on batches, not individual samples).
   3. Apply the transform to the `(images, labels)` pair to generate augmented training data.

3. **Migrating to Transforms v2**
   1. Update the import from `torchvision.transforms` to `torchvision.transforms.v2`.
   2. Use `v2.Compose` for combining transforms.
   3. Switch from PIL-based logic to Tensor-based logic for significant performance gains.
   4. Leverage v2's ability to handle dicts/tuples for complex inputs like `{image, boxes, mask}`.

## Non-Obvious Insights

- **Weight-specific Transforms**: Preprocessing is now bundled with weights; accessing `weights.transforms()` ensures the inference data exactly matches the training distribution of the specific weight recipe.
- **TVTensors**: v2 transforms recognize special tensor subclasses (`TVTensors`) for bounding boxes and masks, allowing them to be rotated or flipped automatically whenever the image is.
- **Backend Performance**: The `video_reader` backend is faster than `pyav` but requires manual compilation from source in some environments to be available.

## Evidence

- "As of v0.13, TorchVision offers a new Multi-weight support API... weights = ResNet50_Weights.DEFAULT." (https://pytorch.org/vision/stable/models.html)
- "v2 transforms generally accept an arbitrary number of leading dimensions (..., C, H, W) and can handle batched images or batched videos." (https://pytorch.org/vision/stable/transforms.html)

## Scripts

- `scripts/torchvision_tool.py`: Utility to load models and apply v2 transforms to batched data.
- `scripts/torchvision_tool.js`: Node.js interface to process images via TorchVision Python scripts.

## Dependencies

- torchvision
- torch
- pillow (for image loading)

## References

- [TorchVision Reference](references/README.md)