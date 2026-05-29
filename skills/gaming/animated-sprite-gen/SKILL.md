---
name: animated-sprite-gen
description: Use when generating animated game sprites, creating sprite sheets, building character animations for 2D games, or needing consistent multi-frame pixel art from AI image generation models
---

# Animated game sprite generation

A workflow for generating consistent animated sprite sheets using AI image models (GPT Image 1.5, Nano Banana 2, or similar). The key insight: generate full animation strips from a single anchor frame, not frame-by-frame.

## Core workflow

### 1. Start from a shipped seed frame

Anchor the model to an actual production sprite, not a loose concept. This locks in palette, proportions, line weight, and shading direction.

### 2. Build a reference canvas

Don't send the raw sprite directly. Upscale with nearest-neighbor and place into a larger transparent canvas (1024x1024) with reserved frame slots.

```python
# Upscale a 64x64 sprite to fit in a 1024x1024 edit canvas
# with reserved slots for animation frames
```

The larger canvas gives the model room to generate multi-frame sequences.

### 3. Generate full strips, not individual frames

Frame-by-frame generation causes character drift. Instead, request the entire animation strip in one prompt:

```
Generate a [N]-frame [animation_type] animation strip of this character.
Keep the character consistent across all frames.
Arrange frames left-to-right in a single row.
Maintain the same art style, proportions, and color palette.
```

This produces much better consistency than iterative frame edits.

### 4. Normalize into game-ready frames

The raw strip needs post-processing:
- Detect individual sprite components in the strip
- Use the anchor image to compute a shared scale for all frames
- Optionally lock frame 1 to the exact shipped idle frame
- Export to standard frame size (e.g., 64x64) with transparency padding

### 5. Handle complex poses

When one pose is taller than another (e.g., sword-up attack vs neutral):
- Use **one global scale** for the entire strip
- Let pose differences show as extra height inside the frame
- Never scale individual frames independently (causes size inconsistency)

## Model comparison for sprites

| Model | Strength | Weakness |
|-------|----------|----------|
| GPT Image 1.5 | Good anchor-based editing, edit API supports canvas workflow | Frame size consistency varies |
| Nano Banana 2 | Better consistency across frames, cheaper, faster | May struggle with complex directions |
| Retro Diffusion Pro | Purpose-built for pixel art (uses Gemini) | More specialized, less flexible |

Community reports suggest NB2 outperforms GPT Image 1.5 for sprite sheet consistency. Limiting output to max 9 objects per request reduces hallucinations.

## Tips

- **Isometric sprites**: Still an open challenge — no established best practice yet
- **Consistency ceiling**: Limit strips to 4-8 frames per generation for best results
- **Video-to-sprite alternative**: Generate an animation of the character, then slice frames and use OpenCV for realignment and framing
- **ChatGPT shortcut**: Ask DALL-E for a spritesheet, then ask Data Analysis to "slice this sprite sheet and make a gif" with frame dimensions

## Verification checklist

1. Anchor frame matches shipped production sprite exactly
2. All frames share the same global scale
3. Frame 1 is locked to the original idle sprite
4. Preview in-engine before marking as production-ready
5. Check for palette drift between first and last frames

## Attribution

Based on ["Generating Animated Game Sprites using GPT 5.4 + Image 1.5"](https://x.com/chongdashu) by [@chongdashu](https://x.com/chongdashu) on X (Mar 2026). Original guide covers the anchor-frame workflow, canvas setup, strip normalization, and pose handling for consistent AI-generated sprite animations.
