---
name: forge-normal-maps
description: Add tangent-space normal mapping to an SDL GPU project. Extends the vertex layout with tangent vectors, constructs a TBN matrix in the vertex shader, and samples/decodes normal maps in the fragment shader for per-texel surface detail.
---

# Normal Maps Skill

Add tangent-space normal mapping to a 3D scene rendered with SDL's GPU
API. Normal maps add surface detail (bumps, grooves, patterns) without
increasing triangle count.

## When to use

- You have a textured 3D mesh and want to add surface detail
- Your model has a normal map texture (tangent-space, glTF convention)
- You need to compute tangent vectors for a mesh that doesn't supply them
- You want to implement the TBN (tangent-bitangent-normal) pipeline

## Prerequisites

- Working 3D rendering with Blinn-Phong lighting (Lesson 10 / `/forge-basic-lighting`)
- Texture sampling already set up (Lesson 04 / `/forge-textures-and-samplers`)
- glTF or OBJ model loading (Lesson 09 / `/forge-scene-loading`)

## Key concepts

### Vertex layout

Extend your vertex struct with a vec4 tangent:

```c
typedef struct SceneVertex {
    vec3 position;    /* TEXCOORD0 */
    vec3 normal;      /* TEXCOORD1 */
    vec2 uv;          /* TEXCOORD2 */
    vec4 tangent;     /* TEXCOORD3 — xyz = direction, w = handedness */
} SceneVertex;
```

### Tangent computation (Lengyel's method)

For models without supplied tangents, compute them from triangle edges:

1. For each triangle, solve for T and B from edge vectors and UV deltas
2. Accumulate per-vertex (average across sharing triangles)
3. Orthogonalize T against N using Gram-Schmidt: `T' = normalize(T - N * dot(N, T))`
4. Compute handedness: `sign(dot(cross(N, T), B))`

### Vertex shader — TBN construction

```hlsl
/* Normal: adjugate transpose for non-uniform scale */
float3x3 m = (float3x3)model;
float3x3 adj_t;
adj_t[0] = cross(m[1], m[2]);
adj_t[1] = cross(m[2], m[0]);
adj_t[2] = cross(m[0], m[1]);
float3 N = normalize(mul(adj_t, input.normal));

/* Tangent: transform by model matrix */
float3 T = normalize(mul(m, input.tangent.xyz));

/* Gram-Schmidt re-orthogonalization */
T = normalize(T - N * dot(N, T));

/* Bitangent with handedness */
float3 B = cross(N, T) * input.tangent.w;
```

### Fragment shader — normal map sampling

```hlsl
/* Build TBN matrix (T, B, N as rows) */
float3x3 TBN = float3x3(
    normalize(input.world_tangent),
    normalize(input.world_bitan),
    normalize(input.world_normal));

/* Decode normal map: [0,1] → [-1,1] */
float3 map_normal = normal_tex.Sample(normal_smp, input.uv).rgb;
map_normal = map_normal * 2.0 - 1.0;

/* Transform to world space */
float3 N = normalize(mul(map_normal, TBN));
```

## Pipeline setup

### Fragment shader resources

The fragment shader needs **2 samplers** (diffuse + normal map):

```c
#define FS_NUM_SAMPLERS 2
```

### Binding textures

```c
SDL_GPUTextureSamplerBinding bindings[2];
bindings[0].texture = diffuse_texture;
bindings[0].sampler = sampler;
bindings[1].texture = normal_texture;
bindings[1].sampler = sampler;
SDL_BindGPUFragmentSamplers(pass, 0, bindings, 2);
```

### Flat normal map placeholder

For materials without a normal map, use a 1x1 texture encoding (128, 128, 255)
which decodes to tangent-space normal (0, 0, 1) — no perturbation.

## Common mistakes

1. **Forgetting handedness** — The tangent.w sign must be used when computing
   the bitangent. Without it, mirrored UVs produce inverted normal maps.

2. **Wrong normal map convention** — glTF uses OpenGL convention (Y up /
   right-handed). DirectX-convention normal maps need Y flipped.

3. **Not re-orthogonalizing** — After different transforms (adjugate for N,
   direct for T), the basis vectors may not be perpendicular. Gram-Schmidt
   fixes this.

4. **Normalizing in VS only** — After rasterizer interpolation, the TBN
   vectors are no longer unit length. Always re-normalize in the fragment shader.

5. **mul order in HLSL** — `mul(map_normal, TBN)` with TBN rows = T, B, N
   gives the correct tangent-to-world transformation.

## glTF parser extension

The forge-gpu glTF parser stores tangents in `ForgeGltfPrimitive.tangents`
(a separate vec4 array) and normal map paths in `ForgeGltfMaterial.normal_map_path`.

## Reference

- [Lesson 17 source](../../../lessons/gpu/17-normal-maps/)
- Eric Lengyel, "Foundations of Game Engine Development, Volume 2: Rendering"
- glTF 2.0 specification: tangent vectors and normal textures
