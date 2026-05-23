---
name: ta-procedural-terrain
description: Procedural terrain generation algorithms and techniques for Three.js/R3F. Research-based skill with patterns from THREE.Terrain, Nathan Pointer's landscape rendering, and academic papers.
category: shader
---

# Procedural Terrain Generation Skill

> "Research-backed algorithms for creating natural, playable terrain in multiplayer games."

## Overview

This skill consolidates research from multiple sources on procedural terrain generation:
- **THREE.Terrain** library (IceCreamYou/THREE.Terrain) - Comprehensive procedural terrain engine
- **Nathan Pointer's landscape rendering** - Production techniques for semi-realistic browser terrain
- **Academic research** - FBM, Perlin/Simplex noise, Diamond-Square algorithms

## When to Use This Skill

Use when your task involves:
- Creating procedural heightmap generators
- Implementing terrain generation algorithms (Perlin, Simplex, Diamond-Square)
- Building caldera/crater terrain with radial patterns
- Multi-pass noise composition for detail
- Terrain filtering and smoothing
- Height-based vertex coloring

## Core Concepts

### 1. Heightmap Representation

```typescript
// Heightmap as Float32Array - most efficient for WebGL
type Heightmap = Float32Array;  // [0, 1] or actual heights

// 2D access pattern
function getAt(heightmap: Float32Array, x: number, z: number, size: number): number {
  return heightmap[z * size + x];
}

function setAt(heightmap: Float32Array, x: number, z: number, size: number, value: number): void {
  heightmap[z * size + x] = value;
}
```

### 2. Noise Fundamentals

#### Perlin Noise (Classic)

```typescript
// Using Three.js ImprovedNoise
import { ImprovedNoise } from 'three/examples/jsm/math/ImprovedNoise.js';

const noise = new ImprovedNoise();
const value = noise.noise(x, y, z);  // Returns [-1, 1]
```

#### Simplex Noise (Faster, Less Directional Artifacts)

```typescript
// Simplex is ~10% faster than Perlin
// Better dimensional scaling
// Fewer directional artifacts
```

#### FBM (Fractal Brownian Motion)

```typescript
/**
 * FBM stacks multiple octaves of noise:
 * - Low frequency: Large terrain shapes (hills, valleys)
 * - High frequency: Small details (bumps, texture)
 */
function fbm(
  x: number, z: number,
  octaves: number,
  persistence: number,
  lacunarity: number,
  noise: ImprovedNoise
): number {
  let total = 0;
  let frequency = 1;
  let amplitude = 1;
  let maxValue = 0;

  for (let i = 0; i < octaves; i++) {
    total += noise.noise(x * frequency, z * frequency, 0) * amplitude;
    maxValue += amplitude;
    amplitude *= persistence;     // Amplitude decay (0.5)
    frequency *= lacunarity;      // Frequency increase (2.0)
  }

  return total / maxValue;  // Normalize to [-1, 1]
}
```

### 3. Generation Algorithms

#### Diamond-Square (Classic Heightmap)

```typescript
/**
 * Diamond-Square Algorithm
 * Good for: Self-similar terrain, fractal appearance
 * Time: O(n log n) where n = grid size
 *
 * Based on: https://github.com/IceCreamYou/THREE.Terrain
 */
function diamondSquare(
  size: number,     // Must be power of 2 + 1
  maxHeight: number,
  roughness: number  // Height randomness (0-1)
): Float32Array {
  const segments = Math.pow(2, Math.ceil(Math.log2(size - 1)));
  const gridSize = segments + 1;
  const heightmap = new Float32Array(gridSize * gridSize);
  const smoothing = maxHeight * 2;

  // Initialize corners
  heightmap[0] = Math.random() * maxHeight;
  heightmap[gridSize - 1] = Math.random() * maxHeight;
  heightmap[(gridSize - 1) * gridSize] = Math.random() * maxHeight;
  heightmap[gridSize * gridSize - 1] = Math.random() * maxHeight;

  for (let step = segments; step >= 2; step /= 2) {
    const half = step / 2;
    smoothing /= 2;

    // Diamond step
    for (let x = 0; x < segments; x += step) {
      for (let z = 0; z < segments; z += step) {
        const avg = (
          heightmap[z * gridSize + x] +
          heightmap[z * gridSize + x + step] +
          heightmap[(z + step) * gridSize + x] +
          heightmap[(z + step) * gridSize + x + step]
        ) / 4;
        const center = (z + half) * gridSize + (x + half);
        heightmap[center] = avg + (Math.random() * 2 - 1) * smoothing;
      }
    }

    // Square step
    for (let x = 0; x <= segments; x += half) {
      for (let z = (x + half) % step; z <= segments; z += step) {
        let count = 0;
        let sum = 0;

        // Sample neighbors
        const neighbors = [
          [x - half, z], [x + half, z],
          [x, z - half], [x, z + half]
        ];

        for (const [nx, nz] of neighbors) {
          if (nx >= 0 && nx <= segments && nz >= 0 && nz <= segments) {
            sum += heightmap[nz * gridSize + nx];
            count++;
          }
        }

        heightmap[z * gridSize + x] = sum / count + (Math.random() * 2 - 1) * smoothing;
      }
    }
  }

  return heightmap;
}
```

#### Perlin Layers (Multi-Octave)

```typescript
/**
 * Perlin Layers - Multiple Perlin passes at different frequencies
 * Good for: Natural-looking hills and mountains
 */
function perlinLayers(config: {
  size: number,
  maxHeight: number,
  seed: number
}): Float32Array {
  const { size, maxHeight, seed } = config;
  const noise = new ImprovedNoise();
  const heightmap = new Float32Array(size * size);

  // Layer 1: Base terrain (large features)
  for (let z = 0; z < size; z++) {
    for (let x = 0; x < size; x++) {
      let height = 0;

      // Octave 1: Large shapes (frequency: 1.25)
      height += noise.noise(x * 0.01 + seed, z * 0.01 + seed, 0) * 0.5 * maxHeight;

      // Octave 2: Medium detail (frequency: 2.5)
      height += noise.noise(x * 0.02 + seed, z * 0.02 + seed, 0) * 0.25 * maxHeight;

      // Octave 3: Fine detail (frequency: 5.0)
      height += noise.noise(x * 0.05 + seed, z * 0.05 + seed, 0) * 0.125 * maxHeight;

      // Octave 4: Micro detail (frequency: 10.0)
      height += noise.noise(x * 0.1 + seed, z * 0.1 + seed, 0) * 0.0625 * maxHeight;

      heightmap[z * size + x] = (height / maxHeight + 1) * 0.5 * maxHeight;
    }
  }

  return heightmap;
}
```

#### Fault Lines (Dramatic Terrain)

```typescript
/**
 * Fault Line Algorithm
 * Good for: Canyons, cliffs, dramatic elevation changes
 *
 * Based on: http://www.lighthouse3d.com/opengl/terrain/index.php3?fault
 */
function faultLines(config: {
  size: number,
  maxHeight: number,
  iterations: number
}): Float32Array {
  const { size, maxHeight, iterations } = config;
  const heightmap = new Float32Array(size * size);
  const displacement = maxHeight / iterations / 2;
  const d = Math.sqrt(size * size * 2);  // Diagonal distance

  for (let k = 0; k < iterations; k++) {
    const v = Math.random();
    const a = Math.sin(v * Math.PI * 2);   // Random direction
    const b = Math.cos(v * Math.PI * 2);
    const c = Math.random() * d - d / 2;   // Random offset

    for (let z = 0; z < size; z++) {
      for (let x = 0; x < size; x++) {
        const distance = a * x + b * z - c;
        const idx = z * size + x;

        if (distance > 0) {
          heightmap[idx] += displacement;
        } else {
          heightmap[idx] -= displacement;
        }
      }
    }
  }

  return normalize(heightmap, 0, maxHeight);
}
```

#### Hill/Radial Deposition

```typescript
/**
 * Hill Algorithm
 * Good for: Rolling hills, islands, organic shapes
 *
 * Based on: THREE.Terrain.Hill
 */
function hillAlgorithm(config: {
  size: number,
  maxHeight: number,
  numHills: number
}): Float32Array {
  const { size, maxHeight, numHills } = config;
  const heightmap = new Float32Array(size * size);

  for (let i = 0; i < numHills; i++) {
    // Random hill center
    const hx = Math.random() * size;
    const hz = Math.random() * size;

    // Random radius and height
    const radius = 5 + Math.random() * 15;
    const hillHeight = maxHeight * (0.1 + Math.random() * 0.2);

    // Apply hill to heightmap
    for (let z = 0; z < size; z++) {
      for (let x = 0; x < size; x++) {
        const dist = Math.sqrt((x - hx) ** 2 + (z - hz) ** 2);
        if (dist < radius) {
          // Cosine hill shape
          const t = dist / radius;
          const influence = (Math.cos(t * Math.PI) + 1) / 2;
          heightmap[z * size + x] += hillHeight * influence;
        }
      }
    }
  }

  return normalize(heightmap, 0, maxHeight);
}
```

### 4. Caldera/Crater Terrain

```typescript
/**
 * Generate Caldera/Crater Terrain
 * Creates a volcanic caldera topology with:
 * - Central water body (deep depression below water level)
 * - Steep rising walls around the center
 * - Dramatic crater rim with directional ridges (starburst pattern)
 * - Rugged outer mountains
 *
 * @param size Grid size (128 = 128x128 heightmap)
 * @param maxHeight Maximum terrain height in meters
 * @param waterLevel Water level in meters (typically 4-5m)
 * @param seed Random seed for noise variation
 */
function generateCaldera(
  size: number,
  maxHeight: number,
  waterLevel: number,
  seed: number
): Float32Array {
  const noise = new ImprovedNoise();
  const heightmap = new Float32Array(size * size);
  const centerX = size / 2;
  const centerZ = size / 2;

  // Define ridge directions for "starburst" pattern (8 ridges radiating from center)
  const ridgeAngles = [
    0, Math.PI / 4, Math.PI / 2, 3 * Math.PI / 4,
    Math.PI, 5 * Math.PI / 4, 3 * Math.PI / 2, 7 * Math.PI / 4
  ];

  for (let z = 0; z < size; z++) {
    for (let x = 0; x < size; x++) {
      // Normalized distance from center (0 at center, ~1.4 at corners)
      const dx = (x - centerX) / (size / 2);
      const dz = (z - centerZ) / (size / 2);
      const dist = Math.sqrt(dx * dx + dz * dz);

      // Calculate angle from center for directional variation
      const angle = Math.atan2(dz, dx); // -PI to PI

      // Calculate directional multiplier for ridges (starburst pattern)
      let ridgeMultiplier = 1.0;
      for (const ridgeAngle of ridgeAngles) {
        const angleDiff = Math.abs(angle - ridgeAngle);
        const angleDiffAlt = Math.abs(angle - (ridgeAngle + Math.PI));
        const minDiff = Math.min(angleDiff, angleDiffAlt);
        // Gaussian-like bump centered on ridge direction
        ridgeMultiplier += Math.exp(-minDiff * minDiff * 3) * 0.4;
      }

      // Caldera zone definitions (normalized distance)
      const craterFloorRadius = 0.25;    // Central lake floor
      const wallStartRadius = 0.25;      // Where steep walls begin
      const wallEndRadius = 0.45;        // Where walls end, rim begins
      const rimPeakRadius = 0.55;        // Peak of crater rim
      const outerSlopeStart = 0.60;      // Start of outer mountains

      let height = 0;

      if (dist < craterFloorRadius) {
        // CENTRAL CRATER LAKE (deep depression)
        const t = dist / craterFloorRadius;
        const bowlShape = t * t;
        const depthBelowWater = 3.0; // meters
        height = (waterLevel - depthBelowWater + bowlShape * depthBelowWater) / maxHeight;

        // Add subtle variation to lake floor
        height += noise.noise(x * 0.15 + seed, z * 0.15 + seed, 0) * 0.03;

      } else if (dist < wallEndRadius) {
        // CRATER WALLS (steep rise from lake)
        const t = (dist - wallStartRadius) / (wallEndRadius - wallStartRadius);
        const wallShape = t * t * (3 - 2 * t); // Smoothstep
        const baseHeight = waterLevel / maxHeight + wallShape * 0.7;

        // Add directional ridge variation
        height = baseHeight * ridgeMultiplier;

        // Add rugged noise to walls
        const wallNoise = fbm(x, z, 4, 0.5, 2.0, noise);
        height += wallNoise * 0.15 * t;

      } else if (dist < outerSlopeStart) {
        // CRATER RIM (highest point with ridges)
        const t = (dist - wallEndRadius) / (outerSlopeStart - wallEndRadius);
        const normalizedDist = (dist - wallEndRadius) / (rimPeakRadius - wallEndRadius);
        const domeShape = Math.max(0, 1 - normalizedDist * normalizedDist * 4);

        height = 0.85 + domeShape * 0.25; // Base rim height

        // Strong directional variation for starburst ridges
        height *= ridgeMultiplier;

        // Add rocky detail
        height += noise.noise(x * 0.1, z * 0.1, seed + 50) * 0.08;

      } else {
        // OUTER MOUNTAINS (descending from rim)
        const t = (dist - outerSlopeStart) / (1.0 - outerSlopeStart);
        const slopeShape = Math.exp(-t * 2.5) * 0.6;

        height = 0.3 + slopeShape;

        // Add mountain noise
        const mountainNoise = fbm(x, z, 5, 0.5, 2.0, noise);
        height += mountainNoise * 0.4;

        // Preserve some ridge structure in outer mountains
        height *= (0.7 + ridgeMultiplier * 0.3);

        // Add variation
        height += noise.noise(x * 0.05, z * 0.05, seed + 100) * 0.1;
      }

      // Add base FBM noise for overall terrain detail
      const baseNoise = fbm(x, z, 4, 0.5, 2.0, noise);
      height += baseNoise * 0.08;

      // Clamp and scale
      height = Math.max(0, Math.min(1, height));
      heightmap[z * size + x] = height * maxHeight;
    }
  }

  return heightmap;
}
```

### 5. Filtering and Smoothing

```typescript
/**
 * Clamping - Rescale heightmap to fit within range
 */
function clamp(
  heightmap: Float32Array,
  minHeight: number,
  maxHeight: number,
  stretch: boolean = true
): Float32Array {
  let min = Infinity;
  let max = -Infinity;

  // Find actual range
  for (let i = 0; i < heightmap.length; i++) {
    if (heightmap[i] < min) min = heightmap[i];
    if (heightmap[i] > max) max = heightmap[i];
  }

  const actualRange = max - min;
  const targetRange = maxHeight - minHeight;

  for (let i = 0; i < heightmap.length; i++) {
    const normalized = (heightmap[i] - min) / actualRange;
    if (stretch) {
      heightmap[i] = normalized * targetRange + minHeight;
    } else {
      heightmap[i] = Math.max(minHeight, Math.min(maxHeight, heightmap[i]));
    }
  }

  return heightmap;
}

/**
 * Smooth - Set each point to mean of neighbors
 */
function smooth(
  heightmap: Float32Array,
  size: number,
  weight: number = 0
): Float32Array {
  const smoothed = new Float32Array(heightmap.length);

  for (let z = 0; z < size; z++) {
    for (let x = 0; x < size; x++) {
      let sum = 0;
      let count = 0;

      // 3x3 neighborhood
      for (let nz = -1; nz <= 1; nz++) {
        for (let nx = -1; nx <= 1; nx++) {
          const cx = x + nx;
          const cz = z + nz;
          if (cx >= 0 && cx < size && cz >= 0 && cz < size) {
            sum += heightmap[cz * size + cx];
            count++;
          }
        }
      }

      const avg = sum / count;
      smoothed[z * size + x] = (avg + heightmap[z * size + x] * weight) / (1 + weight);
    }
  }

  return smoothed;
}

/**
 * Edges - Create island walls or borders
 */
function edges(
  heightmap: Float32Array,
  size: number,
  direction: 'up' | 'down',
  distance: number,
  easing: (t: number) => number = (t => t)
): Float32Array {
  const peak = direction === 'up' ? 24 : 0;
  const numSegments = Math.floor(distance / (256 / size)) || 1;
  const xl = size;
  const yl = size;

  for (let i = 0; i < xl; i++) {
    for (let j = 0; j < numSegments; j++) {
      const multiplier = easing(1 - j / numSegments);

      // Top edge
      const k1 = j * xl + i;
      heightmap[k1] = direction === 'up'
        ? Math.max(heightmap[k1], (peak - heightmap[k1]) * multiplier + heightmap[k1])
        : Math.min(heightmap[k1], (peak - heightmap[k1]) * multiplier + heightmap[k1]);

      // Bottom edge
      const k2 = (size - 1 - j) * xl + i;
      heightmap[k2] = direction === 'up'
        ? Math.max(heightmap[k2], (peak - heightmap[k2]) * multiplier + heightmap[k2])
        : Math.min(heightmap[k2], (peak - heightmap[k2]) * multiplier + heightmap[k2]);
    }
  }

  return heightmap;
}
```

### 6. Easing Functions

```typescript
/**
 * Common easing functions for terrain shaping
 * From: THREE.Terrain core.js
 */
const Easing = {
  Linear: (x: number) => x,

  // x^2 - accelerates from zero
  EaseIn: (x: number) => x * x,

  // -x(x-2) - decelerates to zero
  EaseOut: (x: number) => -x * (x - 2),

  // x^2(3-2x) - smooth S-curve
  EaseInOut: (x: number) => x * x * (3 - 2 * x),

  // 0.5*(2x-1)^3+0.5 - inverse S-curve
  InEaseOut: (x: number) => {
    const y = 2 * x - 1;
    return 0.5 * y * y * y + 0.5;
  },

  // x^1.55 - gentle ease-in
  EaseInWeak: (x: number) => Math.pow(x, 1.55),

  // x^7 - strong ease-in
  EaseInStrong: (x: number) => Math.pow(x, 7)
};
```

### 7. Multi-Pass Composition

```typescript
/**
 * MultiPass - Layer multiple generation methods
 * From: THREE.Terrain.MultiPass
 */
interface Pass {
  method: (heightmap: Float32Array, config: any) => Float32Array;
  amplitude?: number;  // Height multiplier
  frequency?: number;  // Noise frequency (if supported)
}

function multiPass(
  size: number,
  passes: Pass[],
  baseConfig: any
): Float32Array {
  let heightmap = new Float32Array(size * size);

  for (const pass of passes) {
    const amp = pass.amplitude ?? 1;
    const passConfig = { ...baseConfig, frequency: pass.frequency };

    // Generate this pass
    const passHeightmap = pass.method(new Float32Array(size * size), passConfig);

    // Add to result with amplitude
    for (let i = 0; i < heightmap.length; i++) {
      heightmap[i] += passHeightmap[i] * amp;
    }
  }

  return heightmap;
}

// Example: Layered terrain
const layeredTerrain = multiPass(128, [
  {
    method: (h) => perlinLayers({ size: 128, maxHeight: 24, seed: 42 }),
    amplitude: 1.0,
    frequency: 1.25
  },
  {
    method: (h) => perlinLayers({ size: 128, maxHeight: 24, seed: 43 }),
    amplitude: 0.5,
    frequency: 2.5
  },
  {
    method: (h) => perlinLayers({ size: 128, maxHeight: 24, seed: 44 }),
    amplitude: 0.25,
    frequency: 5.0
  }
], {});
```

### 8. Applying to Three.js Geometry

```typescript
/**
 * Apply heightmap to Three.js PlaneGeometry
 * Critical: Must recompute bounding sphere after vertex modification
 */
function applyHeightmapToGeometry(
  geometry: THREE.PlaneGeometry,
  heightmap: Float32Array,
  config: { mapSize: number; segments: number; maxHeight: number }
): void {
  const positions = geometry.attributes.position.array as Float32Array;
  const colors = new Float32Array(positions.length);
  const verticesPerRow = config.segments + 1;

  for (let i = 0; i < positions.length; i += 3) {
    const vertexIndex = i / 3;
    const row = Math.floor(vertexIndex / verticesPerRow);
    const col = vertexIndex % verticesPerRow;

    const heightmapIndex = row * verticesPerRow + col;
    const height = heightmap[heightmapIndex];

    // Apply height to Y coordinate (vertices[i + 1])
    positions[i + 1] = height;

    // Height-based coloring
    const color = getTerrainColor(height, config.maxHeight);
    colors[i] = color.r;
    colors[i + 1] = color.g;
    colors[i + 2] = color.b;
  }

  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.computeVertexNormals();

  // CRITICAL: Recompute bounding sphere after modifying vertices
  // Without this, frustum culling may incorrectly cull the entire mesh
  geometry.computeBoundingSphere();
}

function getTerrainColor(height: number, maxHeight: number): THREE.Color {
  const waterLevel = maxHeight * 0.1875;  // 4.5m / 24m

  if (height < waterLevel) {
    // Water gradient
    const depth = waterLevel - height;
    const t = Math.min(1, depth / waterLevel);
    const deepWater = new THREE.Color(0x1a5276);
    const shallowWater = new THREE.Color(0x2980b9);
    return new THREE.Color().lerpColors(shallowWater, deepWater, t);
  }
  if (height < maxHeight * 0.33) return new THREE.Color(0xc2b280);  // Sand
  if (height < maxHeight * 0.58) return new THREE.Color(0x4d7c0f);  // Grass
  if (height < maxHeight * 0.83) return new THREE.Color(0x6b5344);  // Dirt
  return new THREE.Color(0x8b7355);  // Rock
}
```

## Algorithm Selection Guide

| Desired Terrain | Best Algorithm | Parameters |
|----------------|----------------|------------|
| Rolling hills | Perlin Layers | octaves: 4, persistence: 0.5 |
| Mountains | Perlin + Fault | High frequency, high iterations |
| Crater/Caldera | Radial + FBM | Custom radial zones |
| Islands | Hill + Edges | numHills: 50+, edges: 'down' |
| Canyons | Fault Lines | iterations: 1000+ |
| Natural mixed | MultiPass | Layer multiple methods |

## Performance Considerations

### Triangle Count Budget

```typescript
// PlaneGeometry(256, 256, 128, 128)
// Non-indexed: 128 * 128 * 2 = 32,768 triangles
// This is within the <50K budget for terrain

// For larger maps, consider LOD
function getTerrainSegments(distance: number): number {
  if (distance < 50) return 128;   // High detail nearby
  if (distance < 100) return 64;   // Medium
  return 32;                        // Low detail far away
}
```

### Memory Optimization

```typescript
// Use Float32Array, not regular Array
const heightmap = new Float32Array(size * size);  // ~4x less memory

// Reuse noise instance
const noise = new ImprovedNoise();  // Create once, use many times

// Avoid creating temporary arrays in loops
```

## Common Issues and Solutions

### Terrain Looks Flat

**Cause:** Heightmap values not properly scaled or noise frequency too high.

**Fix:**
```typescript
// Check actual height range
const heights = Array.from(heightmap);
console.log('Height stats:', {
  min: Math.min(...heights),
  max: Math.max(...heights),
  avg: heights.reduce((a, b) => a + b, 0) / heights.length
});

// Use clamp to normalize
heightmap = clamp(heightmap, 0, maxHeight, true);
```

### Visible Grid Artifacts

**Cause:** Frequency too low relative to grid size.

**Fix:**
```typescript
// Increase noise frequency or reduce grid size
const frequency = size / 100;  // Adjust based on grid size
```

### Terrain Too Smooth

**Cause:** Not enough octaves or persistence too low.

**Fix:**
```typescript
// Add more octaves with higher persistence
fbm(x, z, 6, 0.6, 2.0, noise);  // More detail
```

## Research Sources

1. **THREE.Terrain Library** - https://github.com/IceCreamYou/THREE.Terrain
   - Multi-pass composition
   - Diamond-Square implementation
   - Filtering and smoothing algorithms

2. **Nathan Pointer's Landscape Rendering** - https://nathanpointer.com/blog/landscapes
   - Heightmap/displacement maps
   - Splat texturing for biomes
   - Normal map blending

3. **Perlin Noise Research** - https://rtouti.github.io/graphics/perlin-noise-algorithm
   - FBM fundamentals
   - Octave summation

4. **Procedural Generation Academic Papers**:
   - "Procedural terrain generation plane and spherical surfaces" - L Belda Calvo (2021)
   - "TERRAIN GENERATION ALGORITHMS" - Niko Sainio

## Related Skills

- `ta-terrain-mesh` - Mesh-based terrain component
- `ta-water-shader` - Water plane with Gerstner waves
- `ta-foliage-instancing` - Grass placement on terrain
- `ta-paint-territory` - Paint overlay system
- `ta-territory-grid-cpu` - CPU-based territory grid
- `ta-terrain-testing` - E2E testing patterns

## Implementation Checklist

When implementing procedural terrain:

- [ ] Select appropriate generation algorithm(s)
- [ ] Configure noise parameters (scale, octaves, persistence)
- [ ] Generate heightmap as Float32Array
- [ ] Apply filtering (smooth, clamp) as needed
- [ ] Apply heightmap to geometry vertices
- [ ] Add height-based vertex colors
- [ ] Recompute bounding sphere and vertex normals
- [ ] Test with wireframe to verify mesh structure
- [ ] Validate height range matches expectations
- [ ] Performance test at 60 FPS
