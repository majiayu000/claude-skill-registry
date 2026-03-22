---
name: forge-planar-reflections
description: >
  Add planar reflections with oblique near-plane clipping and Fresnel-blended
  water to an SDL GPU project.
---

Add a reflective water surface (or any flat mirror) to an SDL3 GPU scene using
planar reflections. The technique mirrors the camera across the reflection
plane, renders the scene from that mirrored viewpoint into an offscreen
texture, and composites the result using Fresnel blending. Use this skill when
you need pixel-perfect reflections on flat surfaces — water, polished floors,
or wall mirrors.

See [GPU Lesson 30 — Planar Reflections](../../../lessons/gpu/30-planar-reflections/)
for the full walkthrough.

## Key API calls

| Function | Purpose |
|----------|---------|
| `mat4_reflect(a, b, c, d)` | Build a 4x4 reflection matrix for plane `ax+by+cz+d=0` |
| `mat4_oblique_near_plane(proj, clip_plane_view)` | Replace the near plane of a projection matrix with an arbitrary clip plane (Lengyel's method) |
| `SDL_CreateGPUTexture` | Create the offscreen reflection color and depth textures |
| `SDL_BeginGPURenderPass` | Begin the reflection render pass with the mirrored camera |
| `SDL_BindGPUFragmentSamplers` | Bind the reflection texture for sampling in the water shader |

## Correct order

1. **Shadow pass** — render depth from the directional light
2. **Reflection pass** — mirror the camera, apply oblique near-plane clip,
   render the scene (minus water and floor) into an offscreen texture
3. **Main scene pass** — standard forward render to the swapchain
4. **Water pass** — alpha-blended quad sampling the reflection texture with
   Fresnel blending

## Common mistakes

- **Forgetting oblique near-plane clipping.** Without it, geometry below the
  water plane leaks into the reflection texture. Use
  `mat4_oblique_near_plane()` on the mirrored projection matrix.

- **Not reversing winding order.** The reflection matrix flips triangle
  winding. Set the front-face to `SDL_GPU_FRONTFACE_CLOCKWISE` for the
  reflection pass pipeline (or vice versa if your normal pipeline uses CW).

- **Rendering the water or floor in the reflection pass.** The reflection
  should only contain objects *above* the water plane. Rendering the water
  surface creates infinite recursion; rendering the floor shows geometry
  that should be clipped.

- **Missing Y-flip in screen-space UV.** Vulkan/Metal texture coordinates
  have V increasing downward, but clip-space Y increases upward. The water
  shader must flip: `screen_uv.y = 1.0 - screen_uv.y`.

- **Submitting or canceling the command buffer incorrectly.** After acquiring
  a swapchain texture, you *must* submit (not cancel) the command buffer, even
  on error. Cancel is only valid before swapchain acquisition.

- **Using the main camera's projection for the reflection pass.** The
  reflection pass needs its own projection matrix with the oblique near plane.
  Reusing the main projection skips the clip and shows underwater artifacts.

## Ready-to-use template

```c
/* ── Reflection matrix ──────────────────────────────────────────── */

static mat4 mat4_reflect(float a, float b, float c, float d)
{
    mat4 m;
    m.m[0]  = 1.0f - 2.0f*a*a;  m.m[1]  =      -2.0f*a*b;
    m.m[2]  =      -2.0f*a*c;   m.m[3]  = 0.0f;
    m.m[4]  =      -2.0f*b*a;   m.m[5]  = 1.0f - 2.0f*b*b;
    m.m[6]  =      -2.0f*b*c;   m.m[7]  = 0.0f;
    m.m[8]  =      -2.0f*c*a;   m.m[9]  =      -2.0f*c*b;
    m.m[10] = 1.0f - 2.0f*c*c;  m.m[11] = 0.0f;
    m.m[12] = -2.0f*a*d;        m.m[13] = -2.0f*b*d;
    m.m[14] = -2.0f*c*d;        m.m[15] = 1.0f;
    return m;
}

/* ── Oblique near-plane clipping (Lengyel 2005) ─────────────────── */

static float signf_of(float x)
{
    if (x > 0.0f) return  1.0f;
    if (x < 0.0f) return -1.0f;
    return 0.0f;
}

static mat4 mat4_oblique_near_plane(mat4 proj, vec4 clip_plane_view)
{
    vec4 q;
    q.x = (signf_of(clip_plane_view.x) + proj.m[8])  / proj.m[0];
    q.y = (signf_of(clip_plane_view.y) + proj.m[9])  / proj.m[5];
    q.z = -1.0f;
    q.w = (1.0f + proj.m[10]) / proj.m[14];

    float dot = clip_plane_view.x * q.x + clip_plane_view.y * q.y +
                clip_plane_view.z * q.z + clip_plane_view.w * q.w;
    if (SDL_fabsf(dot) < 1e-6f) return proj;

    float scale = 1.0f / dot;
    proj.m[2]  = clip_plane_view.x * scale;
    proj.m[6]  = clip_plane_view.y * scale;
    proj.m[10] = clip_plane_view.z * scale;
    proj.m[14] = clip_plane_view.w * scale;
    return proj;
}

/* ── Per-frame reflection setup ─────────────────────────────────── */

/* Mirror camera across the water plane Y = WATER_LEVEL. */
vec3 reflected_cam = cam_position;
reflected_cam.y = 2.0f * WATER_LEVEL - reflected_cam.y;

mat4 reflect_mat = mat4_reflect(0.0f, 1.0f, 0.0f, -WATER_LEVEL);
mat4 reflected_view = mat4_multiply(view, reflect_mat);

/* Transform water plane to reflected view space for oblique clipping. */
mat4 vit = mat4_transpose(mat4_inverse(reflected_view));
float pw[4] = { 0.0f, 1.0f, 0.0f, -WATER_LEVEL };
vec4 cpv;
cpv.x = vit.m[0]*pw[0] + vit.m[4]*pw[1] + vit.m[8]*pw[2]  + vit.m[12]*pw[3];
cpv.y = vit.m[1]*pw[0] + vit.m[5]*pw[1] + vit.m[9]*pw[2]  + vit.m[13]*pw[3];
cpv.z = vit.m[2]*pw[0] + vit.m[6]*pw[1] + vit.m[10]*pw[2] + vit.m[14]*pw[3];
cpv.w = vit.m[3]*pw[0] + vit.m[7]*pw[1] + vit.m[11]*pw[2] + vit.m[15]*pw[3];

mat4 oblique_proj = mat4_oblique_near_plane(proj, cpv);
mat4 reflected_vp = mat4_multiply(oblique_proj, reflected_view);

/* ── Water fragment shader (HLSL) ───────────────────────────────── */
/*
float2 screen_uv = proj_pos.xy / proj_pos.w;
screen_uv = screen_uv * 0.5 + 0.5;
screen_uv.y = 1.0 - screen_uv.y;

float3 reflection = reflection_tex.Sample(linear_sampler, screen_uv).rgb;

float3 N = float3(0, 1, 0);
float3 V = normalize(eye_pos - world_pos);
float NdotV = saturate(dot(N, V));

float fresnel = fresnel_f0 + (1.0 - fresnel_f0) * pow(1.0 - NdotV, 5.0);
float3 color = lerp(water_tint.rgb, reflection, fresnel);
float  alpha = lerp(0.6, 1.0, fresnel);
*/
```
