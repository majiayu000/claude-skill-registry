---
name: dev-review-diagrams
description: Validate diagram correctness against the lesson README before pushing
argument-hint: "[lesson-key, e.g. gpu/34 or math/05]"
disable-model-invocation: false
---

Pre-push validation skill that cross-checks every diagram function against the
lesson README to catch correctness issues before they reach CodeRabbit review.

**When to use this skill:**

- Before pushing a lesson that includes diagrams
- As part of `/dev-final-pass` (section 18)
- After modifying diagram functions or the README sections they illustrate
- When CodeRabbit flagged diagram correctness issues in a previous round

The user provides:

- **Lesson key**: e.g. `gpu/34`, `math/05`, `engine/04`

If missing, infer from the current branch name or most recent lesson directory.

## Steps

### 1. Identify all diagrams for the lesson

Read `scripts/forge_diagrams/__main__.py` and find the lesson's entry in the
`DIAGRAMS` dict. List every `(filename, function)` pair registered for the
lesson key.

If the lesson has no registered diagrams, report "No diagrams registered for
this lesson" and exit.

### 2. Read the lesson README

Read the full `lessons/<category>/<NN-name>/README.md`. For each diagram file
referenced in the README (via `![...](assets/<name>.png)`), note:

- The surrounding text — what does the README claim this diagram shows?
- Any equations, coordinate systems, or algorithm steps described nearby
- Variable names and terminology used in the explanation
- Whether the README describes 2D or 3D, which axes, which orientation

### 3. Cross-check each diagram function

For each diagram function, read its source code in the relevant per-lesson file
under `scripts/forge_diagrams/<track>/lesson_NN.py` and verify:

#### Geometry and math accuracy

- [ ] Plotted geometry matches the documented equations (if the README says
  `y = sin(x)`, the code must plot `np.sin(x)`, not `np.cos(x)`)
- [ ] Coordinate systems are consistent (if the README says Y-up, the
  diagram must not show Z-up)
- [ ] If the README describes an OBB, the diagram draws a rotated box — not
  an axis-aligned one
- [ ] If the README describes a 3D concept, all three axes are present and
  labeled correctly
- [ ] Arrow directions match the data flow or vector directions described
  in the README

#### Labels and annotations

- [ ] Axis labels match the README's variable names (if README says
  "view-space depth", the axis label must not say "world-space Z")
- [ ] Annotations use the same terminology as the README — no synonyms
  that could confuse readers (e.g. "fragment" vs "pixel" must match)
- [ ] Mathematical notation in labels matches the README's notation

#### Algorithm and pipeline correctness

- [ ] If the README describes N pipeline stages, the diagram shows all N
- [ ] Stencil/blend operations match the described algorithm (increment
  vs decrement, src-alpha vs one-minus-src-alpha)
- [ ] State transitions match the order described in the README

#### Docstring accuracy

- [ ] The function's docstring accurately describes what the function
  actually plots (not a copy-paste from a different diagram)
- [ ] The docstring does not claim the diagram shows something it does not

### 4. Run each diagram

Execute each diagram and verify it generates without errors:

```bash
python scripts/forge_diagrams --lesson <lesson-key>
```

If any diagram raises an exception, report the error with traceback.

### 5. Report results

Present a checklist per diagram:

```text
Diagram Review — Lesson NN: Name
==================================

1. diagram_name.png (function: diagram_diagram_name)
   [PASS] Geometry matches README equations
   [PASS] Axis labels match README terminology
   [PASS] Docstring matches actual content
   [FAIL] README says "3 cascade levels" but diagram only shows 2
   [PASS] Generates without errors

2. another_diagram.png (function: diagram_another)
   [PASS] All checks passed

Overall: 1 issue found — fix before pushing
```

For each failure, include:

- The specific README text that the diagram contradicts
- The specific line(s) in the diagram function that need fixing
- A suggested correction

## What this skill does NOT do

- Does not check visual style (colors, fonts, spacing) — the STYLE dict and
  `/dev-create-diagram` handle that
- Does not check Python code quality — Ruff handles that
- Does not modify any files — it only reports findings
- Does not check screenshots — only matplotlib-generated diagrams
