---
name: generative-art-algorithms
description: Create algorithmic and generative art using mathematical patterns, noise functions, particle systems, and procedural generation. Covers flow fields, L-systems, fractals, and creative coding foundations. Triggers on generative art, algorithmic art, creative coding, procedural generation, or mathematical visualization requests.
license: MIT
---

# Generative Art Algorithms

Create art through code, mathematics, and emergence.

## Core Philosophy

### Generative Art Principles

1. **Rules create emergence** - Simple rules yield complex results
2. **Controlled randomness** - Seeded random for reproducibility
3. **Parameter exploration** - Same algorithm, infinite variations
4. **Happy accidents** - Bugs as features

### The Creative Coding Loop

```
Idea → Algorithm → Parameters → Render → Evaluate → Iterate
   ↑                                                   │
   └───────────────────────────────────────────────────┘
```

---

## Noise Functions

### Perlin/Simplex Noise

Smooth, continuous random values perfect for organic motion.

```javascript
// p5.js example
function draw() {
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      let n = noise(x * 0.01, y * 0.01, frameCount * 0.01);
      stroke(n * 255);
      point(x, y);
    }
  }
}
```

### Noise Parameters

| Parameter | Effect |
|-----------|--------|
| Scale (frequency) | Zoom level of noise (smaller = more detail) |
| Octaves | Layers of detail |
| Amplitude | Height of values |
| Time offset | Animate through noise space |

### Noise Applications

- Terrain generation
- Texture synthesis
- Organic movement
- Flow fields
- Cloud/smoke effects

---

## Flow Fields

### Basic Flow Field

```javascript
// Generate angle at each grid point from noise
function setup() {
  createCanvas(800, 800);
  
  let resolution = 20;
  let cols = width / resolution;
  let rows = height / resolution;
  
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      let angle = noise(x * 0.1, y * 0.1) * TWO_PI * 2;
      
      // Draw vector
      push();
      translate(x * resolution, y * resolution);
      rotate(angle);
      stroke(0);
      line(0, 0, resolution * 0.8, 0);
      pop();
    }
  }
}
```

### Particles in Flow Field

```javascript
class Particle {
  constructor() {
    this.pos = createVector(random(width), random(height));
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
    this.maxSpeed = 2;
    this.prevPos = this.pos.copy();
  }
  
  follow(flowField, resolution) {
    let x = floor(this.pos.x / resolution);
    let y = floor(this.pos.y / resolution);
    let index = x + y * floor(width / resolution);
    let force = flowField[index];
    this.applyForce(force);
  }
  
  applyForce(force) {
    this.acc.add(force);
  }
  
  update() {
    this.vel.add(this.acc);
    this.vel.limit(this.maxSpeed);
    this.prevPos = this.pos.copy();
    this.pos.add(this.vel);
    this.acc.mult(0);
  }
  
  edges() {
    if (this.pos.x > width) { this.pos.x = 0; this.prevPos.x = 0; }
    if (this.pos.x < 0) { this.pos.x = width; this.prevPos.x = width; }
    if (this.pos.y > width) { this.pos.y = 0; this.prevPos.y = 0; }
    if (this.pos.y < 0) { this.pos.y = height; this.prevPos.y = height; }
  }
  
  show() {
    stroke(0, 10);
    strokeWeight(1);
    line(this.pos.x, this.pos.y, this.prevPos.x, this.prevPos.y);
  }
}
```

---

## L-Systems

### Grammar Structure

```
Axiom: Starting string
Rules: Replacement rules
Angle: Turning angle
Iterations: Recursion depth
```

### Classic L-Systems

**Fractal Tree**:
```
Axiom: F
Rules: F → FF+[+F-F-F]-[-F+F+F]
Angle: 25°
```

**Koch Snowflake**:
```
Axiom: F
Rules: F → F+F--F+F
Angle: 60°
```

**Sierpinski Triangle**:
```
Axiom: F-G-G
Rules: F → F-G+F+G-F, G → GG
Angle: 120°
```

### L-System Rendering

```javascript
// Interpret string as drawing commands
function render(sentence) {
  for (let char of sentence) {
    switch(char) {
      case 'F':
        line(0, 0, 0, -len);
        translate(0, -len);
        break;
      case '+':
        rotate(angle);
        break;
      case '-':
        rotate(-angle);
        break;
      case '[':
        push();
        break;
      case ']':
        pop();
        break;
    }
  }
}
```

---

## Fractals

### Mandelbrot Set

```javascript
function mandelbrot(x, y, maxIter) {
  let real = x;
  let imag = y;
  
  for (let i = 0; i < maxIter; i++) {
    let tempReal = real * real - imag * imag + x;
    imag = 2 * real * imag + y;
    real = tempReal;
    
    if (real * real + imag * imag > 4) {
      return i;
    }
  }
  return maxIter;
}
```

### Julia Set

Same iteration, different starting point:
```javascript
function julia(x, y, cx, cy, maxIter) {
  let real = x;
  let imag = y;
  
  for (let i = 0; i < maxIter; i++) {
    let tempReal = real * real - imag * imag + cx;
    imag = 2 * real * imag + cy;
    real = tempReal;
    
    if (real * real + imag * imag > 4) {
      return i;
    }
  }
  return maxIter;
}
```

### Recursive Subdivision

```javascript
function subdivide(x, y, w, h, depth) {
  if (depth === 0 || w < 2 || h < 2) {
    rect(x, y, w, h);
    return;
  }
  
  let splitH = random() > 0.5;
  
  if (splitH) {
    let split = random(0.3, 0.7) * w;
    subdivide(x, y, split, h, depth - 1);
    subdivide(x + split, y, w - split, h, depth - 1);
  } else {
    let split = random(0.3, 0.7) * h;
    subdivide(x, y, w, split, depth - 1);
    subdivide(x, y + split, w, h - split, depth - 1);
  }
}
```

---

## Particle Systems

### Basic Particle

```javascript
class Particle {
  constructor(x, y) {
    this.pos = createVector(x, y);
    this.vel = p5.Vector.random2D().mult(random(1, 3));
    this.acc = createVector(0, 0);
    this.lifespan = 255;
    this.size = random(5, 15);
  }
  
  applyForce(force) {
    this.acc.add(force);
  }
  
  update() {
    this.vel.add(this.acc);
    this.pos.add(this.vel);
    this.acc.mult(0);
    this.lifespan -= 2;
  }
  
  isDead() {
    return this.lifespan <= 0;
  }
  
  show() {
    noStroke();
    fill(255, this.lifespan);
    ellipse(this.pos.x, this.pos.y, this.size);
  }
}
```

### Forces

```javascript
// Gravity
let gravity = createVector(0, 0.1);
particle.applyForce(gravity);

// Attraction to point
function attract(target, particle, strength) {
  let force = p5.Vector.sub(target, particle.pos);
  let distance = constrain(force.mag(), 5, 25);
  force.normalize();
  let magnitude = strength / (distance * distance);
  force.mult(magnitude);
  return force;
}

// Repulsion
function repel(target, particle, strength) {
  return attract(target, particle, -strength);
}
```

---

## Color Algorithms

### Palette Generation

```javascript
// Complementary
function complementary(hue) {
  return [(hue + 180) % 360];
}

// Triadic
function triadic(hue) {
  return [(hue + 120) % 360, (hue + 240) % 360];
}

// Analogous
function analogous(hue, spread = 30) {
  return [(hue - spread + 360) % 360, (hue + spread) % 360];
}

// Split complementary
function splitComplementary(hue) {
  return [(hue + 150) % 360, (hue + 210) % 360];
}
```

### Color Interpolation

```javascript
// Lerp between colors
function lerpColor(c1, c2, t) {
  colorMode(HSB);
  return color(
    lerp(hue(c1), hue(c2), t),
    lerp(saturation(c1), saturation(c2), t),
    lerp(brightness(c1), brightness(c2), t)
  );
}

// Palette from noise
function noiseColor(t, palette) {
  let n = noise(t) * (palette.length - 1);
  let i = floor(n);
  let f = n - i;
  return lerpColor(palette[i], palette[i + 1], f);
}
```

---

## Pattern Algorithms

### Truchet Tiles

```javascript
function truchetTile(x, y, size, type) {
  push();
  translate(x, y);
  
  if (type === 0) {
    arc(0, 0, size, size, 0, HALF_PI);
    arc(size, size, size, size, PI, PI + HALF_PI);
  } else {
    arc(size, 0, size, size, HALF_PI, PI);
    arc(0, size, size, size, PI + HALF_PI, TWO_PI);
  }
  
  pop();
}
```

### Voronoi

```javascript
// Simple Voronoi via distance check
function voronoi(points) {
  for (let x = 0; x < width; x++) {
    for (let y = 0; y < height; y++) {
      let closest = 0;
      let minDist = Infinity;
      
      for (let i = 0; i < points.length; i++) {
        let d = dist(x, y, points[i].x, points[i].y);
        if (d < minDist) {
          minDist = d;
          closest = i;
        }
      }
      
      stroke(points[closest].color);
      point(x, y);
    }
  }
}
```

---

## Seeded Randomness

```javascript
// Use seed for reproducibility
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);

// Or generate from string
function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash) + str.charCodeAt(i);
    hash = hash & hash;
  }
  return hash;
}

randomSeed(hashCode("my-artwork-2024"));
```

---

## Creative Coding Tools

| Tool | Language | Best For |
|------|----------|----------|
| p5.js | JavaScript | Beginners, web |
| Processing | Java | Desktop, print |
| Three.js | JavaScript | 3D, WebGL |
| TouchDesigner | Visual | Real-time, AV |
| Hydra | JavaScript | Live visuals |
| Shadertoy | GLSL | GPU shaders |
| Nannou | Rust | Performance |

---

---

## Related Skills

### Complementary Skills (Use Together)
- **[algorithmic-art](../algorithmic-art/)** - Complete workflow for creating interactive p5.js generative art
- **[canvas-design](../canvas-design/)** - Canvas API patterns for custom rendering
- **[theme-factory](../theme-factory/)** - Design color palettes and visual themes

### Alternative Skills (Similar Purpose)
- **[three-js-interactive-builder](../three-js-interactive-builder/)** - For 3D generative art with Three.js

### Prerequisite Skills (Learn First)
- None required - includes foundational creative coding patterns

---

## References

- `references/noise-recipes.md` - Noise function patterns
- `references/color-palettes.md` - Curated color schemes
- `references/shader-patterns.md` - GLSL snippets
