---
name: algorithmic-art
description: Create algorithmic and generative art using p5.js, canvas APIs, and computational aesthetics. Use when users want to create generative art, procedural graphics, creative coding visualizations, or interactive art pieces with seeded randomness for reproducibility.
---

# Algorithmic Art

## Overview

Create museum-quality generative art using computational techniques. This skill focuses on p5.js for browser-based creative coding with emphasis on seeded randomness, interactive parameters, and self-contained HTML artifacts.

## Core Capabilities

1. **Generative Aesthetics**: Develop unique visual philosophies expressed through code
2. **p5.js Integration**: Create interactive sketches with parameter controls
3. **Seeded Randomness**: Reproducible outputs for consistent artistic results
4. **Canvas Optimization**: Performance-focused rendering for smooth animations

## Quick Start

```javascript
// Basic p5.js generative pattern
function setup() {
  createCanvas(800, 800);
  randomSeed(42); // Reproducible randomness
  noLoop();
}

function draw() {
  background(20);
  for (let i = 0; i < 100; i++) {
    let x = random(width);
    let y = random(height);
    let size = random(10, 50);
    fill(random(255), random(255), random(255), 150);
    ellipse(x, y, size);
  }
}
```

## Design Principles

- **Seeded Randomness**: Always use `randomSeed()` for reproducible outputs
- **Parameter Controls**: Expose key variables for interactive exploration
- **Performance**: Use `noLoop()` for static pieces, optimize for animations
- **Self-Contained**: Bundle as single HTML artifacts for easy sharing

## Workflow

1. Define aesthetic concept and visual philosophy
2. Implement core algorithm with configurable parameters
3. Add interactivity (mouse, keyboard, sliders)
4. Optimize performance for target framerate
5. Bundle as self-contained HTML artifact
