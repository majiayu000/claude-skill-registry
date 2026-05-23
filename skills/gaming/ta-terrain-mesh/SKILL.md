---
name: ta-terrain-mesh
description: Mesh-based terrain generation using PlaneGeometry and heightmap. Use for creating multiplayer game terrain - NOT raymarching. This is the NEW approach for terrain.
category: shader
---

# Terrain Mesh Skill

> "Mesh-based terrain for multiplayer games - Playable, performant, networkable."

## Overview

**IMPORTANT:** This skill replaces the raymarching/SDF approach for terrain. Multiplayer games require:
- Physics collision (Rapier integration)
- Network-synchronizable state
- 60 FPS with 32 players
- Server-authoritative territory tracking

Mesh-based terrain uses `THREE.PlaneGeometry` with heightmap displacement instead of raymarching shaders.

## When to Use This Skill

Use when your task involves:
- Creating terrain for multiplayer gameplay
- Terrain that requires physics collision
- Territory control with server validation
- Paint/splat systems
- Height-based gameplay mechanics

**NOT for:** Single-player tech demos, raymaching shaders, SDF terrain

## Core Concepts

### Mesh-Based Terrain vs Raymarching

| Aspect | Mesh-Based (This Skill) | Raymarching (Deprecated) |
|--------|-------------------------|---------------------------|
| Performance | 60 FPS with 32 players | ~30 FPS at 1080p |
| Collision | Standard Rapier | Custom raycasting |
| Network | CPU state sync | GPU-only |
| Paint | CPU grid + decal | RenderTexture only |
| Anti-cheat | Server validation | Impossible |
| Debug | Wireframe visible | Black box |

### Terrain Architecture

```
TerrainMesh (PlaneGeometry + heightmap)
    │
    ├──> Provides: getHeightAt(x, z)
    │           isSteepAt(x, z)
    │           getNormalAt(x, z)
    │
    ├──> Used by: GrassInstancer (placement)
    │             PaintOverlay (surface projection)
    │             TerritoryGrid (height multiplier)
    │             Physics (collision mesh)
    │
    └──> Components: WaterPlane (sibling)
                   GrassInstancer (sibling)
                   PaintOverlay (sibling)
```

## Implementation Pattern

### 1. TerrainGenerator Module

```typescript
// src/systems/terrain/TerrainGenerator.ts
import { ImprovedNoise } from 'three/examples/jsm/math/ImprovedNoise.js';

export interface HeightmapConfig {
  size: number;           // 128 (grid cells)
  scale: number;          // 0.02 (noise scale)
  octaves: number;        // 4 (FBM layers)
  persistence: number;    // 0.5 (amplitude decay)
  maxHeight: number;      // 24 (meters)
  seed: number;           // Random seed
}

export class TerrainGenerator {
  private noise: ImprovedNoise;
  private config: HeightmapConfig;

  constructor(config: Partial<HeightmapConfig> = {}) {
    this.config = {
      size: 128,
      scale: 0.02,
      octaves: 4,
      persistence: 0.5,
      maxHeight: 24,
      seed: Math.random() * 1000,
      ...config
    };
    this.noise = new ImprovedNoise();
  }

  /**
   * Generate heightmap using FBM (Fractal Brownian Motion)
   */
  generate(): Float32Array {
    const { size, scale, octaves, persistence, maxHeight } = this.config;
    const data = new Float32Array(size * size);

    for (let z = 0; z < size; z++) {
      for (let x = 0; x < size; x++) {
        let amplitude = 1;
        let frequency = scale;
        let height = 0;
        let maxAmplitude = 0;

        // FBM summation
        for (let o = 0; o < octaves; o++) {
          const nx = x * frequency + this.config.seed;
          const nz = z * frequency + this.config.seed;
          height += amplitude * this.noise.noise(nx, nz, 0);
          maxAmplitude += amplitude;
          amplitude *= persistence;
          frequency *= 2.0;
        }

        // Normalize to [0, 1] then scale
        height = (height / maxAmplitude + 1) * 0.5; // -1..1 to 0..1
        data[z * size + x] = height * maxHeight;
      }
    }

    return data;
  }
}
```

### 2. TerrainMesh Component

```typescript
// src/components/game/environment/TerrainMesh.tsx
import { useRef, useMemo, useEffect } from 'react';
import * as THREE from 'three';

export interface TerrainMeshConfig {
  mapSize: number;        // 256 meters
  maxHeight: number;      // 24 meters
  segments: number;       // 128 (matches 2m grid)
  waterLevel: number;     // 4.5 meters
  castShadow: boolean;
  receiveShadow: boolean;
}

export const TerrainMesh = ({
  config,
  onReady
}: {
  config: Partial<TerrainMeshConfig>;
  onReady?: (mesh: THREE.Mesh) => void;
}) => {
  const meshRef = useRef<THREE.Mesh>(null);

  const fullConfig: TerrainMeshConfig = {
    mapSize: 256,
    maxHeight: 24,
    segments: 128,
    waterLevel: 4.5,
    castShadow: false,
    receiveShadow: true,
    ...config
  };

  // Generate geometry with heightmap
  const geometry = useMemo(() => {
    const generator = new TerrainGenerator({
      size: fullConfig.segments + 1,  // +1 for vertices
      maxHeight: fullConfig.maxHeight
    });

    const heightmap = generator.generate();

    const geo = new THREE.PlaneGeometry(
      fullConfig.mapSize,
      fullConfig.mapSize,
      fullConfig.segments,
      fullConfig.segments
    );

    // Apply heightmap to vertices
    const positions = geo.attributes.position.array as Float32Array;
    const colors = new Float32Array(positions.length);

    for (let i = 0; i < positions.length; i += 3) {
      const x = positions[i];
      const z = positions[i + 2];

      // Map world position to heightmap coords
      const hx = Math.floor((x + fullConfig.mapSize / 2) / fullConfig.mapSize * 128);
      const hz = Math.floor((z + fullConfig.mapSize / 2) / fullConfig.mapSize * 128);
      const index = Math.min(hz * 128 + hx, heightmap.length - 1);

      const height = heightmap[index];
      positions[i + 1] = height;

      // Height-based coloring
      const color = getTerrainColor(height);
      colors[i] = color.r;
      colors[i + 1] = color.g;
      colors[i + 2] = color.b;
    }

    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.computeVertexNormals();

    // Store heightmap for queries
    (geo as any).userData.heightmap = heightmap;

    return geo;
  }, [fullConfig]);

  const material = useMemo(() => {
    return new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.85,
      metalness: 0.0,
      flatShading: false,
      side: THREE.DoubleSide
    });
  }, []);

  // Notify when ready
  useEffect(() => {
    if (meshRef.current && onReady) {
      onReady(meshRef.current);
    }
  }, [onReady]);

  return (
    <mesh
      ref={meshRef}
      geometry={geometry}
      material={material}
      rotation={[-Math.PI / 2, 0, 0]}
      castShadow={fullConfig.castShadow}
      receiveShadow={fullConfig.receiveShadow}
    />
  );
};

// Height zone colors from GDD
function getTerrainColor(height: number): THREE.Color {
  const TERRAIN_COLORS = {
    sand: new THREE.Color(0xc2b280),    // < 4.5m
    grass: new THREE.Color(0x4d7c0f),   // 4.5-8m
    dirt: new THREE.Color(0x6b5344),    // 8-14m
    rock: new THREE.Color(0x8b7355),    // 14-20m
    snow: new THREE.Color(0xe8e8e8)     // > 20m
  };

  if (height < 4.5) return TERRAIN_COLORS.sand;
  if (height < 8) return TERRAIN_COLORS.grass;
  if (height < 14) return TERRAIN_COLORS.dirt;
  if (height < 20) return TERRAIN_COLORS.rock;
  return TERRAIN_COLORS.snow;
}
```

### 3. Height Query API

```typescript
// Add to TerrainMesh or separate utility
export class TerrainHeightQuery {
  private heightmap: Float32Array;
  private config: TerrainMeshConfig;

  getHeightAt(worldX: number, worldZ: number): number {
    const { mapSize, segments } = this.config;

    // Convert world position to heightmap coords
    const hx = Math.floor((worldX + mapSize / 2) / mapSize * segments);
    const hz = Math.floor((worldZ + mapSize / 2) / mapSize * segments);

    // Clamp to bounds
    const x = Math.max(0, Math.min(segments, hx));
    const z = Math.max(0, Math.min(segments, hz));

    const index = z * (segments + 1) + x;
    return this.heightmap[index] || 0;
  }

  isSteepAt(worldX: number, worldZ: number, threshold: number = 0.7): boolean {
    const samples = [
      [0, 0],
      [1, 0], [-1, 0],
      [0, 1], [0, -1]
    ];

    const centerHeight = this.getHeightAt(worldX, worldZ);
    let maxSlope = 0;

    for (const [dx, dz] of samples) {
      const h = this.getHeightAt(worldX + dx * 2, worldZ + dz * 2);
      const slope = Math.abs(h - centerHeight) / 2; // 2m grid
      maxSlope = Math.max(maxSlope, slope);
    }

    return maxSlope > threshold;
  }

  getNormalAt(worldX: number, worldZ: number): THREE.Vector3 {
    const hL = this.getHeightAt(worldX - 1, worldZ);
    const hR = this.getHeightAt(worldX + 1, worldZ);
    const hD = this.getHeightAt(worldX, worldZ - 1);
    const hU = this.getHeightAt(worldX, worldZ + 1);

    return new THREE.Vector3(
      hL - hR,
      2,
      hD - hU
    ).normalize();
  }
}
```

## GDD Specifications

From `docs/design/gdd/11_level_design.md`:

| Property | Value | Source |
|----------|-------|--------|
| Map Size | 256m × 256m | GDD |
| Grid Cells | 128×128 (2m each) | GDD |
| Max Height | 24m | GDD |
| Base Height | ~8m (below spawn) | GDD |
| Water Level | 4.5m | GDD |
| Spawn Zones | 32m × 32m | GDD |

## Height Zones Coloring

```typescript
const HEIGHT_ZONES = {
  sand:   { min: 0,    max: 4.5,  color: 0xc2b280 }, // Beach
  grass:  { min: 4.5,  max: 8,    color: 0x4d7c0f }, // Lowland
  dirt:   { min: 8,    max: 14,   color: 0x6b5344 }, // Mixed
  rock:   { min: 14,   max: 20,   color: 0x8b7355 }, // Mountain
  snow:   { min: 20,   max: 24,   color: 0xe8e8e8 }  // Peaks
};
```

## Performance Guidelines

### Triangle Count

```typescript
// PlaneGeometry(256, 256, 128, 128)
// Non-indexed: 128 * 128 * 2 = 32,768 triangles
// This is within the <50K budget for terrain
```

### LOD Considerations

```typescript
// For larger maps, consider LOD
function getTerrainSegments(distance: number): number {
  if (distance < 50) return 128;   // High detail nearby
  if (distance < 100) return 64;   // Medium
  return 32;                        // Low detail far away
}
```

## Test Scene Pattern

```typescript
// src/components/testscenes/TerrainMeshTestScene.tsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, AxesHelper } from '@react-three/drei';
import { TerrainMesh } from './TerrainMesh';

export const TerrainMeshTestScene = () => {
  return (
    <Canvas
      camera={{ position: [50, 50, 50], fov: 50 }}
      shadows
    >
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 20, 10]} castShadow />

      <TerrainMesh
        config={{
          mapSize: 256,
          maxHeight: 24,
          segments: 128,
          waterLevel: 4.5,
          receiveShadow: true
        }}
        onReady={(mesh) => {
          // Expose for testing
          (window as any).terrainMesh = mesh;
        }}
      />

      {/* Debug helpers */}
      <Grid args={[256, 256]} position={[0, 0.1, 0]} cellSize={2} />
      <AxesHelper args={[10]} />
      <OrbitControls />

      {/* Test helpers */}
      <TestHelpers />
    </Canvas>
  );
};

const TestHelpers = () => {
  useFrame(() => {
    // Expose height query function
    const mesh = (window as any).terrainMesh;
    if (mesh) {
      (window as any).getTerrainHeight = (x: number, z: number) => {
        // Sample height at position
        return 0; // Implement actual sampling
      };
    }
  });
  return null;
};
```

## E2E Test Pattern

```typescript
// tests/e2e/terrain-mesh.spec.ts
test.describe('Phase 1: Terrain Mesh', () => {
  test('renders with visible colors (not all black/white)', async ({ page }) => {
    await page.goto('http://localhost:3000/?scene=terrain-mesh');

    const hasColor = await page.evaluate(() => {
      const canvas = document.querySelector('canvas');
      const ctx = canvas?.getContext('2d');
      if (!ctx) return false;

      const imageData = ctx.getImageData(100, 100, 200, 200);
      const data = imageData.data;

      for (let i = 0; i < data.length; i += 4) {
        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];
        if (Math.abs(r - g) > 20 || Math.abs(r - b) > 20) {
          return true; // Has color variation
        }
      }
      return false;
    });

    expect(hasColor).toBe(true);
  });

  test('performance: renders at 60 FPS', async ({ page }) => {
    await page.goto('http://localhost:3000/?scene=terrain-mesh');

    const fps = await page.evaluate(() => {
      return new Promise((resolve) => {
        let frames = 0;
        const startTime = performance.now();

        function countFrame() {
          frames++;
          const elapsed = performance.now() - startTime;
          if (elapsed >= 1000) {
            resolve(frames);
          } else {
            requestAnimationFrame(countFrame);
          }
        }
        requestAnimationFrame(countFrame);
      });
    });

    expect(fps).toBeGreaterThanOrEqual(55);
  });
});
```

## Common Issues

### Terrain Looks Flat

**Cause:** Heightmap not applied or scale too small.

**Fix:** Check heightmap generation and scale parameter.

```typescript
// Verify heightmap applied
const positions = geometry.attributes.position.array;
console.log('Height range:',
  Math.min(...Array.from(positions.filter((_, i) => i % 3 === 1))),
  Math.max(...Array.from(positions.filter((_, i) => i % 3 === 1)))
);
```

### Colors Wrong

**Cause:** Height zone thresholds don't match generated heights.

**Fix:** Adjust thresholds or normalize heightmap.

```typescript
// Debug: Log height distribution
const heights = Array.from(heightmap);
console.log('Height stats:', {
  min: Math.min(...heights),
  max: Math.max(...heights),
  avg: heights.reduce((a, b) => a + b, 0) / heights.length
});
```

### Z-Fighting with Water

**Cause:** Water plane at same height as terrain vertices.

**Fix:** Offset water slightly or adjust water level.

```typescript
waterMesh.position.y = config.waterLevel + 0.01; // Small offset
```

## Related Skills

For water plane: `Skill("ta-water-shader")`
For grass placement: `Skill("ta-foliage-instancing")`
For paint overlay: `Skill("ta-paint-territory")`
For territory grid: `Skill("ta-territory-grid-cpu")`
For E2E testing: `Skill("ta-terrain-testing")`

## External References

- Implementation plan: `docs/implementation/terrain-refactor-plan.md`
- Research doc: `docs/research/terrain-shader-research.md`
- Color palette: `docs/references/terrain/color-palette.ts`
- Bruno Simon style: `docs/references/terrain/README.md`

## Migration from Raymarching

**Old approach (deprecated):**
```typescript
// Raymarching shader - DON'T USE
const terrainMaterial = new THREE.ShaderMaterial({
  vertexShader: raymarchingVertexShader,
  fragmentShader: sdfMapFragmentShader,
  uniforms: { ... }
});
```

**New approach (use this):**
```typescript
// Mesh-based terrain - USE THIS
const terrainMesh = new THREE.Mesh(
  new THREE.PlaneGeometry(256, 256, 128, 128),
  new THREE.MeshStandardMaterial({ vertexColors: true })
);
// Apply heightmap to vertices
```
