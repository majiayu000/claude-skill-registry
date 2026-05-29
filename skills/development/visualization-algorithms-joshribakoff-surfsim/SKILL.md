---
name: visualization-algorithms
description: Evaluate and implement visualization algorithms for ocean/foam rendering. Use when discussing rendering techniques, contour algorithms, performance optimization for graphics, or evaluating algorithm tradeoffs. Auto-apply when editing files in src/render/.
---

# Visualization Algorithms Skill

This project renders ocean waves and foam using Canvas 2D with custom algorithms. Apply this skill when evaluating or implementing visualization approaches.

## Current Algorithm: Marching Squares

Location: `src/render/marchingSquares.js`

### How It Works

1. **Build intensity grid** from foam row data
2. **Apply box blur** to smooth the data
3. **Extract contours** at threshold levels
4. **Render** as lines or filled shapes

```
Foam Rows → Intensity Grid → Blur → Marching Squares → Contours → Canvas
```

### Key Functions

| Function | Purpose |
|----------|---------|
| `buildIntensityGrid()` | Convert foam rows to 2D grid |
| `boxBlur()` | Smooth grid with 3x3 kernel |
| `extractContours()` | Trace closed contour paths |
| `extractLineSegments()` | Get raw line segments (debug) |
| `renderMultiContour()` | Multi-threshold nested rings |

### Dispersion Options (A/B/C)

Three approaches for foam dispersion over time:

**Option A: Expanding Segment Bounds**
- Segment bounds expand outward over time
- Core intensity fades faster than edges
- Creates halo effect around original foam

**Option B: Age-Based Blur**
- More blur passes as foam ages
- Simpler but affects all foam uniformly
- Good for performance

**Option C: Per-Row Dispersion Radius**
- Each row tracks individual expansion
- Spreads in X and Y directions
- Most physically accurate

## Algorithm Evaluation Criteria

When comparing visualization algorithms, consider:

### 1. Visual Quality
- Smoothness of contours
- Natural appearance of foam dispersion
- Correct representation of physics (energy dissipation)

### 2. Performance
- Target: 16ms frame budget (60fps)
- Grid resolution tradeoffs (80x60 default)
- Blur pass count vs. quality

### 3. Configurability
- Threshold levels for contour density
- Color/opacity mapping
- Animation parameters

### 4. Debugging
- Can render raw line segments for inspection
- Multi-threshold shows algorithm behavior
- Stories in Ladle for visual comparison

## Performance Optimization Patterns

### Grid Resolution
```javascript
// Lower resolution = faster, less detail
const gridW = 80;  // Default
const gridH = 60;

// For mobile/low-end: 40x30
// For high quality: 120x90
```

### Blur Optimization
```javascript
// Box blur is O(n) per pixel with separable passes
// Multiple passes approximate Gaussian blur
const blurPasses = 2;  // Default - good balance
```

### Typed Arrays
```javascript
// Use Float32Array for grid data
const grid = new Float32Array(gridW * gridH);
```

## Stories for Visual Testing

Located in `src/stories/FoamRendering.stories.jsx`:

| Story | Purpose |
|-------|---------|
| `Zones Early/Mid/Late Wave` | Wave lifecycle stages |
| `Samples Early/Mid Wave` | Algorithm comparison |
| `Comparison Mid Wave` | Side-by-side options |
| `Small/Large Wave` | Size variations |
| `Zones T0-T35` | Animation frames |

## When Evaluating New Algorithms

1. **Create a story** for visual comparison
2. **Benchmark performance** with perf tests
3. **Test edge cases**: empty data, single row, many rows
4. **Compare to physics** expectations from `00-principles.md`
5. **Document tradeoffs** in a plan document

## Alternative Algorithms to Consider

### Metaballs / Implicit Surfaces
- Smoother organic shapes
- Higher computational cost
- Better for sparse data

### SDF (Signed Distance Fields)
- Resolution-independent
- GPU-friendly
- More complex implementation

### Particle Systems
- Individual foam bubbles
- Very expensive at scale
- Most realistic appearance

### Noise-Based
- Procedural detail
- Good for texture, not structure
- Can augment other methods

## Reference Files

- `plans/visuals/60-foam-effects.md` - Foam design
- `plans/visuals/132-foam-rendering-layers.md` - Layered approach
- `plans/visuals/foam-dispersion-v2-tests.md` - Dispersion testing
- `plans/00-principles.md` - Physics basis for visual behavior
