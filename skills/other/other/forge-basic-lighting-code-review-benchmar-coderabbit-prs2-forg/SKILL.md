---
name: forge-basic-lighting
description: Add Blinn-Phong lighting (ambient + diffuse + specular) to a 3D scene with world-space normals, light direction, and camera position uniforms. Use when someone needs to light a mesh, add shading, or implement basic real-time lighting in SDL3 GPU.
---

# Basic Lighting — Blinn-Phong Shading

This skill teaches how to add Blinn-Phong lighting to a rendered 3D scene.
It builds on `scene-loading` (Lesson 09) and adds world-space lighting
calculations in the fragment shader.

## When to use

- Adding lighting/shading to a 3D model or scene
- Implementing ambient, diffuse, or specular shading
- Passing light direction and camera position as shader uniforms
- Transforming normals from object space to world space
- Setting up a fragment shader with per-pixel lighting

## Key API calls (ordered)

1. `forge_gltf_load(path, &scene)` — parse glTF (provides normals)
2. Upload vertex + index buffers to GPU (same as scene-loading skill)
3. `SDL_CreateGPUGraphicsPipeline` — 3 vertex attributes (pos, normal, uv)
4. `SDL_PushGPUVertexUniformData` — push MVP matrix + Model matrix (128 bytes)
5. `SDL_PushGPUFragmentUniformData` — push lighting params (64 bytes)
6. `SDL_DrawGPUIndexedPrimitives` — draw with lighting

## Uniform layouts

### Vertex uniforms (128 bytes)

Both matrices must be `column_major` in HLSL to match C `mat4` layout.

```c
typedef struct VertUniforms {
    mat4 mvp;     /* combined Model-View-Projection for clip space */
    mat4 model;   /* model (world) matrix for lighting calculations */
} VertUniforms;
```

```hlsl
cbuffer VertUniforms : register(b0, space1)
{
    column_major float4x4 mvp;
    column_major float4x4 model;
};
```

### Fragment uniforms (64 bytes)

Use `float4` (not `float3`) for vectors to avoid HLSL cbuffer packing issues.

```c
typedef struct FragUniforms {
    float base_color[4];   /* material color (RGBA)              */
    float light_dir[4];    /* normalized, toward light (xyz)     */
    float eye_pos[4];      /* camera world position (xyz)        */
    Uint32 has_texture;    /* 0 = solid color, 1 = sample tex    */
    float shininess;       /* specular exponent (32, 64, 128...) */
    float ambient;         /* ambient intensity [0..1]           */
    float specular_str;    /* specular intensity [0..1]          */
} FragUniforms;
```

```hlsl
cbuffer FragUniforms : register(b0, space3)
{
    float4 base_color;
    float4 light_dir;
    float4 eye_pos;
    uint   has_texture;
    float  shininess;
    float  ambient;
    float  specular_str;
};
```

## Code template

### Vertex shader — normal transformation (adjugate transpose)

```hlsl
/* World-space position for view direction calculation */
float4 wp = mul(model, float4(input.position, 1.0));
output.world_pos = wp.xyz;

/* Transform normal by the ADJUGATE TRANSPOSE of the model matrix's
 * upper-left 3x3.  Unlike (float3x3)model, this preserves
 * perpendicularity even under non-uniform scale.  The rows of the
 * adjugate transpose are cross products of pairs of model matrix rows.
 * Do NOT normalize here — the rasterizer will interpolate, and we
 * normalize per-pixel in the fragment shader. */
float3x3 m = (float3x3)model;
float3x3 adj_t;
adj_t[0] = cross(m[1], m[2]);
adj_t[1] = cross(m[2], m[0]);
adj_t[2] = cross(m[0], m[1]);
output.world_norm = mul(adj_t, input.normal);
```

### Fragment shader — Blinn-Phong

```hlsl
/* MUST normalize after interpolation — interpolated normals aren't unit length */
float3 N = normalize(input.world_norm);
float3 L = normalize(light_dir.xyz);          /* toward light */
float3 V = normalize(eye_pos.xyz - input.world_pos);  /* toward camera */

/* Ambient: constant minimum brightness */
float3 ambient_term = ambient * surface_color.rgb;

/* Diffuse: Lambert's cosine law */
float NdotL = max(dot(N, L), 0.0);
float3 diffuse_term = NdotL * surface_color.rgb;

/* Specular: Blinn half-vector */
float3 H = normalize(L + V);
float NdotH = max(dot(N, H), 0.0);
float3 specular_term = specular_str * pow(NdotH, shininess) * float3(1, 1, 1);

float3 final = ambient_term + diffuse_term + specular_term;
```

### C side — pushing lighting uniforms

```c
/* Vertex: MVP + model matrix */
VertUniforms vu;
vu.mvp   = mat4_multiply(vp, node->world_transform);
vu.model = node->world_transform;
SDL_PushGPUVertexUniformData(cmd, 0, &vu, sizeof(vu));

/* Fragment: material + lighting */
FragUniforms fu;
fu.base_color[0] = mat->base_color[0]; /* ... etc */
fu.light_dir[0] = light_dir.x;
fu.light_dir[1] = light_dir.y;
fu.light_dir[2] = light_dir.z;
fu.light_dir[3] = 0.0f;
fu.eye_pos[0] = cam_pos.x;
fu.eye_pos[1] = cam_pos.y;
fu.eye_pos[2] = cam_pos.z;
fu.eye_pos[3] = 0.0f;
fu.shininess    = 64.0f;
fu.ambient      = 0.15f;
fu.specular_str = 0.5f;
SDL_PushGPUFragmentUniformData(cmd, 0, &fu, sizeof(fu));
```

## Common mistakes

1. **Forgetting to normalize interpolated normals** — The rasterizer
   interpolates vertex shader outputs linearly. Even if every vertex normal
   is unit length, the interpolated result won't be. Always `normalize()` in
   the fragment shader.

2. **Missing `column_major` on both matrices** — If you add the model matrix
   but forget `column_major`, the multiplication will be wrong. Both `mvp`
   and `model` must have it.

3. **Using `float3` in the cbuffer** — HLSL packs `float3` to 16 bytes
   with 4 bytes of padding, which silently misaligns subsequent fields.
   Use `float4` and explicitly pad the w component to 0.

4. **Light direction convention** — Our convention: light_dir points FROM the
   surface TOWARD the light. Some tutorials use the opposite. If your model
   looks like the dark side is lit, negate the direction.

5. **Normalizing in the vertex shader** — Don't normalize normals in the
   vertex shader. The rasterizer will interpolate them anyway, making the
   normalization pointless. Save it for the fragment shader.

6. **Normal transformation with non-uniform scale** — `(float3x3)model`
   only works correctly for rotation + uniform scale. Always use the
   adjugate transpose instead — three cross products of the matrix rows:
   `adj_t[0] = cross(m[1], m[2])` etc. This is correct for ALL matrices
   (including singular ones) and cheaper than inverse-transpose.

## Typical parameter values

| Parameter | Value | Effect |
|-----------|-------|--------|
| shininess | 8-16 | Rough, matte surface |
| shininess | 32-64 | Typical plastic / painted |
| shininess | 128-256 | Polished, metallic |
| ambient | 0.05-0.15 | Subtle fill light |
| ambient | 0.2-0.3 | Bright ambient (indoor) |
| specular_str | 0.3-0.5 | Moderate shine |
| specular_str | 0.8-1.0 | Very shiny / wet |

## References

- **GPU Lesson 10** — Basic Lighting (full implementation)
- **Math Lesson 01** — Vectors (dot product, normalize)
- **Math Lesson 02** — Coordinate Spaces (object, world, view)
- **Math Lesson 05** — Matrices (model matrix transformation)
