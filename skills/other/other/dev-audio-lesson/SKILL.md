---
name: dev-audio-lesson
description: Add an audio lesson — sound playback, mixing, spatial audio, DSP effects, with SDL GPU scenes and forge UI
argument-hint: "[number] [topic-name] [description]"
---

Every audio lesson produces two things: **library code** and a **demo
program**. The library — `common/audio/forge_audio.h` — is the primary
deliverable. The lessons teach concepts; the library is what remains when the
learning is done. It must be correct, efficient, tested, and safe. The demo
program visualizes and controls the audio in action, rendered with SDL GPU
and controlled through forge UI panels.

**When to use this skill:**

- You need to teach audio playback, mixing, spatial sound, or DSP effects
- A learner wants to understand PCM audio, streaming, attenuation, or filters
- The concept benefits from a visual 3D scene showing audio source positions
- New functionality needs to be added to `common/audio/forge_audio.h`

**Smart behavior:**

- Before creating a lesson, check if an existing audio lesson already covers it
- **Library first, demo second.** Design, implement, document, and test the
  library code before writing a single line of the demo program. The demo
  exercises the library — it does not replace it.
- Audio lessons are interactive — every concept must be audible in the running
  program and controllable via forge UI
- Focus on *why* the technique works, not just the code — connect DSP math to
  what the listener hears
- Use simple geometric shapes for sound source visualization — the audio is
  the focus
- All scene geometry comes from `common/shapes/forge_shapes.h` — never write
  inline geometry generation functions
- Cross-reference math lessons (vectors, dot products) and GPU lessons where
  relevant

## Arguments

The user (or you) can provide:

- **Number**: two-digit lesson number (e.g. 01, 02)
- **Topic name**: kebab-case (e.g. audio-basics, sound-effects)
- **Description**: what this teaches (e.g. "PCM fundamentals, WAV loading,
  SDL audio streams")

If any are missing, infer from context or ask.

## Steps

### 1. Analyze what's needed

- **Check existing audio lessons**: Is there already a lesson for this topic?
- **Check `common/audio/`**: Does relevant library code already exist?
- **Check `common/ui/`**: Does the UI library provide the widgets needed for
  audio controls? If a required widget is missing, note it.
- **Identify the scope**: What specific audio concepts does this lesson cover?
- **Find cross-references**: Which math/GPU/UI lessons relate?
- **Check PLAN.md**: Where does this lesson fit in the audio track?

### 2. Create the lesson directory

`lessons/audio/NN-topic-name/`

With subdirectories:

```text
lessons/audio/NN-topic-name/
  main.c
  CMakeLists.txt
  README.md
  audio.conf           (gitignored — local path to audio files)
  assets/
    screenshot.png     (lesson screenshot — checked in)
```

Baseline rendering shaders (shadow, scene, grid, sky, UI) are provided by
`forge_scene.h` — no per-lesson copies needed. If the lesson introduces a
topic-specific shader (e.g. a waveform visualization pass), add a `shaders/`
subdirectory for those files only.

### 3. Design and implement the audio library code

Every audio lesson adds to `common/audio/forge_audio.h`. This is not
optional — it is the primary deliverable. The demo program exists to exercise
and visualize the library; the library is what ships.

For the first audio lesson, create the file. For subsequent lessons, extend
it. Design the API before writing the demo. The demo calls the library —
never the reverse.

#### Library standards

**Correctness:**

- Every function must implement a named, well-understood technique. Cite the
  source in the doc comment — a textbook, paper, or DSP reference.
- Audio processing must not introduce clicks, pops, or DC offset. Transitions
  (volume changes, crossfades) must be smooth.
- Sample rate conversion and channel mapping must be handled correctly via
  SDL audio stream properties.
- Buffer sizes and sample counts must be computed correctly — off-by-one
  errors in audio produce audible artifacts.

**Thread safety:**

- SDL audio streams deliver data on a separate audio thread. Any shared state
  between the main thread and audio processing must use SDL atomics or
  SDL mutexes.
- Volume, panning, and effect parameters should be set atomically so partial
  updates don't produce glitches.
- Resource lifetimes must be clear — never free audio data while a stream
  might still reference it.

**Performance:**

- Audio processing runs in real time — dropped samples cause audible glitches.
  Keep per-sample operations simple (multiply, add, table lookup).
- Precompute coefficients (filter taps, attenuation curves, panning tables)
  at init time or when parameters change, not per-sample.
- Use `float` for all audio processing. Convert to/from integer formats only
  at the SDL boundary.

**Numerical safety:**

- Clamp output samples to `[-1.0f, 1.0f]` before delivery to prevent
  clipping distortion beyond what the user intends.
- Guard against division by zero in attenuation calculations (zero distance).
- Filter coefficients must be validated to prevent instability (poles inside
  the unit circle for IIR filters).

**Header-only implementation:**

- `static inline` for all functions — no separate `.c` compilation unit
- Guard with `#ifndef FORGE_AUDIO_H` / `#define` / `#endif`
- Include only SDL3, `"math/forge_math.h"`, and standard C headers
- No heap allocation in per-sample paths — allocate buffers at init time
- Deterministic: identical input samples and parameters produce identical output

**Documentation (every function, no exceptions):**

```c
/* Load a WAV file into an audio buffer.
 *
 * Reads the WAV file at the given path using SDL_LoadWAV and converts
 * it to the specified format. The returned buffer owns its sample data
 * and must be freed with forge_audio_buffer_free().
 *
 * Parameters:
 *   path   — file path to the WAV file (must not be NULL)
 *   spec   — desired output format (sample rate, channels, format)
 *
 * Returns:
 *   ForgeAudioBuffer with sample data, or a zero-initialized struct
 *   on failure (check .data != NULL).
 *
 * Usage:
 *   ForgeAudioBuffer buf = forge_audio_load_wav("/path/to/audio/click.wav", spec);
 *   if (!buf.data) { SDL_Log("Failed to load WAV"); return; }
 *
 * See: Audio Lesson 01 — Audio Basics
 * Ref: SDL3 documentation, SDL_LoadWAV
 */
```

Every doc comment must include:

- Summary (one sentence — what it does)
- Algorithm or technique being implemented
- Parameters with types, valid ranges, and nullability
- Return value (if any) with format/units
- Usage example
- Cross-reference to the lesson that introduces it
- Reference to the source material

**Naming:**

- Functions: `forge_audio_verb_noun()` — e.g. `forge_audio_init()`,
  `forge_audio_load_wav()`, `forge_audio_play_oneshot()`
- Types: `ForgeAudioNoun` — e.g. `ForgeAudioBuffer`, `ForgeAudioSource`,
  `ForgeAudioMixer`, `ForgeAudioListener`
- Constants: `FORGE_AUDIO_UPPER` — e.g. `FORGE_AUDIO_MAX_SOURCES`

**Core types to establish in Lesson 01:**

```c
#ifndef FORGE_AUDIO_H
#define FORGE_AUDIO_H

#include <SDL3/SDL.h>
#include "math/forge_math.h"

/* --- Audio buffer (decoded sample data) --------------------------------- */

typedef struct ForgeAudioBuffer {
    float *data;          /* interleaved float samples                       */
    int    sample_count;  /* total samples (frames * channels)               */
    int    channels;      /* 1 = mono, 2 = stereo                           */
    int    sample_rate;   /* Hz — typically 44100 or 48000                   */
} ForgeAudioBuffer;

/* --- Audio source (a playing instance) ---------------------------------- */

typedef struct ForgeAudioSource {
    const ForgeAudioBuffer *buffer;  /* sample data (not owned)             */
    int    cursor;          /* current read position in samples              */
    float  volume;          /* linear gain [0..1]                            */
    float  pan;             /* stereo pan [-1..1], 0 = center                */
    bool   looping;         /* true = restart at end of buffer               */
    bool   playing;         /* true = actively producing samples             */
} ForgeAudioSource;

/* ... functions grow lesson by lesson ... */

#endif /* FORGE_AUDIO_H */
```

#### Testing the library (MANDATORY)

The audio library is tested independently of the demo program. Tests validate
correctness, edge cases, and determinism. Every function added to
`forge_audio.h` must have corresponding tests in `tests/audio/test_audio.c`.

**Test categories (every function must have all applicable categories):**

1. **Basic correctness** — Known inputs produce expected outputs. For audio
   processing functions, verify output samples against hand-computed values.

2. **Edge cases** — Empty buffers, zero-length audio, single-sample buffers,
   zero volume, maximum volume, out-of-range panning values, mismatched
   sample rates.

3. **No artifacts** — Volume transitions produce no clicks (verify samples
   are continuous). Looping produces seamless playback (verify loop-point
   samples match). Mixing does not overflow `[-1, 1]` without explicit
   clipping.

4. **Determinism** — Two identical sources with identical parameters produce
   bit-identical output.

5. **Thread safety** — Parameter changes during playback do not crash. Verify
   with single-threaded simulation (no need to test actual SDL threads in
   unit tests).

**Test infrastructure:**

- Test file: `tests/audio/test_audio.c`
- Register in root `CMakeLists.txt` as `test_audio`
- Use the same `ASSERT_NEAR` / test macros as `tests/math/test_math.c`
- Run: `cmake --build build --target test_audio && ctest --test-dir build -R audio`
- Tests must pass before the demo program is written

### 4. Create the demo program (`main.c`)

A focused C program that demonstrates audio concepts with both audible output
and visual feedback using SDL GPU and forge UI.

**MANDATORY: Use `forge_scene.h` for the rendering baseline.** The scene
library provides Blinn-Phong lighting, shadow mapping, grid floor, sky
gradient, FPS camera, and UI in a single `forge_scene_init()` call. This
eliminates hundreds of lines of rendering boilerplate and lets the lesson
focus on audio. See the `forge-scene-renderer` skill for the full API.

**Every audio lesson MUST include these features:**

1. **SDL GPU rendered scene via `forge_scene.h`** — A 3D scene providing
   visual context for the audio. For spatial audio lessons, this means visible
   sound source positions in the scene. For fundamentals lessons, a simple
   scene with visual feedback (waveform visualization, VU meters as colored
   geometry) is sufficient. The rendering baseline (Blinn-Phong, grid, shadow
   map, depth buffer, sRGB swapchain, sky) is provided by `forge_scene.h`.

2. **First-person camera** — Provided by `forge_scene.h`. The camera position
   (accessible via `forge_scene_cam_pos()`) doubles as the audio listener
   position for spatial audio lessons.

3. **Forge UI panel** — Provided by `forge_scene.h` via
   `forge_scene_begin_ui()` / `forge_scene_end_ui()`. Every lesson must have
   at least:
   - Master volume slider
   - Play/pause button (or status indicator)
   - Lesson-specific controls (per-source volume, panning, effect parameters)

4. **Capture support** — `forge_capture.h` integration (when `FORGE_CAPTURE`
   defined) via `scripts/capture_lesson.py`.

**Audio requirements:**

- **SDL audio stream** — All audio output goes through `SDL_AudioStream`.
  Create the stream at init, feed samples in the iterate callback or via
  SDL's audio device callback.
- **User-supplied audio files** — Audio files are **not** checked into the
  repository. Each lesson has an `audio.conf` file (gitignored) that points
  to a local directory containing the user's audio files. See step 7 for the
  full config workflow.
- **Real-time parameter control** — UI sliders and keys should change audio
  parameters (volume, pan, effect intensity) in real time with audible
  results.

**Simulation controls:**

| Key | Action |
|---|---|
| R | Reset / replay audio from start |
| P | Pause / resume audio playback |
| 1–9 | Trigger sound effects (where applicable) |
| +/- | Adjust master volume |

**Scene geometry via `forge_shapes.h` (MANDATORY):**

All scene geometry **must** come from `common/shapes/forge_shapes.h`. Use
spheres or icospheres for sound source positions, cones for directional
sources. Never write inline geometry generation functions.

**Template structure:**

```c
/*
 * Audio Lesson NN — Topic Name
 *
 * Demonstrates: [what this shows]
 *
 * Controls:
 *   WASD / Arrow keys — move camera (listener position)
 *   Mouse             — look around
 *   R                 — reset / replay audio
 *   P                 — pause / resume
 *   1–9               — trigger sound effects
 *   +/-               — adjust master volume
 *   Escape            — release mouse / quit
 *
 * SPDX-License-Identifier: Zlib
 */

#define SDL_MAIN_USE_CALLBACKS 1
#include <SDL3/SDL.h>
#include <SDL3/SDL_main.h>
#include <stddef.h>

#include "math/forge_math.h"
#include "audio/forge_audio.h"
#include "shapes/forge_shapes.h"

#define FORGE_SCENE_IMPLEMENTATION
#include "scene/forge_scene.h"

/* ── Constants ────────────────────────────────────────────────────── */

#define AUDIO_SAMPLE_RATE 48000

/* ── Types ────────────────────────────────────────────────────────── */

typedef struct app_state {
    ForgeScene scene;  /* rendering, camera, shadow map, grid, sky, UI */

    /* GPU resources — app-owned geometry */
    SDL_GPUBuffer *sphere_vb, *sphere_ib;
    int sphere_index_count;

    /* Audio state — lesson-specific */
    SDL_AudioStream *audio_stream;  /* SDL audio output stream          */
    /* ForgeAudioBuffer buffers[N]; */
    /* ForgeAudioSource sources[N]; */
    float master_volume;            /* linear gain [0..1]               */
    bool  audio_paused;             /* true = audio playback frozen     */
} app_state;
```

**Init pattern:**

```c
SDL_AppResult SDL_AppInit(void **appstate, int argc, char **argv)
{
    app_state *state = SDL_calloc(1, sizeof(*state));
    if (!state) return SDL_APP_FAILURE;
    *appstate = state;

    ForgeSceneConfig cfg = forge_scene_default_config("Audio NN — Topic");
    cfg.cam_start_pos = vec3_create(0.0f, 4.0f, 12.0f);
    cfg.font_path = "assets/fonts/liberation_mono/LiberationMono-Regular.ttf";

    if (!forge_scene_init(&state->scene, &cfg, argc, argv))
        return SDL_APP_FAILURE;

    state->master_volume = 1.0f;

    /* Read audio directory from audio.conf */
    char audio_dir[512];
    if (!read_audio_conf("audio.conf", audio_dir, sizeof(audio_dir))) {
        SDL_Log("audio.conf not found or not configured.");
        SDL_Log("See the lesson README for setup instructions.");
        return SDL_APP_FAILURE;
    }

    /* Load audio files from user's directory, set up SDL audio stream,
     * upload shapes ... */
    return SDL_APP_CONTINUE;
}
```

**Iterate pattern (camera position as listener):**

```c
SDL_AppResult SDL_AppIterate(void *appstate)
{
    app_state *state = appstate;
    ForgeScene *s = &state->scene;

    if (!forge_scene_begin_frame(s)) return SDL_APP_CONTINUE;

    /* Use camera position as audio listener */
    vec3 listener_pos = forge_scene_cam_pos(s);

    /* Shadow pass */
    forge_scene_begin_shadow_pass(s);
    /* forge_scene_draw_shadow_mesh(s, vb, ib, count, model); */
    forge_scene_end_shadow_pass(s);

    /* Main pass */
    forge_scene_begin_main_pass(s);
    /* Draw sound source markers as colored spheres */
    /* forge_scene_draw_mesh(s, vb, ib, count, model, color); */
    forge_scene_draw_grid(s);
    forge_scene_end_main_pass(s);

    /* UI pass — audio controls */
    float mx, my;
    Uint32 buttons = SDL_GetMouseState(&mx, &my);
    forge_scene_begin_ui(s, mx, my, (buttons & SDL_BUTTON_LMASK) != 0);
    /* forge_ui_* slider/button calls for volume, pan, effects ... */
    forge_scene_end_ui(s);

    return forge_scene_end_frame(s);
}
```

### 5. Shaders

The baseline shaders (scene, grid, shadow, sky, UI) are compiled into
`forge_scene.h` — no per-lesson copies needed. If the lesson introduces a
topic-specific shader (e.g. a waveform or spectrum visualization pass),
add those files to `shaders/` and compile them:

```bash
python scripts/compile_shaders.py audio/NN-topic-name
```

Most audio lessons need no lesson-specific shaders at all.

### 6. Create `CMakeLists.txt`

```cmake
add_executable(NN-topic-name WIN32 main.c)
target_include_directories(NN-topic-name PRIVATE ${FORGE_COMMON_DIR})
target_link_libraries(NN-topic-name PRIVATE SDL3::SDL3
    $<$<NOT:$<C_COMPILER_ID:MSVC>>:m>)

if(FORGE_CAPTURE)
    target_compile_definitions(NN-topic-name PRIVATE FORGE_CAPTURE)
endif()

# Copy SDL3 DLL next to executable (Windows)
if(TARGET SDL3::SDL3-shared)
    add_custom_command(TARGET NN-topic-name POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            $<TARGET_FILE:SDL3::SDL3-shared>
            $<TARGET_FILE_DIR:NN-topic-name>
    )
endif()

# Copy font asset next to executable
add_custom_command(TARGET NN-topic-name POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory
        $<TARGET_FILE_DIR:NN-topic-name>/assets/fonts/liberation_mono
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${CMAKE_SOURCE_DIR}/assets/fonts/liberation_mono/LiberationMono-Regular.ttf
        $<TARGET_FILE_DIR:NN-topic-name>/assets/fonts/liberation_mono/
)

# Copy audio.conf next to executable (user-local audio file paths)
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/audio.conf)
    add_custom_command(TARGET NN-topic-name POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            ${CMAKE_CURRENT_SOURCE_DIR}/audio.conf
            $<TARGET_FILE_DIR:NN-topic-name>/audio.conf
    )
endif()
```

### 7. Set up audio file configuration

Audio files are **not** checked into the repository. Each lesson uses a
gitignored `audio.conf` file that points to a local directory containing the
user's own audio files. This avoids distributing copyrighted or large binary
assets.

#### 7a. Create the `audio.conf` file

Create `lessons/audio/NN-topic-name/audio.conf`:

```ini
# Audio file configuration for Audio Lesson NN — Topic Name
#
# This file is gitignored. Point audio_dir to a local directory containing
# audio files for this lesson. See README.md for what types of files work
# best.
#
# Royalty-free audio files can be obtained from sites like:
#   freesound.org, pixabay.com/music, opengameart.org, incompetech.com
#
audio_dir = /path/to/your/audio/files
```

This bare-bones config is created by the developer scaffolding the lesson.
It ships with a placeholder path that the user replaces with their own.

#### 7b. Add `audio.conf` to `.gitignore`

Ensure the root `.gitignore` contains:

```text
# Audio lesson config — local paths to user-supplied audio files
lessons/**/audio.conf
```

Add this entry if it does not already exist.

#### 7c. Document audio file requirements in the README

Every audio lesson README must have an **"Audio files"** section (see step 8)
that explains:

1. **What types of audio files** the lesson needs — be specific about content,
   not just format. Examples:
   - "A short percussive sound (click, snap, or drum hit) for one-shot
     playback"
   - "A looping ambient sound (rain, wind, or drone) for continuous playback"
   - "Two distinct sounds for mixing (e.g. a melody and a rhythm track)"
   - "A mono sound effect for spatial positioning (footstep, ping, or alarm)"

2. **Format requirements** — WAV preferred, mono or stereo, 16-bit or 32-bit
   float, 44100 or 48000 Hz. Note any specific requirements (e.g. "must be
   mono for spatial audio").

3. **Where to find royalty-free audio** — Point readers to sources:
   - freesound.org (CC0 and CC-BY samples)
   - pixabay.com/sound-effects (royalty-free)
   - opengameart.org (game-oriented audio)
   - incompetech.com (Kevin MacLeod music, CC-BY)

4. **How to configure** — Tell the reader to edit `audio.conf` and set
   `audio_dir` to the directory containing their files.

#### 7d. Load audio files at runtime via `audio.conf`

The lesson's `main.c` reads `audio.conf` at startup to find the audio
directory, then loads files from that directory. Add a config-reading helper
to `forge_audio.h` (or use a local helper if it's lesson-specific):

```c
/* Read the audio_dir path from audio.conf.
 * Returns true on success, false if the file is missing or
 * the path is the unedited placeholder. */
static bool read_audio_conf(const char *conf_path, char *out_dir, int max_len)
{
    SDL_IOStream *io = SDL_IOFromFile(conf_path, "r");
    if (!io) return false;

    char line[1024];
    bool found = false;
    Sint64 size = SDL_GetIOSize(io);
    if (size > 0 && size < (Sint64)sizeof(line)) {
        /* Read entire small file */
        size_t bytes_read = SDL_ReadIO(io, line, (size_t)size);
        if (bytes_read != (size_t)size) { SDL_CloseIO(io); return false; }
        line[bytes_read] = '\0';
        /* Parse audio_dir = <path> */
        const char *key = "audio_dir";
        char *pos = strstr(line, key);
        if (pos) {
            pos += strlen(key);
            while (*pos == ' ' || *pos == '=') pos++;
            /* Trim trailing whitespace / newline */
            char *end = pos + strlen(pos) - 1;
            while (end > pos && (*end == '\n' || *end == '\r' || *end == ' '))
                *end-- = '\0';
            /* Reject placeholder or empty path */
            if (*pos == '\0' || strstr(pos, "/path/to/") || strstr(pos, "\\path\\to\\")) {
                SDL_CloseIO(io);
                return false;
            }
            SDL_snprintf(out_dir, max_len, "%s", pos);
            found = true;
        }
    }
    SDL_CloseIO(io);
    return found;
}
```

At init time:

```c
char audio_dir[512];
if (!read_audio_conf("audio.conf", audio_dir, sizeof(audio_dir))) {
    SDL_Log("audio.conf not found or not configured.");
    SDL_Log("Create lessons/audio/NN-topic-name/audio.conf with:");
    SDL_Log("  audio_dir = /path/to/your/audio/files");
    SDL_Log("See the lesson README for what audio files are needed.");
    return SDL_APP_FAILURE;
}

/* Build full paths to specific audio files */
char wav_path[512];
SDL_snprintf(wav_path, sizeof(wav_path), "%s/click.wav", audio_dir);
ForgeAudioBuffer click = forge_audio_load_wav(wav_path, spec);
```

#### 7e. Assist the user with audio file selection

When creating a lesson, **if `audio.conf` already exists** with a valid
`audio_dir`, scan that directory and help the user choose appropriate files:

1. List all `.wav`, `.ogg`, `.mp3`, and `.flac` files in the directory
2. For each file, report: filename, duration, channels, sample rate (use
   `ffprobe` or `soxi` if available, otherwise just list filenames)
3. Based on the lesson's audio requirements, suggest which files would work
   best. For example:
   - For a one-shot effect lesson: suggest short files (< 2 seconds)
   - For a spatial audio lesson: suggest mono files
   - For a mixing lesson: suggest 2-3 files with different character
4. Present recommendations to the user and let them confirm or choose
   differently

**If `audio.conf` does not exist or has the placeholder path**, ask the user:

```text
This lesson needs audio files. Please provide a path to a directory
containing audio files (WAV, OGG, MP3, or FLAC).

This lesson needs:
- [specific audio requirements from the lesson design]

Royalty-free audio can be found at freesound.org, pixabay.com, or
opengameart.org.

What is the path to your audio directory?
```

Then create `audio.conf` with their answer and proceed with file selection.

#### 7f. Reference audio files by name in the code

The lesson code should reference audio files by well-known names that
correspond to their purpose, not opaque filenames. Define constants:

```c
/* Audio file names — the user places files with these names in their
 * audio directory, or the lesson maps their chosen files to these names. */
#define AUDIO_FILE_CLICK   "click.wav"
#define AUDIO_FILE_AMBIENT "ambient.wav"
#define AUDIO_FILE_MUSIC   "music.wav"
```

The README should list these expected filenames and what each one is for,
so the user knows which of their files to use (or rename).

### 8. Create `README.md`

Structure:

````markdown
# Audio Lesson NN — Topic Name

[Brief subtitle explaining the audio concept]

## What you'll learn

[Bullet list of audio and implementation concepts covered]

## Result

<!-- TODO: screenshot -->

[Brief description of what the demo shows and sounds like.]

![Screenshot](assets/screenshot.png)

**Controls:**

| Key | Action |
|---|---|
| WASD / Arrows | Move camera (listener position) |
| Mouse | Look around |
| R | Reset / replay audio |
| P | Pause / resume |
| 1–9 | Trigger sound effects |
| +/- | Adjust master volume |
| Escape | Release mouse / quit |

## Audio files

This lesson needs the following audio files. Audio is not included in the
repository — you supply your own files via `audio.conf`.

| Name | Purpose | Requirements |
|---|---|---|
| `click.wav` | One-shot playback demo | Short percussive sound (< 1 s), mono or stereo |
| `ambient.wav` | Looping playback demo | 2–5 s ambient loop, mono or stereo |

**Format:** WAV, 16-bit or 32-bit float, 44100 or 48000 Hz.

**Where to find royalty-free audio:**

- [freesound.org](https://freesound.org) — CC0 and CC-BY samples
- [pixabay.com/sound-effects](https://pixabay.com/sound-effects) — royalty-free
- [opengameart.org](https://opengameart.org) — game-oriented sounds
- [incompetech.com](https://incompetech.com) — Kevin MacLeod music (CC-BY)

**Setup:** Edit `audio.conf` in this lesson directory and set `audio_dir` to
the directory containing your audio files. The program loads files by the
names listed above from that directory.

## The audio

[Main explanation of the audio concepts, with diagrams where helpful.
Use /dev-create-diagram for waveform visualizations, signal flow diagrams,
filter response curves, etc.]

### [Core concept 1]

[Explanation with equations where relevant. For example:]

Linear attenuation reduces volume based on distance from the listener:

$$
\text{gain} = 1 - \frac{d}{d_{\text{max}}}
$$

### [Core concept 2]

[More explanation]

## The code

### Audio initialization

[Explain SDL audio stream setup and buffer management]

### Processing loop

[Walk through the audio update function with annotated code]

### UI controls

[Explain how forge UI sliders and buttons connect to audio parameters]

### Rendering

[Explain how audio state maps to the visual scene. Brief — point readers
to GPU and UI lessons for rendering details.]

## Key concepts

- **Concept 1** — Brief explanation
- **Concept 2** — Brief explanation

## The audio library

This lesson adds the following to `common/audio/forge_audio.h`:

| Function | Purpose |
|---|---|
| `forge_audio_function_name()` | Brief description |

See: [common/audio/README.md](../../../common/audio/README.md)

## Where it's used

- [Math Lesson NN](../../math/NN-name/) provides the [math concept] used here

## Building

```bash
cmake -B build
cmake --build build --config Debug

# Windows
build\lessons\audio\NN-topic-name\Debug\NN-topic-name.exe

# Linux / macOS
./build/lessons/audio/NN-topic-name/NN-topic-name
```

## Exercises

1. [Exercise extending the audio concept]
2. [Exercise modifying parameters to observe different behavior]
3. [Exercise adding a new audio feature]

## Further reading

- [Relevant math lesson for the underlying math]
- [External resource — The Audio Programming Book, DAFX, Julius O. Smith, etc.]
````

### 9. Update project files

- **`CMakeLists.txt` (root)**: Add `add_subdirectory(lessons/audio/NN-topic-name)`
  under an "Audio Lessons" section (create the section if it doesn't exist
  yet, placed after Physics Lessons)
- **`README.md` (root)**: Add a row to the audio lessons table in an
  "Audio Lessons (lessons/audio/)" section — follow the same format as
  the existing track sections. Create the section if this is the first audio
  lesson.
- **`lessons/audio/README.md`**: Create the track README if this is the first
  lesson, or add a row to the existing lessons table
- **`PLAN.md`**: Check off the audio lesson entry

### 10. Cross-reference other lessons

- **Find related math lessons**: Vectors (for spatial audio), signal processing
- **Find related GPU lessons**: Rendering techniques used (lighting, UI rendering)
- **Find related UI lessons**: Widgets used in the control panel
- **Update those lesson READMEs**: Add a note like "See
  [Audio Lesson NN](../../audio/NN-topic/) for this concept in action"
- **Update audio lesson README**: List related lessons in "Where it's used"

### 11. Build and test

```bash
# Compile lesson-specific shaders (skip if lesson has no shaders/ directory)
python scripts/compile_shaders.py audio/NN-topic-name

# Build
cmake -B build
cmake --build build --config Debug

# Run
./build/lessons/audio/NN-topic-name/NN-topic-name
```

Use a Task agent with `model: "haiku"` for build commands per project
conventions.

Verify:

- The program opens a window with the grid floor and scene visible
- Objects are lit with Blinn-Phong shading
- Camera controls work (WASD + mouse)
- Audio plays through speakers/headphones
- UI panel is visible and interactive
- Volume sliders change audio volume in real time
- R resets/replays the audio
- P pauses/resumes audio

### 12. Capture screenshots

```bash
# Configure with capture support
cmake -B build -DFORGE_CAPTURE=ON
cmake --build build --config Debug --target NN-topic-name

# Static screenshot
python scripts/capture_lesson.py lessons/audio/NN-topic-name
```

Copy output to `lessons/audio/NN-topic-name/assets/`.

### 13. Verify key topics are fully explained

**Before finalizing, launch a verification agent** using the Task tool
(`subagent_type: "general-purpose"`). Give the agent the paths to the lesson's
`README.md` and `main.c` and ask it to audit every key topic for completeness.

**For each key topic / "What you'll learn" bullet, the agent must check:**

1. **Explained in the README** — Is the concept described clearly enough that
   a reader encountering it for the first time could understand it?
2. **Demonstrated in the program** — Does `main.c` actually exercise this
   concept with audible and visible behavior?
3. **All referenced terms are defined** — Read the exact wording of each key
   topic and identify every technical term. For each term, confirm it is
   explained somewhere in the lesson.
4. **Equations match code** — Every formula in the README should have a
   corresponding implementation in the code, and vice versa.

**The lesson is incomplete until every key topic passes all four checks.**

### 14. Run markdown linting

Use the `/dev-markdown-lint` skill to check all markdown files:

```bash
npx markdownlint-cli2 "**/*.md"
```

## Audio Lesson Conventions

### Scope

Audio lessons cover sound concepts with real-time playback and visual feedback:

- **Fundamentals** — PCM audio, sample rates, bit depth, channels, WAV loading
- **Playback** — One-shot and looping sounds, volume control, fading
- **Mixing** — Combining multiple sources, panning, master volume, clipping
- **Spatial audio** — Distance attenuation, stereo panning, Doppler effect
- **Streaming** — Large file playback, crossfading, looping with intro sections
- **DSP effects** — Filters, reverb, echo, chorus, per-source and master bus

Audio lessons do **not** cover:

- Advanced rendering techniques in depth (point to GPU lessons instead)
- UI widget implementation details (point to UI lessons instead)
- Mathematical derivations from scratch (point to math lessons instead)
- Codec implementation (WAV only — SDL handles the format)

### Rendering and UI baseline

Every audio lesson includes the same rendering and UI foundation so the
focus stays on the audio. This baseline is **not optional**.

**Use `forge_scene.h`** — one `forge_scene_init()` call provides all of
the following. See the `forge-scene-renderer` skill for the full API.

| Feature | Provided by `forge_scene.h` | Original skill reference |
|---|---|---|
| Blinn-Phong lighting | Per-material ambient + diffuse + specular | `forge-blinn-phong-materials` |
| Procedural grid floor | Anti-aliased shader grid on XZ plane | `forge-shader-grid` |
| Shadow map | Single directional shadow map | `forge-cascaded-shadow-maps` |
| Sky gradient | Procedural sky background | `forge-procedural-sky` |
| Camera controls | WASD + mouse look with delta time | `forge-camera-and-input` |
| Depth buffer | Depth testing with appropriate format | `forge-depth-and-3d` |
| sRGB swapchain | SDR_LINEAR for correct gamma | `forge-sdl-gpu-setup` |
| Forge UI panel | Immediate-mode controls for audio parameters | `forge-ui-rendering` |
| Procedural geometry | All shapes from `forge_shapes.h` | `forge-procedural-geometry` |
| Capture support | Screenshot via forge_capture.h | `dev-add-screenshot` |

### Audio-specific visual elements

Sound sources and audio state should have visual representation:

- **Sound source markers** — Spheres or icons at the 3D position of each audio
  source, color-coded by state (playing = green, paused = yellow, stopped = gray)
- **Volume indicators** — Sphere scale or color intensity proportional to volume
- **Distance rings** — Optional: circles on the ground showing attenuation
  distance thresholds (for spatial audio lessons)
- **Waveform display** — UI panel widget showing the current waveform or
  spectrum (for fundamentals and DSP lessons)
- **VU meters** — UI panel widget showing output level per channel

### Tone

Audio lessons should be practical and grounded. Digital audio has deep
signal-processing roots — present the essential math clearly while keeping
the focus on audible results.

- **Name the techniques** — "Constant-power panning", "inverse-distance
  attenuation", "biquad filter" — named techniques carry weight
- **Hear it, then understand it** — Let the listener experience the effect
  before explaining the math
- **Explain artifacts** — Why clipping sounds harsh, why discontinuities
  cause clicks, why aliasing produces unexpected frequencies
- **Encourage experimentation** — Audio is best learned by tweaking parameters
  and listening. Exercises should modify volume, distance, filter cutoffs,
  and other values.

### Code style

Follow the same conventions as all forge-gpu code:

- C99, matching SDL's style
- `ForgeAudio` prefix for public types, `forge_audio_` for functions
- `PascalCase` for typedefs, `lowercase_snake_case` for locals
- `UPPER_SNAKE_CASE` for `#define` constants
- No magic numbers — `#define` or `enum` everything
- Extensive comments explaining *why* and *purpose*

## Diagrams

Use the `/dev-create-diagram` skill for:

- Signal flow diagrams (source → mixer → master → speakers)
- Waveform visualizations (sine, square, noise)
- Filter frequency response curves
- Attenuation curves (linear, inverse, exponential)
- Stereo panning diagrams
- Audio buffer memory layout

### KaTeX math

Audio lessons use formulas for DSP concepts. Use inline `$...$` and display
`$$...$$` math notation. Display math blocks must be split across three lines
(CI enforces this).

## When NOT to Create an Audio Lesson

- The topic is covered by an existing audio lesson
- The concept is pure math with no audio aspect (belongs in a math lesson)
- The concept is purely about rendering (belongs in a GPU lesson)
- The concept is about UI widget implementation (belongs in a UI lesson)
- The topic is too narrow for a full lesson (add to an existing lesson instead)

In these cases, update existing documentation or plan for later.

## Tips

- **Start with the audio** — Get the sound working with placeholder
  rendering first, then polish the visuals. Correct audio with basic
  visuals is better than a beautiful scene with broken sound.
- **Use headphones** — Spatial audio and stereo effects are best evaluated
  with headphones. Note this in the README.
- **Audio files are user-supplied** — The repo does not distribute audio. Each
  lesson's `audio.conf` (gitignored) points to a local directory. The README
  describes what types of files work best and where to find royalty-free audio.
- **Show state** — Use forge UI to display volume levels, cursor positions,
  buffer states, and other audio internals. Audio is easier to learn when
  you can see the numbers alongside hearing the results.
- **ASCII-only console output** — Use only ASCII characters in printf output
  for cross-platform compatibility.
