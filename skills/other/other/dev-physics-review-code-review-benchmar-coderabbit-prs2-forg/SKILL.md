---
name: dev-physics-review
description: Code quality, correctness, and documentation review for physics lessons — run before dev-final-pass
argument-hint: "[lesson-number or lesson-name]"
disable-model-invocation: false
---

Run a physics-specific quality review on a physics lesson before running
`/dev-final-pass`. This skill catches the recurring code quality, correctness,
and documentation issues specific to `forge_physics.h` and its callers. It is
not a replacement for `/dev-final-pass` — it covers the physics-domain concerns
that the general final pass does not.

The user provides:

- **Lesson number or name** (e.g. `01` or `point-particles`)

If missing, infer from the current branch name or most recent physics lesson
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
`common/physics/forge_physics.h`, the lesson's `main.c`, and the relevant test
files (`tests/physics/test_physics.c`). Each agent works independently and
reports findings.

### Agent 1: Memory safety

- Buffer overflows, out-of-bounds access, use-after-free
- Array index bounds relative to capacity/count fields (particle arrays,
  contact arrays, constraint arrays)
- Pointer arithmetic that could go out of range
- String operations without length checks

### Agent 2: Parameter validation

- NULL pointer dereference on every function parameter
- Integer overflow or underflow on size/count parameters
- Negative mass, negative dt, zero-length vectors passed to normalize
- Functions that silently accept invalid state (e.g. NaN position)

### Agent 3: Bug detection

- Off-by-one errors in loops and index calculations (particle iteration,
  contact pair enumeration)
- Incorrect operator precedence in compound expressions (force calculations,
  dot/cross products)
- Copy-paste errors (wrong axis in repeated x/y/z blocks, wrong particle in
  pair operations)
- Incorrect comparison operators (< vs <=, == vs !=)
- Integer truncation or implicit narrowing conversions (float to int in
  index calculations)

### Agent 4: Undefined behavior

- Signed integer overflow
- Shift amounts exceeding type width
- Uninitialized variables read before assignment (especially in struct init
  functions — every field must have an explicit initial value)
- Strict aliasing violations
- Division by zero without guards (mass, vector length, denominator in
  impulse calculations)

### Agent 5: Resource cleanup

- Every `SDL_malloc`/`SDL_calloc`/`SDL_realloc` has a matching `SDL_free` on
  every exit path — bare `malloc`/`free` must not be used; the codebase uses
  SDL's allocation functions exclusively
- Every dynamically allocated array inside a struct is freed with `SDL_free`
  when the struct is destroyed
- Early-return paths release all resources allocated before the return
  (GPU buffers, shape data, textures)
- `forge_shapes_free()` called for every generated shape after GPU upload
- Cleanup functions handle partially initialized state (NULL fields)
- SDL GPU resources (buffers, textures, pipelines, samplers) released in
  `SDL_AppQuit`

After collecting findings from all five agents:

1. **Validate** — review each finding to confirm it is a real issue
2. **Fix** — apply corrections to the source files
3. **Revalidate** — have the agents re-check the fixed code
4. **Repeat** until zero findings remain
5. **Add tests** — write tests covering every function reviewed and every issue
   found. Ensure callers of these functions check return values.

---

## Phase 2 — Verification checks

Spawn **one agent per check** to verify the following across all changed files.
The scope for each check is specified in its description.

### Check 1: Test return value assertions

**Scope:** all test files in `tests/physics/`

For setup and success-path code, wrap `forge_physics_*` calls that return
`false` on failure with `ASSERT_TRUE(...)` so tests fail immediately on
unexpected errors.

For negative-path tests that intentionally trigger failures, assert the expected
failure explicitly with `ASSERT_FALSE(...)` (or equivalent).

**What to look for:**

- Bare calls like `forge_physics_integrate(&p, dt)` without checking the return
- Calls inside helper functions that swallow the return value
- Setup code that calls library functions but does not propagate failures

### Check 2: Magic numbers in tests

**Scope:** all test files in `tests/physics/`

Numeric literals representing reusable or semantically meaningful tuning
parameters (masses, forces, timesteps, tolerances, domain constants) should be
defined as `#define` or `enum` at the top of the relevant test section. Other
test sections in the same file already follow this convention — new code must
match. One-off literals in a single tightly scoped assertion are acceptable
when they remain clear and do not obscure intent.

**Acceptable bare numbers:**

- `0`, `1`, `-1` as trivial loop/comparison values
- Array indices into small known-size arrays
- Mathematical constants inherent to formulas (e.g. `2.0f` in `2 * pi`)

**Unacceptable bare numbers:**

- Mass values (`2.0f`, `0.5f`)
- Force magnitudes (`9.81f` outside of a named constant)
- Timestep values (`0.016f`, `1.0f / 60.0f`)
- Restitution or damping coefficients (`0.8f`, `0.99f`)
- Position coordinates used as initial conditions (`10.0f`, `5.0f`)
- Tolerance values for `ASSERT_NEAR` (`1e-4f`, `1e-6f`)
- Iteration counts for stability tests (`10000`)
- Expected velocity, position, or energy thresholds

### Check 3: Numerical safety

**Scope:** `common/physics/forge_physics.h` (all `forge_physics_*` functions)

Ensure that any arithmetic that could produce `inf`, `NaN`, or wildly
incorrect results is handled:

- Division by zero: `1.0f / mass` without checking `mass > 0`,
  or computing `inv_mass` from an invalid mass value; `vec3_normalize()`
  on a zero-length vector; denominator in impulse calculations
  (e.g. `sum_inv_mass`) must be checked before dividing
- `sqrtf(negative)` — squared distance checks should guard against floating-
  point rounding producing tiny negative values before taking square root
- Accumulated floating-point drift producing ±inf over many simulation steps
  (especially with high iteration counts or extreme forces)
- Functions that accept `float` parameters should reject or clamp non-finite
  values at entry
- Vector normalization must check `vec3_length() > epsilon` before dividing
- Restitution must be clamped to `[0, 1]`, damping to `[0, 1]`, penetration
  depth to `>= 0`

### Check 4: Integration correctness

**Scope:** `common/physics/forge_physics.h` (integration and force functions)

Verify that the integration follows the documented algorithm exactly:

- **Symplectic Euler order** — velocity updated before position. If the README
  documents symplectic Euler, the code must update `v += a * dt` then
  `x += v * dt` (using the *new* velocity), not `x += v * dt` then
  `v += a * dt` (which is explicit Euler)
- **Force accumulator cleared** after integration — forces must not persist
  across frames
- **Damping applied correctly** — multiplicative damping
  (`v *= pow(damping, dt)` or `v *= damping`) not additive
- **inv_mass used for acceleration** — `a = force * inv_mass`, not
  `a = force / mass` (which would divide by zero for static objects)
- **Static objects skipped** — `if (inv_mass == 0) return` at the top of
  integration and force functions

### Check 5: Unused variables

**Scope:** `common/physics/forge_physics.h`, the lesson's `main.c`, all
changed test files

Remove any unused variables. Check for:

- Variables assigned but never read
- Function parameters that are never used (add `(void)param;` or remove)
- `#define` constants that are never referenced
- `typedef` types that are never instantiated
- Struct fields that are set but never read

### Check 6: API comment accuracy

**Scope:** `common/physics/forge_physics.h`, the lesson's `main.c`, the
lesson's `README.md`

Update or remove misleading or incorrect API comments:

- Comments describing behavior that the code does not implement
- Parameter descriptions that don't match the actual parameter type or meaning
- Return value documentation that doesn't match the actual return semantics
- Cited algorithm names that don't match the actual implementation (e.g.
  comment says "Verlet" but code implements symplectic Euler)
- Reference citations (textbook, paper) that are incorrect or don't exist
- TODO/FIXME comments for work that has been completed
- Comments referencing renamed or removed functions/fields

### Check 7: Simulation determinism

**Scope:** `common/physics/forge_physics.h`, the lesson's `main.c`

Ensure the simulation is deterministic with fixed timestep and identical inputs:

- No use of `rand()`, `time()`, or other non-deterministic functions in the
  physics step (randomness for initial conditions is fine, but must use a
  seeded RNG that can be reset)
- No floating-point operation order that varies by frame (e.g. summing forces
  in a data-dependent order)
- `PHYSICS_DT` is a constant, not derived from frame time
- The accumulator pattern correctly drains without skipping or doubling steps
- Reset (R key) restores the exact initial state — no accumulated drift in
  "initial" values
- Pause (Space) truly freezes physics — no partial steps leak through

### Check 8: Test setup return values

**Scope:** all test files in `tests/physics/`

Ensure any test setup/helper code that can fail returns a boolean value. If the
helper allocates resources, initializes particles, or calls `forge_physics_*`
functions, it should return `bool` and the caller should `ASSERT_TRUE` on it.

### Check 9: Mandatory lesson contract

**Scope:** the lesson's `main.c` and shaders

Every physics lesson must include the rendering baseline and controls defined
in `/dev-physics-lesson`. Verify each item is present — the review FAILS if
any are missing:

**Rendering baseline (all required):**

- **Blinn-Phong lighting** — scene shader computes ambient + diffuse + specular
  with material uniforms
- **Procedural grid floor** — grid shaders exist and are drawn on the XZ plane
- **Shadow map** — a depth-only shadow pass renders to a shadow texture; the
  scene shader samples it for shadows
- **Camera controls** — WASD + mouse look using the quaternion camera pattern
  (`quat_from_euler`, `mat4_view_from_quat`)
- **Depth buffer** — depth texture created and used for depth testing
- **Procedural geometry** — all shapes come from `forge_shapes.h` (no inline
  geometry generation functions, no model loading)

**Simulation controls (all required):**

- **R key** — resets simulation to initial state
- **P key** — pauses/resumes physics (camera still works while paused)
- **T key** — toggles slow motion

**Deliverables (all required):**

- **Screenshot** — `assets/screenshot.png` exists or capture support is wired
- **Animated GIF** — `assets/animation.gif` exists or GIF capture is wired
  (physics is dynamic — a static screenshot alone is insufficient)

### Writing tests for checks 3, 4, and 7

After completing checks 3, 4, and 7, write **dedicated tests** for every
finding and for the general cases covered:

- **Numerical safety tests** — pass zero mass, negative mass, `INFINITY`,
  `NAN`, zero-length vectors, and zero dt to functions and verify they return
  `false` or produce clamped/safe output. Run long simulations (10000+ steps)
  and verify no position or velocity becomes NaN or infinity.
- **Integration correctness tests** — verify symplectic Euler produces the
  documented update order. Compare single-step results against hand-calculated
  reference values. Verify force accumulator is zeroed after integration.
  Verify static objects are unmoved.
- **Determinism tests** — run two identical simulations and verify bit-for-bit
  identical results. Run a simulation, reset, run again, and verify identical
  results. Verify that different frame rates with the same fixed timestep
  produce the same physics state.

All new tests must follow the guidelines from checks 1 and 2:

- Wrap `forge_physics_*` calls with `ASSERT_TRUE` where they return bool
- Define numeric literals as `#define` constants at the top of the test section

After collecting findings from all eight checks:

1. **Validate** — review each finding to confirm it is a real issue
2. **Fix** — apply corrections to the source and test files
3. **Revalidate** — have the agents re-check the fixed code
4. **Repeat** until zero findings remain

---

## Phase 3 — Documentation and content verification

Spawn **one agent per check** to verify documentation quality.

### Doc check 1: Struct and function documentation

**Scope:** `common/physics/forge_physics.h`

Verify that **every** struct field has an inline comment explaining:

- **Why** it exists (not just what it is)
- **Units** (kg, m/s, m/s², N, radians, seconds)
- **Valid range** (>= 0, [0..1], non-NULL, 0 for static)
- **Relationship** to other fields when relevant (e.g. `inv_mass` is
  precomputed from `mass`)

Bad: `float mass; /* mass */`
Good: `float mass; /* kg — zero means infinite mass (immovable object) */`

Verify that **every** function has a doc comment with:

- Summary (one sentence — what it does)
- Algorithm or physical law being implemented
- Parameters with types, valid ranges, units, and nullability
- Return value (if any) with units
- Usage example
- Cross-reference to the lesson that introduces it
- Reference to source material (textbook, paper)

### Doc check 2: KaTeX consistency

**Scope:** the lesson's `README.md`

Verify that any KaTeX math notation follows the same conventions as other
forge-gpu lessons:

- Inline math uses `$...$` (single dollar signs)
- Display math uses three-line format:

  ```text
  $$
  formula here
  $$
  ```

- Variable names are consistent with the code (`\text{velocity}` matches
  `velocity`, `\Delta t` matches `dt`)
- Formulas are correct and match the implementation in `forge_physics.h`
  and `main.c`
- Symplectic Euler equations show velocity updated before position

### Doc check 3: Matplotlib diagram compliance

**Scope:** any diagram scripts modified or added for this lesson

Verify diagrams adhere to the `/dev-create-diagram` skill guidelines:

- All colors come from `STYLE` dict — no hardcoded colors
- Text uses `path_effects` readability stroke
- Title has `pad >= 12`
- Labels do not overlap each other or lines
- Figure size follows the common size guidelines
- Function is registered in `DIAGRAMS` dict in `__main__.py`
- Function is re-exported through the track subpackage `__init__.py`
  (e.g. `scripts/forge_diagrams/physics/__init__.py`) — the reorg'd
  structure requires both `__main__.py` registration and track-level export
- Diagram passes `ruff check` and `ruff format --check`

### Doc check 4: README-to-code accuracy

**Scope:** the lesson's `README.md`, `main.c`, and `common/physics/forge_physics.h`

Verify that every code snippet, function signature, struct definition, and API
example shown in the README **exactly matches** the actual code in
`forge_physics.h` and `main.c`. Check for:

- Function names that were renamed in code but not updated in the README
- Parameter lists that differ between README examples and actual signatures
- Struct fields shown in the README that don't exist in the code (or vice versa)
- Integration equations in the README that don't match the code's update order
- Code flow described in prose that doesn't match the actual execution order
- Return types or error handling described differently than implemented

### Doc check 5: README currency

**Scope:** `README.md` (root), `lessons/physics/README.md`,
`common/physics/README.md`, `CLAUDE.md`, `PLAN.md`

Verify all index files are up to date with the changes from this lesson:

- **Root `README.md`**: Physics lessons section has a row for this lesson
  (create the section if this is the first physics lesson)
- **`lessons/physics/README.md`**: lessons table includes this lesson
- **`common/physics/README.md`**: all new types and functions added to the
  library are documented in the API reference; the lesson appears in
  "Where It's Used"
- **`CLAUDE.md`**: if the lesson changes project structure, conventions, or
  adds new modules, `CLAUDE.md` reflects those changes
- **`PLAN.md`**: the physics lesson entry is checked off

After collecting findings from all five doc checks:

1. **Validate** — review each finding to confirm it is a real issue
2. **Fix** — apply corrections to documentation, diagrams, and README files
3. **Revalidate** — have the agents re-check the fixed content
4. **Repeat** until zero findings remain

---

## Reporting

After completing all phases, report a summary table:

```text
Physics Review Results — Lesson NN: Name
==========================================

Phase 1 — Code Correctness
  Memory safety        ✅ PASS  (N functions checked)
  Parameter validation ✅ PASS  (N functions checked)
  Bug detection        ✅ PASS
  Undefined behavior   ✅ PASS
  Resource cleanup     ✅ PASS

Phase 2 — Verification Checks
  1. Test assertions       ✅ PASS  (N calls wrapped)
  2. Magic numbers         ⚠️  FIXED (N constants extracted)
  3. Numerical safety      ✅ PASS  (N guards added, N tests written)
  4. Integration correct.  ✅ PASS  (N paths checked, N tests written)
  5. Unused variables      ✅ PASS
  6. Comment accuracy      ✅ PASS
  7. Determinism           ✅ PASS  (N tests written)
  8. Setup returns         ✅ PASS
  9. Lesson contract       ✅ PASS  (rendering baseline, controls, deliverables)

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
