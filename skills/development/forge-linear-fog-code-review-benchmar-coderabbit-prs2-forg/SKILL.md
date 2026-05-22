---
name: forge-linear-fog
description: >
  Add depth-based distance fog to an SDL GPU project. Supports linear,
  exponential, and exponential-squared modes. Fog is applied in the fragment
  shader after lighting, blending the lit color toward a fog color based on
  camera distance.
---

# Linear Fog Skill

Adds distance fog to any SDL3 GPU scene. Derived from Lesson 20.

## When to use

- Adding atmospheric perspective to a 3D scene
- Fading distant objects into a background color
- Simulating haze, mist, or ground fog
- Hiding the far-plane clipping boundary

## Fog uniform block (append to existing fragment cbuffer)

```hlsl
/* Append these fields to your existing fragment uniform buffer.
 * Total addition: 32 bytes (2 x float4 worth). */
float4 fog_color;     /* Must match the clear color (rgb)    */
float  fog_start;     /* Linear mode: distance where fog begins */
float  fog_end;       /* Linear mode: fully fogged distance     */
float  fog_density;   /* Exp/Exp2 modes: density coefficient    */
uint   fog_mode;      /* 0 = linear, 1 = exp, 2 = exp-squared  */
```

Matching C struct fields:

```c
float fog_color[4];
float fog_start;
float fog_end;
float fog_density;
Uint32 fog_mode;
```

## HLSL fog calculation (paste after lighting)

```hlsl
/* Compute Euclidean distance from fragment to camera. */
float dist = length(eye_pos.xyz - input.world_pos);

float fog_factor = 1.0;
if (fog_mode == 0)
{
    /* Linear */
    fog_factor = saturate((fog_end - dist) / (fog_end - fog_start));
}
else if (fog_mode == 1)
{
    /* Exponential */
    fog_factor = saturate(exp(-fog_density * dist));
}
else
{
    /* Exponential squared */
    float f = fog_density * dist;
    fog_factor = saturate(exp(-(f * f)));
}

/* Blend: fog_factor=1 → lit color, fog_factor=0 → fog color */
float3 final_color = lerp(fog_color.rgb, lit_color, fog_factor);
```

## Typical parameter values

| Parameter | Value | Notes |
|-----------|-------|-------|
| fog_color | match your clear color | Must equal the framebuffer clear color |
| fog_start | 2.0 | Linear mode: fully visible before this distance |
| fog_end | 18.0 | Linear mode: fully fogged beyond this distance |
| fog_density (exp) | 0.12 | Exponential mode |
| fog_density (exp2) | 0.08 | Exp-squared mode |

## Key rules

1. **Fog color = clear color.** Always set the framebuffer clear color to the
   same RGB as the fog color. Otherwise there will be a visible seam at the
   horizon.

2. **Apply fog to ALL shaders.** Every fragment shader in the scene (objects,
   grid, terrain, particles) must apply the same fog with the same parameters.
   Inconsistent fog breaks the atmospheric illusion.

3. **Use Euclidean distance, not Z depth.** Compute `length(eye - frag_pos)`
   in world space.  Using only the Z component causes fog to shift when the
   camera rotates.

4. **Fog goes after lighting.** Compute the full Blinn-Phong (or PBR) result
   first, then blend it toward the fog color.  Applying fog to individual
   lighting terms produces incorrect results.

5. **Clamp the fog factor.** Use `saturate()` to keep the factor in [0, 1].
   Without clamping, objects beyond the fog end distance can produce negative
   values that invert the fog.

## Common mistakes

- **Fog color doesn't match clear color** — creates a visible horizon line
  between fogged geometry and the background.
- **Only one shader has fog** — the grid floor appears to float on top of the
  fog while objects fade correctly (or vice versa).
- **Using Z depth instead of distance** — fog shifts when the camera rotates
  because fragments at the same world position get different fog values.
- **Applying fog before lighting** — the ambient/diffuse/specular terms get
  fogged individually, producing darker or brighter results than expected.
- **Forgetting to pass fog_mode to the shader** — defaults to 0 but toggling
  modes at runtime requires updating the uniform each frame.

## Reference

- Lesson 20: `lessons/gpu/20-linear-fog/`
- Fragment shader: `lessons/gpu/20-linear-fog/shaders/fog.frag.hlsl`
- Grid shader: `lessons/gpu/20-linear-fog/shaders/grid_fog.frag.hlsl`
