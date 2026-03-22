---
name: dev-final-pass
description: Run a quality review pass on a lesson before publishing, catching recurring issues found across project PR history
argument-hint: "[lesson-number or lesson-name]"
disable-model-invocation: false
---

Run a systematic quality review on any lesson (GPU, math, engine, UI, physics,
audio, or asset pipeline) before creating a PR with `/dev-create-pr`. This skill
encodes recurring themes from PR review feedback across the project's history.

The user provides:

- **Lesson number or name** (e.g. `17` or `normal-maps`)

If missing, infer from the current branch name or most recent lesson directory.

## How to run this skill

Work through each section below **in order**. For each check, read the relevant
files and verify compliance. Report a summary at the end with pass/fail per
section and specific issues found.

**Be literal and exhaustive.** This is C — no RAII, no garbage collector. Every
resource you acquire must be released on every exit path, every struct field
must be documented, every error must be handled. Do not rationalize away
findings with "it's probably fine" or "the section comment covers it." If the
check says every field, check every field. If it says every error path, trace
every error path.

Use a Task agent (model: haiku) for builds, shader compilation, linting, and
other command execution — never run those directly from the main agent.

---

## 0. Required files

Verify the lesson has all required pieces.

**What to check:**

- [ ] `lessons/<track>/NN-name/README.md` exists
- [ ] `lessons/<track>/NN-name/main.c` exists (GPU, physics, audio, engine
  lessons) — asset lessons may use Python entry points instead
- [ ] `lessons/<track>/NN-name/CMakeLists.txt` exists (C lessons only — asset
  lessons that are pure Python do not need one)
- [ ] `lessons/<track>/NN-name/assets/screenshot.png` exists (GPU, physics,
  audio lessons) — **not** just a placeholder
- [ ] `.claude/skills/<topic>/SKILL.md` exists (the matching skill)
- [ ] Root `CMakeLists.txt` includes `add_subdirectory(lessons/<track>/NN-name)`
  (C lessons only)
- [ ] Root `PLAN.md` has the lesson checked off or added

**Shader directory:** Only required if the lesson has its own shaders beyond
what `forge_scene.h` provides. GPU lessons using `forge_scene.h` for the
rendering baseline do not need a `shaders/` directory unless they add
lesson-specific shaders.

---

## 1. SDL GPU bool return checks (40+ PR comments historically)

**This is the single most common PR finding.** Every SDL function that returns
`bool` must be checked. Search **all** `.c` and `.h` files in the lesson
directory (not just `main.c`) for every SDL call and verify each one that
returns `bool` has error handling.

**Functions that return bool (non-exhaustive):**

- `SDL_Init`
- `SDL_ClaimWindowForGPUDevice`
- `SDL_SetGPUSwapchainParameters`
- `SDL_SubmitGPUCommandBuffer`
- `SDL_CancelGPUCommandBuffer`
- `SDL_UploadToGPUBuffer` (via command buffer submit)
- `SDL_WindowSupportsGPUSwapchainComposition`
- `SDL_SetGPUBufferName` / `SDL_SetGPUTextureName`

**Required pattern:**

```c
if (!SDL_SomeFunction(args)) {
    SDL_Log("SDL_SomeFunction failed: %s", SDL_GetError());
    /* clean up any resources allocated so far */
    return false; /* or SDL_APP_FAILURE */
}
```

**What to check:**

- [ ] Every `SDL_SubmitGPUCommandBuffer` call checks the return value
- [ ] Every `SDL_SetGPUSwapchainParameters` call checks the return value
- [ ] `SDL_Init` return is checked in `SDL_AppInit`
- [ ] `SDL_ClaimWindowForGPUDevice` return is checked
- [ ] Helper functions that call SDL submit propagate failure (return NULL or false)
- [ ] Failure paths log the **function name** and `SDL_GetError()`
- [ ] Failure paths clean up resources allocated before the failure point

**How to search:** Use Grep for patterns like `SDL_Submit`, `SDL_SetGPUSwapchain`,
`SDL_Init(`, `SDL_Claim` across all `.c` and `.h` files in the lesson directory
and verify each has an `if (!...)` wrapper.

**Skip for:** math lessons, engine lessons, UI lessons, asset lessons (no SDL
GPU calls).

---

## 2. Command buffer lifecycle (acquired from Lesson 24 review)

**Every acquired command buffer must be either submitted or canceled.** There
is no automatic cleanup — an abandoned command buffer is a resource leak. This
is C: if you acquire it, you release it, on every path.

**Key SDL3 constraint:** `SDL_CancelGPUCommandBuffer` is **not allowed** after
a swapchain texture has been acquired on that command buffer. After swapchain
acquisition, you **must** submit (even on error).

**What to check:**

- [ ] Every `SDL_AcquireGPUCommandBuffer` has a matching submit or cancel on
  **every** code path that follows — including early returns from failed
  `BeginRenderPass`, failed `ensure_*` helpers, etc.
- [ ] Error paths **before** swapchain acquisition use
  `SDL_CancelGPUCommandBuffer(cmd)`
- [ ] Error paths **after** swapchain acquisition use
  `SDL_SubmitGPUCommandBuffer(cmd)` (submit the partial/empty command buffer)
- [ ] The `!swapchain_tex` (minimized window) path submits the empty
  command buffer and returns `SDL_APP_CONTINUE`

**Skip for:** math, engine, UI, asset lessons.

---

## 3. Magic numbers (20+ PR comments)

Every numeric literal that represents a tuning parameter, spec-defined default,
buffer size, or domain constant must be a `#define` or `enum` at the top of the
file (or in a shared header if reused).

**What to check:**

- [ ] No bare float literals used as thresholds, cutoffs, or defaults (e.g. `0.5f`
  alpha cutoff, `0.3f` rotation speed, `50.0f` light distance)
- [ ] No bare integer literals for array sizes, cascade counts, sample counts
- [ ] Spec-defined values cite the spec (e.g. `/* glTF 2.0 sec 3.9.4 */`)
- [ ] Sentinel values like `1e30f` or `FLT_MAX` are named
  (`#define AABB_SENTINEL 1e30f`)
- [ ] Mathematical constants like `2.0f` in formulas are acceptable only when
  they are inherent to the math (e.g. `2.0 * dot(N, I)` in reflection) — but
  domain-specific multipliers should be named

---

## 4. Resource leaks on error paths (15+ PR comments)

When initialization fails partway through, all resources allocated before the
failure point must be released. This is C — no destructors, no RAII, no GC.
If you allocate it, you must free it on every exit path.

**What to check:**

- [ ] Every early-return in init/load functions releases GPU buffers, textures,
  and samplers allocated earlier in the same function
- [ ] `gpu_primitive_count` (or equivalent) is updated incrementally so cleanup
  can release partial uploads
- [ ] Transfer buffer failures don't leak the destination GPU buffer
- [ ] Sampler creation failures don't leak previously created samplers
- [ ] Helper functions (e.g. `upload_gpu_buffer`, `create_white_texture`) return
  NULL on failure and don't leak internal resources
- [ ] `init_fail` cleanup matches `SDL_AppQuit` cleanup — every resource freed
  in `SDL_AppQuit` must also be freed in `init_fail` (including conditional
  resources like `#ifdef FORGE_CAPTURE`)
- [ ] `ensure_*` functions that destroy-then-recreate handle partial failure
  (some resources recreated, some not) without leaking

**Skip for:** math, engine, UI, asset lessons (no GPU resources).

---

## 5. Naming conventions (15+ PR comments)

**Public API** (in `common/` headers): `Prefix_PascalCase` for types
(e.g. `ForgeGltfScene`), `prefix_snake_case` for functions
(e.g. `forge_gltf_load`).

**Internal typedefs** (in lesson `main.c`): **PascalCase** for struct typedefs
(e.g. `SceneVertex`, `VertUniforms`, `GpuPrimitive`). This is the project
convention, confirmed in `.coderabbit.yaml` and consistent across all lessons.

**Local variables and app_state**: `lowercase_snake_case`.

**What to check:**

- [ ] Public types in `common/` use `Forge` prefix (e.g. `ForgeGltfScene`)
- [ ] Internal typedefs in main.c use PascalCase consistently
  (e.g. `VertUniforms`, not `vertUniforms` or `vert_uniforms`)
- [ ] The `app_state` struct uses lowercase_snake_case (exception: it holds
  all per-session state and is always lowercase by convention)
- [ ] Local helper functions use `snake_case` (not `camelCase`)
- [ ] `#define` constants use `UPPER_SNAKE_CASE`

---

## 6. Per-field intent comments (15+ PR comments)

**Every** struct field needs an inline comment — no exceptions, no "the section
header covers it." Section headers group related fields; inline comments
explain each individual field's purpose, units, format, or valid range.

**What to check:**

- [ ] Uniform struct fields have inline comments (units, range, purpose)
- [ ] Vertex layout fields document their semantic meaning
- [ ] **`app_state` fields each have an inline comment** — not just section
  headers. Every pipeline, texture, sampler, buffer, setting, and state
  variable gets its own comment explaining what it is, its format/units
  where applicable, and how it's used
- [ ] Push constant structs explain each member
- [ ] GPU type struct fields (e.g. `GpuPrimitive`, `GpuMaterial`, `ModelData`)
  document each field

---

## 7. Spec and documentation accuracy (5+ PR comments)

When referencing specifications (glTF 2.0, Vulkan, etc.) or external standards,
the wording must match the spec's normative language.

**What to check:**

- [ ] "MUST" vs "SHOULD" vs "MAY" matches the source spec exactly
- [ ] Section numbers or clause references are correct
- [ ] Algorithm descriptions match the reference (not a paraphrase that changes
  the meaning)
- [ ] External links are valid and point to the right section

---

## 8. Skill documentation completeness (5+ PR comments)

The matching skill in `.claude/skills/<topic>/SKILL.md` must have all required
sections.

**What to check:**

- [ ] YAML frontmatter with `name` and `description`
- [ ] Overview paragraph explaining when to use the skill
- [ ] "Key API calls" section listing the SDL/math functions introduced
- [ ] "Correct order" or workflow section showing the sequence of operations
- [ ] "Common mistakes" section documenting gotchas
- [ ] "Ready-to-use template" or code skeleton

---

## 9. README structure and content

**What to check:**

- [ ] Starts with `# Lesson NN — Title`
- [ ] Has "What you'll learn" section near the top
- [ ] **GPU/physics/audio lessons:** Has screenshot in a "Result" section near
  the top (not a placeholder)
- [ ] **Math lessons:** "Result" section comes **after** "Building" (not near
  the top) — math results are text output that would be intimidating before
  the lesson content
- [ ] **GPU lessons only:** If the lesson has shader files, has a "Shaders"
  section immediately before "Building" that lists each shader file with a
  brief description of what it does
- [ ] Has "Building" section with build commands
- [ ] Has "AI skill" section linking to the skill
- [ ] Ends with "Exercises" section (3-4 exercises)
- [ ] "What's next" comes before "Exercises" (not after)
- [ ] No use of banned words: "trick", "hack", "magic", "clever", "neat"
  (per CLAUDE.md tone principles)

---

## 10. Concept introduction for new readers

**Lessons are written for readers who know nothing unless a previous lesson
taught it.** Every concept, API, tool, or term that appears for the first time
must be briefly defined in the README — or the README must link to the specific
earlier lesson or engine/math lesson that introduced it.

**What to check:**

- [ ] Every SDL API function used for the first time in the lesson series is
  briefly explained (what it does, why it is needed) — not just named
- [ ] Every graphics or GPU concept introduced for the first time (e.g.
  swapchain, render pass, command buffer, pipeline, vertex buffer, shader,
  depth buffer) has a plain-language definition before or alongside its first
  use
- [ ] Domain-specific terms (e.g. "sRGB", "linear color space", "NDC",
  "back-face culling") are defined when first used, or explicitly deferred
  with a note pointing to the future lesson that will cover them
- [ ] Links to **engine lessons** are provided where they offer deeper
  background on foundational topics
- [ ] Links to **math lessons** are provided when the lesson uses math
  concepts (vectors, matrices, coordinate spaces) for the first time
- [ ] No concept is used in the README or code comments with the implicit
  assumption that "everyone knows what this is"

---

## 11. main.c structure (from publish-lesson validation)

**What to check:**

- [ ] Uses `#define SDL_MAIN_USE_CALLBACKS 1`
- [ ] Implements all 4 callbacks: `SDL_AppInit`, `SDL_AppEvent`,
  `SDL_AppIterate`, `SDL_AppQuit`
- [ ] Uses `SDL_calloc` for app_state allocation
- [ ] Includes error handling with `SDL_Log` on all GPU calls
- [ ] Window size is 1280x720 (16:9) — standard for consistent screenshots
- [ ] Has comprehensive comments explaining *why* and *purpose*, not just
  *what*
- [ ] **No bare C stdlib calls** — use SDL-prefixed APIs where available
  (`SDL_fabsf`, `SDL_sinf`, `SDL_memset`, etc.), and approved project wrappers
  for C99 functions SDL lacks (`forge_isfinite`, `forge_fmaxf`, `forge_fminf`)

**Skip `SDL_MAIN_USE_CALLBACKS` check for:** math, engine lessons that use
`main()` directly.

---

## 12. `forge_scene.h` usage (GPU, physics, audio lessons)

**All GPU lessons, all physics lessons, and all audio lessons** must use
`forge_scene.h` for the rendering baseline (shadow map, Blinn-Phong, grid,
sky, camera, UI). This eliminates hundreds of lines of boilerplate and ensures
a consistent rendering foundation.

**What to check:**

- [ ] `main.c` includes `#define FORGE_SCENE_IMPLEMENTATION` followed by
  `#include "scene/forge_scene.h"`
- [ ] `app_state` contains a `ForgeScene scene` field instead of individual
  pipelines, textures, and samplers for the baseline rendering
- [ ] Rendering uses `forge_scene_begin_frame` / `forge_scene_begin_shadow_pass`
  / `forge_scene_begin_main_pass` / `forge_scene_end_frame` pattern
- [ ] No duplicate baseline shaders in the lesson's `shaders/` directory
  (scene, grid, shadow, sky, UI shaders are provided by `forge_scene.h`)
- [ ] Lesson-specific shaders (if any) serve a purpose beyond the baseline

**Skip this check for:** math, engine, UI, asset lessons.

---

## 13. Markdown linting

Run the linter and resolve all issues.

```bash
npx markdownlint-cli2 "lessons/<track>/NN-name/**/*.md" ".claude/skills/<topic>/SKILL.md"
```

**Common issues from PR feedback:**

- [ ] All code blocks have language tags (`c`, `bash`, `text`, `hlsl`)
- [ ] Display math uses 3-line format (`$$\n...\n$$`), not inline `$$...$$`
- [ ] Tables have consistent column counts
- [ ] No trailing whitespace or missing blank lines around headings

---

## 14. Python linting (if scripts were modified)

If any Python scripts in `scripts/` were added or modified:

```bash
uv run ruff check scripts/
uv run ruff format --check scripts/
```

- [ ] No lint errors from `ruff check`
- [ ] No format issues from `ruff format --check`
- [ ] Auto-fix with `uv run ruff check --fix scripts/ && uv run ruff format scripts/` if needed

---

## 15. Pyright type checking (if Python files were modified)

If any Python files in `scripts/` or `pipeline/` were added or modified:

```bash
uv run pyright
```

- [ ] No errors from `pyright`
- [ ] No private import usage (`reportPrivateImportUsage`)
- [ ] No unresolved imports (`reportMissingImports`)

---

## 16. SDL stdinc compliance

**Never use bare C stdlib calls when an SDL_ equivalent exists.** This is a
cross-platform portability requirement.

**What to check:**

- [ ] No bare C stdlib calls (`fabsf`, `sinf`, `memset`, `strcmp`, `malloc`,
  etc.) when an SDL equivalent exists. Grep for bare names in `.c` and `.h`
  files and verify all matches use the `SDL_` prefix.

---

## 17. Build and shader compilation

Verify the lesson compiles and shaders are up to date.

**For GPU, physics, and audio lessons (C with shaders):**

```bash
python scripts/compile_shaders.py NN -v
cmake --build build --target NN-name
```

- [ ] Shaders compile to both SPIRV and DXIL without warnings
- [ ] Lesson builds with no errors or warnings
- [ ] Generated shader headers are up to date (not stale from a previous edit)

**For math/engine lessons (C without shaders):**

```bash
cmake --build build --target NN-name
```

- [ ] Lesson builds with no errors or warnings

**For asset lessons (Python):**

```bash
uv run pytest tests/pipeline/ -v
```

- [ ] Pipeline tests pass

**Skip for:** UI lessons (no standalone executable).

---

## 18. Diagram correctness (recurring in PRs #152, #167, #168, #179, #185)

If the lesson has diagrams (check for `assets/*.png` files that are not
screenshots), verify each diagram function against the README:

- [ ] Every diagram's plotted geometry matches the README's equations
- [ ] Annotations use the same variable names as the README
- [ ] Coordinate systems are consistent with the lesson's conventions
- [ ] Docstrings accurately describe what the function plots
- [ ] Diagrams generate without errors

For a thorough review, invoke `/dev-review-diagrams` with the lesson key.
If there are no diagrams for the lesson, skip this section.

---

## Reporting

After completing all checks, report a summary table:

```text
Final Pass Results — Lesson NN: Name
=====================================

 0. Required files       ✅ PASS  (all files present)
 1. SDL bool returns     ✅ PASS  (N calls checked)
 2. Command buffer life  ✅ PASS  (N paths checked)
 3. Magic numbers        ✅ PASS
 4. Resource leaks       ⚠️  WARN  (1 potential leak in load_scene)
 5. Naming conventions   ✅ PASS
 6. Intent comments      ✅ PASS
 7. Spec accuracy        ✅ PASS
 8. Skill completeness   ✅ PASS
 9. README structure     ✅ PASS
10. Concept introduction ✅ PASS
11. main.c structure     ✅ PASS
12. forge_scene.h usage  ✅ PASS
13. Markdown lint        ✅ PASS
14. Python lint          ⏭️  SKIP  (no scripts modified)
15. Pyright types        ⏭️  SKIP  (no scripts modified)
16. SDL stdinc compliance ✅ PASS
17. Build & shaders      ✅ PASS
18. Diagram correctness  ⏭️  SKIP  (no diagrams)
```

For each WARN or FAIL, list the specific file, line, and issue with a suggested
fix. Ask the user if they want you to apply the fixes before proceeding to
`/dev-create-pr`.
