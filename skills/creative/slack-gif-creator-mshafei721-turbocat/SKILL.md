---
name: slack-gif-creator
description: Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."
---

# Slack GIF Creator

## Overview

Toolkit for creating Slack-optimized animated GIFs with technical specifications, Python utilities, and animation concepts.

## Key Dimensions & Parameters

**Size Requirements:**
- Emoji GIFs: 128x128 pixels
- Message GIFs: 480x480 pixels

**Performance:**
- FPS range: 10-30 (lower = smaller files)
- Color palette: 48-128 colors
- Duration: Under 3 seconds for emoji

## Core Utilities

```python
from gif_builder import GIFBuilder
from validators import validate_gif
from easing import ease_in_out

# Create a simple animated GIF
builder = GIFBuilder(size=(128, 128), fps=15)
builder.add_frames(frames)
builder.save("output.gif")

# Validate for Slack
validate_gif("output.gif", target="emoji")
```

## Animation Techniques

- **Shake/Vibrate**: Oscillating position offsets
- **Pulse/Heartbeat**: Rhythmic scaling
- **Bounce**: Gravity with easing functions
- **Spin/Rotate**: Angular transformations
- **Fade In/Out**: Alpha channel adjustments
- **Slide**: Directional movement with easing
- **Zoom**: Scale and crop operations
- **Explode/Particles**: Radiating burst effects

## Design Philosophy

Create polished graphics using PIL primitives:
- Use thicker lines (width >= 2)
- Layer shapes for depth
- Vibrant colors with contrast
- Calculated symmetry for complex forms

## Dependencies

```bash
pip install Pillow imageio numpy
```

## Quick Start

```python
from PIL import Image, ImageDraw
import imageio

frames = []
for i in range(20):
    img = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Animation logic here
    frames.append(img)

imageio.mimsave('output.gif', frames, fps=15)
```
