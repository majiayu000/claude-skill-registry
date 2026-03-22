---
name: dev-ui-review
description: Code quality, correctness, and documentation review for UI lessons — run before dev-final-pass
argument-hint: "[lesson-number or lesson-name]"
disable-model-invocation: false
---

Run a UI-specific quality review on a UI lesson before running `/dev-final-pass`.
This skill catches the recurring code quality, correctness, and documentation
issues specific to the `forge_ui` / `forge_ui_ctx` libraries and their callers.
It is not a replacement for `/dev-final-pass` — it covers the UI-domain concerns
that the general final pass does not.

The user provides:

- **Lesson number or name** (e.g. `12` or `auto-widget-layout`)

If missing, infer from the current branch name or most recent UI lesson directory.

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
`common/ui/forge_ui.h`, `common/ui/forge_ui_ctx.h`, the lesson's `main.c`, and
the relevant test files. Each agent works independently and reports findings.

### Agent 1: Memory safety

- Buffer overflows, out-of-bounds access, use-after-free
- Array index bounds relative to capacity/count fields
- Pointer arithmetic that could go out of range
- String operations without length checks

### Agent 2: Parameter validation

- NULL pointer dereference on every function parameter
- Integer overflow or underflow on size/count parameters
- Negative dimensions, zero denominators, empty arrays
- Functions that silently accept invalid state

### Agent 3: Bug detection

- Off-by-one errors in loops and index calculations
- Incorrect operator precedence in compound expressions
- Copy-paste errors (wrong variable name in repeated blocks)
- Incorrect comparison operators (< vs <=, == vs !=)
- Integer truncation or implicit narrowing conversions

### Agent 4: Undefined behavior

- Signed integer overflow
- Shift amounts exceeding type width
- Uninitialized variables read before assignment
- Strict aliasing violations
- Division by zero without guards

### Agent 5: Resource cleanup

- Every `SDL_malloc`/`SDL_calloc`/`SDL_realloc` has a matching `SDL_free` on
  every exit path — bare `malloc`/`free` must not be used; the codebase uses
  SDL's allocation functions exclusively
- Every dynamically allocated array inside a struct is freed with `SDL_free`
  when the struct is destroyed
- Early-return paths release all resources allocated before the return
- Cleanup functions handle partially initialized state (NULL fields)

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

**Scope:** all test files in `tests/ui/`

For setup and success-path code, wrap `forge_ui_*` / `forge_ui_ctx_*` calls that
return `false` on failure with `ASSERT_TRUE(...)` so tests fail immediately on
unexpected errors.

For negative-path tests that intentionally trigger failures, assert the expected
failure explicitly with `ASSERT_FALSE(...)` (or equivalent).

**What to look for:**

- Bare calls like `forge_ui_ctx_init(&ctx, ...)` without checking the return
- Calls inside helper functions that swallow the return value
- Setup code that calls library functions but does not propagate failures

### Check 2: Magic numbers in tests

**Scope:** all test files in `tests/ui/`

Numeric literals representing reusable or semantically meaningful tuning
parameters (buffer sizes, dimensions, thresholds, domain constants) should be
defined as `#define` or `enum` at the top of the relevant test section. Other
test sections in the same file already follow this convention — new code must
match. One-off literals in a single tightly scoped assertion are acceptable
when they remain clear and do not obscure intent.

**Acceptable bare numbers:**

- `0`, `1`, `-1` as trivial loop/comparison values
- Array indices into small known-size arrays
- Mathematical constants inherent to formulas (e.g. `2.0f` in `2 * pi`)

**Unacceptable bare numbers:**

- Widget dimensions (`200, 300`)
- Font sizes (`16.0f`)
- Color values (`0.5f, 0.8f, 1.0f`)
- Padding, margins, spacing values
- Expected counts, positions, or thresholds

### Check 3: Inf/NaN handling

**Scope:** `common/ui/forge_ui_ctx.h` (all `forge_ui_ctx_*` functions)

Ensure that any arithmetic that could produce `inf` or `NaN` is handled:

- Division by zero (zero-width windows, zero-height panels, zero scale)
- `log(0)`, `sqrt(negative)`, or similar domain errors
- Accumulated floating-point drift producing ±inf over many frames
- Functions that accept `float` parameters should reject or clamp non-finite
  values at entry

### Check 4: State cleanup on early return

**Scope:** `common/ui/forge_ui.h`, `common/ui/forge_ui_ctx.h`

Ensure that context state is correctly cleared and no stale references persist:

- Early returns in begin/end pairs (e.g. `forge_ui_ctx_begin_window` /
  `forge_ui_ctx_end_window`) must restore the context to a consistent state
- Resource cleanup functions must zero out pointers after freeing
- Functions that modify shared state (active window, current layout, cursor
  position) must restore it on failure paths
- Partially initialized objects must not be left in arrays or lists

### Check 5: Unused variables

**Scope:** `common/ui/forge_ui.h`, `common/ui/forge_ui_ctx.h`, the lesson's
`main.c`, all changed test files

Remove any unused variables. Check for:

- Variables assigned but never read
- Function parameters that are never used (add `(void)param;` or remove)
- `#define` constants that are never referenced
- `typedef` types that are never instantiated

### Check 6: API comment accuracy

**Scope:** `common/ui/forge_ui.h`, `common/ui/forge_ui_ctx.h`, the lesson's
`main.c`, the lesson's `README.md`

Update or remove misleading or incorrect API comments:

- Comments describing behavior that the code does not implement
- Parameter descriptions that don't match the actual parameter type or meaning
- Return value documentation that doesn't match the actual return semantics
- TODO/FIXME comments for work that has been completed
- Comments referencing renamed or removed functions/fields

### Check 7: Shared state isolation

**Scope:** `common/ui/forge_ui_ctx.h`

Ensure separate windows, panels, or other UI objects are not sharing state
unexpectedly:

- Each window should have its own layout cursor, content bounds, and scroll
  state
- Collapsing one window must not affect another window's collapse state
- Z-order operations on one window must not corrupt another window's z-index
- Drag state for one window must not leak to another when windows overlap
- Widget IDs within different windows must not collide

### Check 8: Test setup return values

**Scope:** all test files in `tests/ui/`

Ensure any test setup/helper code that can fail returns a boolean value. If the
helper allocates resources, initializes contexts, or calls `forge_ui_*`
functions, it should return `bool` and the caller should `ASSERT_TRUE` on it.

### Writing tests for checks 3, 4, and 7

After completing checks 3, 4, and 7, write **dedicated tests** for every
finding and for the general cases covered:

- **Inf/NaN tests** — pass zero-size, negative, `INFINITY`, and `NAN` values
  to functions and verify they return `false` or produce clamped/safe output
- **State cleanup tests** — trigger early returns (e.g. begin a window then
  immediately end it, begin with invalid params) and verify context state is
  clean afterward
- **Shared state tests** — create multiple windows, manipulate each
  independently, and verify none affect the others

All new tests must follow the guidelines from checks 1 and 2:

- Wrap `forge_ui_*` calls with `ASSERT_TRUE`
- Define numeric literals as `#define` constants at the top of the test section

After collecting findings from all eight checks:

1. **Validate** — review each finding to confirm it is a real issue
2. **Fix** — apply corrections to the source and test files
3. **Revalidate** — have the agents re-check the fixed code
4. **Repeat** until zero findings remain

---

## Phase 3 — Documentation and content verification

Spawn **one agent per check** to verify documentation quality.

### Doc check 1: Struct property documentation

**Scope:** `common/ui/forge_ui.h`, `common/ui/forge_ui_ctx.h`

Verify that **every** new or modified struct field has an inline comment
explaining:

- **Why** it exists (not just what it is)
- **Units** where applicable (pixels, normalized 0-1, radians)
- **Valid range** where applicable (>=0, 0-255, NULL if unused)
- **Relationship** to other fields when relevant

Bad: `int count; /* count */`
Good: `int count; /* number of active windows, 0 when no windows are open */`

### Doc check 2: KaTeX consistency

**Scope:** the lesson's `README.md`

Verify that any KaTeX math notation follows the same conventions as previous UI
and GPU lessons:

- Inline math uses `$...$` (single dollar signs)
- Display math uses three-line format:

  ```text
  $$
  formula here
  $$
  ```

- Variable names are consistent with the code (`\text{width}` matches `width`)
- Formulas are correct and match the implementation in `main.c`

### Doc check 3: Matplotlib diagram compliance

**Scope:** any diagram scripts modified or added for this lesson

Verify diagrams adhere to the `/dev-create-diagram` skill guidelines:

- All colors come from `STYLE` dict — no hardcoded colors
- Text uses `path_effects` readability stroke
- Title has `pad >= 12`
- Labels do not overlap each other or lines
- Figure size follows the common size guidelines
- Function is registered in `DIAGRAMS` dict in `__main__.py`
- Diagram passes `ruff check` and `ruff format --check`

### Doc check 4: README-to-code accuracy

**Scope:** the lesson's `README.md` and `main.c`

Verify that every code snippet, function signature, struct definition, and API
example shown in the README **exactly matches** the actual code in `main.c` and
the library headers. Check for:

- Function names that were renamed in code but not updated in the README
- Parameter lists that differ between README examples and actual signatures
- Struct fields shown in the README that don't exist in the code (or vice versa)
- Code flow described in prose that doesn't match the actual execution order
- Return types or error handling described differently than implemented

### Doc check 5: README currency

**Scope:** `README.md` (root), `lessons/ui/README.md`, `common/ui/README.md`,
`CLAUDE.md`, previous lesson's `README.md`

Verify all index files are up to date with the changes from this lesson:

- **Root `README.md`**: UI lessons table has a row for this lesson
- **`lessons/ui/README.md`**: lessons table includes this lesson
- **`common/ui/README.md`**: any new types or functions added to the library
  are documented in the API reference; the lesson appears in "Where It's Used"
- **`CLAUDE.md`**: if the lesson changes project structure, conventions, or
  adds new modules, `CLAUDE.md` reflects those changes
- **Previous lesson's `README.md`**: "What's next" section links to this lesson

After collecting findings from all five doc checks:

1. **Validate** — review each finding to confirm it is a real issue
2. **Fix** — apply corrections to documentation, diagrams, and README files
3. **Revalidate** — have the agents re-check the fixed content
4. **Repeat** until zero findings remain

---

## Reporting

After completing all phases, report a summary table:

```text
UI Review Results — Lesson NN: Name
=====================================

Phase 1 — Code Correctness
  Memory safety        ✅ PASS  (N functions checked)
  Parameter validation ✅ PASS  (N functions checked)
  Bug detection        ✅ PASS
  Undefined behavior   ✅ PASS
  Resource cleanup     ✅ PASS

Phase 2 — Verification Checks
  1. Test assertions   ✅ PASS  (N calls wrapped)
  2. Magic numbers     ⚠️  FIXED (N constants extracted)
  3. Inf/NaN handling  ✅ PASS  (N guards added, N tests written)
  4. State cleanup     ✅ PASS  (N paths checked, N tests written)
  5. Unused variables  ✅ PASS
  6. Comment accuracy  ✅ PASS
  7. Shared state      ✅ PASS  (N tests written)
  8. Setup returns     ✅ PASS

Phase 3 — Documentation
  1. Struct docs       ✅ PASS  (N fields documented)
  2. KaTeX consistency ✅ PASS
  3. Diagram compliance ⏭️  SKIP (no diagrams modified)
  4. README accuracy   ✅ PASS
  5. README currency   ✅ PASS
```

For each WARN, FIXED, or FAIL, list the specific file, line, and issue with
the fix applied (or suggested if not yet applied). Ask the user if they want
to proceed to `/dev-final-pass`.
