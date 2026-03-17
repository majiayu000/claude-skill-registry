---
name: shader-noise
description: Procedural noise functions in GLSL—Perlin, simplex, Worley/cellular, value noise, FBM (Fractal Brownian Motion), turbulence, and domain warping. Use when creating organic textures, terrain, clouds, water, fire, or any natural-looking procedural patterns.
---

# Shader Noise

Procedural noise creates natural-looking randomness. Unlike `random()`, noise is coherent—nearby inputs produce nearby outputs.

## Quick Start

```glsl
// Simple usage
float n = snoise(uv * 5.0);              // Simplex 2D
float n = snoise(vec3(uv, uTime));       // Animated 3D
float n = fbm(uv, 4);                    // Layered detail

// Common range adjustments
float n01 = n * 0.5 + 0.5;               // [-1,1] → [0,1]
float sharp = step(0.0, n);              // Binary threshold
float smooth = smoothstep(-0.2, 0.2, n); // Soft threshold
```

## Noise Types Comparison

| Type | Speed | Quality | Use Case |
|------|-------|---------|----------|
| Value | Fastest | Blocky | Quick prototypes |
| Perlin | Fast | Good | General purpose |
| Simplex | Fast | Best | Modern default |
| Worley | Slower | Cellular | Cells, cracks, scales |

## Value Noise

Interpolated random values at grid points. Simple but blocky.

```glsl
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

float valueNoise(vec2 st) {
  vec2 i = floor(st);
  vec2 f = fract(st);
  
  // Smoothstep interpolation
  vec2 u = f * f * (3.0 - 2.0 * f);
  
  // Four corners
  float a = random(i);
  float b = random(i + vec2(1.0, 0.0));
  float c = random(i + vec2(0.0, 1.0));
  float d = random(i + vec2(1.0, 1.0));
  
  // Bilinear interpolation
  return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
```

## Simplex Noise (Recommended)

Best quality-to-performance ratio. Use this as default.

### 2D Simplex

```glsl
vec3 permute(vec3 x) { return mod(((x*34.0)+1.0)*x, 289.0); }

float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                      -0.577350269189626, 0.024390243902439);
  vec2 i  = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod(i, 289.0);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
  m = m*m;
  m = m*m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
  vec3 g;
  g.x = a0.x * x0.x + h.x * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
```

### 3D Simplex

```glsl
vec4 permute(vec4 x) { return mod(((x*34.0)+1.0)*x, 289.0); }
vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

float snoise(vec3 v) {
  const vec2 C = vec2(1.0/6.0, 1.0/3.0);
  const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
  
  vec3 i  = floor(v + dot(v, C.yyy));
  vec3 x0 = v - i + dot(i, C.xxx);
  
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min(g.xyz, l.zxy);
  vec3 i2 = max(g.xyz, l.zxy);
  
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy;
  vec3 x3 = x0 - D.yyy;
  
  i = mod(i, 289.0);
  vec4 p = permute(permute(permute(
    i.z + vec4(0.0, i1.z, i2.z, 1.0))
    + i.y + vec4(0.0, i1.y, i2.y, 1.0))
    + i.x + vec4(0.0, i1.x, i2.x, 1.0));
    
  float n_ = 0.142857142857;
  vec3 ns = n_ * D.wyz - D.xzx;
  
  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
  
  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_);
  
  vec4 x = x_ *ns.x + ns.yyyy;
  vec4 y = y_ *ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);
  
  vec4 b0 = vec4(x.xy, y.xy);
  vec4 b1 = vec4(x.zw, y.zw);
  
  vec4 s0 = floor(b0)*2.0 + 1.0;
  vec4 s1 = floor(b1)*2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));
  
  vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy;
  vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww;
  
  vec3 p0 = vec3(a0.xy, h.x);
  vec3 p1 = vec3(a0.zw, h.y);
  vec3 p2 = vec3(a1.xy, h.z);
  vec3 p3 = vec3(a1.zw, h.w);
  
  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
  p0 *= norm.x;
  p1 *= norm.y;
  p2 *= norm.z;
  p3 *= norm.w;
  
  vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
}
```

## Worley (Cellular) Noise

Creates cell-like patterns. Great for scales, cracks, caustics.

```glsl
vec2 random2(vec2 st) {
  st = vec2(dot(st, vec2(127.1, 311.7)), dot(st, vec2(269.5, 183.3)));
  return fract(sin(st) * 43758.5453123);
}

float worley(vec2 st) {
  vec2 i_st = floor(st);
  vec2 f_st = fract(st);
  
  float minDist = 1.0;
  
  // Check 3x3 neighborhood
  for (int y = -1; y <= 1; y++) {
    for (int x = -1; x <= 1; x++) {
      vec2 neighbor = vec2(float(x), float(y));
      vec2 point = random2(i_st + neighbor);
      
      // Animate points
      // point = 0.5 + 0.5 * sin(uTime + 6.2831 * point);
      
      vec2 diff = neighbor + point - f_st;
      float dist = length(diff);
      minDist = min(minDist, dist);
    }
  }
  
  return minDist;
}

// F2 - F1 variant (cracks/veins)
vec2 worley2(vec2 st) {
  vec2 i_st = floor(st);
  vec2 f_st = fract(st);
  
  float f1 = 1.0;  // Closest
  float f2 = 1.0;  // Second closest
  
  for (int y = -1; y <= 1; y++) {
    for (int x = -1; x <= 1; x++) {
      vec2 neighbor = vec2(float(x), float(y));
      vec2 point = random2(i_st + neighbor);
      vec2 diff = neighbor + point - f_st;
      float dist = length(diff);
      
      if (dist < f1) {
        f2 = f1;
        f1 = dist;
      } else if (dist < f2) {
        f2 = dist;
      }
    }
  }
  
  return vec2(f1, f2);
}
```

## FBM (Fractal Brownian Motion)

Layer multiple noise octaves for natural detail at all scales.

```glsl
float fbm(vec2 st, int octaves) {
  float value = 0.0;
  float amplitude = 0.5;
  float frequency = 1.0;
  
  for (int i = 0; i < octaves; i++) {
    value += amplitude * snoise(st * frequency);
    frequency *= 2.0;      // Lacunarity
    amplitude *= 0.5;      // Gain/Persistence
  }
  
  return value;
}

// Configurable FBM
float fbm(vec2 st, int octaves, float lacunarity, float gain) {
  float value = 0.0;
  float amplitude = 0.5;
  float frequency = 1.0;
  
  for (int i = 0; i < octaves; i++) {
    value += amplitude * snoise(st * frequency);
    frequency *= lacunarity;
    amplitude *= gain;
  }
  
  return value;
}
```

### FBM Variants

```glsl
// Ridged FBM (mountains, lightning)
float ridgedFbm(vec2 st, int octaves) {
  float value = 0.0;
  float amplitude = 0.5;
  float frequency = 1.0;
  
  for (int i = 0; i < octaves; i++) {
    float n = snoise(st * frequency);
    n = 1.0 - abs(n);  // Ridge
    n = n * n;          // Sharpen
    value += amplitude * n;
    frequency *= 2.0;
    amplitude *= 0.5;
  }
  
  return value;
}

// Turbulence (absolute value, always positive)
float turbulence(vec2 st, int octaves) {
  float value = 0.0;
  float amplitude = 0.5;
  float frequency = 1.0;
  
  for (int i = 0; i < octaves; i++) {
    value += amplitude * abs(snoise(st * frequency));
    frequency *= 2.0;
    amplitude *= 0.5;
  }
  
  return value;
}
```

## Domain Warping

Distort the input coordinates with noise for organic shapes.

```glsl
// Simple domain warp
float warpedNoise(vec2 st) {
  vec2 q = vec2(
    snoise(st),
    snoise(st + vec2(5.2, 1.3))
  );
  
  return snoise(st + q * 2.0);
}

// Double domain warp (more complex)
float doubleWarp(vec2 st) {
  vec2 q = vec2(
    fbm(st, 4),
    fbm(st + vec2(5.2, 1.3), 4)
  );
  
  vec2 r = vec2(
    fbm(st + q * 4.0 + vec2(1.7, 9.2), 4),
    fbm(st + q * 4.0 + vec2(8.3, 2.8), 4)
  );
  
  return fbm(st + r * 4.0, 4);
}

// Animated warp
float animatedWarp(vec2 st, float time) {
  vec2 q = vec2(
    fbm(st + vec2(0.0, 0.0), 4),
    fbm(st + vec2(5.2, 1.3), 4)
  );
  
  vec2 r = vec2(
    fbm(st + q * 4.0 + vec2(1.7, 9.2) + 0.15 * time, 4),
    fbm(st + q * 4.0 + vec2(8.3, 2.8) + 0.126 * time, 4)
  );
  
  return fbm(st + r * 4.0, 4);
}
```

## Common Use Cases

### Terrain Height

```glsl
float terrainHeight(vec2 pos) {
  float height = 0.0;
  
  // Base terrain
  height += fbm(pos * 0.01, 6) * 100.0;
  
  // Mountains (ridged)
  height += ridgedFbm(pos * 0.005, 4) * 200.0;
  
  // Detail
  height += snoise(pos * 0.1) * 5.0;
  
  return height;
}
```

### Clouds

```glsl
float clouds(vec2 uv, float time) {
  vec2 motion = vec2(time * 0.1, 0.0);
  
  float density = fbm(uv * 3.0 + motion, 5);
  density = smoothstep(0.0, 0.5, density);
  
  return density;
}
```

### Fire/Flames

```glsl
float fire(vec2 uv, float time) {
  // Upward motion
  uv.y -= time * 2.0;
  
  // Turbulent distortion
  float turb = turbulence(uv * 4.0, 4);
  
  // Fade out at top
  float fade = 1.0 - uv.y;
  
  return turb * fade;
}
```

### Water Caustics

```glsl
float caustics(vec2 uv, float time) {
  vec2 w = worley2(uv * 8.0 + time * 0.5);
  return pow(1.0 - w.x, 3.0);
}
```

### Marble/Stone

```glsl
float marble(vec2 uv) {
  float n = fbm(uv * 2.0, 4);
  float veins = sin(uv.x * 10.0 + n * 10.0);
  return veins * 0.5 + 0.5;
}
```

## Performance Tips

| Technique | Impact |
|-----------|--------|
| Fewer octaves in FBM | Major speedup |
| 2D vs 3D noise | 2D ~2x faster |
| Bake to texture | Massive speedup for static |
| Lower frequency = fewer samples | Faster |

## File Structure

```
shader-noise/
├── SKILL.md
├── references/
│   ├── noise-comparison.md    # Visual comparison of types
│   └── optimization.md        # Performance techniques
└── scripts/
    ├── noise/
    │   ├── simplex2d.glsl     # Copy-paste simplex 2D
    │   ├── simplex3d.glsl     # Copy-paste simplex 3D
    │   ├── worley.glsl        # Copy-paste Worley
    │   └── fbm.glsl           # FBM variants
    └── examples/
        ├── terrain.glsl       # Terrain generation
        ├── clouds.glsl        # Cloud shader
        └── fire.glsl          # Fire effect
```

## Reference

- `references/noise-comparison.md` — Visual comparison of noise types
- `references/optimization.md` — Performance optimization techniques
