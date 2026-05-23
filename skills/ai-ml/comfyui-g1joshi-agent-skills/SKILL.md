---
name: comfyui
description: ComfyUI node-based Stable Diffusion. Use for image generation.
---

# ComfyUI

ComfyUI is a node-based GUI for Stable Diffusion. It gives you infinite control over the generation pipeline. 2025 update (UI Overhaul) makes it more accessible.

## When to Use

- **Complex Workflows**: Hires.fix, Inpainting, ControlNet, and Upscaling in one pipeline.
- **Video**: AnimateDiff and video-to-video workflows.
- **Optimization**: Runs on lower VRAM than WebUI (A1111).

## Core Concepts

### Nodes & Noodles

Connect "Load Checkpoint" -> "CLIP Text Encode" -> "KSampler" -> "VAE Decode" -> "Save Image".

### Workflow Format

Workflows are saved as PNG metadata. Drag a PNG into ComfyUI to load its workflow.

### Custom Nodes

Community plugins (thousands available via ComfyUI Manager).

## Best Practices (2025)

**Do**:

- **Use ComfyUI Manager**: Essential for installing missing custom nodes.
- **Use XY Plot**: To test different parameters (CFG vs Steps) grid.
- **Save Workflows**: Organize your JSON/PNG workflows.

**Don't**:

- **Don't fear the spaghetti**: It looks complex, but logic is linear.

## References

- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
