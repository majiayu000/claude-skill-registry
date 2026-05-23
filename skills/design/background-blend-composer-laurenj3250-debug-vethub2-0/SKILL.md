---
name: background-blend-composer
description: Design layered backgrounds that make PNG assets blend naturally. Use when hero assets float awkwardly on gradients, multiple images don't blend, or need seamless foreground/background integration. Outputs layer stacks, blend modes, edge-tinting strategies, and exact CSS.
---

# Background & Blend Composer (Hintergrund-Mischer)

Design layered backgrounds that make PNG assets blend naturally.

## When to Use

- Hero asset floating on random gradient
- Multiple images that don't blend
- Need seamless foreground/background integration
- Harsh edges between images and backgrounds

## Process

### 1. Analyze Assets

For each asset, identify:
- **Background type**: Transparent, white, dark, colored
- **Color palette**: Dominant colors, edge colors
- **Style**: Flat, detailed, textured, gradient

### 2. Design Layer Stack

Build from back to front:

```
Layer 1: SOLID BASE
├── Single color matching darkest asset tones
├── Purpose: Unifying foundation

Layer 2: GRADIENT ATMOSPHERE
├── Subtle gradient adding depth
├── Direction should complement composition

Layer 3: SIDE/BACKGROUND ASSETS
├── Images that frame the composition
├── Use appropriate blend modes
├── Mask edges for seamless blending

Layer 4: HERO/FOREGROUND ASSET
├── Main focal point
├── Handle background removal
├── Add edge blending if needed

Layer 5: OVERLAYS/EFFECTS
├── Atmospheric effects (mist, particles)
├── Vignettes, glows
```

### 3. Blend Mode Selection

| Asset Background | Blend Mode | Why |
|------------------|------------|-----|
| White | `multiply` | White becomes transparent |
| Black | `screen` or `lighten` | Black becomes transparent |
| Transparent | `normal` | Already clean |
| Dark (matching base) | `lighten` | Shows lighter elements |

### 4. Edge Blending Techniques

**For white backgrounds with multiply:**
```css
/* Problem: Harsh rectangular edge */
/* Solution: Edge-tinting overlay */
.hero-container {
  position: relative;
}
.hero-container::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse 70% 80% at 50% 50%,
    transparent 40%,
    rgba(BASE_COLOR, 0.6) 70%,
    BASE_COLOR 100%
  );
  mix-blend-mode: multiply;
  pointer-events: none;
}
```

**For side images:**
```css
mask-image: linear-gradient(
  to right, /* or to left */
  black 0%,
  black 60%,
  transparent 100%
);
```

### 5. Z-Index Strategy

```
z-0: Base color, gradients
z-1: Background assets (trees, mountains)
z-2: Hero/main asset
z-3: Atmospheric effects
z-4: UI elements
```

## Common Problems & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Hard rectangular edges | No edge blending | Add gradient mask or tinting overlay |
| Hero too faded | Blend mode too aggressive | Limit blend to edges only |
| Colors don't match | Different palettes | Sample from assets, unify base |
| "Floating" asset | No grounding | Add soft shadow or ambient glow |
| Muddy center | Too many layers | Reduce count, increase contrast |

## Example: Ice Climber Dashboard

**Assets:**
- Hero: Ice climber (white bg, teal/cyan)
- Left: Night forest (dark navy)
- Right: Pine trees (dark navy)

**Solution:**
```
Layer 1: #0c1e2b (base)
Layer 2: Radial glow at center
Layer 3: Left/right images (z-1, lighten, edge masks)
Layer 4: Hero (z-2, multiply + edge tint overlay)
Layer 5: Stars, snow particles (z-3+)
```
