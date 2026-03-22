---
name: forge-scene-model-loading
description: Load and render pipeline-processed 3D models (.fscene + .fmesh + .fmat) through forge_scene.h with per-primitive materials, mesh instancing, and scene hierarchy traversal.
trigger: Use when someone needs to load glTF-derived models, render multi-material meshes, or asks about ForgeSceneModel.
---

# forge-scene-model-loading

Load pipeline-processed 3D models through `forge_scene.h`. One
`forge_scene_load_model()` call handles file loading, GPU buffer upload, and
per-material texture loading. The draw functions traverse the scene node
hierarchy and bind materials per-submesh.

## Prerequisites

Models must be processed through the asset pipeline tools first:

```bash
# Process mesh (produces .fmesh + .fmat)
./build/tools/mesh/forge_mesh_tool input.gltf output.fmesh --verbose

# Process scene hierarchy (produces .fscene)
./build/tools/scene/forge_scene_tool input.gltf output.fscene --verbose

# Copy textures alongside the .fmat file
cp source_textures/*.png output_dir/
```

## Usage pattern

```c
#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
#include "math/forge_math.h"

#define FORGE_PIPELINE_IMPLEMENTATION
#include "pipeline/forge_pipeline.h"

#define FORGE_SCENE_MODEL_SUPPORT
#define FORGE_SCENE_IMPLEMENTATION
#include "scene/forge_scene.h"

typedef struct {
    ForgeScene      scene;
    ForgeSceneModel model;
} app_state;

SDL_AppResult SDL_AppInit(void **appstate, int argc, char **argv)
{
    app_state *state = (app_state *)SDL_calloc(1, sizeof(*state));
    if (!state) return SDL_APP_FAILURE;
    *appstate = state;

    ForgeSceneConfig cfg = forge_scene_default_config("Model Viewer");
    cfg.cam_start_pos = vec3_create(0.0f, 2.0f, 5.0f);
    cfg.font_path = "assets/fonts/liberation_mono/LiberationMono-Regular.ttf";

    if (!forge_scene_init(&state->scene, &cfg, argc, argv))
        return SDL_APP_FAILURE;

    /* Load a pipeline-processed model.
     * base_dir is where textures are found (same dir as .fmat). */
    if (!forge_scene_load_model(&state->scene, &state->model,
                                "assets/MyModel/MyModel.fscene",
                                "assets/MyModel/MyModel.fmesh",
                                "assets/MyModel/MyModel.fmat",
                                "assets/MyModel")) {
        SDL_Log("Failed to load model");
        return SDL_APP_FAILURE;
    }

    return SDL_APP_CONTINUE;
}

SDL_AppResult SDL_AppEvent(void *appstate, SDL_Event *event)
{
    app_state *state = (app_state *)appstate;
    return forge_scene_handle_event(&state->scene, event);
}

SDL_AppResult SDL_AppIterate(void *appstate)
{
    app_state *state = (app_state *)appstate;
    ForgeScene *s = &state->scene;

    if (!forge_scene_begin_frame(s)) return SDL_APP_CONTINUE;

    mat4 placement = mat4_translate(vec3_create(0.0f, 0.0f, 0.0f));

    /* Shadow pass */
    forge_scene_begin_shadow_pass(s);
    forge_scene_draw_model_shadows(s, &state->model, placement);
    forge_scene_end_shadow_pass(s);

    /* Main pass */
    forge_scene_begin_main_pass(s);
    forge_scene_draw_model(s, &state->model, placement);
    forge_scene_draw_grid(s);
    forge_scene_end_main_pass(s);

    return forge_scene_end_frame(s);
}

void SDL_AppQuit(void *appstate, SDL_AppResult result)
{
    (void)result;
    app_state *state = (app_state *)appstate;
    if (!state) return;
    if (forge_scene_device(&state->scene)) {
        if (!SDL_WaitForGPUIdle(forge_scene_device(&state->scene))) {
            SDL_Log("SDL_WaitForGPUIdle failed: %s", SDL_GetError());
        }
        forge_scene_free_model(&state->scene, &state->model);
    }
    forge_scene_destroy(&state->scene);
    SDL_free(state);
}
```

## Key defines

Both defines must appear before including `forge_scene.h`:

| Define | Purpose |
|--------|---------|
| `FORGE_SCENE_MODEL_SUPPORT` | Enables model types and functions (pulls in `forge_pipeline.h`) |
| `FORGE_SCENE_IMPLEMENTATION` | Compiles the implementation (one `.c` file only) |
| `FORGE_PIPELINE_IMPLEMENTATION` | Compiles the pipeline library (one `.c` file only) |

## ForgeSceneModelVertex layout

The model pipeline uses a 48-byte vertex with tangent data for normal mapping:

| Field    | Type   | Size  | Offset | HLSL      |
|----------|--------|-------|--------|-----------|
| position | float3 | 12 B  | 0      | TEXCOORD0 |
| normal   | float3 | 12 B  | 12     | TEXCOORD1 |
| uv       | float2 | 8 B   | 24     | TEXCOORD2 |
| tangent  | float4 | 16 B  | 32     | TEXCOORD3 |

## ForgeSceneModel struct

After `forge_scene_load_model`, the struct contains:

| Field | Type | Description |
|-------|------|-------------|
| `scene_data` | `ForgePipelineScene` | Node hierarchy with world transforms |
| `mesh` | `ForgePipelineMesh` | Vertex/index data, submeshes, LODs |
| `materials` | `ForgePipelineMaterialSet` | PBR material descriptions |
| `vertex_buffer` | `SDL_GPUBuffer *` | Uploaded 48-byte vertices |
| `index_buffer` | `SDL_GPUBuffer *` | Uploaded uint32 indices |
| `mat_textures[]` | `ForgeSceneModelTextures` | Per-material GPU textures |
| `draw_calls` | `uint32_t` | Updated each `draw_model` call |

## Pipeline variants

The renderer selects a pipeline per-submesh based on material properties:

| Variant | Condition | Behavior |
|---------|-----------|----------|
| `model_pipeline` | Default (opaque) | Cull back, depth test + write |
| `model_pipeline_blend` | `alpha_mode == BLEND` | Alpha blend, no depth write |
| `model_pipeline_double` | `double_sided == true` | Cull none, depth test + write |

## Texture slots and fallbacks

Each material binds up to 5 textures. Missing slots use 1x1 fallbacks:

| Slot | Texture | Fallback | sRGB |
|------|---------|----------|------|
| 0 | Base color | White (1,1,1,1) | Yes |
| 1 | Normal map | Flat (0.5,0.5,1) | No |
| 2 | Metallic-roughness | White (1,1,1,1) | No |
| 3 | Occlusion | White (1,1,1,1) | No |
| 4 | Emissive | Black (0,0,0,1) | Yes |
| 5 | Shadow map | Scene shadow map | No |

## CMakeLists.txt

Models require cJSON for `.fmat` parsing:

```cmake
add_executable(my-lesson WIN32
    main.c
    ${CMAKE_SOURCE_DIR}/third_party/cJSON/cJSON.c)
target_include_directories(my-lesson PRIVATE
    ${FORGE_COMMON_DIR}
    ${CMAKE_SOURCE_DIR}/third_party/cJSON)
target_link_libraries(my-lesson PRIVATE SDL3::SDL3
    $<$<NOT:$<C_COMPILER_ID:MSVC>>:m>)

# Copy model assets to build output
add_custom_command(TARGET my-lesson POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_CURRENT_SOURCE_DIR}/assets
        $<TARGET_FILE_DIR:my-lesson>/assets)
```

## Common mistakes

- **Forgetting `FORGE_SCENE_MODEL_SUPPORT`.** Without this define, the model
  types and functions are not compiled. You get "unknown type" errors for
  `ForgeSceneModel`.

- **Forgetting `FORGE_PIPELINE_IMPLEMENTATION`.** The pipeline library must be
  compiled in exactly one `.c` file. Without it, you get linker errors for
  `forge_pipeline_load_scene`, etc.

- **Wrong texture paths.** The `.fmat` stores source-relative texture paths
  from the original glTF. `forge_scene_load_model` extracts just the filename
  and looks for it in `base_dir`. Textures must be copied alongside the `.fmat`
  file.

- **Not freeing models before `forge_scene_destroy`.** Call
  `forge_scene_free_model` for each loaded model before destroying the scene.
  The model holds GPU resources (buffers, textures) that reference the device.

- **Applying redundant scale.** Some glTF models (e.g., Duck) have scale
  transforms baked into their scene hierarchy. Check the node world transforms
  before applying additional scaling in the placement matrix.

## Reference

- Source: `common/scene/forge_scene.h` (model support section)
- Shaders: `common/scene/shaders/scene_model.vert.hlsl`, `scene_model.frag.hlsl`
- Lesson: `lessons/gpu/41-scene-model-loading/`
- Pipeline types: `common/pipeline/forge_pipeline.h`
