---
name: forge-blinn-phong-materials
description: Add per-material Blinn-Phong lighting with ambient, diffuse, specular colors and shininess. Use when someone needs to render multiple objects with distinct material appearances, add material property systems, or extend basic lighting with per-object parameters in SDL3 GPU.
---

Add per-material Blinn-Phong lighting to an SDL GPU project. Extends the basic
lighting pattern from the `basic-lighting` skill with full material properties.

## When to use

- Rendering multiple objects that need to look different (metal vs plastic vs stone)
- Adding a material property system to a 3D scene
- Extending Lesson 10-style Blinn-Phong with per-object material colors
- Foundation for PBR-style material workflows

## Key concepts

### Material struct

```c
typedef struct Material {
    float ambient[4];    /* ambient reflectance (rgb, w unused)       */
    float diffuse[4];    /* diffuse reflectance (rgb, w unused)       */
    float specular[4];   /* specular reflectance (rgb), shininess (w) */
} Material;
```

Pack shininess into `specular[3]` — saves a uniform slot and aligns naturally
to 16 bytes per row.

### Predefined materials (OpenGL Programming Guide / Devernay tables)

```c
/* Metallic — colored specular highlights */
static const Material MATERIAL_GOLD = {
    { 0.24725f, 0.1995f,  0.0745f,  0.0f },  /* ambient  */
    { 0.75164f, 0.60648f, 0.22648f, 0.0f },  /* diffuse  */
    { 0.628281f, 0.555802f, 0.366065f, 51.2f } /* specular + shininess */
};

/* Dielectric — near-white specular */
static const Material MATERIAL_RED_PLASTIC = {
    { 0.0f, 0.0f, 0.0f, 0.0f },
    { 0.5f, 0.0f, 0.0f, 0.0f },
    { 0.7f, 0.6f, 0.6f, 32.0f }
};
```

### Fragment uniform layout (96 bytes)

```c
typedef struct FragUniforms {
    float mat_ambient[4];   /* 16 bytes */
    float mat_diffuse[4];   /* 16 bytes */
    float mat_specular[4];  /* 16 bytes — rgb + shininess in w */
    float light_dir[4];     /* 16 bytes */
    float eye_pos[4];       /* 16 bytes */
    Uint32 has_texture;     /*  4 bytes */
    float _pad[3];          /* 12 bytes — total: 96 bytes */
} FragUniforms;
```

### HLSL fragment shader

```hlsl
cbuffer FragUniforms : register(b0, space3)
{
    float4 mat_ambient;
    float4 mat_diffuse;
    float4 mat_specular;   /* rgb + shininess in w */
    float4 light_dir;
    float4 eye_pos;
    uint   has_texture;
};

float4 main(PSInput input) : SV_Target
{
    float3 diffuse_color = mat_diffuse.rgb;
    if (has_texture)
        diffuse_color *= diffuse_tex.Sample(smp, input.uv).rgb;

    float3 N = normalize(input.world_norm);
    float3 L = normalize(light_dir.xyz);
    float3 V = normalize(eye_pos.xyz - input.world_pos);

    /* Ambient */
    float3 ambient_term = mat_ambient.rgb;

    /* Diffuse (Lambert) */
    float NdotL = max(dot(N, L), 0.0);
    float3 diffuse_term = NdotL * diffuse_color;

    /* Specular (Blinn) — full RGB, not always white */
    float3 H = normalize(L + V);
    float NdotH = max(dot(N, H), 0.0);
    float shininess = mat_specular.w;
    float3 specular_term = pow(NdotH, shininess) * mat_specular.rgb;

    return float4(ambient_term + diffuse_term + specular_term, 1.0);
}
```

### Per-object rendering pattern

```c
for (int i = 0; i < num_objects; i++) {
    const Material *mat = objects[i].material;

    /* Position each object */
    mat4 model = mat4_translate(objects[i].position);
    mat4 mvp = mat4_multiply(vp, model);

    /* Push vertex uniforms */
    VertUniforms vu = { .mvp = mvp, .model = model };
    SDL_PushGPUVertexUniformData(cmd, 0, &vu, sizeof(vu));

    /* Push material + lighting uniforms */
    FragUniforms fu;
    SDL_memcpy(fu.mat_ambient,  mat->ambient,  sizeof(fu.mat_ambient));
    SDL_memcpy(fu.mat_diffuse,  mat->diffuse,  sizeof(fu.mat_diffuse));
    SDL_memcpy(fu.mat_specular, mat->specular, sizeof(fu.mat_specular));
    /* ... set light_dir, eye_pos, has_texture ... */
    SDL_PushGPUFragmentUniformData(cmd, 0, &fu, sizeof(fu));

    /* Draw */
    SDL_DrawGPUIndexedPrimitives(pass, index_count, 1, 0, 0, 0);
}
```

## Common mistakes

1. **Always-white specular.** Lesson 10 uses `float3(1,1,1)` for specular.
   Metals need colored specular — use `mat_specular.rgb` instead.

2. **Forgetting to push uniforms per object.** `SDL_PushGPUFragmentUniformData`
   must be called before each draw call, not once for the whole scene.

3. **Mismatched cbuffer layout.** The C struct and HLSL cbuffer must have
   identical sizes and alignment. Use `float4` (16 bytes) per row in HLSL
   to avoid packing surprises.

4. **Shininess of zero.** `pow(x, 0)` = 1.0 for all x, producing a flat white
   overlay. Use shininess >= 1.0.

## Metallic vs dielectric guide

| Type | Ambient | Diffuse | Specular | Shininess |
|------|---------|---------|----------|-----------|
| Metal | Dark, tinted | Medium, tinted | Bright, same tint | 30–80 |
| Plastic | Very dark | Saturated color | Near-white (0.6–0.8) | 20–50 |
| Stone/gem | Dark, slightly tinted | Muted color | Gray (0.2–0.4) | 10–20 |
| Pearl | Warm dark | Off-white/cream | Gray (0.2–0.3) | 8–15 |

## Dependencies

- Extends: `basic-lighting` skill (Lesson 10 patterns)
- Uses: `math/forge_math.h` for vectors and matrices
- Uses: `gltf/forge_gltf.h` for model loading
- Reference: [Lesson 18 — Blinn-Phong with Materials](../../../lessons/gpu/18-blinn-phong-materials/)
