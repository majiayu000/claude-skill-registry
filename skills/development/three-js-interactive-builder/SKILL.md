---
name: three-js-interactive-builder
description: Scaffold and build interactive 3D visualizations using Three.js with emphasis on algorithmic art, sacred geometry, temporal animations, and modular architecture. Use when creating WebGL visualizations, generative art pieces, interactive 3D experiences, particle systems, flow fields, or projects like gravitational spirals, temporal perspective pieces, or illuminated visual narratives. Triggers on requests for Three.js projects, 3D web graphics, algorithmic visualizations, or sacred geometry renders.
license: MIT
---

# Three.js Interactive Builder

Build production-ready Three.js visualizations with algorithmic art principles.

## Core Architecture

Every project follows modular synthesis philosophy: components as oscillators, connections as patches.

```
project/
├── index.html          # Entry point with canvas
├── src/
│   ├── main.js         # Scene orchestrator
│   ├── geometry/       # Shape generators
│   ├── animation/      # Temporal controllers
│   ├── shaders/        # GLSL programs
│   └── utils/          # Math helpers
└── assets/             # Textures, fonts
```

## Quick Start

1. Copy boilerplate from `assets/threejs-boilerplate/`
2. Initialize scene with preferred renderer settings
3. Add geometry generators from `scripts/`
4. Wire animation loops

## Geometry Patterns

### Sacred Geometry Primitives

Use `scripts/sacred_geometry.py` to generate vertex data for:
- **Flower of Life**: Overlapping circles, customizable depth
- **Metatron's Cube**: 13-circle formation with connecting lines
- **Sri Yantra**: 9 interlocking triangles
- **Seed of Life**: 7-circle genesis pattern
- **Vesica Piscis**: Intersection geometry

### Spiral Systems

For gravitational/golden spirals:

```javascript
function goldenSpiral(loops, pointsPerLoop, scale) {
  const phi = (1 + Math.sqrt(5)) / 2;
  const points = [];
  for (let i = 0; i < loops * pointsPerLoop; i++) {
    const theta = i * 0.1;
    const r = scale * Math.pow(phi, theta / (2 * Math.PI));
    points.push(new THREE.Vector3(r * Math.cos(theta), r * Math.sin(theta), 0));
  }
  return points;
}
```

### Lane Systems

For multi-lane visualizations (soul lanes, data streams):

```javascript
function createLaneSystem(laneCount, radius, spacing) {
  const lanes = [];
  for (let i = 0; i < laneCount; i++) {
    lanes.push({ radius: radius + (i * spacing), objects: [], speed: 1 / (i + 1) });
  }
  return lanes;
}
```

## Animation Patterns

### Temporal Perspective

For simultaneous time visualization (all moments visible at once):

```javascript
class TemporalController {
  constructor(timeline) {
    this.moments = timeline;
    this.currentView = 'linear';
  }
  setSimultaneous() {
    this.moments.forEach((m, i) => {
      m.mesh.visible = true;
      m.mesh.material.opacity = 0.3 + (0.7 * (i / this.moments.length));
    });
  }
}
```

### Breath-Based Animation

Organic pulsing using sine waves:

```javascript
function breathe(object, speed = 1, amplitude = 0.1) {
  const scale = 1 + Math.sin(Date.now() * 0.001 * speed) * amplitude;
  object.scale.setScalar(scale);
}
```

## Shader Patterns

See `references/glsl-patterns.md` for glow effects, noise functions, color gradients, and symbol rendering.

## Project Types

**Algorithmic Art**: Define rules → Generate geometry → Add temporal dimension → Apply aesthetic layer

**Interactive Visualization**: OrbitControls → Raycasting → UI overlay → State management

**Narrative Experience**: Story beats as states → Transitions → Audio cues → Navigation

## Performance

- BufferGeometry for >1000 vertices
- InstancedMesh for repeated objects
- LOD for complex scenes
- Merge geometries to reduce draw calls

## References

- `references/glsl-patterns.md` - Shader code library
- `references/sacred-geometry-math.md` - Mathematical foundations
