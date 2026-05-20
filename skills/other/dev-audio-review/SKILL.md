---
name: dev-audio-review
description: Code quality, correctness, and documentation review for audio lessons — run before dev-final-pass
argument-hint: "[lesson-number or lesson-name]"
disable-model-invocation: false
---

Run an audio-specific quality review on an audio lesson before running
`/dev-final-pass`. This skill catches the recurring code quality, correctness,
and documentation issues specific to `forge_audio.h` and its callers. It is
not a replacement for `/dev-final-pass` — it covers the audio-domain concerns
that the general final pass does not.

The user provides:

- **Lesson number or name** (e.g. `01` or `audio-basics`)

If missing, infer from the current branch name or most recent audio lesson
directory.

## How to run this skill

Work through the three phases below **in order**. Each phase launches parallel
agents. After each phase, validate findings, apply fixes, then have the agents
revalidate. Repeat until no more issues are found.

Use a Task agent (model: haiku) for builds, test runs, and linting — never run
those directly from the main agent.

**Be literal and exhaustive.** This is C — no RAII, no garbage collector. Every
resource you acquire must be released on every exit path, every struct field
must be documented, every error must be handled. Do not rationalize away
findings with "it's probably fine." If the check says every function, check
every function.

---

## Phase 1 — Code correctness sweep

Spawn **one agent per concern** to review every function added or modified in
`common/audio/forge_audio.h`, the lesson's `main.c`, and the relevant test
files (`tests/audio/test_audio.c`). Each agent works independently and
reports findings.

### Agent 1: Memory safety

- Buffer overflows in sample arrays, out-of-bounds reads past buffer end
- Reading beyond `sample_count` in audio buffers
- Pointer arithmetic on sample data that could go out of range
- Use-after-free on audio buffers while streams are still playing

### Agent 2: Parameter validation

- NULL pointer dereference on every function parameter
- Negative volume, out-of-range panning (`< -1` or `> 1`)
- Zero or negative sample rate, zero channels
- Buffer cursor exceeding sample count

### Agent 3: Bug detection

- Off-by-one errors in sample loops (especially at buffer boundaries and
  loop points)
- Incorrect channel interleaving (reading left sample as right or vice versa)
- Copy-paste errors (wrong channel, wrong buffer in stereo processing)
- Incorrect operator precedence in DSP calculations
- Integer truncation in sample index calculations

### Agent 4: Thread safety

- Shared state between main thread and audio callback/stream without
  synchronization
- Non-atomic reads/writes of volume, pan, playing state, cursor position
- Race conditions on buffer pointer (main thread frees while audio reads)
- Missing memory barriers for parameter updates visible to audio thread

### Agent 5: Resource cleanup

- Every `SDL_malloc`/`SDL_calloc` has a matching `SDL_free` on every exit path
- `SDL_DestroyAudioStream` called for every created stream
- Audio buffers freed when no longer needed
- Early-return paths release all resources (GPU buffers, audio data, shapes)
- `forge_shapes_free()` called for every generated shape after GPU upload
- SDL GPU resources released in `SDL_AppQuit`
- Audio device properly shut down in cleanup

After collecting findings from all five agents:

1. **Validate** — review each finding to confirm it is a real issue
2. **Fix** — apply corrections to the source files
3. **Revalidate** — have the agents re-check the fixed code
4. **Repeat** until zero findings remain
5. **Add tests** — write tests covering every function reviewed and every issue
   found

---

## Phase 2 — Verification checks

Spawn **one agent per check** to verify the following across all changed files.

### Check 1: Test return value assertions

**Scope:** all test files in `tests/audio/`

Wrap `forge_audio_*` calls that return `false` or NULL on failure with
`ASSERT_TRUE(...)` or `ASSERT(... != NULL)` so tests fail immediately on
unexpected errors.

### Check 2: Magic numbers in tests

**Scope:** all test files in `tests/audio/`

Numeric literals representing sample rates, volumes, channel counts, buffer
sizes, panning values, and tolerances should be `#define` constants. Follow
the same convention as other test files in the project.

### Check 3: Numerical safety

**Scope:** `common/audio/forge_audio.h`

- Output samples clamped to `[-1.0f, 1.0f]` before delivery
- Division by zero guarded in attenuation (zero distance), normalization,
  and filter coefficient calculations
- No `sqrtf(negative)` in distance calculations
- Volume and pan parameters clamped to valid ranges at entry
- Long playback does not accumulate floating-point drift (especially for
  phase accumulators in oscillators)

### Check 4: Audio correctness

**Scope:** `common/audio/forge_audio.h`

- Stereo panning uses constant-power law (sin/cos), not linear, to avoid
  volume dip at center — or if linear is used, document the trade-off
- Sample rate matches between buffer and output stream
- Channel count is consistent through the processing chain
- Loop points produce seamless audio (no click at loop boundary)
- Volume transitions are smoothed (per-sample interpolation) to prevent clicks
- Buffer reads do not go past `sample_count`

### Check 5: Unused variables

**Scope:** `common/audio/forge_audio.h`, the lesson's `main.c`, all
changed test files

Remove any unused variables, `#define` constants, typedefs, or struct fields.

### Check 6: API comment accuracy

**Scope:** `common/audio/forge_audio.h`, the lesson's `main.c`, the
lesson's `README.md`

Update or remove misleading or incorrect API comments. Check that documented
behavior matches actual behavior, parameter descriptions match actual types,
and cited references are correct.

### Check 7: UI integration

**Scope:** the lesson's `main.c`

- Forge UI panel is initialized and rendered every frame
- Volume sliders actually control audio volume in real time
- UI state updates do not cause audio glitches
- UI rendering uses the `forge-ui-rendering` pattern
- Font atlas texture is created and uploaded correctly
- UI vertex/index buffers are streamed correctly

### Check 8: Test setup return values

**Scope:** all test files in `tests/audio/`

Ensure test setup/helper code that can fail returns a boolean value and
callers `ASSERT_TRUE` on it.

### Check 9: Mandatory lesson contract

**Scope:** the lesson's `main.c` and shaders

Every audio lesson must include the rendering and UI baseline defined in
`/dev-audio-lesson`. Verify each item is present — the review FAILS if
any are missing:

**Rendering baseline (all required):**

- **Blinn-Phong lighting** — scene shader computes ambient + diffuse + specular
- **Procedural grid floor** — grid shaders drawn on the XZ plane
- **Shadow map** — depth-only shadow pass, scene shader samples for shadows
- **Camera controls** — WASD + mouse look using quaternion camera pattern
- **Depth buffer** — depth texture created and used for depth testing
- **Procedural geometry** — all shapes from `forge_shapes.h`

**UI baseline (all required):**

- **Forge UI panel** — at least master volume slider and play/pause indicator
- **UI rendering** — forge UI rendered via the GPU UI pipeline
- **Interactive controls** — sliders and buttons respond to mouse input

**Audio baseline (all required):**

- **SDL audio stream** — output goes through `SDL_AudioStream`
- **WAV loading** — at least one sound loaded from `assets/`
- **Volume control** — master volume adjustable via UI and/or keyboard

After collecting findings:

1. **Validate** — review each finding
2. **Fix** — apply corrections
3. **Revalidate** — re-check
4. **Repeat** until zero findings

---

## Phase 3 — Documentation and content verification

Spawn **one agent per check** to verify documentation quality.

### Doc check 1: Struct and function documentation

**Scope:** `common/audio/forge_audio.h`

Verify that **every** struct field has an inline comment explaining:

- **Why** it exists
- **Units** (Hz, samples, dB, linear gain, seconds)
- **Valid range** (>= 0, [0..1], [-1..1], non-NULL)
- **Relationship** to other fields when relevant

Verify that **every** function has a doc comment with:

- Summary, algorithm/technique, parameters, return value, usage example,
  lesson cross-reference, source reference

### Doc check 2: KaTeX consistency

**Scope:** the lesson's `README.md`

Verify KaTeX math follows project conventions: inline `$...$`, display
`$$...$$` on three lines, variable names match code, formulas are correct.

### Doc check 3: Matplotlib diagram compliance

**Scope:** any diagram scripts modified or added for this lesson

Verify diagrams adhere to `/dev-create-diagram` guidelines.

### Doc check 4: README-to-code accuracy

**Scope:** the lesson's `README.md`, `main.c`, and `common/audio/forge_audio.h`

Verify every code snippet, function signature, and struct definition in the
README exactly matches the actual code.

### Doc check 5: README currency

**Scope:** `README.md` (root), `lessons/audio/README.md`,
`common/audio/README.md`, `CLAUDE.md`, `PLAN.md`

Verify all index files are up to date:

- **Root `README.md`**: Audio lessons section has a row for this lesson
- **`lessons/audio/README.md`**: lessons table includes this lesson
- **`common/audio/README.md`**: all new types and functions documented
- **`CLAUDE.md`**: reflects any structural changes
- **`PLAN.md`**: the audio lesson entry is checked off

After collecting findings:

1. **Validate** — review each finding
2. **Fix** — apply corrections
3. **Revalidate** — re-check
4. **Repeat** until zero findings

---

## Reporting

After completing all phases, report a summary table:

```text
Audio Review Results — Lesson NN: Name
=======================================

Phase 1 — Code Correctness
  Memory safety        ✅ PASS  (N functions checked)
  Parameter validation ✅ PASS  (N functions checked)
  Bug detection        ✅ PASS
  Thread safety        ✅ PASS
  Resource cleanup     ✅ PASS

Phase 2 — Verification Checks
  1. Test assertions       ✅ PASS  (N calls wrapped)
  2. Magic numbers         ✅ PASS
  3. Numerical safety      ✅ PASS  (N guards verified)
  4. Audio correctness     ✅ PASS  (N paths checked)
  5. Unused variables      ✅ PASS
  6. Comment accuracy      ✅ PASS
  7. UI integration        ✅ PASS
  8. Setup returns         ✅ PASS
  9. Lesson contract       ✅ PASS  (rendering, UI, audio baselines)

Phase 3 — Documentation
  1. Struct/function docs  ✅ PASS  (N fields, N functions documented)
  2. KaTeX consistency     ✅ PASS
  3. Diagram compliance    ⏭️  SKIP (no diagrams modified)
  4. README accuracy       ✅ PASS
  5. README currency       ✅ PASS
```

For each WARN, FIXED, or FAIL, list the specific file, line, and issue with
the fix applied (or suggested if not yet applied). Ask the user if they want
to proceed to `/dev-final-pass`.
