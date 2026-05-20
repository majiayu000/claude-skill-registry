---
name: forge-scene-renderer
description: Set up a complete 3D scene with forge_scene.h — shadow mapping, Blinn-Phong lighting, grid floor, sky gradient, FPS camera, and UI in one init call.
trigger: Use when someone needs a full 3D scene setup, wants to avoid rendering boilerplate, or asks about forge_scene.h.
---

# forge-scene-renderer

Set up a complete 3D rendering scene using the `forge_scene.h` header-only
library. One `forge_scene_init()` call creates the GPU device, window, depth
texture, shadow map, six graphics pipelines (shadow, scene, scene
double-sided, grid, sky, UI), a quaternion FPS camera, and an optional
immediate-mode UI system.

## Usage pattern

```c
#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
#include "math/forge_math.h"

#define FORGE_SCENE_IMPLEMENTATION
#include "scene/forge_scene.h"

typedef struct {
    ForgeScene scene;
    SDL_GPUBuffer *mesh_vb;
    SDL_GPUBuffer *mesh_ib;
    Uint32 index_count;
} app_state;

SDL_AppResult SDL_AppInit(void **appstate, int argc, char **argv)
{
    app_state *state = SDL_calloc(1, sizeof(*state));
    if (!state) return SDL_APP_FAILURE;
    *appstate = state;

    ForgeSceneConfig cfg = forge_scene_default_config("My Scene");
    cfg.cam_start_pos = vec3_create(0.0f, 2.0f, 5.0f);
    cfg.font_path = "assets/fonts/liberation_mono/LiberationMono-Regular.ttf";

    if (!forge_scene_init(&state->scene, &cfg, argc, argv))
        return SDL_APP_FAILURE;

    /* Upload your geometry using forge_scene_upload_buffer.
     * Always check for NULL — upload can fail if the GPU runs out of memory. */
    state->mesh_vb = forge_scene_upload_buffer(&state->scene,
        SDL_GPU_BUFFERUSAGE_VERTEX, vertices, vertex_size);
    state->mesh_ib = forge_scene_upload_buffer(&state->scene,
        SDL_GPU_BUFFERUSAGE_INDEX, indices, index_size);
    if (!state->mesh_vb || !state->mesh_ib) return SDL_APP_FAILURE;

    state->index_count = /* number of indices in your mesh */;

    return SDL_APP_CONTINUE;
}

SDL_AppResult SDL_AppEvent(void *appstate, SDL_Event *event)
{
    return forge_scene_handle_event(&((app_state *)appstate)->scene, event);
}

SDL_AppResult SDL_AppIterate(void *appstate)
{
    app_state *state = appstate;
    ForgeScene *s = &state->scene;

    if (!forge_scene_begin_frame(s)) return SDL_APP_CONTINUE;

    /* Shadow pass */
    forge_scene_begin_shadow_pass(s);
    forge_scene_draw_shadow_mesh(s, state->mesh_vb, state->mesh_ib,
                                 state->index_count, model_matrix);
    forge_scene_end_shadow_pass(s);

    /* Main pass (sky drawn automatically) */
    forge_scene_begin_main_pass(s);
    float color[4] = { 0.8f, 0.3f, 0.2f, 1.0f };
    forge_scene_draw_mesh(s, state->mesh_vb, state->mesh_ib,
                          state->index_count, model_matrix, color);
    forge_scene_draw_grid(s);
    forge_scene_end_main_pass(s);

    /* UI pass (optional) */
    float mx, my;
    Uint32 buttons = SDL_GetMouseState(&mx, &my);
    bool mouse_down = !state->scene.mouse_captured
                    && (buttons & SDL_BUTTON_LMASK) != 0;
    forge_scene_begin_ui(s, mx, my, mouse_down);
    ForgeUiWindowContext *wctx = forge_scene_window_ui(s);
    if (wctx) {
        if (forge_ui_wctx_window_begin(wctx, "Title", &state->ui_window)) {
            ForgeUiContext *ui = wctx->ctx;
            /* ... forge_ui_ctx_* widget calls ... */
            forge_ui_wctx_window_end(wctx);
        }
    }
    forge_scene_end_ui(s);

    return forge_scene_end_frame(s);
}

void SDL_AppQuit(void *appstate, SDL_AppResult result)
{
    (void)result;
    app_state *state = appstate;
    if (!state) return;
    /* Release your own GPU buffers before destroying the scene.
     * forge_scene_destroy does NOT track buffers you created via
     * forge_scene_upload_buffer — those are app-owned. */
    SDL_GPUDevice *dev = forge_scene_device(&state->scene);
    if (dev) {
        if (!SDL_WaitForGPUIdle(dev)) {
            SDL_Log("SDL_WaitForGPUIdle failed: %s", SDL_GetError());
        }
        if (state->mesh_vb) SDL_ReleaseGPUBuffer(dev, state->mesh_vb);
        if (state->mesh_ib) SDL_ReleaseGPUBuffer(dev, state->mesh_ib);
    }
    forge_scene_destroy(&state->scene);
    SDL_free(state);
}
```

## ForgeSceneVertex layout

The built-in scene pipeline expects `ForgeSceneVertex`:

| Field    | Type | Size   | HLSL       |
|----------|------|--------|------------|
| position | vec3 | 12 B   | TEXCOORD0  |
| normal   | vec3 | 12 B   | TEXCOORD1  |

Total stride: 24 bytes.

When using `forge_shapes.h` (struct-of-arrays), interleave before upload:

```c
for (int i = 0; i < shape->vertex_count; i++) {
    verts[i].position = shape->positions[i];
    verts[i].normal   = shape->normals[i];
}
```

## Configuration

Override fields on `ForgeSceneConfig` before passing to `forge_scene_init`:

| Field             | Default          | Purpose                              |
|-------------------|------------------|--------------------------------------|
| cam_start_pos     | (0, 4, 12)      | Initial camera position              |
| move_speed        | 5.0              | Camera movement speed                |
| mouse_sensitivity | 0.003            | Mouse look sensitivity               |
| fov_deg           | 60.0             | Vertical field of view               |
| light_dir         | (0.4, 0.8, 0.6) | Direction toward the light (normalized) |
| shadow_map_size   | 2048             | Shadow map resolution                |
| font_path         | NULL             | TTF path (NULL disables UI)          |

## Accessors

```c
SDL_GPUDevice  *dev = forge_scene_device(s);
float           dt  = forge_scene_dt(s);
mat4            vp  = forge_scene_view_proj(s);
vec3            cam = forge_scene_cam_pos(s);
ForgeUiContext *ui  = forge_scene_ui(s);   /* NULL if UI disabled */
```

## Common mistakes

- **Forgetting to release app-owned buffers.** `forge_scene_destroy` releases
  the library's internal resources (pipelines, shadow map, grid buffers, UI
  atlas) but does NOT release buffers you created with
  `forge_scene_upload_buffer`. Release those yourself in `SDL_AppQuit` before
  calling `forge_scene_destroy`.

- **Using `forge_ui_ctx_label()` inside panels.** Always use
  `forge_ui_ctx_label_layout()` inside `panel_begin/end` blocks. Absolute
  coordinates fall outside the panel's clip rect (content starts below the
  title bar + padding), causing glyph ascenders to be clipped and characters
  to appear as different letters.

- **Returning `SDL_APP_SUCCESS` from `SDL_AppInit`.** That means "quit
  immediately with exit code 0" — not "init succeeded." Return
  `SDL_APP_CONTINUE` on success.

- **Using struct-of-arrays data with the scene pipeline.** The built-in
  pipeline expects interleaved `ForgeSceneVertex` (position + normal, 24
  bytes). Interleave `forge_shapes.h` data before upload.

- **`light_dir` points TOWARD the light.** A positive Y component means the
  light comes from above. The shader uses `normalize(light_dir)` directly —
  no negation needed.

## Reference

- Source: `common/scene/forge_scene.h`
- Lesson: `lessons/gpu/40-scene-renderer/`
- Shaders: `common/scene/shaders/` (HLSL sources + compiled headers)
