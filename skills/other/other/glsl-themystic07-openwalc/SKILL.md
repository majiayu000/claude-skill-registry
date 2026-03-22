---
name: glsl
description: GLSL shader programming for JARVIS holographic effects
model: sonnet
risk_level: LOW
version: 1.1.0
---

# GLSL Shader Programming Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced shader patterns.

## 1. Overview

This skill provides GLSL shader expertise for creating holographic visual effects in the JARVIS AI Assistant HUD. It focuses on efficient GPU programming for real-time rendering.

**Risk Level**: LOW - GPU-side code with limited attack surface, but can cause performance issues

**Primary Use Cases**:
- Holographic panel effects with scanlines
- Animated energy fields and particle systems
- Data visualization with custom rendering
- Post-processing effects (bloom, glitch, chromatic aberration)

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write visual regression tests and shader unit tests before implementation
2. **Performance Aware**: Profile GPU performance, optimize for 60 FPS target
3. **Precision Matters**: Use appropriate precision qualifiers for performance
4. **Avoid Branching**: Minimize conditionals in shaders for GPU efficiency
5. **Optimize Math**: Use built-in functions, avoid expensive operations
6. **Uniform Safety**: Validate uniform inputs before sending to GPU
7. **Loop Bounds**: Always use constant loop bounds to prevent GPU hangs
8. **Memory Access**: Optimize texture lookups and varying interpolation

## 3. Implementation Workflow (TDD)

### 3.1 Step 1: Write Failing Test First

```typescript
// tests/shaders/holographic-panel.test.ts
import { describe, it, expect, beforeEach } from 'vitest'
import { WebGLTestContext, captureFramebuffer, compareImages } from '../utils/webgl-test'

describe('HolographicPanelShader', () => {
  let ctx: WebGLTestContext

  beforeEach(() => {
    ctx = new WebGLTestContext(256, 256)
  })

  // Unit test: Shader compiles
  it('should compile without errors', () => {
    const shader = ctx.compileShader(holoFragSource, ctx.gl.FRAGMENT_SHADER)
    expect(shader).not.toBeNull()
    expect(ctx.getShaderErrors()).toEqual([])
  })

  // Unit test: Uniforms are accessible
  it('should have required uniforms', () => {
    const program = ctx.createProgram(vertSource, holoFragSource)
    expect(ctx.getUniformLocation(program, 'uTime')).not.toBeNull()
    expect(ctx.getUniformLocation(program, 'uColor')).not.toBeNull()
    expect(ctx.getUniformLocation(program, 'uOpacity')).not.toBeNull()
  })

  // Visual regression test
  it('should render scanlines correctly', async () => {
    ctx.renderShader(holoFragSource, { uTime: 0, uColor: [0, 0.5, 1], uOpacity: 1 })
    const result = captureFramebuffer(ctx)
    const baseline = await loadBaseline('holographic-scanlines.png')
    expect(compareImages(result, baseline, { threshold: 0.01 })).toBeLessThan(0.01)
  })

  // Edge case test
  it('should handle extreme UV values', () => {
    const testCases = [
      { uv: [0, 0], expected: 'no crash' },
      { uv: [1, 1], expected: 'no crash' },
      { uv: [0.5, 0.5], expected: 'no crash' }
    ]
    testCases.forEach(({ uv }) => {
      expect(() => ctx.renderAtUV(holoFragSource, uv)).not.toThrow()
    })
  })
})
```

### 3.2 Step 2: Implement Minimum to Pass

```glsl
// Start with minimal shader that passes tests
#version 300 es
precision highp float;

uniform float uTime;
uniform vec3 uColor;
uniform float uOpacity;

in vec2 vUv;
out vec4 fragColor;

void main() {
  // Minimal implementation to pass compilation test
  fragColor = vec4(uColor, uOpacity);
}
```

### 3.3 Step 3: Refactor with Full Implementation

```glsl
// Expand to full implementation after tests pass
void main() {
  vec2 uv = vUv;
  float scanline = sin(uv.y * 100.0) * 0.1 + 0.9;
  float pulse = sin(uTime * 2.0) * 0.1 + 0.9;
  vec3 color = uColor * scanline * pulse;
  fragColor = vec4(color, uOpacity);
}
```

### 3.4 Step 4: Run Full Verification

```bash
# Run all shader tests
npm run test:shaders

# Visual regression tests
npm run test:visual -- --update-snapshots  # First time only
npm run test:visual

# Performance benchmark
npm run bench:shaders

# Cross-browser compilation check
npm run test:webgl-compat
```

## 4. Technology Stack & Versions

### 4.1 GLSL Versions

| Version | Context | Features |
|---------|---------|----------|
| GLSL ES 3.00 | WebGL 2.0 | Modern features, better precision |
| GLSL ES 1.00 | WebGL 1.0 | Legacy support |

### 4.2 Shader Setup

```glsl
#version 300 es
precision highp float;
precision highp int;

// WebGL 2.0 shader header
```

## 5. Performance Patterns

### 5.1 Avoid Branching - Use Mix/Step

```glsl
// ❌ BAD - GPU branch divergence
vec3 getColor(float value) {
  if (value < 0.3) {
    return vec3(1.0, 0.0, 0.0);  // Red
  } else if (value < 0.7) {
    return vec3(1.0, 1.0, 0.0);  // Yellow
  } else {
    return vec3(0.0, 1.0, 0.0);  // Green
  }
}

// ✅ GOOD - Branchless with mix/step
vec3 getColor(float value) {
  vec3 red = vec3(1.0, 0.0, 0.0);
  vec3 yellow = vec3(1.0, 1.0, 0.0);
  vec3 green = vec3(0.0, 1.0, 0.0);

  vec3 color = mix(red, yellow, smoothstep(0.3, 0.31, value));
  color = mix(color, green, smoothstep(0.7, 0.71, value));
  return color;
}
```

### 5.2 Texture Atlases - Reduce Draw Calls

```glsl
// ❌ BAD - Multiple texture bindings
uniform sampler2D uIcon1;
uniform sampler2D uIcon2;
uniform sampler2D uIcon3;

vec4 getIcon(int id) {
  if (id == 0) return texture(uIcon1, vUv);
  if (id == 1) return texture(uIcon2, vUv);
  return texture(uIcon3, vUv);
}

// ✅ GOOD - Single atlas texture
uniform sampler2D uIconAtlas;
uniform vec4 uAtlasOffsets[3];  // [x, y, width, height] for each icon

vec4 getIcon(int id) {
  vec4 offset = uAtlasOffsets[id];
  vec2 atlasUV = offset.xy + vUv * offset.zw;
  return texture(uIconAtlas, atlasUV);
}
```

### 5.3 Level of Detail (LOD) - Distance-Based Quality

```glsl
// ❌ BAD - Same quality regardless of distance
const int NOISE_OCTAVES = 8;

float noise(vec3 p) {
  float result = 0.0;
  for (int i = 0; i < NOISE_OCTAVES; i++) {
    result += snoise(p * pow(2.0, float(i)));
  }
  return result;
}

// ✅ GOOD - Reduce octaves based on distance
uniform float uCameraDistance;

float noise(vec3 p) {
  // Fewer octaves when far away (detail not visible)
  int octaves = int(mix(2.0, 8.0, 1.0 - smoothstep(10.0, 100.0, uCameraDistance)));
  float result = 0.0;
  for (int i = 0; i < 8; i++) {
    if (i >= octaves) break;
    result += snoise(p * pow(2.0, float(i)));
  }
  return result;
}
```

### 5.4 Uniform Batching - Minimize CPU-GPU Transfers

```glsl
// ❌ BAD - Many individual uniforms
uniform float uPosX;
uniform float uPosY;
uniform float uPosZ;
uniform float uRotX;
uniform float uRotY;
uniform float uRotZ;
uniform float uScaleX;
uniform float uScaleY;
uniform float uScaleZ;

// ✅ GOOD - Packed into vectors/matrices
uniform vec3 uPosition;
uniform vec3 uRotation;
uniform vec3 uScale;
// Or even better:
uniform mat4 uTransform;
```

### 5.5 Precision Optimization - Use Appropriate Precision

```glsl
// ❌ BAD - Everything highp (wastes GPU cycles)
precision highp float;

highp vec3 color;
highp float alpha;
highp vec2 uv;

// ✅ GOOD - Match precision to data needs
precision highp float;  // Default for calculations

mediump vec3 color;     // 0-1 range, mediump sufficient
mediump float alpha;    // 0-1 range
highp vec2 uv;          // Need precision for texture coords
lowp int flags;         // Boolean-like values
```

### 5.6 Cache Texture Lookups

```glsl
// ❌ BAD - Redundant texture fetches
void main() {
  vec3 diffuse = texture(uTexture, vUv).rgb;
  // ... some code ...
  float alpha = texture(uTexture, vUv).a;  // Same lookup!
  // ... more code ...
  vec3 doubled = texture(uTexture, vUv).rgb * 2.0;  // Again!
}

// ✅ GOOD - Cache the result
void main() {
  vec4 texSample = texture(uTexture, vUv);
  vec3 diffuse = texSample.rgb;
  float alpha = texSample.a;
  vec3 doubled = texSample.rgb * 2.0;
}
```

## 6. Implementation Patterns

### 6.1 Holographic Panel Shader

```glsl
// shaders/holographic-panel.frag
#version 300 es
precision highp float;

uniform float uTime;
uniform vec3 uColor;
uniform float uOpacity;
uniform vec2 uResolution;

in vec2 vUv;
out vec4 fragColor;

const int SCANLINE_COUNT = 50;

void main() {
  vec2 uv = vUv;

  // Scanline effect
  float scanline = 0.0;
  for (int i = 0; i < SCANLINE_COUNT; i++) {
    float y = float(i) / float(SCANLINE_COUNT);
    scanline += smoothstep(0.0, 0.002, abs(uv.y - y));
  }
  scanline = 1.0 - scanline * 0.3;

  // Edge glow
  float edge = 1.0 - smoothstep(0.0, 0.05, min(
    min(uv.x, 1.0 - uv.x),
    min(uv.y, 1.0 - uv.y)
  ));

  // Animated pulse
  float pulse = sin(uTime * 2.0) * 0.1 + 0.9;

  vec3 color = uColor * scanline * pulse;
  color += vec3(0.0, 0.5, 1.0) * edge * 0.5;

  fragColor = vec4(color, uOpacity);
}
```

### 6.2 Energy Field Shader

```glsl
// shaders/energy-field.frag
#version 300 es
precision highp float;

uniform float uTime;
uniform vec3 uColor;

in vec2 vUv;
in vec3 vNormal;
in vec3 vViewPosition;
out vec4 fragColor;

float snoise(vec3 v) {
  return fract(sin(dot(v, vec3(12.9898, 78.233, 45.543))) * 43758.5453);
}

void main() {
  vec3 viewDir = normalize(-vViewPosition);
  float fresnel = pow(1.0 - abs(dot(viewDir, vNormal)), 3.0);
  float noise = snoise(vec3(vUv * 5.0, uTime * 0.5));

  vec3 color = uColor * fresnel;
  color += uColor * noise * 0.2;
  float alpha = fresnel * 0.8 + noise * 0.1;

  fragColor = vec4(color, alpha);
}
```

### 6.3 Data Visualization Shader

```glsl
// shaders/data-bar.frag
#version 300 es
precision highp float;

uniform float uValue;
uniform float uThreshold;
uniform vec3 uColorLow;
uniform vec3 uColorHigh;
uniform vec3 uColorWarning;

in vec2 vUv;
out vec4 fragColor;

void main() {
  float fill = step(vUv.x, uValue);
  vec3 color = mix(uColorLow, uColorHigh, uValue);
  color = mix(color, uColorWarning, step(uThreshold, uValue));
  float gradient = vUv.y * 0.3 + 0.7;
  fragColor = vec4(color * gradient * fill, fill);
}
```

## 7. Security & Performance Standards

### 7.1 GPU Safety

| Risk | Mitigation |
|------|------------|
| Infinite loops | Always use constant loop bounds |
| GPU hangs | Test shaders with small datasets first |
| Memory exhaustion | Limit texture sizes |

### 7.2 Loop Safety Pattern

```glsl
// ❌ BAD - Dynamic loop bound
for (int i = 0; i < int(uCount); i++) { }

// ✅ GOOD - Constant loop bound
const int MAX_ITERATIONS = 100;
for (int i = 0; i < MAX_ITERATIONS; i++) {
  if (i >= int(uCount)) break;
}
```

## 8. Common Mistakes & Anti-Patterns

### 8.1 Never: Use Dynamic Loop Bounds

```glsl
// ❌ DANGEROUS - May cause GPU hang
for (int i = 0; i < uniformValue; i++) { }

// ✅ SAFE - Constant bound with early exit
const int MAX = 100;
for (int i = 0; i < MAX; i++) {
  if (i >= uniformValue) break;
}
```

### 8.2 Never: Divide Without Checking Zero

```glsl
// ❌ DANGEROUS - Division by zero
float result = value / divisor;

// ✅ SAFE - Guard against zero
float result = value / max(divisor, 0.0001);
```

## 9. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Write shader compilation test
- [ ] Write uniform accessibility test
- [ ] Create baseline images for visual regression tests
- [ ] Define performance targets (FPS, draw calls)
- [ ] Review existing shaders for reusable patterns

### Phase 2: During Implementation

- [ ] All loops have constant bounds
- [ ] No division by zero possible
- [ ] Using branchless patterns (mix/step)
- [ ] Appropriate precision qualifiers
- [ ] Texture lookups cached
- [ ] Uniforms batched into vectors/matrices

### Phase 3: Before Committing

- [ ] All shader tests pass: `npm run test:shaders`
- [ ] Visual regression tests pass: `npm run test:visual`
- [ ] Performance benchmark meets targets: `npm run bench:shaders`
- [ ] Cross-browser compatibility verified
- [ ] No artifacts at edge cases (UV 0,0 and 1,1)
- [ ] Smooth animation timing verified

## 10. Summary

GLSL shaders power the visual effects in JARVIS HUD:

1. **TDD First**: Write tests before shaders - compilation, uniforms, visual regression
2. **Performance**: Use branchless patterns, texture atlases, LOD, precision optimization
3. **Safety**: Constant loop bounds, guard divisions
4. **Testing**: Verify across target browsers, benchmark GPU performance

**Remember**: Shaders run on GPU - a single bad shader can freeze the entire system.

---

**References**:
- `references/advanced-patterns.md` - Complex shader techniques
