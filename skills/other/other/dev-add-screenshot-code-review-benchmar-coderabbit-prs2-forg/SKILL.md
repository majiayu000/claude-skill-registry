---
name: dev-add-screenshot
description: Capture a screenshot or animated GIF for a forge-gpu lesson and update its README
argument-hint: "[lesson-path]"
disable-model-invocation: false
---

Capture a screenshot (PNG) or animated GIF from a lesson executable and
embed it in the lesson's README.

## When to use

- After creating or updating a GPU lesson
- When a lesson README has a `<!-- TODO: screenshot -->` placeholder
- When the visual output of a lesson has changed
- **Use GIF mode for animated lessons** — any lesson with motion, animation,
  or time-varying output (uniforms, particles, physics, etc.) should use an
  animated GIF instead of a static screenshot

## How it works

Lessons include `capture/forge_capture.h` which adds a `--screenshot`
command-line flag. The Python orchestration script runs the lesson, converts
the BMP output to PNG, and updates the README.

**Important:** Lessons using `forge_scene.h` (physics, audio, GPU lessons
40+) already have capture support built in — `forge_scene.h` includes
`forge_capture.h` and handles init, frame capture, and cleanup internally.
No changes to `main.c` are needed for these lessons. Just build with
`-DFORGE_CAPTURE=ON` and run the capture script.

For early GPU lessons (02–39) that do NOT use `forge_scene.h`, the lesson's
`main.c` must have capture support integrated manually. If it doesn't, add
it before the capture script will work (see "Adding capture support to a
lesson" below).

## Key API calls

- **Configure build:** `cmake -B build -DFORGE_CAPTURE=ON`
- **Build target:** `cmake --build build --config Debug --target <target-name>`
- **Screenshot:** `python scripts/capture_lesson.py lessons/gpu/<lesson-dir>`
- **Start frame:** `--capture-frame N` (default: 5, increase if output is black)
- **Skip README update:** `--no-update-readme`
- **Force rebuild:** `--build`

## Code template

```bash
# 1. Configure with capture support (REQUIRED — without this the capture
#    code is not compiled even if main.c has the #ifdef blocks)
cmake -B build -DFORGE_CAPTURE=ON

# 2. Build the lesson (use a Task agent with model: "haiku")
cmake --build build --config Debug --target <target-name>

# 3a. Capture a static screenshot
python scripts/capture_lesson.py lessons/gpu/<lesson-dir>

# 3b. OR capture an animated GIF (for lessons with motion/animation)
python scripts/capture_lesson.py lessons/gpu/<lesson-dir> --gif
```

## Steps

### 1. Identify the lesson

From the user's argument, resolve the lesson directory path. Accept any of:

- `01` or `01-hello-window` (resolved to `lessons/gpu/01-hello-window`)
- `lessons/gpu/01-hello-window` (used directly)

### 2. Check for capture support

Search the lesson's `main.c` for `forge_capture`. If it is missing, add
capture support following the integration guide below before proceeding.

### 3. Configure with capture support

```bash
cmake -B build -DFORGE_CAPTURE=ON
```

This step is **required** — without it, `FORGE_CAPTURE` is not defined and
all capture `#ifdef` blocks compile to nothing. If you skip this, the
executable will run but never exit (no `--screenshot` handling), and the
capture script will time out after 30 seconds.

### 4. Build the lesson

Use a Task agent with `model: "haiku"` per project conventions:

```bash
cmake --build build --config Debug --target <target-name>
```

### 5. Run the capture script

**Static screenshot** (for lessons with no animation):

```bash
python scripts/capture_lesson.py lessons/gpu/<lesson-dir>
```

**Animated GIF** (for lessons with motion, animation, or time-varying output):

```bash
python scripts/capture_lesson.py lessons/gpu/<lesson-dir> --gif
```

The GIF captures 120 frames at 30 fps by default (4 seconds). Adjust with
`--gif-frames N` and `--gif-fps N`. Pillow assembles the frames — it is
already installed in the project environment.

**When to use GIF vs screenshot:** If the lesson has any animation or motion
(uniforms changing over time, particles, physics, camera movement), use
`--gif`. Static scenes (hello window, first triangle, texture display) use
a screenshot.

### 6. Verify the output

- **Screenshot:** Check that `lessons/gpu/<lesson-dir>/assets/screenshot.png` exists
- **GIF:** Check that `lessons/gpu/<lesson-dir>/assets/animation.gif` exists
- Verify the README was updated (TODO placeholder replaced with image markdown)

### 7. Report to the user

Show the output file path and size. If the user wants to inspect the image,
tell them where to find it.

## Adding capture support to a lesson

If a lesson's `main.c` does not reference `forge_capture`, you must add it
in five places. The CMakeLists.txt `FORGE_CAPTURE` define is usually already
present — check and add it if not.

Use any existing lesson (e.g. `lessons/gpu/01-hello-window/main.c`) as a
reference. The pattern has five insertion points:

### 1. Include (after other `#include` lines)

```c
/* This is NOT part of the lesson — it's build infrastructure that lets us
 * programmatically capture screenshots for the README.  Compiled only when
 * cmake is run with -DFORGE_CAPTURE=ON.  You can ignore these #ifdef blocks
 * entirely; the lesson works the same with or without them.
 * See: scripts/capture_lesson.py, common/capture/forge_capture.h */
#ifdef FORGE_CAPTURE
#include "capture/forge_capture.h"
#endif
```

### 2. AppState field (inside the `app_state` typedef)

```c
#ifdef FORGE_CAPTURE
    ForgeCapture capture;   /* screenshot infrastructure — see note above */
#endif
```

### 3. AppInit — parse args and init (after state is allocated and device/window are assigned)

Remove `(void)argc; (void)argv;` if present (the capture code uses them).

```c
#ifdef FORGE_CAPTURE
    forge_capture_parse_args(&state->capture, argc, argv);
    if (state->capture.mode != FORGE_CAPTURE_NONE) {
        if (!forge_capture_init(&state->capture, device, window)) {
            SDL_Log("Failed to initialise capture");
            SDL_ReleaseWindowFromGPUDevice(device, window);
            SDL_DestroyWindow(window);
            SDL_DestroyGPUDevice(device);
            SDL_free(state);
            return SDL_APP_FAILURE;
        }
    }
#endif
```

### 4. AppIterate — finish frame and conditional submit

**Critical:** `forge_capture_finish_frame` submits the command buffer
internally. The lesson's normal `SDL_SubmitGPUCommandBuffer` call must be
wrapped in an `else` block so it only runs when capture is inactive.
Without this, you get an assertion failure: `"Command buffer already
submitted!"`.

Replace the existing submit:

```c
/* BEFORE (causes double-submit assertion when capture is active): */
if (!SDL_SubmitGPUCommandBuffer(cmd)) { ... }

/* AFTER: */
#ifdef FORGE_CAPTURE
    if (state->capture.mode != FORGE_CAPTURE_NONE) {
        if (!forge_capture_finish_frame(&state->capture, cmd, swapchain_tex)) {
            SDL_SubmitGPUCommandBuffer(cmd);
        }
        if (forge_capture_should_quit(&state->capture)) {
            return SDL_APP_SUCCESS;
        }
    } else
#endif
    {
        if (!SDL_SubmitGPUCommandBuffer(cmd)) {
            SDL_Log("SDL_SubmitGPUCommandBuffer failed: %s", SDL_GetError());
            return SDL_APP_FAILURE;
        }
    }
```

The `else` on the `#endif` line connects the `#ifdef` block to the normal
submit block — when `FORGE_CAPTURE` is not defined, the braces compile as
a plain block and the submit runs unconditionally.

### 5. AppQuit — destroy capture resources (before other cleanup)

```c
#ifdef FORGE_CAPTURE
    forge_capture_destroy(&state->capture, state->device);
#endif
```

## Headless capture (no GPU)

On servers without a display or GPU hardware, screenshots can be captured
using **lavapipe** (Mesa's CPU-based Vulkan driver) and **Xvfb** (a virtual
X11 display).

### Prerequisites

```bash
apt install mesa-vulkan-drivers xvfb
```

### Usage

Pass `--headless` to the capture script:

```bash
python scripts/capture_lesson.py lessons/gpu/<lesson-dir> --headless
```

**Auto-detection:** When `DISPLAY` is not set (typical on CI or remote
servers), the script automatically enables headless mode if both `xvfb-run`
and the lavapipe ICD file are available. No flag needed.

### How it works

- **Lavapipe** implements the Vulkan API entirely on the CPU — no GPU
  hardware required. The environment variables `VK_ICD_FILENAMES` and
  `VK_DRIVER_FILES` point SDL's Vulkan backend at the lavapipe driver.
- **Xvfb** provides a virtual X11 display so SDL can create a window without
  a physical monitor. The script uses `xvfb-run -a` to allocate a free
  display automatically.

## Capture script options

| Flag | Default | Description |
|---|---|---|
| `--capture-frame N` | 5 | Which frame to start capturing |
| `--no-update-readme` | off | Skip README placeholder replacement |
| `--build` | auto | Force rebuild before capturing |
| `--headless` | auto | Use lavapipe + Xvfb (auto-detected when no `DISPLAY`) |
| `--gif` | off | Capture an animated GIF instead of a screenshot |
| `--gif-frames N` | 120 | Number of frames to capture for GIF |
| `--gif-fps N` | 30 | Playback frame rate for the GIF |

## Output locations

- Screenshots: `lessons/gpu/<name>/assets/screenshot.png`
- Animated GIFs: `lessons/gpu/<name>/assets/animation.gif`

## Expected dimensions

All lessons should use 1280×720 (16:9). If a screenshot has unexpected
dimensions, verify the lesson's `WINDOW_WIDTH`/`WINDOW_HEIGHT` defines.

## Common issues

- **Timeout (executable never exits):** The lesson is missing capture
  support, or you forgot `cmake -B build -DFORGE_CAPTURE=ON`. The
  executable runs normally but ignores `--screenshot` because the capture
  code was compiled out. Reconfigure with `-DFORGE_CAPTURE=ON` and rebuild.
- **"Command buffer already submitted!" assertion:** The lesson submits
  the command buffer after `forge_capture_finish_frame` already submitted
  it. Wrap the normal submit in the `else` pattern shown above.
- **Black image:** The `--capture-frame` default of 5 skips the first few
  frames so the GPU pipeline is warmed up. If you still get black, try
  `--capture-frame 10`.
- **Build not found:** Run `cmake --build build --config Debug` first or
  pass `--build` to the capture script.
- **Wrong colors:** The capture uses the swapchain's sRGB format. If the
  lesson does not set `SDR_LINEAR`, colors may look washed out.
- **Headless: "lavapipe ICD not found":** Install Mesa's Vulkan drivers with
  `apt install mesa-vulkan-drivers`. The script looks for the ICD file at
  `/usr/share/vulkan/icd.d/lvp_icd.json`.
- **Headless: "xvfb-run not found":** Install Xvfb with `apt install xvfb`.
- **Headless: visual differences:** Lavapipe is a software renderer. Colors
  and anti-aliasing may differ slightly from hardware GPU output.
