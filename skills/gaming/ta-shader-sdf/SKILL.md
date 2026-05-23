---
name: ta-shader-sdf
description: Signed Distance Functions for shader-based 3D primitives. Use when creating procedural geometry, raymarching, SDF terrain.
category: shader
---
# Shader SDF Skill

> "Model everything with math – SDFs enable infinite resolution procedural geometry."

## When to Use This Skill

Use when:

- Creating procedural 3D shapes in shaders
- Implementing ray marching
- Building shader-based geometry
- Creating soft/blended shapes

## Quick Start

```glsl
// Sphere SDF
float sdSphere(vec3 p, float r) {
  return length(p) - r;
}

// Box SDF
float sdBox(vec3 p, vec3 b) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// Use in fragment shader
float dist = sdSphere(position, 1.0);
if (dist < 0.0) {
  // Inside sphere
}
```

## SDF Primitives

### Basic Shapes

```glsl
// Sphere - radius r
float sdSphere(vec3 p, float r) {
  return length(p) - r;
}

// Box - size b (half-extents)
float sdBox(vec3 p, vec3 b) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

// Rounded box
float sdRoundedBox(vec3 p, vec3 b, float r) {
  vec3 q = abs(p) - b;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r;
}

// Cylinder (infinite height)
float sdCylinder(vec3 p, float r) {
  return length(p.xz) - r;
}

// Cylinder (finite height h)
float sdCylinder(vec3 p, float h, float r) {
  vec2 d = abs(vec2(length(p.xz), p.y)) - vec2(r, h);
  return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
}

// Cone
float sdCone(vec3 p, vec2 c, float h) {
  vec2 q = h * vec2(c.x / c.y, -1.0);
  vec2 w = vec2(length(p.xz), p.y);
  vec2 a = w - q * clamp(dot(w, q) / dot(q, q), 0.0, 1.0);
  vec2 b = w - q * vec2(clamp(w.x / q.x, 0.0, 1.0), 1.0);
  float k = sign(q.y);
  float d = min(dot(a, a), dot(b, b));
  float s = max(k * (w.x * q.y - w.y * q.x), k * (w.y - q.y));
  return sqrt(d) * sign(s);
}

// Torus
float sdTorus(vec3 p, vec2 t) {
  vec2 q = vec2(length(p.xz) - t.x, p.y);
  return length(q) - t.y;
}
```

### 2D Shapes (for UV patterns)

```glsl
// Circle
float sdCircle(vec2 p, float r) {
  return length(p) - r;
}

// Box 2D
float sdBox2D(vec2 p, vec2 b) {
  vec2 d = abs(p) - b;
  return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

// Triangle
float sdTriangle(vec2 p, vec2 p0, vec2 p1, vec2 p2) {
  vec2 e0 = p1 - p0;
  vec2 e1 = p2 - p1;
  vec2 e2 = p0 - p2;

  vec2 v0 = p - p0;
  vec2 v1 = p - p1;
  vec2 v2 = p - p2;

  vec2 pq0 = v0 - e0 * clamp(dot(v0, e0) / dot(e0, e0), 0.0, 1.0);
  vec2 pq1 = v1 - e1 * clamp(dot(v1, e1) / dot(e1, e1), 0.0, 1.0);
  vec2 pq2 = v2 - e2 * clamp(dot(v2, e2) / dot(e2, e2), 0.0, 1.0);

  float s = sign(e0.x * e2.y - e0.y * e2.x);
  vec2 d = min(min(vec2(dot(pq0, pq0), s * (v0.x * e0.y - v0.y * e0.x)),
                   vec2(dot(pq1, pq1), s * (v1.x * e1.y - v1.y * e1.x))),
                   vec2(dot(pq2, pq2), s * (v2.x * e2.y - v2.y * e2.x)));

  return -sqrt(d.x) * sign(d.y);
}
```

## SDF Operations

```glsl
// Smooth minimum (for organic blending)
float smin(float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}

// Union
float opUnion(float d1, float d2) {
  return min(d1, d2);
}

// Smooth union
float opSmoothUnion(float d1, float d2, float k) {
  return smin(d1, d2, k);
}

// Subtraction
float opSubtraction(float d1, float d2) {
  return max(-d1, d2);
}

// Intersection
float opIntersection(float d1, float d2) {
  return max(d1, d2);
}

// Repeat space
vec3 opRepeat(vec3 p, vec3 c) {
  return mod(p, c) - 0.5 * c;
}

// Displacement
float opDisplacement(vec3 p, float d) {
  float d1 = sdSphere(p, 1.0);
  float d2 = sin(10.0 * p.x) * sin(10.0 * p.y) * sin(10.0 * p.z) * 0.1;
  return d1 + d2;
}
```

## Ray Marching

```glsl
#define MAX_STEPS 100
#define MAX_DIST 100.0
#define SURF_DIST 0.001

float map(vec3 p) {
  // Combine SDFs here
  float sphere = sdSphere(p - vec3(0.0, 1.0, 0.0), 1.0);
  float box = sdBox(p - vec3(0.0, -1.0, 0.0), vec3(1.0));
  return opSmoothUnion(sphere, box, 0.5);
}

float rayMarch(vec3 ro, vec3 rd) {
  float dO = 0.0;
  for (int i = 0; i < MAX_STEPS; i++) {
    vec3 p = ro + rd * dO;
    float dS = map(p);
    dO += dS;
    if (dO > MAX_DIST || dS < SURF_DIST) break;
  }
  return dO;
}

vec3 getNormal(vec3 p) {
  float d = map(p);
  vec2 e = vec2(0.001, 0.0);
  vec3 n = d - vec3(
    map(p - e.xyy),
    map(p - e.yxy),
    map(p - e.yyx)
  );
  return normalize(n);
}
```

## ShaderToy MCP for SDF Research

> "Query thousands of ray marching shaders for SDF patterns and optimization techniques."

**For general ShaderToy MCP usage (tools, conversion patterns), see:** `Skill("ta-shader-development")`

### SDF-Specific Shader Search

```bash
# Search for SDF/raymarching patterns
search_shader("terrain SDF")
search_shader("raymarching clouds")
search_shader("procedural mountains")

# Get shader code for analysis
get_shader_info("Mtd3Wf")  # Vale terrain shader
get_shader_info("4tdSWr")  # Raymarching example
```

### Common ShaderToy SDF Shaders

| Shader ID | Effect | What to Extract |
|-----------|--------|-----------------|
| `4tdSWr` | Terrain Raymarching | Height SDF, smooth min, LOD |
| `Mtd3Wf` | Vale Terrain | Noise-based terrain, water |
| `XsjXRz` | Cloud SDF | FBM noise, volumetric |
| `WtBDWf` | Hologram SDF | Fresnel, scanline patterns |
| `MsS2Wc` | Ocean Waves | Displacement, foam patterns |

### SDF Patterns from ShaderToy

**Terrain Height SDF:**
```glsl
// From ShaderToy "Terrain Raymarching" shaders
float getTerrainHeight(vec2 p) {
  float h = 0.0;
  float amplitude = 1.0;
  float frequency = 1.0;

  // FBM-based terrain
  for(int i = 0; i < 6; i++) {
    h += amplitude * noise(p * frequency);
    amplitude *= 0.5;
    frequency *= 2.0;
  }

  return h * 0.3;
}

float sdTerrain(vec3 p) {
  float h = getTerrainHeight(p.xz);
  return p.y - h;
}
```

**Smooth Union for Organic Shapes:**
```glsl
// Polynomial smooth min (k = 0.1)
float smin(float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}

// Use for blending terrain features
float map(vec3 p) {
  float ground = sdTerrain(p);
  float rock = sdSphere(p - vec3(2.0, 1.0, 0.0), 0.5);
  return smin(ground, rock, 0.5);
}
```

**Displacement for Detail:**
```glsl
// Add surface detail with displacement
float opDisplacement(vec3 p, float d) {
  float disp = sin(p.x * 10.0) * sin(p.z * 10.0) * 0.05;
  return d + disp;
}

void main() {
  float d = map(p);
  d = opDisplacement(p, d);
  // ...
}
```

### Attribution Protocol

```tsx
/**
 * Terrain Raymarching Shader
 * Based on "[Original Name]" by [Author] on ShaderToy
 * Original: https://www.shadertoy.com/view/[shaderId]
 * SDF patterns: terrain height, smooth union, FBM noise
 * Adapted for React Three Fiber by [Your Name]
 */
```

## React Three Fiber Usage

```tsx
import { shaderMaterial } from '@react-three/drei';
import { extend } from '@react-three/fiber';

const SDFMaterial = shaderMaterial(
  { uTime: 0, uColor: new THREE.Color(0.0, 0.5, 1.0) },
  // Vertex shader
  `
    varying vec3 vPosition;
    varying vec3 vNormal;
    void main() {
      vPosition = position;
      vNormal = normal;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  // Fragment shader with SDF
  `
    uniform float uTime;
    uniform vec3 uColor;
    varying vec3 vPosition;
    varying vec3 vNormal;

    float sdSphere(vec3 p, float r) {
      return length(p) - r;
    }

    void main() {
      // Animate SDF
      vec3 p = vPosition;
      p.x += sin(uTime) * 0.5;

      // Calculate SDF
      float d = sdSphere(p, 1.0);

      // Color based on distance
      vec3 color = uColor;
      color += vec3(d * 0.5);

      gl_FragColor = vec4(color, 1.0);
    }
  `
);

extend({ SDFMaterial });
```

## Anti-Patterns

❌ **DON'T:**

- Use SDFs for simple geometry (use meshes instead)
- Forget to normalize normals
- Use too many ray march steps on mobile
- Create complex SDFs without optimization

✅ **DO:**

- Use SDFs for procedural/organic shapes
- Cache SDF calculations when possible
- Optimize step count based on scene complexity
- Combine with traditional geometry

## Checklist

Before using SDF shaders:

- [ ] SDF shape is appropriate for use case
- [ ] Ray march steps optimized for target platform
- [ ] Normal calculation is correct
- [ ] Smooth minimum used for blending
- [ ] Performance tested on target hardware

## Related Skills

For general ShaderToy MCP usage: `Skill("ta-shader-development")`
For material basics: `Skill("ta-r3f-materials")`

## External References

- [Inigo Quilez SDF Functions](https://iquilezles.org/articles/distfunctions/)
- [Shadertoy SDF Examples](https://www.shadertoy.com/)
