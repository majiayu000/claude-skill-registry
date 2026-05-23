---
version: 4.1.0-fractal
name: slack-gif-creator
description: Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."
license: Complete terms in LICENSE.txt
---

# Slack GIF Creator

A toolkit providing utilities and knowledge for creating animated GIFs optimized for Slack.

## Slack Requirements

**Dimensions:**
- Emoji GIFs: 128x128 (recommended)
- Message GIFs: 480x480

**Parameters:**
- FPS: 10-30 (lower is smaller file size)
- Colors: 48-128 (fewer = smaller file size)
- Duration: Keep under 3 seconds for emoji GIFs

## Core Workflow

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. Create builder
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. Generate frames
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # Draw your animation using PIL primitives
    # (circles, polygons, lines, etc.)

    builder.add_frame(frame)

# 3. Save with optimization
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## Drawing Graphics

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Working with User-Uploaded Images](./sub-skills/working-with-user-uploaded-images.md)
### 2. [Drawing from Scratch](./sub-skills/drawing-from-scratch.md)
### 3. [Making Graphics Look Good](./sub-skills/making-graphics-look-good.md)
### 4. [GIFBuilder (`core.gif_builder`)](./sub-skills/gifbuilder-coregif_builder.md)
### 5. [Validators (`core.validators`)](./sub-skills/validators-corevalidators.md)
### 6. [Easing Functions (`core.easing`)](./sub-skills/easing-functions-coreeasing.md)
### 7. [Frame Helpers (`core.frame_composer`)](./sub-skills/frame-helpers-coreframe_composer.md)
### 8. [Shake/Vibrate](./sub-skills/shakevibrate.md)
### 9. [Pulse/Heartbeat](./sub-skills/pulseheartbeat.md)
### 10. [Bounce](./sub-skills/bounce.md)
### 11. [Spin/Rotate](./sub-skills/spinrotate.md)
### 12. [Fade In/Out](./sub-skills/fade-inout.md)
### 13. [Slide](./sub-skills/slide.md)
### 14. [Zoom](./sub-skills/zoom.md)
### 15. [Explode/Particle Burst](./sub-skills/explodeparticle-burst.md)
