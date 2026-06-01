---
name: diverge
description: |
  Generate 3–5 conceptually distinct approaches to a task before implementing.
  Labels each by creativity dimension: Novel, Surprising, Diverse, or Conventional.
  Holds for user selection before writing any code. Based on Creative Preference
  Optimization (Ismayilzada et al., 2025) — brainstorm-then-select for maximizing
  novelty, surprise, and diversity in outputs.
---

# Diverge

Use this skill when solving a problem where multiple non-obvious approaches exist.

## Behavior

When this skill is active and you receive a task, do not implement immediately.

First, generate **3–5 approaches** that are genuinely conceptually distinct — different in underlying mechanism, not just vocabulary.

Label each:
- **[Novel]** — semantically far from the conventional solution; different conceptual basis
- **[Surprising]** — violates the obvious assumption; would not be the first answer
- **[Diverse]** — maximally different from the other options in this list
- **[Conventional]** — the expected path, included for contrast

For each provide:
1. Core mechanism — one sentence
2. How it works and what makes it distinct — two to three sentences
3. Main tradeoff — one sentence

Then stop. Present all approaches and ask the user which to implement, or whether to synthesize elements from multiple.

## Constraints

- At least one approach must be **[Surprising]**
- At least one must be **[Novel]**
- No two approaches should restate the same idea in different vocabulary
- Novelty and surprise take priority over quality in this phase
- Do not write implementation code until the user selects a direction

## After selection

Implement the selected approach fully. If asked to synthesize, identify which elements are mechanically compatible and propose a hybrid plan before proceeding.
