---
name: forge-shader-noise
description: Add GPU noise functions (hash, value, Perlin, fBm, domain warping) to an SDL GPU project
user_invokable: true
---

# Shader Noise

Add procedural noise functions to an SDL GPU fragment shader. Implements
GPU-friendly hash functions, value noise, Perlin gradient noise, fBm
(fractal Brownian motion), and domain warping — all running per-pixel
on the GPU with no texture assets.

## When to use

- Procedural textures (marble, wood, clouds, terrain)
- Terrain height and coloring without texture assets
- Dissolve and erosion effects
- Adding organic variation to materials or lighting
- Any situation requiring randomness in a fragment shader

## HLSL noise library

Add these functions to your fragment shader. They are self-contained
and require no external textures or buffers.

### Hash functions

GPU shaders lack `rand()`. Use deterministic integer hashes instead —
same input always produces the same output.

```hlsl
/* Thomas Wang 32-bit integer hash — good avalanche properties */
uint wang_hash(uint seed)
{
    seed = (seed ^ 61u) ^ (seed >> 16u);
    seed *= 9u;
    seed = seed ^ (seed >> 4u);
    seed *= 0x27d4eb2du;
    seed = seed ^ (seed >> 15u);
    return seed;
}

/* Map hash to float in [0, 1) */
float hash_to_float(uint h)
{
    return float(h) / 4294967296.0;
}

/* Combine two hash values (Boost hash_combine pattern) */
uint hash_combine(uint seed, uint value)
{
    return seed ^ (value + 0x9e3779b9u + (seed << 6u) + (seed >> 2u));
}

/* Hash 2D integer coordinates to uint */
uint hash2d_uint(int2 p)
{
    uint h = wang_hash(uint(p.x));
    h = hash_combine(h, uint(p.y));
    return wang_hash(h);
}

/* Hash 2D integer coordinates to float in [0, 1) */
float hash2d(int2 p)
{
    return hash_to_float(hash2d_uint(p));
}
```

### White noise

Random value per integer cell. Useful for TV static, sparkle effects.

```hlsl
float white_noise(float2 p, float time_seed)
{
    int2 ip = int2(floor(p));
    uint seed = hash_combine(hash2d_uint(ip), uint(time_seed * 60.0));
    return hash_to_float(seed);
}
```

### Value noise

Smoothly interpolated random values at lattice points.

```hlsl
float value_noise(float2 p)
{
    int2 i = int2(floor(p));
    float2 f = frac(p);
    float2 u = f * f * (3.0 - 2.0 * f);  /* Hermite smoothstep */

    float a = hash2d(i);
    float b = hash2d(i + int2(1, 0));
    float c = hash2d(i + int2(0, 1));
    float d = hash2d(i + int2(1, 1));

    return lerp(lerp(a, b, u.x), lerp(c, d, u.x), u.y);
}
```

### Gradient noise (Perlin 2D)

Smoother than value noise with C2 continuity.

```hlsl
float grad2d(uint hash, float2 d)
{
    uint h = hash & 3u;
    float u = ((h & 1u) != 0u) ? -d.x : d.x;
    float v = ((h & 2u) != 0u) ? -d.y : d.y;
    return u + v;
}

float2 quintic(float2 t)
{
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
}

float perlin2d(float2 p)
{
    int2 i = int2(floor(p));
    float2 f = frac(p);
    float2 u = quintic(f);

    float a = grad2d(hash2d_uint(i),              f);
    float b = grad2d(hash2d_uint(i + int2(1, 0)), f - float2(1.0, 0.0));
    float c = grad2d(hash2d_uint(i + int2(0, 1)), f - float2(0.0, 1.0));
    float d = grad2d(hash2d_uint(i + int2(1, 1)), f - float2(1.0, 1.0));

    return lerp(lerp(a, b, u.x), lerp(c, d, u.x), u.y);
}
```

### fBm (fractal Brownian motion)

Stack multiple octaves of Perlin noise for natural fractal detail.

```hlsl
float fbm(float2 p)
{
    float value     = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;

    for (int oct = 0; oct < 6; oct++)
    {
        value     += amplitude * perlin2d(p * frequency);
        frequency *= 2.0;   /* lacunarity  */
        amplitude *= 0.5;   /* persistence */
    }

    return value;
}
```

### Domain warping

Compose fBm with itself for organic, marble-like patterns.

```hlsl
float domain_warp(float2 p)
{
    float2 q = float2(
        fbm(p + float2(0.0, 0.0)),
        fbm(p + float2(5.2, 1.3))
    );

    float2 r = float2(
        fbm(p + 4.0 * q + float2(1.7, 9.2)),
        fbm(p + 4.0 * q + float2(8.3, 2.8))
    );

    return fbm(p + 4.0 * r);
}
```

### Dithering (Interleaved Gradient Noise)

Break up 8-bit color banding with blue-noise-like dithering.

```hlsl
float ign(float2 screen_pos)
{
    float3 ign_coeffs = float3(0.06711056, 0.00583715, 52.9829189);
    return frac(ign_coeffs.z * frac(dot(screen_pos, ign_coeffs.xy)));
}

/* Apply after computing final color: */
color += (ign(screen_pos) - 0.5) / 255.0;
```

## Integration pattern

### Using noise in an existing scene shader

Add the noise functions to your fragment shader and use them to modify
materials, lighting, or geometry:

```hlsl
/* Procedural terrain coloring */
float height = fbm(world_pos.xz * 0.1);
float3 base_color = terrain_color(height);

/* Add organic variation to a material */
float variation = perlin2d(world_pos.xz * 2.0 + time * 0.1);
diffuse_color *= 0.9 + 0.1 * variation;

/* Dissolve effect */
float noise = fbm(world_pos * 3.0);
clip(noise - dissolve_threshold);  /* discard if below threshold */
```

### Fullscreen noise visualization

For standalone noise visualization, use the SV_VertexID fullscreen quad
pattern from [Lesson 21 — HDR & Tone Mapping](../../../lessons/gpu/21-hdr-tone-mapping/)
(no vertex buffer, pipeline with no vertex input state).

Fragment uniforms (register b0, space3 for SDL GPU):

```hlsl
cbuffer NoiseParams : register(b0, space3)
{
    float  time;
    int    mode;
    int    dither_enabled;
    float  scale;
    float2 resolution;
    float2 _pad;
};
```

## C-side uniform struct

```c
typedef struct NoiseUniforms {
    float time;
    int   mode;
    int   dither_enabled;
    float scale;
    vec2  resolution;
    float _pad[2];
} NoiseUniforms;
```

## Common patterns

### Aspect-correct noise coordinates

```hlsl
float aspect = resolution.x / resolution.y;
float2 p = uv * scale;
p.x *= aspect;  /* prevent stretching */
```

### Remapping noise range

Perlin/fBm output is approximately [-1, 1]. Remap to [0, 1] for
display or color mapping:

```hlsl
float n = fbm(p);
n = n * 0.5 + 0.5;  /* remap to [0, 1] */
```

### Terrain color mapping

Map noise height to biome colors with smooth transitions:

```hlsl
float3 color = deep_water;
color = lerp(color, grass,  smoothstep(0.38, 0.50, height));
color = lerp(color, rock,   smoothstep(0.62, 0.75, height));
color = lerp(color, snow,   smoothstep(0.75, 0.85, height));
```

## Common mistakes

- **Forgetting aspect ratio correction** — multiply `uv.x *= aspect` before
  sampling noise, otherwise noise cells appear stretched on non-square windows
- **Not remapping Perlin/fBm output** — `perlin2d()` returns approximately
  [-1, 1]; use `n * 0.5 + 0.5` to remap to [0, 1] for display or color mapping
- **cbuffer alignment** — the uniform struct must be padded to a multiple of
  16 bytes; misaligned fields silently read wrong values on some backends
- **Using `int` casts on negative coordinates** — `int2(floor(p))` is correct;
  `int2(p)` truncates toward zero, causing a seam at the origin where two
  adjacent cells map to the same integer
- **Animating white noise with `frac(time)`** — produces periodic patterns;
  use `hash_combine` with an integer time seed instead for true per-frame
  randomness

## Reference

- [Lesson 25 — Shader Noise](../../../lessons/gpu/25-shader-noise/)
- [Math Lesson 12 — Hash Functions](../../../lessons/math/12-hash-functions/)
- [Math Lesson 13 — Gradient Noise](../../../lessons/math/13-gradient-noise/)
- [Math Lesson 14 — Blue Noise](../../../lessons/math/14-blue-noise-sequences/)
