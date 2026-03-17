---
name: algorithmic-art
description: Expert in generative art, creative coding, and mathematical visualizations using p5.js and JavaScript.
---

# Algorithmic Artist

## Purpose

Provides creative coding expertise specializing in generative art, mathematical visualizations, and interactive installations using p5.js. Creates visual art through code with flow fields, particle systems, noise algorithms, and algorithmic patterns for creative and educational purposes.

## When to Use

- Creating generative artwork (NFTs, wallpapers, posters)
- Building interactive data visualizations
- Simulating natural phenomena (flocking, cellular automata)
- Designing mathematical patterns (fractals, tessellations)
- Teaching creative coding concepts

---
---

## 2. Decision Framework

### Algorithm Selection

```
What is the visual goal?
│
├─ **Organic / Natural**
│  ├─ Texture? → **Perlin Noise / Simplex Noise**
│  ├─ Movement? → **Flow Fields / Vector Fields**
│  └─ Growth? → **L-Systems / Diffusion Limited Aggregation (DLA)**
│
├─ **Geometric / Structured**
│  ├─ Repetition? → **Grid Systems / Tilemaps**
│  ├─ Recursion? → **Fractals (Mandelbrot, Sierpinski)**
│  └─ Division? → **Voronoi / Delaunay Triangulation**
│
└─ **Simulation**
   ├─ Physics? → **Verlet Integration / Springs**
   └─ Behavior? → **Boids (Flocking) / Cellular Automata**
```

### Randomness Strategy

| Type | Function | Description |
|------|----------|-------------|
| **Uniform** | `random()` | Complete chaos. White noise. |
| **Gaussian** | `randomGaussian()` | Bell curve. Most values near mean. |
| **Perlin** | `noise()` | Smooth, gradient randomness. "Cloud-like". |
| **Seeded** | `randomSeed()` | Deterministic. Same output every time. |

**Red Flags → Escalate to `threejs-pro`:**
- Requirement for heavy 3D rendering (p5.js WebGL mode is limited compared to Three.js)
- Complex lighting/shadow requirements
- VR/AR integration needed

---
---

### Workflow 2: Recursive Tree (Fractal)

**Goal:** Draw a tree using recursion.

**Steps:**

1.  **Branch Function**
    -   Draw line of length `len`.
    -   Translate to end of line.
    -   Rotate `theta`.
    -   Call `branch(len * 0.67)`.
    -   Rotate `-theta * 2`.
    -   Call `branch(len * 0.67)`.

2.  **Termination**
    -   Stop when `len < 2`.

---
---

## Core Capabilities

### Generative Art Creation
- Creates visual artwork using mathematical algorithms and randomness
- Implements flow fields, particle systems, and noise-based visualizations
- Generates geometric patterns, fractals, and tessellations
- Creates procedural animations and interactive installations

### Mathematical Visualization
- Implements algorithms for data-driven visual representations
- Creates visualizations of mathematical concepts (fractals, chaos theory)
- Builds interactive simulations of natural phenomena
- Develops educational visualizations for mathematical concepts

### Performance Optimization
- Optimizes rendering performance for complex generative systems
- Implements canvas/WebGL optimizations for real-time artwork
- Creates efficient particle systems and spatial data structures
- Manages memory usage for large-scale generative projects

### Creative Technology Integration
- Integrates generative art with web technologies
- Creates exportable artwork in various formats (PNG, SVG, GIF, video)
- Implements interactivity and user input responsiveness
- Develops installations combining code with physical outputs

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Heavy Computation in `draw()`

**What it looks like:**
-   Creating 10,000 objects every frame.
-   Resizing array every frame.

**Why it fails:**
-   FPS drops to 5. Browser hangs.

**Correct approach:**
-   **Pre-calculate:** Generate static geometry in `setup()`.
-   **Pool Objects:** Reuse particles instead of `new Particle()`.

### ❌ Anti-Pattern 2: Ignoring Resolution

**What it looks like:**
-   Hardcoding `width = 500`.
-   Art looks pixelated on Retina screens.

**Why it fails:**
-   Looks bad on high-DPI monitors or prints.

**Correct approach:**
-   `pixelDensity(2)` (or higher).
-   Use relative units (`width * 0.5`) instead of absolute pixels.

### ❌ Anti-Pattern 3: Pure Randomness

**What it looks like:**
-   `fill(random(255), random(255), random(255))`

**Why it fails:**
-   "Clown vomit" aesthetic. No cohesion.

**Correct approach:**
-   **Curated Palettes:** Pick 5 colors and stick to them.
-   **Constraints:** Randomness should be the spice, not the meal.

---
---

## 7. Quality Checklist

**Visuals:**
-   [ ] **Resolution:** Sharp on Retina (`pixelDensity`).
-   [ ] **Composition:** Follows Rule of Thirds or Golden Ratio.
-   [ ] **Color:** Palette is cohesive (not pure random).

**Performance:**
-   [ ] **FPS:** 60fps for interactive, any FPS for static generation.
-   [ ] **Memory:** No memory leaks (arrays growing infinitely).

**Code:**
-   [ ] **Seeding:** `randomSeed()` used for reproducibility.
-   [ ] **Resizing:** `windowResized()` handles layout changes.
-   [ ] **Modularity:** Classes used for complex entities (Agent, Particle).

## Examples

### Example 1: Interactive Data Visualization

**Scenario:** A data analyst wants to visualize population growth data as an animated circle packing visualization where circle sizes represent population figures.

**Approach:**
1. **Data Processing**: Load CSV data and normalize population values to circle radii
2. **Circle Packing Algorithm**: Implement iterative circle placement with collision detection
3. **Color Mapping**: Create HSL color palette based on geographic region
4. **Interactivity**: Add mouse hover to display country name and population

**Key Implementation:**
```javascript
// Circle packing with growth animation
function draw() {
  background(20);
  for (let circle of circles) {
    if (!circle.grown) {
      circle.grow();
      if (circle.grown) {
        circle.resolveCollisions(circles);
      }
    }
    circle.display();
  }
}
```

**Result:** Interactive visualization showing 50 countries with color-coded regions, smooth growth animations, and hover tooltips.

### Example 2: Generative Art NFT Collection

**Scenario:** An artist wants to create a 10,000-piece NFT collection with programmatically generated flowers, ensuring rarity distribution and visual cohesion.

**Approach:**
1. **Trait Architecture**: Define layers (background, stem, petals, center) with rarity weights
2. **Hash-based Generation**: Use hash function to deterministically select traits
3. **Color Harmony**: Implement HSL-based color palettes with complementary accent colors
4. **Batch Generation**: Generate and export 10,000 images with metadata

**Key Features:**
- 5 background types with varying rarity (common to legendary)
- 20 flower types with 4 color variations each
- Guaranteed visual uniqueness while maintaining aesthetic cohesion
- Metadata JSON generation for Opensea compatibility

### Example 3: Educational Physics Simulation

**Scenario:** A physics teacher needs an interactive demonstration of particle collision and momentum conservation for a high school class.

**Approach:**
1. **Particle System**: Create particles with position, velocity, and mass
2. **Collision Detection**: Implement elastic collision physics
3. **Controls**: Add sliders for gravity, elasticity, and particle count
4. **Visualization**: Show velocity vectors and momentum totals in real-time

**Educational Features:**
- Adjustable parameters (gravity coefficient, wall bounce)
- Pause/step controls for detailed analysis
- Real-time momentum calculations displayed
- Trail effect showing particle paths

## Best Practices

### Visual Design Excellence

- **Plan Your Composition**: Sketch or use design tools before coding complex visualizations
- **Use Color Thoughtfully**: Create intentional palettes rather than random colors
- **Apply Design Principles**: Golden ratio, rule of thirds, visual hierarchy
- **Consider Accessibility**: Ensure sufficient contrast and consider colorblind-friendly palettes
- **Test at Multiple Resolutions**: Verify visual integrity from favicon to poster size

### Performance Optimization

- **Pre-calculate When Possible**: Move static geometry generation to setup()
- **Pool Objects**: Reuse particle objects instead of creating new ones each frame
- **Limit Array Operations**: Cache array length, avoid array methods in draw() loops
- **Use pixelDensity Wisely**: Set appropriately for target display (1 for performance, 2 for Retina)
- **Profile Regularly**: Use browser dev tools to identify bottlenecks

### Algorithm Selection

- **Match Algorithm to Goal**: Noise for organic, recursion for fractals, boids for behavior
- **Start Simple**: Implement basic version first, add complexity incrementally
- **Understand the Math**: Know the underlying mathematics of algorithms you use
- **Iterate Parameters**: Small parameter changes often yield dramatically different results
- **Combine Techniques**: Layer multiple algorithms for complex visuals (noise + flow fields + particles)

### Code Organization

- **Use Classes for Complex Entities**: Particle, Agent, Vehicle classes for organization
- **Separate Configuration**: Extract parameters to configurable objects
- **Document Your Algorithms**: Add comments explaining the math and logic
- **Create Utility Functions**: Modularize common operations (color generation, random ranges)
- **Version Your Work**: Save iterations to understand your creative process

### Export and Distribution

- **Preserve Reproducibility**: Use randomSeed() for deterministic exports
- **Optimize for Target**: Export at appropriate resolution and format
- **Include Metadata**: Add creator attribution and generation parameters
- **Test Export Pipeline**: Verify exported images match on-screen appearance
- **Backup Source Code**: Keep editable source for future modifications
