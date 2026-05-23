---
name: ta-foliage-instancing
description: GPU instanced grass and vegetation with wind animation and LOD for high-performance terrain foliage. Use when creating grass, plants, or any instanced vegetation systems.
category: shader
---

# Foliage Instancing Skill

> "Millions of grass blades, one draw call."

## Overview

GPU instancing allows rendering 200,000+ grass blades with a single draw call. Combined with wind animation, LOD (Level of Detail), and infinite sliding window for player movement, this creates lush, performant vegetation.

## When to Use This Skill

Use when your task involves:
- Grass fields or meadows
- Vegetation patches
- Instanced plant rendering
- Wind animation on foliage
- Performance-critical vegetation
- Terrain decoration

## Core Concepts

### GPU Instancing

Each instance has its own transform but shares geometry:

```typescript
// Create instanced mesh
const geometry = new THREE.BufferGeometry();
// ... set up attributes (position, color, yaw, origin, random)

const mesh = new THREE.InstancedMesh(geometry, material, count);
mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
```

### Grass Blade Geometry

Each blade is a triangle with 3 vertices:

```
    Top (vertex 2)
   / \
  /   \
Bottom Left   Bottom Right
(vertex 0)    (vertex 1)
```

**Color encoding for fake AO:**
- Vertex 0 (bottom-left): `color.r = 0.1` (dark edge)
- Vertex 1 (bottom-right): `color.b = 0.1` (dark edge)
- Vertex 2 (top): `color = vec3(1.0)` (bright tip)

### Wind Animation

Wind uses rotation matrix based on noise:

```glsl
// Sample wind noise
vec2 noiseUV = vec2(origin.x * 0.09, origin.z * 0.09);
mat2 rotation = mat2(cos(uWindDirection), -sin(uWindDirection),
                     sin(uWindDirection), cos(uWindDirection));
vec2 rotatedUV = rotation * noiseUV + uTime * vec2(uWindSpeed);
vec3 windNoise = texture2D(uNoiseTexture, rotatedUV).rgb;

// Calculate bend angle (only for top vertex)
float angle = radians(map(windNoise.g + windNoise.b, 0.0, 2.0, -22.0, 22.0)) * color.g;

// Apply rotation matrix
mat3 rotMatrix = mat3(
  vec3(cos(angle), 0.0, sin(angle)),
  vec3(0.0, 1.0, 0.0),
  vec3(-sin(angle), 0.0, cos(angle))
);
```

### Infinite Sliding Window

Grass wraps around player position for infinite feel:

```glsl
float halfPatchSize = uPatchSize * 0.5;
vec2 offset = origin.xz - uPlayerPosition.xz;

// Modulo for wrapping
origin.x = mod(offset.x + halfPatchSize, uPatchSize) - halfPatchSize + uPlayerPosition.x;
origin.z = mod(offset.z + halfPatchSize, uPatchSize) - halfPatchSize + uPlayerPosition.z;
```

### LOD System

Reduce detail at distance:

```glsl
// Calculate distance
float dist = length(origin.xz - uPlayerPosition.xz);

// LOD factor (0 = near, 1 = far)
float lodFactor = smoothstep(uLODNearDist, uLODFarDist, dist);

// Reduce height at distance
heightModifier *= (1.0 - lodFactor * 0.5);

// Darken at distance
grassColor.rgb *= (1.0 - lodFactor * 0.3);
```

## Implementation Pattern

### TypeScript Class Structure

```typescript
export class FoliageShader {
  private mesh: THREE.InstancedMesh | null = null;

  public readonly uniforms: {
    uTime: { value: number };
    uPlayerPosition: { value: THREE.Vector3 };
    uHeightMap: { value: THREE.Texture | null };
    uNoiseTexture: { value: THREE.Texture | null };
    uDiffuseMap: { value: THREE.Texture | null };
    uPatchSize: { value: number };
    uBladeWidth: { value: number };
    uWindSpeed: { value: number };
    uWindDirection: { value: number };
    uMaxBladeHeight: { value: number };
    uLODNearDist: { value: number };
    uLODFarDist: { value: number };
    uEnableLOD: { value: number };
  };

  constructor(config?: FoliageConfig) {
    // Initialize with defaults
  }

  buildFoliage(terrainMesh?: THREE.Object3D): THREE.InstancedMesh {
    // Generate grass positions and build mesh
  }

  updateTime(time: number): void {
    this.uniforms.uTime.value = time;
  }

  updatePlayerPosition(position: THREE.Vector3): void {
    this.uniforms.uPlayerPosition.value.copy(position);
  }

  setWind(speed: number, direction: number): void {
    this.uniforms.uWindSpeed.value = speed;
    this.uniforms.uWindDirection.value = direction;
  }

  dispose(): void {
    if (this.mesh) {
      this.mesh.geometry.dispose();
      (this.mesh.material as THREE.Material).dispose();
    }
  }
}
```

### Sampling from Terrain

Use `MeshSurfaceSampler` for natural distribution:

```typescript
import { MeshSurfaceSampler } from 'three/addons/math/MeshSurfaceSampler.js';

private sampleFromTerrain(
  terrainMesh: THREE.Object3D,
  count: number,
  positions: number[],
  colors: number[],
  yaws: number[],
  bladeOrigins: number[],
  randoms: number[]
): void {
  const sampler = new MeshSurfaceSampler(terrainMesh).build();
  const tempPosition = new THREE.Vector3();
  const tempNormal = new THREE.Vector3();

  for (let i = 0; i < count; i++) {
    sampler.sample(tempPosition, tempNormal);

    const yaw = Math.random() * Math.PI * 2;
    const rnd = Math.random();

    // Three vertices per blade
    // ... add data to arrays
  }
}
```

## Performance Guidelines

### Target Counts

| Platform | Target Blades | Draw Calls |
|----------|---------------|------------|
| Desktop (high) | 500,000 | 1-2 |
| Desktop (mid) | 200,000 | 1 |
| Mobile | 50,000 | 1 |

### Memory Optimization

```typescript
// Use Float32BufferAttribute for GPU efficiency
geometry.setAttribute('position',
  new THREE.Float32BufferAttribute(positions, 3));

// Reuse vectors in loops
const tempVec = new THREE.Vector3();
for (let i = 0; i < count; i++) {
  tempVec.set(x, y, z);
  // ... use tempVec
}
```

### LOD Settings

```typescript
const DEFAULT_LOD = {
  nearDist: 20,   // Full quality up to 20m
  farDist: 100,   // Reduced quality beyond 100m
};
```

## GDD Specifications

From `docs/design/gdd/`:

| Property | Value |
|----------|-------|
| Patch Size | 50m x 50m |
| Blade Height | 0.15m (avg), 0.3m (max) |
| Blade Width | 0.08m |
| Wind Speed | 0.3 |
| Wind Direction | PI * 0.25 (diagonal) |

## Asset References

Use existing sprites from `src/assets/Foliage Pack/`:

- **Grass sprites** - 76+ grass variations
- **Plant sprites** - Flowers, reeds, small plants
- **Noise texture** - Wind variation

## Integration with Terrain

**For the NEW mesh-based terrain approach (multiplayer):**
- Use `Skill("ta-terrain-mesh")` for terrain mesh with heightmap
- TerrainMesh provides `getHeightAt(x, z)` for grass placement
- Grid-aligned sampling: `const height = terrain.getHeightAt(worldX, worldZ);`

**For legacy SDF/heightmap texture sampling:**
```glsl
// Sample heightmap for grass placement
vec2 heightUV = vec2(
  map(origin.x, -100.0, 100.0, 0.0, 1.0),
  map(origin.z, -100.0, 100.0, 0.0, 1.0)
);
float terrainHeight = 0.0;
if (uHeightMap != null) {
  terrainHeight = texture2D(uHeightMap, heightUV).r * 10.0;
}
transformed.y += terrainHeight;
```

### Paint System Integration

Grass should not grow on painted areas:

```glsl
// Sample paint texture
vec4 paintData = texture2D(uPaintTexture, heightUV);

// Reduce/don't spawn grass on painted areas
float paintAmount = paintData.a;
if (paintAmount > 0.5) {
  // Don't render or reduce height
  heightModifier *= (1.0 - paintAmount);
}
```

## Debug Visualization

```typescript
// Show grass without wind for debugging
this.uniforms.uWindSpeed.value = 0;

// Visualize LOD zones
const lodHelper = new THREE.Mesh(
  new THREE.RingGeometry(20, 20.5, 32),
  new THREE.MeshBasicMaterial({ color: 0x00ff00, side: THREE.DoubleSide })
);
lodHelper.rotation.x = -Math.PI / 2;
lodHelper.position.y = 0.1;
```

## Common Issues

### Grass Pops Into View

Fix: Extend near LOD distance or add fade:

```glsl
// Fade in at near distance
float fadeIn = smoothstep(0.0, 5.0, dist);
alpha *= fadeIn;
```

### Wind Looks Synchronized

Fix: Add per-blade randomness:

```glsl
vec3 windNoise = texture2D(uNoiseTexture, rotatedUV + aRandom * 10.0).rgb;
```

### Performance Drops

1. Reduce blade count
2. Increase LOD distances
3. Use lower resolution textures
4. Disable in distance fog

## Related Skills

For water bodies near vegetation: `Skill("ta-water-shader")`
For terrain SDF for grass placement: `Skill("ta-shader-sdf")`
For general performance tips: `Skill("ta-r3f-performance")`

## External References

- Implementation plan: `docs/implementation/terrain-refactor-plan.md` (Phase 3)
- Research guide: `docs/research/terrain-shader-research.md`
- Visual reference: `docs/references/terrain/README.md`
- Antaeus AR Ghibli Grass: https://medium.com/antaeus-ar/making-grass-with-triangles-in-glsl-using-three-js-e106771a71ff
- Codrops Fluffiest Grass: https://tympanus.net/codrops/2025/02/04/how-to-make-the-fluffiest-grass-with-three-js/
