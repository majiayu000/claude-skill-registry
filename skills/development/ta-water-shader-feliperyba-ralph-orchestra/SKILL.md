---
name: ta-water-shader
description: Gerstner wave simulation with foam and caustics for realistic water surfaces in Three.js/R3F. Use when creating water shaders, oceans, lakes, or any animated liquid surfaces.
category: shader
---

# Water Shader Skill

> "Realistic water that moves like water."

## Overview

Water shaders simulate liquid surfaces using Gerstner waves for realistic wave motion, foam generation at wave peaks, fresnel reflections for depth, and caustics for underwater light patterns.

## When to Use This Skill

Use when your task involves:
- Water surfaces (oceans, lakes, rivers, pools)
- Wave simulation and animation
- Foam and spray effects
- Underwater caustics
- Fresnel reflections on liquid
- Buoyancy and floating objects

## Core Concepts

### Gerstner Waves

Gerstner waves are a more realistic wave model than simple sine waves:

```
Direction: Waves travel in a specific direction
Steepness: Controls how peaked the waves are (0-1)
Wavelength: Distance between wave crests
Speed: Wave velocity based on physics (sqrt(9.8 / k))
```

**Shader Implementation:**

```glsl
vec3 gerstnerWave(vec3 position, float steepness, float wavelength) {
  float k = 2.0 * PI / wavelength;  // Wave number
  float c = sqrt(9.8 / k);           // Wave speed (physics-based)
  vec2 d = vec2(cos(uWaveDirection), sin(uWaveDirection));
  float f = k * (dot(d, position.xz) - c * uTime * uWaveSpeed);
  float a = steepness / k;           // Wave amplitude

  return vec3(
    d.x * a * cos(f),  // X displacement
    a * sin(f),        // Y displacement (height)
    d.y * a * cos(f)   // Z displacement
  );
}
```

### Layered Waves

Multiple wave layers create complexity:

```glsl
// Primary waves - large, slow
vec3 wave1 = gerstnerWave(position, 0.25, 15.0);

// Secondary waves - medium
vec3 wave2 = gerstnerWave(position, 0.15, 10.0);

// Tertiary waves - small, fast details
vec3 wave3 = gerstnerWave(position, 0.10, 5.0);

// Combine with different weights
transformed += wave1 + wave2 * 0.5 + wave3 * 0.25;
```

### Foam Generation

Foam appears at wave peaks with noise variation:

```glsl
// Wave height determines foam
float foamThreshold = uWaveHeight * 0.7;
float foamNoise = noise(worldPosition.xz * 0.05 + uTime * 0.05);

// Smooth threshold for soft edges
float foam = smoothstep(
  foamThreshold - 0.1,
  foamThreshold,
  vWaveHeight + foamNoise * 0.2
);

// Add variation with second noise layer
foam *= smoothstep(0.3, 0.6, noise(uv * 2.0 + 100.0));

// Mix foam color
vec3 color = mix(waterColor, foamColor, foam);
```

### Fresnel Reflections

Fresnel effect makes edges more reflective:

```glsl
vec3 viewDirection = normalize(cameraPosition - worldPosition);
vec3 normal = normalize(vNormal);

// Fresnel = more reflection at grazing angles
float fresnel = pow(1.0 - max(dot(normal, viewDirection), 0.0), 3.0);

vec3 reflectionColor = mix(waterColor, skyColor, fresnel * 0.5);
```

### Caustics

Underwater light patterns using layered noise:

```glsl
vec2 causticUV = uv * 20.0 + uTime * 0.1;
float caustic = noise(causticUV) * noise(causticUV * 1.5 + 50.0);
color += vec3(caustic * 0.05);
```

## Implementation Pattern

### TypeScript Class Structure

```typescript
export class WaterShader {
  private material: THREE.ShaderMaterial;

  public readonly uniforms: {
    uTime: { value: number };
    uWaveDirection: { value: number };
    uWaveSpeed: { value: number };
    uWaveHeight: { value: number };
    uWaveFrequency: { value: number };
    uWaterColor: { value: THREE.Color };
    uFoamColor: { value: THREE.Color };
    uNoiseTexture: { value: THREE.Texture | null };
    uCameraPosition: { value: THREE.Vector3 };
  };

  constructor(config?: WaterShaderConfig) {
    // Initialize uniforms with defaults
    // Create shader material
  }

  public getMaterial(): THREE.Material {
    return this.material;
  }

  public updateTime(time: number): void {
    this.uniforms.uTime.value = time;
  }

  public updateCameraPosition(position: THREE.Vector3): void {
    this.uniforms.uCameraPosition.value.copy(position);
  }

  public setWaveParams(direction: number, speed: number, height: number): void {
    this.uniforms.uWaveDirection.value = direction;
    this.uniforms.uWaveSpeed.value = speed;
    this.uniforms.uWaveHeight.value = height;
  }

  public dispose(): void {
    this.material.dispose();
  }
}
```

### Usage in R3F

```typescript
import { WaterShader, createWaterPlane } from './components/shaders/WaterShader';

// In your scene component
const waterMesh = createWaterPlane(256, 128, {
  waveSpeed: 1.0,
  waveHeight: 0.3,
  waterColor: 0x1a5276,
  foamColor: 0xecf0f1,
});

// In animation loop
useFrame((state, delta) => {
  updateWaterMesh(waterMesh, delta, state.camera.position);
});
```

## Performance Optimization

### Geometry Segments

Use appropriate segment count for wave displacement:

```typescript
// Good balance for 256m x 256m water
const geometry = new THREE.PlaneGeometry(256, 256, 128, 128);

// Lower segments for distant water
const distantWater = new THREE.PlaneGeometry(256, 256, 32, 32);
```

### LOD Strategy

```glsl
// Distance-based wave detail reduction
float dist = length(worldPosition.xz - cameraPosition.xz);
float lodFactor = smoothstep(50.0, 200.0, dist);

// Reduce wave height at distance
transformed *= (1.0 - lodFactor * 0.5);
```

### Optimization Tips

1. **Shared noise texture** - Use single noise texture for all water
2. **Lower resolution for caustics** - Don't need full res
3. **Cull distant water** - Use frustum culling aggressively
4. **Reuse geometry** - Same plane geometry for all water instances

## GDD Specifications

From `docs/design/gdd/`:

| Property | Value |
|----------|-------|
| Map Size | 256m x 256m |
| Water Level | y = 2m |
| Wave Direction | PI * 0.25 (diagonal) |
| Wave Speed | 1.0 (adjustable) |
| Max Wave Height | 0.3m |
| Water Color | Deep blue (#1a5276) |
| Foam Color | White (#ecf0f1) |

## Asset References

Use existing textures from `src/assets/`:

- **Pattern Pack** - Water surface patterns
- **Noise textures** - For foam/caustic variation

## Debug Visualization

Add wireframe helper to see wave displacement:

```typescript
const wireframe = new THREE.WireframeGeometry(waterMesh.geometry);
const line = new THREE.LineSegments(wireframe);
line.position.copy(waterMesh.position);
scene.add(line);
```

## Common Issues

### Waves Too Sharp

Reduce steepness in gerstnerWave function:

```glsl
// Before: 0.25 (sharp peaks)
vec3 wave1 = gerstnerWave(position, 0.25, 15.0);

// After: 0.15 (softer waves)
vec3 wave1 = gerstnerWave(position, 0.15, 15.0);
```

### Foam Looks Static

Add time-based animation to noise UVs:

```glsl
vec2 noiseUV = worldPosition.xz * 0.05 + uTime * 0.05;
```

### No Reflections

Check normal calculation - normals must be recalculated after wave displacement:

```glsl
// Finite difference method for normals
float eps = 0.01;
vec3 p1 = position + gerstnerWave(position + vec3(eps, 0.0, 0.0), ...);
vec3 p2 = position + gerstnerWave(position + vec3(0.0, 0.0, eps), ...);

vec3 normal = normalize(vec3(
  p1.x - transformed.x,
  eps,
  p2.z - transformed.z
));
```

## Related Skills

For general shader patterns: `Skill("ta-shader-development")`
For vegetation placement near water: `Skill("ta-foliage-instancing")`
For water-based paint mechanics: `Skill("ta-paint-territory")`

## External References

- Implementation plan: `docs/implementation/terrain-refactor-plan.md` (Phase 2)
- Research guide: `docs/research/terrain-shader-research.md`
- Color palette: `docs/references/terrain/color-palette.ts`
- Visual reference: `docs/references/terrain/README.md`
- ShaderToy Seascape: https://www.shadertoy.com/view/Ms2SD1
- Three.js Journey Raging Sea
