---
name: dev-math-lesson
description: Add a math concept - create lesson, update library, document usage
argument-hint: "[number] [concept-name] [description]"
---

Create a new math lesson and update the math library (`common/math/forge_math.h`).

**When to use this skill:**

- You need math functionality that doesn't exist in `forge_math.h` yet
- A GPU lesson requires new math operations
- You want to teach a foundational math concept

**Smart behavior:**

- Before creating a lesson, check if the math already exists in `forge_math.h`
- If it exists, just document it better or create a lesson for existing code
- If creating from a GPU lesson's needs, extract only the math (not GPU-specific code)

## Arguments

The user (or you) can provide:

- **Number**: two-digit lesson number (e.g. 01, 02)
- **Concept name**: kebab-case (e.g. vectors, matrices, quaternions)
- **Description**: what this teaches (e.g. "Vectors, dot product, normalization")

If any are missing, infer from context or ask.

## Steps

### 1. Analyze what's needed

- **Check `common/math/forge_math.h`**: Does this math already exist?
- **Check existing math lessons**: Is there already a lesson for this?
- **Identify the scope**: What specific operations/concepts are needed?

### 2. Create the lesson directory

`lessons/math/NN-concept-name/`

### 3. Create a demo program (`main.c`)

A small, focused C program that demonstrates the math concept visually or numerically.

**Requirements:**

- **Standalone** — Can run without GPU (uses SDL for window/input if visual, or just printf if not)
- **Clear output** — Shows the math in action (visualization or printed results)
- **Well-commented** — Explains what's happening and why
- **Uses the math library** — `#include "math/forge_math.h"`

**Examples:**

- Vectors: print dot products, show perpendicular/parallel cases
- Matrices: print a rotation matrix, show before/after transformation
- Visual: use SDL to draw vectors, show transformations in a window

**Template structure:**

```c
/*
 * Math Lesson NN — Concept Name
 *
 * Demonstrates: [what this shows]
 *
 * SPDX-License-Identifier: Zlib
 */

#include <SDL3/SDL.h>
#include "math/forge_math.h"

int main(int argc, char *argv[])
{
    (void)argc;
    (void)argv;

    if (!SDL_Init(SDL_INIT_VIDEO)) {
        SDL_Log("SDL_Init failed: %s", SDL_GetError());
        return 1;
    }

    /* Demonstrate the math concept here */

    SDL_Quit();
    return 0;
}
```

**Console output formatting:**

- **Use ASCII-only characters** for console output (cross-platform compatibility)
- Avoid Unicode box-drawing, symbols, or special characters that may not render on Windows Terminal
- Good: `-`, `=`, `*`, `|`, `->`, `[OK]`, `[!]`, "degrees", "in", "+/-"
- Bad: `─`, `═`, `•`, `↓`, `→`, `✓`, `⚠`, `°`, `∈`, `±` (may render as garbled text on Windows)

### 4. Create `CMakeLists.txt`

```cmake
add_executable(NN-concept-name main.c)
target_include_directories(NN-concept-name PRIVATE ${FORGE_COMMON_DIR})
target_link_libraries(NN-concept-name PRIVATE SDL3::SDL3)

add_custom_command(TARGET NN-concept-name POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_FILE:SDL3::SDL3-shared>
        $<TARGET_FILE_DIR:NN-concept-name>
)
```

### 5. Create `README.md`

Structure:

````markdown
# Math Lesson NN — Concept Name

[Brief subtitle explaining what this teaches]

## What you'll learn

[Bullet list of math concepts covered]

## Key concepts

[Bullet list of core takeaways:]
- **Concept 1** — Brief explanation
- **Concept 2** — Brief explanation
- **Formula/operation** — What it does and when to use it

## The Math

[Explain the concept clearly, with intuition before formulas]

### [Subconcept 1]

[Explanation, formula, geometric meaning]

### [Subconcept 2]

[Explanation, formula, geometric meaning]

## Where it's used

Graphics and game programming uses this for:
- [Use case 1]
- [Use case 2]

**In forge-gpu lessons:**
- [Link to GPU lesson] uses `function_name()` for [purpose]
- [Link to GPU lesson] uses `function_name()` for [purpose]

## Building

```bash
cmake -B build
cmake --build build --config Debug

# Windows
build\lessons\math\NN-concept-name\Debug\NN-concept-name.exe

# Linux / macOS
./build/lessons/math/NN-concept-name/NN-concept-name
```

[Brief note on what the demo shows]

## Result

[Brief description of expected demo output or what the program demonstrates]

**Example output:**
```text
[Copy actual program output here]
```

**Important:** Copy output directly from running the program—don't manually type it.

## Exercises

1. [Exercise extending the concept]
2. [Exercise applying it differently]
3. [Exercise combining with other concepts]

## Further reading

- [Relevant math lesson that builds on this]
- [External resource if helpful]
````

### 6. Update `common/math/forge_math.h`

**Add the new math functions** following the library's conventions:

- **Documentation**: Summary, parameters, returns, usage example, geometric intuition
- **Naming**: `typeN_verb` (e.g., `vec3_dot`, `mat4_rotate_x`)
- **Implementation**: Clear, readable, matches textbook descriptions
- **Inline**: Use `static inline` for header-only functions
- **Comments**: Explain the math, not just the code

**Example:**

```c
/* Compute the dot product of two 3D vectors.
 *
 * The dot product measures how much two vectors point in the same direction.
 * Result = |a| * |b| * cos(θ), where θ is the angle between them.
 *
 * If the result is:
 *   - Positive: vectors point somewhat in the same direction
 *   - Zero:     vectors are perpendicular
 *   - Negative: vectors point in opposite directions
 *
 * Usage:
 *   vec3 a = vec3_create(1.0f, 0.0f, 0.0f);
 *   vec3 b = vec3_create(0.0f, 1.0f, 0.0f);
 *   float d = vec3_dot(a, b);  // 0.0 — perpendicular
 *
 * See: lessons/math/01-vectors
 */
static inline float vec3_dot(vec3 a, vec3 b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}
```

**If the function already exists**, improve documentation or skip this step.

### 7. Update project files

- **`CMakeLists.txt` (root)**: Add `add_subdirectory(lessons/math/NN-concept-name)`
- **`lessons/math/README.md`**: Add link to the new lesson (create this file if it doesn't exist)
- **`PLAN.md`**: Note the math lesson if relevant

### 8. Cross-reference GPU lessons

- **Find GPU lessons using this math**: Search for where these functions are (or should be) used
- **Update GPU lesson READMEs**: Add references to the math lesson
- **Update math lesson README**: List GPU lessons that use this math

### 9. Build and test

```bash
cmake -B build
cmake --build build --config Debug
./build/lessons/math/NN-concept-name/NN-concept-name
```

Verify the demo runs and produces expected output.

### 10. Verify key topics are fully explained

**Before finalizing, launch a verification agent** (Task agent) that audits every
key topic in the README for completeness. This catches cases where a key topic
name-drops a term (like "similar triangles") but the lesson never actually
explains what that term means — leaving readers confused.

**For each key topic / "What you'll learn" bullet, the agent must check:**

1. **Explained in the README** — Is the concept described clearly enough that a
   reader encountering it for the first time could understand it? Look in "The
   Math" section, key concepts, and any subsections.
2. **Demonstrated in the C program** — Does `main.c` actually exercise this
   concept with code and output? A key topic that's only mentioned in the README
   but never shown in the demo is incomplete.
3. **All referenced terms are defined** — Read the exact wording of each key
   topic and identify every math term, technical term, or concept it references
   (e.g., "similar triangles", "homogeneous coordinates", "affine transformation",
   "orthonormal basis"). For each referenced term, confirm it is explained
   somewhere in the lesson — either inline where first used, in its own
   subsection, or with a cross-reference to another lesson that covers it.

**What to flag:**

- A key topic references a term that is never defined or explained anywhere in
  the README
- A key topic is listed in "What you'll learn" but has no corresponding section
  in "The Math" or the demo program
- A term is used as though the reader already knows it, but no prior math lesson
  in the curriculum covers it either
- The C program prints results for a concept but the README doesn't explain how
  to interpret those results (or vice versa)

**How to fix flagged issues:**

- Add a brief, plain-language explanation where the term is first used (1-3
  sentences is usually enough — not a full derivation, just enough for the reader
  to follow along)
- If the term deserves a deeper treatment, add a focused subsection under "The
  Math" and link to it from the key topic
- If a prior lesson already covers the term, add an explicit cross-reference:
  "See [Lesson NN — Name](../NN-name/) for an explanation of [term]"
- If a key topic has no demo coverage, either add it to `main.c` or remove/revise
  the key topic to match what the lesson actually teaches

**The lesson is not complete until every key topic passes all three checks.**

### 11. Run markdown linting

Use the `/dev-markdown-lint` skill to check all markdown files:

```bash
npx markdownlint-cli2 "**/*.md"
```

If errors are found:

1. Try auto-fix: `npx markdownlint-cli2 --fix "**/*.md"`
2. Manually fix remaining errors (especially MD040 - missing language tags)
3. Verify: `npx markdownlint-cli2 "**/*.md"`

Common fixes needed:

- Add language tags to code blocks (`` ```text ``, `` ```c ``, `` ```bash ``)
- Use 4 backticks for nested code blocks (when showing markdown in markdown)

## MANDATORY: Chunked writes for large files

Task agents have a 32K output token limit per Write call. **Any file over ~800
lines** MUST be written in chunks — split into parts, write each to `/tmp/`,
then concatenate.

**Recovery rule — if a writing agent fails with a token limit error:**

- **NEVER write a fallback or simplified version.** STOP and report the failure.
- Re-run the write using the chunked approach.

See [`.claude/large-file-strategy.md`](../../../.claude/large-file-strategy.md)
for the full strategy.

## Math Library Conventions

### Coordinate System

- **Right-handed, Y-up**: +X right, +Y up, +Z forward
- **CCW winding**: Front faces have counter-clockwise vertices

### Matrix Layout

- **Column-major storage and math** (matches HLSL)
- Multiplication: `v' = M * v`
- Transform order: `C = A * B` means "apply B first, then A"

### Naming

- `vec2`, `vec3`, `vec4`, `mat4` — types
- `vec3_add`, `mat4_rotate_z` — functions
- No abbreviations except standard terms (vec, mat, lerp)

### Documentation Standard

Every function needs:

1. Summary sentence
2. Parameter descriptions (if not obvious)
3. Return value explanation
4. Geometric intuition
5. Usage example
6. Reference to math lesson

## Example: Adding Vector Operations

**Scenario:** Lesson 02 needs `vec2` and `vec3` for vertex positions and colors.

1. **Check library**: `vec2` and `vec3` types exist, basic ops exist
2. **Determine scope**: Need create, add, scale, normalize, dot, lerp
3. **Create lesson**: `lessons/math/01-vectors/`
4. **Demo program**: Print dot products of various vector pairs, show perpendicular/parallel cases
5. **README**: Explain vectors, dot product, normalization with geometric intuition
6. **Update library**: Add any missing vector operations with full documentation
7. **Cross-reference**: Note that Lesson 02 uses `vec2_create` and `vec3_create`
8. **Build and test**: Verify demo runs

## Example: Extracting Math from a GPU Lesson

**Scenario:** You're reviewing Lesson 03 and notice it has bespoke rotation math.

1. **Identify the math**: 2D rotation using sin/cos
2. **Check library**: `mat4_rotate_z` exists!
3. **Decision**: Don't create a new lesson for rotation yet (matrices lesson will cover it)
4. **Refactor Lesson 03**: Replace bespoke math with `mat4_rotate_z`
5. **Plan**: Add matrices lesson later (lesson 05-matrices)

## Tips

- **Start simple**: Basic operations (add, dot, normalize) before advanced (quaternions, projections)
- **One concept per lesson**: Don't combine vectors and matrices in one lesson
- **Visual when possible**: Showing rotations/transformations visually is more intuitive than printing numbers
- **Cross-reference extensively**: Help users connect math theory to GPU practice
- **Readable code**: This is teaching code, not production — clarity over performance
- **ASCII-only output**: Use only ASCII characters in printf output for cross-platform compatibility (Windows Terminal may not render Unicode correctly)
- **Example output accuracy**: If including example output in README, copy it directly from the actual program—don't manually type it. Learners will compare their output to yours.

## Diagrams and Formulas

**Find opportunities to create compelling diagrams and visualizations via the
matplotlib scripts** — they increase reader engagement and help learners
understand the topics being taught. Use the `/dev-create-diagram` skill to add
diagrams following the project's visual identity and quality standards.

### Matplotlib diagrams

For geometric or mathematical visuals (vector diagrams, interpolation grids,
frustum views), add a diagram function to
`scripts/forge_diagrams/math/lesson_NN.py` (create the file if it doesn't
exist):

1. Write a function following the existing pattern (shared `setup_axes`,
   `draw_vector`, `save` helpers from `_common.py`)
2. Re-export from `scripts/forge_diagrams/math/__init__.py`
3. Import and register in the `DIAGRAMS` dict in `__main__.py` with the lesson key
4. Run `python scripts/forge_diagrams --lesson math/NN` to generate the PNG
5. Reference in the README: `![Description](assets/diagram_name.png)`

Output goes to each lesson's `assets/` directory at 200 DPI (PNG only).

### Mermaid diagrams

For **flow/pipeline diagrams** (transformation pipelines, data flow), use inline
mermaid blocks. GitHub renders these natively:

````markdown
```mermaid
flowchart LR
    A[Step 1] --> B[Step 2] --> C[Step 3]
```
````

Use mermaid for sequential flows.

### KaTeX math

For **formulas**, use inline `$...$` and display `$$...$$` math notation.
GitHub renders these via KaTeX:

- Inline: `$\vec{a} \cdot \vec{b} = a_x b_x + a_y b_y$`
- Display math blocks must be split across three lines (CI enforces this):

```text
$$
\text{lerp}(a, b, t) = a + t \cdot (b - a)
$$
```

Keep worked-examples-with-numbers in ` ```text ` blocks — only convert
symbolic/algebraic formulas to KaTeX.

## When NOT to Create a Lesson

- The math already exists and is well-documented
- The operation is too trivial (e.g., vec3_create — just document it in existing lessons)
- The concept requires prerequisite lessons that don't exist yet
- It's GPU-specific, not pure math (belongs in a GPU lesson, not math lesson)

In these cases, just update documentation or plan for later.
