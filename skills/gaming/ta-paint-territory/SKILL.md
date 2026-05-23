---
name: ta-paint-territory
description: Splatoon-style paint system with RenderTexture-based territory tracking and percentage calculation. Use when implementing territory control, paint decals, or map coverage mechanics.
category: shader
---

# Paint Territory Skill

> "The map is your canvas."

## Overview

The paint territory system uses RenderTexture accumulation to track paint coverage, calculate territory percentages in real-time, and support team-specific paint with pattern overlays for accessibility.

**IMPORTANT NOTE:** This skill covers GPU-based RenderTexture paint rendering for visual effects. For multiplayer server-authoritative territory tracking, use `Skill("ta-territory-grid-cpu")` instead.

## When to Use This Skill

Use when your task involves:
- Territory control mechanics
- Paint/ink splat systems
- Map coverage calculation
- Team-based area control
- Splatoon-style gameplay
- Decal accumulation systems

## Core Concepts

### RenderTexture Accumulation

Paint is rendered to a texture, not the screen:

```typescript
// Create paint render target
const paintTexture = new THREE.WebGLRenderTarget(
  2048,  // Resolution (higher = more accurate %)
  2048,
  {
    format: THREE.RGBAFormat,
    type: THREE.UnsignedByteType,
    minFilter: THREE.LinearFilter,
    magFilter: THREE.LinearFilter,
  }
);
```

### Team Encoding

Store team data in texture channels:

```
R channel: Orange team paint (0-1)
G channel: Reserved (future use)
B channel: Blue team paint (0-1)
A channel: Paint opacity (0-1)
```

This allows single texture to track all territory data.

### Splat Application

Each paint splat is a shader render pass:

```typescript
applySplat(config: SplatConfig): void {
  const { worldX, worldZ, team, radius = 0.5, amount = 0.8 } = config;

  // Convert world position to UV
  const uvX = (worldX / this.mapSize) * 0.5 + 0.5;
  const uvZ = (worldZ / this.mapSize) * 0.5 + 0.5;

  // Create splat material
  const splatMaterial = new THREE.ShaderMaterial({
    uniforms: {
      uPreviousPaint: { value: this.paintTexture.texture },
      uPaintColor: { value: teamColor },
      uRadius: { value: radius * (1.0 / this.mapSize) * 0.5 },
      uCenter: { value: new THREE.Vector2(uvX, uvZ) },
      uAmount: { value: amount },
    },
    vertexShader: `...`,
    fragmentShader: `
      uniform sampler2D uPreviousPaint;
      uniform vec3 uPaintColor;
      uniform float uRadius;
      uniform vec2 uCenter;
      uniform float uAmount;

      varying vec2 vUv;

      void main() {
        vec4 previousColor = texture2D(uPreviousPaint, vUv);

        // Distance from splat center
        float dist = distance(vUv, uCenter);

        // Soft falloff
        float paintAmount = (1.0 - smoothstep(0.0, uRadius, dist)) * uAmount;

        // Team encoding
        vec3 newColor;
        float newAlpha;

        if (uPaintColor.r > 0.5) {
          // Orange team
          newColor = vec3(1.0, previousColor.g, 0.0);
          newAlpha = max(previousColor.a,
            paintAmount * previousColor.r + paintAmount * (1.0 - previousColor.r));
        } else {
          // Blue team
          newColor = vec3(previousColor.r, previousColor.g, 1.0);
          newAlpha = max(previousColor.a,
            paintAmount * previousColor.b + paintAmount * (1.0 - previousColor.b));
        }

        gl_FragColor = vec4(newColor, newAlpha);
      }
    `,
  });

  // Render to paint texture
  renderer.setRenderTarget(this.paintTexture);
  renderer.render(this.paintScene, this.paintCamera);
  renderer.setRenderTarget(null);
}
```

### Territory Calculation

Read pixels and calculate percentages:

```typescript
calculateTerritory(): TerritoryStats {
  // Read pixels from paint texture
  renderer.setRenderTarget(this.paintTexture);
  renderer.readRenderTargetPixels(
    0, 0,
    this.paintResolution,
    this.paintResolution,
    this.pixelBuffer
  );
  renderer.setRenderTarget(null);

  // Sample pixels (every Nth for performance)
  const sampleRate = 100;
  let orangePixels = 0;
  let bluePixels = 0;
  let paintedPixels = 0;
  let totalSampled = 0;

  for (let i = 0; i < this.pixelBuffer.length; i += 4 * sampleRate) {
    const alpha = this.pixelBuffer[i + 3];
    if (alpha > 50) {  // Threshold for "painted"
      paintedPixels++;
      if (this.pixelBuffer[i] > 200) orangePixels++;     // R channel
      if (this.pixelBuffer[i + 2] > 200) bluePixels++;   // B channel
    }
    totalSampled++;
  }

  // Calculate percentages
  const paintCoverage = paintedPixels / totalSampled;
  return {
    orange: orangePixels / totalSampled,
    blue: bluePixels / totalSampled,
    neutral: 1.0 - paintCoverage,
  };
}
```

## Implementation Pattern

### TypeScript Class Structure

```typescript
export class PaintTerritorySystem {
  public paintTexture: THREE.WebGLRenderTarget;
  private paintScene: THREE.Scene;
  private paintCamera: THREE.OrthographicCamera;
  private pixelBuffer: Uint8Array;
  private activeDecals: number = 0;

  constructor(config?: PaintTerritoryConfig) {
    // Initialize with defaults
    // mapSize: 256m
    // textureResolution: 2048
    // maxDecals: 1000
    // cellSize: 2m
  }

  clear(): void {
    // Clear all paint
  }

  applySplat(config: SplatConfig): void {
    // Add paint at world position
  }

  calculateTerritory(): TerritoryStats {
    // Return current percentages
  }

  getGridData(): Uint8Array {
    // Return 128x128 grid data for gameplay
  }

  getStats(): TerritoryStats {
    // Get cached stats
  }

  getPaintTexture(): THREE.WebGLRenderTarget {
    // For use in terrain shader
  }

  dispose(): void {
    // Cleanup
  }
}
```

### Configuration Interface

```typescript
export interface SplatConfig {
  worldX: number;
  worldZ: number;
  team: 'orange' | 'blue' | 'neutral';
  radius?: number;    // Default: 0.5
  amount?: number;    // Default: 0.8
}

export interface TerritoryStats {
  orange: number;  // 0-1, percentage painted orange
  blue: number;    // 0-1, percentage painted blue
  neutral: number; // 0-1, unpainted percentage
}
```

## GDD Specifications

From `docs/design/gdd/4_territory_control.md`:

| Property | Value |
|----------|-------|
| Map Size | 256m x 256m |
| Grid Cells | 128x128 (2m each) |
| Max Decals | 1000 active |
| Paint Resolution | 2048x2048 |
| Orange Team | #FF6B35 (stripes for accessibility) |
| Blue Team | #4A90D9 (dots for accessibility) |
| Win Threshold | 60% coverage or timeout |

### Height Multiplier (DEC-105)

Higher terrain = more points:

```typescript
const heightMultiplier = 1.0 + (terrainHeight / maxTerrainHeight) * 0.5;
const points = basePoints * heightMultiplier;
```

### Team Colors

```typescript
export const TERRITORY_COLORS = {
  orange: new THREE.Color(0xFF6B35),  // Primary orange
  blue: new THREE.Color(0x4A90D9),    // Electric blue
  neutral: new THREE.Color(0x888888), // Gray
} as const;
```

## Integration with Terrain

### Apply Paint to Terrain Shader

```glsl
// In terrain fragment shader
uniform sampler2D uPaintTexture;
uniform vec3 uOrangeColor;
uniform vec3 uBlueColor;

varying vec2 vWorldUV;

void main() {
  vec4 paintData = texture2D(uPaintTexture, vWorldUV);

  // Mix paint color with terrain
  vec3 paintColor = mix(uOrangeColor, uBlueColor, paintData.b > paintData.r ? 1.0 : 0.0);
  vec3 finalColor = mix(terrainColor, paintColor, paintData.a * 0.5);

  // Add accessibility pattern
  float pattern = 0.0;
  if (paintData.r > 0.5) {
    pattern = stripePattern(vWorldUV);      // Orange = stripes
  } else if (paintData.b > 0.5) {
    pattern = dotPattern(vWorldUV);         // Blue = dots
  }

  finalColor = mix(finalColor, vec3(1.0), pattern * 0.1);
  gl_FragColor = vec4(finalColor, 1.0);
}
```

## Performance Optimization

### Pixel Sampling

Don't read all pixels - sample strategically:

```typescript
// Sample rate: higher = faster but less accurate
const sampleRate = 100;  // Read 1/100th of pixels

// For 2048x2048 texture: ~42k reads instead of 4M
```

### Grid-Based Calculation

For gameplay, use grid instead of pixels:

```typescript
// 128x128 grid instead of 2048x2048 pixels
const gridWidth = Math.ceil(this.mapSize / this.cellSize);  // 128
const gridHeight = Math.ceil(this.mapSize / this.cellSize); // 128

// Sample one pixel per grid cell
```

### Decal Limits

Enforce max active decals:

```typescript
if (this.activeDecals >= this.maxDecals) {
  console.warn('[PaintTerritorySystem] Max decals reached');
  return;
}
```

Consider fading oldest decals:

```typescript
// Circular buffer of decals
const decalAges = new Float32Array(this.maxDecals);
// Fade out old decals over time
```

## Debug Visualization

### Visualize Paint Texture

```typescript
// Create debug mesh to see paint texture
const debugMesh = new THREE.Mesh(
  new THREE.PlaneGeometry(10, 10),
  new THREE.MeshBasicMaterial({ map: paintTexture.texture })
);
debugMesh.position.set(0, 5, 0);
scene.add(debugMesh);
```

### Show Territory %

```typescript
// In UI
function updateTerritoryUI(stats: TerritoryStats) {
  document.getElementById('orange-percent').textContent =
    `${(stats.orange * 100).toFixed(1)}%`;
  document.getElementById('blue-percent').textContent =
    `${(stats.blue * 100).toFixed(1)}%`;
  document.getElementById('neutral-percent').textContent =
    `${(stats.neutral * 100).toFixed(1)}%`;
}
```

## Common Issues

### Inaccurate Percentages

**Problem:** Percentages don't match visual paint coverage.

**Solutions:**
1. Increase texture resolution
2. Decrease sample rate (read more pixels)
3. Adjust alpha threshold in calculation

### Paint Flickering

**Problem:** Paint appears/disappears between frames.

**Cause:** Reading render texture before render complete.

**Solution:** Use `renderer.setRenderTarget(null)` properly before reading.

### Performance Drops

**Problem:** Frame rate drops when painting.

**Solutions:**
1. Reduce texture resolution
2. Increase sample rate
3. Limit max decals
4. Use throttle on calculateTerritory()

## Match Rules (Splatoon-style)

### Victory Conditions

1. **Time expired:** Team with higher % wins
2. **Knockout:** One team reaches >60% when other <20%
3. **Overtime:** If <30 seconds left and losing team claims lead

### Scoring

```
Base points per cell: 1
Height multiplier: 1.0 - 1.5x (based on terrain height)
Center bonus: 1.2x for map center (strategic value)
```

## Accessibility Patterns

Per GDD requirements, paint must have visual patterns:

```glsl
// Stripes for orange team
float stripePattern(vec2 uv) {
  float stripe = sin(uv.x * 50.0 + uv.y * 50.0);
  return step(0.8, stripe);
}

// Dots for blue team
float dotPattern(vec2 uv) {
  vec2 grid = fract(uv * 20.0) - 0.5;
  float dot = 1.0 - smoothstep(0.3, 0.5, length(grid));
  return dot;
}
```

## Related Skills

For terrain integration: `Skill("ta-shader-development")`
For grass interaction: `Skill("ta-foliage-instancing")`
For water interaction: `Skill("ta-water-shader")`

## External References

- Research guide: `docs/research/terrain-shader-research.md`
- GDD: `docs/design/gdd/4_territory_control.md`
- GDD: `docs/design/gdd/2_teams.md` (team colors)
