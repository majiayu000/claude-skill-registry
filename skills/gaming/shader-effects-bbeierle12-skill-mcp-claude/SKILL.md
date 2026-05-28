---
name: shader-effects
description: Visual shader effects—glow/bloom, chromatic aberration, distortion, vignette, film grain, scanlines, glitch, dissolve, outline, and fresnel. Use when adding visual polish, post-processing effects, or stylized rendering to shaders.
---

# Shader Effects

Visual effects that add polish, style, and atmosphere to shader output.

## Quick Start

```glsl
// Combine multiple effects
vec3 color = baseColor;
color = applyVignette(color, uv, 0.5);
color = applyGrain(color, uv, uTime, 0.1);
color = applyChromaticAberration(color, uv, 0.005);
```

## Glow / Bloom

### Simple Glow

```glsl
// Distance-based glow
float glow(float d, float radius, float intensity) {
  return pow(radius / max(d, 0.001), intensity);
}

// Usage
float d = sdCircle(uv, 0.2);
vec3 color = vec3(glow(d, 0.1, 2.0)) * glowColor;
```

### Bloom (Multi-sample)

```glsl
// Sample in cross pattern for cheap bloom
vec3 bloom(sampler2D tex, vec2 uv, float radius) {
  vec3 color = vec3(0.0);
  float total = 0.0;
  
  for (float x = -4.0; x <= 4.0; x += 1.0) {
    for (float y = -4.0; y <= 4.0; y += 1.0) {
      float weight = 1.0 / (1.0 + length(vec2(x, y)));
      color += texture2D(tex, uv + vec2(x, y) * radius).rgb * weight;
      total += weight;
    }
  }
  
  return color / total;
}
```

### Gaussian Blur (Separable)

```glsl
// Horizontal pass
vec3 blurH(sampler2D tex, vec2 uv, float radius) {
  vec3 color = vec3(0.0);
  float weights[5] = float[](0.227, 0.194, 0.121, 0.054, 0.016);
  
  color += texture2D(tex, uv).rgb * weights[0];
  for (int i = 1; i < 5; i++) {
    vec2 offset = vec2(float(i) * radius, 0.0);
    color += texture2D(tex, uv + offset).rgb * weights[i];
    color += texture2D(tex, uv - offset).rgb * weights[i];
  }
  
  return color;
}

// Vertical pass (same, swap x/y)
```

## Chromatic Aberration

```glsl
vec3 chromaticAberration(sampler2D tex, vec2 uv, float amount) {
  vec2 dir = uv - 0.5;
  vec2 offset = dir * amount;
  
  vec3 color;
  color.r = texture2D(tex, uv + offset).r;
  color.g = texture2D(tex, uv).g;
  color.b = texture2D(tex, uv - offset).b;
  
  return color;
}

// Radial chromatic aberration (stronger at edges)
vec3 radialCA(sampler2D tex, vec2 uv, float amount) {
  vec2 dir = uv - 0.5;
  float dist = length(dir);
  vec2 offset = dir * amount * dist;
  
  vec3 color;
  color.r = texture2D(tex, uv + offset).r;
  color.g = texture2D(tex, uv).g;
  color.b = texture2D(tex, uv - offset).b;
  
  return color;
}
```

## Distortion

### Wave Distortion

```glsl
vec2 waveDistort(vec2 uv, float time, float freq, float amp) {
  uv.x += sin(uv.y * freq + time) * amp;
  uv.y += cos(uv.x * freq + time) * amp;
  return uv;
}
```

### Barrel/Pincushion Distortion

```glsl
vec2 barrelDistort(vec2 uv, float amount) {
  vec2 centered = uv - 0.5;
  float r2 = dot(centered, centered);
  vec2 distorted = centered * (1.0 + amount * r2);
  return distorted + 0.5;
}
```

### Heat Haze

```glsl
vec2 heatHaze(vec2 uv, float time, float intensity) {
  float noise = snoise(vec3(uv * 10.0, time));
  return uv + vec2(noise) * intensity;
}
```

### Ripple

```glsl
vec2 ripple(vec2 uv, vec2 center, float time, float freq, float amp) {
  vec2 dir = uv - center;
  float dist = length(dir);
  float wave = sin(dist * freq - time) * amp;
  return uv + normalize(dir) * wave;
}
```

## Vignette

```glsl
vec3 vignette(vec3 color, vec2 uv, float intensity, float smoothness) {
  vec2 centered = uv - 0.5;
  float dist = length(centered);
  float vig = smoothstep(0.5, 0.5 - smoothness, dist * intensity);
  return color * vig;
}

// Colored vignette
vec3 coloredVignette(vec3 color, vec2 uv, vec3 vigColor, float intensity) {
  vec2 centered = uv - 0.5;
  float dist = length(centered);
  float vig = smoothstep(0.0, 0.5, dist * intensity);
  return mix(color, vigColor, vig);
}
```

## Film Grain

```glsl
float random(vec2 st) {
  return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

vec3 filmGrain(vec3 color, vec2 uv, float time, float intensity) {
  float grain = random(uv + fract(time)) * 2.0 - 1.0;
  return color + grain * intensity;
}

// Animated grain (smoother)
vec3 animatedGrain(vec3 color, vec2 uv, float time, float intensity) {
  float x = (uv.x + 4.0) * (uv.y + 4.0) * (time * 10.0);
  float grain = mod((mod(x, 13.0) + 1.0) * (mod(x, 123.0) + 1.0), 0.01) - 0.005;
  return color + grain * intensity * 50.0;
}
```

## Scanlines

```glsl
vec3 scanlines(vec3 color, vec2 uv, float count, float intensity) {
  float scanline = sin(uv.y * count * 3.14159) * 0.5 + 0.5;
  return color * (1.0 - intensity + scanline * intensity);
}

// CRT-style scanlines
vec3 crtScanlines(vec3 color, vec2 fragCoord, float intensity) {
  float scanline = sin(fragCoord.y * 0.7) * 0.1 * intensity;
  float flicker = sin(uTime * 10.0) * 0.01 * intensity;
  return color * (1.0 - scanline - flicker);
}
```

## Glitch

```glsl
vec3 glitch(sampler2D tex, vec2 uv, float time, float intensity) {
  // Random block offset
  float blockTime = floor(time * 20.0);
  float blockRand = random(vec2(blockTime, 0.0));
  
  if (blockRand > 0.9) {
    // Horizontal shift
    float shift = (random(vec2(uv.y, blockTime)) - 0.5) * intensity;
    uv.x += shift;
  }
  
  // Color channel split
  vec3 color;
  color.r = texture2D(tex, uv + vec2(intensity * 0.01, 0.0)).r;
  color.g = texture2D(tex, uv).g;
  color.b = texture2D(tex, uv - vec2(intensity * 0.01, 0.0)).b;
  
  // Random color inversion blocks
  if (random(vec2(floor(uv.y * 20.0), blockTime)) > 0.98) {
    color = 1.0 - color;
  }
  
  return color;
}

// Digital glitch with blocks
vec3 blockGlitch(sampler2D tex, vec2 uv, float time, float intensity) {
  vec2 blockSize = vec2(0.1, 0.05);
  vec2 block = floor(uv / blockSize);
  float blockRand = random(block + floor(time * 10.0));
  
  if (blockRand > 1.0 - intensity * 0.1) {
    uv.x += (blockRand - 0.5) * 0.1;
  }
  
  return texture2D(tex, uv).rgb;
}
```

## Dissolve

```glsl
vec3 dissolve(vec3 color, vec2 uv, float progress, float edgeWidth, vec3 edgeColor) {
  float noise = snoise(uv * 10.0);
  
  // Discard dissolved pixels
  if (noise < progress) {
    discard;
  }
  
  // Edge glow
  float edge = smoothstep(progress, progress + edgeWidth, noise);
  return mix(edgeColor, color, edge);
}

// With alpha instead of discard
vec4 dissolveAlpha(vec3 color, vec2 uv, float progress, float edgeWidth, vec3 edgeColor) {
  float noise = snoise(uv * 10.0);
  
  float alpha = smoothstep(progress - edgeWidth, progress, noise);
  float edge = smoothstep(progress, progress + edgeWidth, noise);
  vec3 finalColor = mix(edgeColor, color, edge);
  
  return vec4(finalColor, alpha);
}
```

## Outline

```glsl
// SDF-based outline
vec3 sdfOutline(float d, vec3 fillColor, vec3 outlineColor, float outlineWidth) {
  float aa = fwidth(d);
  float fill = smoothstep(aa, -aa, d);
  float outline = smoothstep(aa, -aa, abs(d) - outlineWidth);
  
  return mix(vec3(0.0), mix(outlineColor, fillColor, fill), max(fill, outline));
}

// Texture-based outline (sample neighbors)
float textureOutline(sampler2D tex, vec2 uv, float thickness) {
  float alpha = texture2D(tex, uv).a;
  
  float outline = 0.0;
  for (float x = -1.0; x <= 1.0; x += 1.0) {
    for (float y = -1.0; y <= 1.0; y += 1.0) {
      outline += texture2D(tex, uv + vec2(x, y) * thickness).a;
    }
  }
  
  return clamp(outline - alpha * 9.0, 0.0, 1.0);
}
```

## Fresnel / Rim Light

```glsl
// 3D fresnel (needs view direction and normal)
float fresnel(vec3 viewDir, vec3 normal, float power) {
  return pow(1.0 - max(dot(viewDir, normal), 0.0), power);
}

// 2D fake fresnel (based on UV distance from center)
float fakeFresnel2D(vec2 uv, float power) {
  vec2 centered = uv - 0.5;
  float dist = length(centered) * 2.0;
  return pow(dist, power);
}

// Usage
vec3 color = baseColor;
float rim = fresnel(viewDir, normal, 3.0);
color += rimColor * rim * rimIntensity;
```

## Color Grading

### Contrast / Brightness / Saturation

```glsl
vec3 adjustContrast(vec3 color, float contrast) {
  return (color - 0.5) * contrast + 0.5;
}

vec3 adjustBrightness(vec3 color, float brightness) {
  return color + brightness;
}

vec3 adjustSaturation(vec3 color, float saturation) {
  float gray = dot(color, vec3(0.299, 0.587, 0.114));
  return mix(vec3(gray), color, saturation);
}
```

### Color Remap

```glsl
vec3 colorRemap(vec3 color, vec3 shadowColor, vec3 highlightColor) {
  float luma = dot(color, vec3(0.299, 0.587, 0.114));
  return mix(shadowColor, highlightColor, luma);
}
```

### Posterize

```glsl
vec3 posterize(vec3 color, float levels) {
  return floor(color * levels) / levels;
}
```

## Dithering

```glsl
// Bayer 4x4 dithering
float bayer4x4(vec2 fragCoord) {
  int x = int(mod(fragCoord.x, 4.0));
  int y = int(mod(fragCoord.y, 4.0));
  
  int bayer[16] = int[](
    0, 8, 2, 10,
    12, 4, 14, 6,
    3, 11, 1, 9,
    15, 7, 13, 5
  );
  
  return float(bayer[y * 4 + x]) / 16.0;
}

vec3 dither(vec3 color, vec2 fragCoord, float levels) {
  float threshold = bayer4x4(fragCoord);
  return floor(color * levels + threshold) / levels;
}
```

## Combining Effects

```glsl
vec3 applyEffects(vec3 color, vec2 uv, float time) {
  // Order matters!
  
  // 1. Distortion (modify UVs first)
  // Already applied to texture sampling
  
  // 2. Color adjustments
  color = adjustContrast(color, 1.1);
  color = adjustSaturation(color, 1.2);
  
  // 3. Chromatic aberration
  // (apply during texture sampling)
  
  // 4. Vignette
  color = vignette(color, uv, 1.2, 0.4);
  
  // 5. Film grain (last, before final output)
  color = filmGrain(color, uv, time, 0.05);
  
  return color;
}
```

## File Structure

```
shader-effects/
├── SKILL.md
├── references/
│   ├── effect-order.md       # Recommended effect ordering
│   └── performance.md        # Effect costs
└── scripts/
    ├── effects/
    │   ├── glow.glsl         # Glow/bloom
    │   ├── distortion.glsl   # Distortion effects
    │   ├── color.glsl        # Color grading
    │   └── retro.glsl        # CRT/retro effects
    └── examples/
        ├── cyberpunk.glsl    # Cyberpunk style combo
        └── vintage.glsl      # Vintage film look
```

## Reference

- `references/effect-order.md` — Recommended order for combining effects
- `references/performance.md` — Performance cost of each effect
