---
name: dev-gpu-lesson
description: Scaffold a new GPU lesson using forge_scene.h for the rendering baseline
argument-hint: "[number] [name] [description]"
disable-model-invocation: true
---

Create a new GPU lesson for the forge-gpu project. Every GPU lesson uses
`forge_scene.h` for the rendering baseline (shadow map, Blinn-Phong lighting,
grid floor, sky gradient, FPS camera, UI). The lesson focuses entirely on its
subject matter, not rendering plumbing.

The user will provide:

- **Number**: two-digit lesson number (e.g. 02)
- **Name**: short kebab-case name (e.g. first-triangle)
- **Description**: what the lesson teaches

If any of these are missing, ask the user before proceeding.

## Steps

1. **Start from a clean main branch**:

   Before creating any files, ensure we're working from the latest main:

   ```bash
   git checkout main
   git pull origin main
   ```

   This avoids conflicts from stale branches and ensures the new lesson
   builds on top of the latest project state.

2. **Determine what math is needed**:
   - Will this lesson use vectors (positions, colors, directions)?
   - Will it use matrices (transformations, rotations)?
   - Check if the math library (`common/math/forge_math.h`) has what you need
   - If new math operations are needed, use `/dev-math-lesson` to add them first

3. **Create the lesson directory**: `lessons/gpu/$ARGUMENTS[0]-$ARGUMENTS[1]/`

4. **Create main.c** using the SDL callback architecture:
   - `#define SDL_MAIN_USE_CALLBACKS 1` before includes
   - **Always use `forge_scene.h`** for the rendering baseline. See the
     `forge-scene-renderer` skill for the full API.
   - Include required headers:

     ```c
     #include <SDL3/SDL.h>
     #include <SDL3/SDL_main.h>
     #include <stddef.h>    /* offsetof */
     #include "math/forge_math.h"

     #define FORGE_SCENE_IMPLEMENTATION
     #include "scene/forge_scene.h"
     ```

   - `SDL_AppInit` — create GPU device, window, claim swapchain, allocate app_state
   - `SDL_AppEvent` — handle SDL_EVENT_QUIT (return SDL_APP_SUCCESS)
   - `SDL_AppIterate` — per-frame GPU work
   - `SDL_AppQuit` — cleanup in reverse order, SDL_free the app_state
   - Use `SDL_calloc` / `SDL_free` for app_state (not malloc/free)
   - Every SDL GPU call gets error handling with `SDL_Log` and descriptive messages
   - **Check every SDL function that returns `bool`** — `SDL_SubmitGPUCommandBuffer`,
     `SDL_SetGPUSwapchainParameters`, `SDL_AcquireGPUSwapchainTexture`, etc. all
     return `false` on failure. Log a descriptive error (include the function name)
     and clean up or early-return. Never ignore a bool return value.
   - Use `#define WINDOW_WIDTH 1280` and `#define WINDOW_HEIGHT 720` (16:9).
     All lessons use this standard size for consistent screenshots.
   - No magic numbers in production/library code — `#define` or `enum`
     everything. In lesson files, inline numeric literals are acceptable when
     one-off demonstration values improve readability (e.g. vertex positions,
     color components, sample coordinates)
   - Extensive comments explaining *why* and *purpose*, not just *what* —
     every pipeline setting, resource binding, and API call should have a brief
     comment stating why that choice was made (e.g. why CULLMODE_NONE, why
     TRIANGLELIST, why we push uniforms each frame). This is a recurring PR
     review requirement.
   - Use C99, matching SDL's own style
   - **Use math library types for all math operations** (see "Using the Math Library" below)

5. **Create CMakeLists.txt**:

   ```cmake
   add_executable(NN-name WIN32 main.c)
   target_include_directories(NN-name PRIVATE ${FORGE_COMMON_DIR})
   target_link_libraries(NN-name PRIVATE SDL3::SDL3)

   add_custom_command(TARGET NN-name POST_BUILD
       COMMAND ${CMAKE_COMMAND} -E copy_if_different
           $<TARGET_FILE:SDL3::SDL3-shared>
           $<TARGET_FILE_DIR:NN-name>
   )
   ```

6. **Create README.md** following this structure:
   - `# Lesson NN — Title`
   - `## What you'll learn` — bullet list of concepts
   - `## Result` — screenshot/GIF first (captured in step 11), then describe what the reader will see
   - `## Key concepts` — explain each new API concept introduced
   - `## Math` — if the lesson uses math operations, link to relevant math lessons
   - `## Building` — standard cmake build instructions
   - `## AI skill` — mention the matching skill created in step 10, with a
     relative link to `.claude/skills/<topic>/SKILL.md`, the `/skill-name`
     invocation, and a note that users can copy it into their own projects
   - `## Exercises` — 3-4 exercises that extend the lesson

7. **Update the root CMakeLists.txt**: add `add_subdirectory(lessons/gpu/NN-name)` under "GPU Lessons"

8. **Update PLAN.md**: check off the lesson if it was listed, or add it

9. **Build and test**: run `cmake --build build --config Debug` and verify it runs

10. **Capture a screenshot**: Use the `/dev-add-screenshot` skill to capture a screenshot
    and embed it in the lesson README. Every lesson must have a visual in the
    "Result" section so readers can see what they're building before diving into code.

    ```bash
    python scripts/capture_lesson.py lessons/gpu/NN-name
    ```

    Verify the image is in `lessons/gpu/NN-name/assets/` and the README
    references it with `![Lesson NN screenshot](assets/screenshot.png)`.

11. **Create a matching skill**: add `.claude/skills/<topic>/SKILL.md` that
    distills the lesson into a reusable pattern with YAML frontmatter

12. **Run markdown linting**: Use the `/dev-markdown-lint` skill to verify all markdown files pass linting:

    ```bash
    npx markdownlint-cli2 "**/*.md"
    ```

    If errors found, auto-fix first then manually fix remaining issues (especially MD040 language tags)

## Using the Math Library

**CRITICAL:** GPU lessons must use the math library (`common/math/forge_math.h`) for all math operations. Never write bespoke math in GPU lessons.

### Vertex data structures

**Always use math library types for vertex attributes:**

```c
typedef struct Vertex {
    vec2 position;   /* NOT float x, y */
    vec3 color;      /* NOT float r, g, b */
} Vertex;
```

**HLSL mapping:**

- `vec2` in C → `float2` in HLSL shader
- `vec3` in C → `float3` in HLSL shader
- `vec4` in C → `float4` in HLSL shader
- Memory layout is identical — no conversion needed

### Vertex attribute setup

```c
vertex_attributes[0].offset = offsetof(Vertex, position);  /* NOT offsetof(Vertex, x) */
vertex_attributes[1].offset = offsetof(Vertex, color);     /* NOT offsetof(Vertex, r) */
```

### Initializing vertex data

Use designated initializers with math library types:

```c
static const Vertex vertices[] = {
    { .position = { 0.0f, 0.5f }, .color = { 1.0f, 0.0f, 0.0f } },
    /* ... */
};
```

Or use constructor functions explicitly:

```c
Vertex v;
v.position = vec2_create(0.0f, 0.5f);
v.color = vec3_create(1.0f, 0.0f, 0.0f);
```

### Common math operations

**Transformations:**

```c
mat4 rotation = mat4_rotate_z(angle);
mat4 translation = mat4_translate(vec3_create(x, y, z));
mat4 scale = mat4_scale(vec3_create(sx, sy, sz));
```

**Vector operations:**

```c
vec3 sum = vec3_add(a, b);
vec3 normalized = vec3_normalize(v);
float distance = vec3_length(vec3_sub(target, position));
```

### When you need new math

If the math library doesn't have an operation you need:

1. Check `common/math/forge_math.h` — might already exist
2. Check `lessons/math/` — might have a lesson teaching it
3. Use `/dev-math-lesson` to add it:

   ```bash
   /dev-math-lesson 02 quaternions "Quaternion rotations"
   ```

4. This creates: math lesson + library update + documentation

### Cross-referencing math lessons

In the lesson README, add a "Math" section linking to relevant math lessons:

```markdown
## Math

This lesson uses:
- **Vectors** — [Math Lesson 01](../math/01-vectors/) for positions and colors
- **Matrices** — [Math Lesson 05](../math/05-matrices/) for rotations
```

## Diagrams and Formulas

**Find opportunities to create compelling diagrams and visualizations via the
matplotlib scripts** — they increase reader engagement and help learners
understand the topics being taught. Use the `/dev-create-diagram` skill to add
diagrams following the project's visual identity and quality standards.

### Matplotlib diagrams

For geometric or visual diagrams (UV mapping, filtering comparison), add a
diagram function to `scripts/forge_diagrams/gpu/lesson_NN.py` (create the file
if it doesn't exist):

1. Write a function following the existing pattern (shared `setup_axes`,
   `draw_vector`, `save` helpers from `_common.py`)
2. Re-export from `scripts/forge_diagrams/gpu/__init__.py`
3. Import and register in the `DIAGRAMS` dict in `__main__.py` with the lesson key (e.g. `"gpu/04"`)
4. Run `python scripts/forge_diagrams --lesson gpu/NN` to generate the PNG
5. Reference in the README: `![Description](assets/diagram_name.png)`

### Mermaid diagrams

For **flow/pipeline diagrams** (texture upload flow, MVP pipeline), use inline
mermaid blocks — GitHub renders them natively:

````markdown
```mermaid
flowchart LR
    A[Step 1] -->|transform| B[Step 2] --> C[Step 3]
```
````

Use mermaid for sequential flows.

### KaTeX math

For **formulas**, use inline `$...$` and display `$$...$$` math notation:

- Inline: `$\text{MVP} = P \times V \times M$`
- Display math blocks must be split across three lines (CI enforces this):

```text
$$
x_{\text{screen}} = \frac{x \cdot n}{-z}
$$
```

Keep worked examples (step-by-step with numbers) in ` ```text ` blocks.

## MANDATORY: Chunked writes for main.c

**ALL GPU lesson `main.c` files MUST use the chunked-write pattern.** Task
agents have a 32K output token limit per Write call. A single Write over ~800
lines fails silently — the file is never created and all work is lost. This is
a fatal error that wastes hours of work.

**Required workflow:**

1. Create a `PLAN.md` in the lesson directory (`lessons/gpu/NN-name/PLAN.md`)
   with a **"main.c Decomposition"** section before any coding agent starts
   writing. Specify what goes in each chunk. This is the lesson-local plan,
   NOT the root `PLAN.md`.
2. Split into 3-4 parts (~400-600 lines each). Write each to `/tmp/`, then
   concatenate with `cat`.
3. Agent A (header + helpers + structs) runs first. Agents B and C run in
   parallel after A completes.

**Recovery rule — if a coding agent fails with a token limit error:**

- **NEVER write a fallback or simplified `main.c`.** This destroys all the
  planning and coding work.
- **STOP immediately** and report the failure to the user.
- Re-plan using the chunked approach and re-run with decomposed agents.

See [`.claude/large-file-strategy.md`](../../../.claude/large-file-strategy.md)
for the full strategy and decomposition template.

## Code style reminders

- Naming: `PascalCase` for typedefs (e.g. `Vertex`, `GpuPrimitive`),
  `lowercase_snake_case` for local variables and functions (e.g. `app_state`),
  `UPPER_SNAKE_CASE` for `#define` constants,
  `Prefix_PascalCase` for public API types (e.g. `ForgeCapture`) and
  `prefix_snake_case` for public API functions (e.g. `forge_capture_init`)
- The `app_state` struct holds all state passed between callbacks
- Build on previous lessons — reference what was introduced before
- Each lesson should introduce ONE new concept at a time
- **Always use the math library** — no bespoke math in GPU lessons
- Link to math lessons when explaining concepts
- **Never extract assets from glTFs à la carte** — when a lesson uses a glTF
  model, copy the complete model (`.gltf`, `.bin`, and all referenced textures)
  into the lesson's `assets/` directory and load it with `forge_gltf_load()`.
  The model's node transforms, materials, and textures should drive the scene
  layout, not hand-coded geometry.
- **Always check SDL return values** — every SDL GPU function that returns
  `bool` must be checked. Log the function name and `SDL_GetError()` on
  failure, then clean up resources and early-return. This includes
  `SDL_SubmitGPUCommandBuffer`, `SDL_SetGPUSwapchainParameters`,
  `SDL_ClaimWindowForGPUDevice`, `SDL_Init`, and others. This is a
  recurring PR review item — get it right the first time.
