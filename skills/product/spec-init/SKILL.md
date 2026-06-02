---
description: Use when starting a new project or product and you want a docs-first plan before writing code — scaffolds an empty, product-neutral spec-driven-development cascade (product vision, MVP PRD, target tech-stack) for a human to fill, then hands off to brainstorm. Emits skeletons only; it never authors product content and never overwrites existing docs.
disable-model-invocation: true
---

# Spec Cascade Init Skill

You are scaffolding a **docs-first cascade**: a small set of empty, human-fillable steering documents that capture product direction *before* any code exists. This is optimus's bootstrap for spec-driven development.

**What you produce** (three skeletons under the project root, all product- and tool-neutral):

- `docs/product/product-context.md` — the long-term product vision.
- `docs/product/mvp-prd.md` — the first product slice (MVP PRD).
- `docs/product/tech-stack.md` — the target technology stack.

**The boundary — do not cross it.** You emit **empty skeletons with `TODO` markers** for a human to fill. You **author no product content** — no personas, no metrics/KPIs, no business-value prose, no technology choices. optimus is an engineering tool; the cascade is product/PM territory that a human owns. The engineering build spec is authored later by `/optimus:brainstorm` (in `docs/specs/`), not here. See `$CLAUDE_PLUGIN_ROOT/references/sdd-mapping.md` for the full contract.

## Step 1 — Pre-flight

- Decide where the cascade should live. Normally that is the current project root. If this directory is part of a larger multi-repo workspace, consult `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` and scaffold at the appropriate level (workspace root vs. a subproject) rather than blindly in the current folder.
- This skill is most valuable on a **greenfield** project (docs-first, before code), but it is safe to run anywhere — Step 2 guarantees it never clobbers existing work.

## Step 2 — Non-destructive existence check

For each of the three target files, check whether it already exists:

- If a file **exists**, never overwrite it — record it as `exists → skipped`.
- If a file is **missing**, you will create it in Step 3.

If all three already exist, the cascade is already scaffolded: report that and skip to Step 4.

## Step 3 — Emit the skeletons

- Read `$CLAUDE_PLUGIN_ROOT/skills/spec-init/references/cascade-templates.md`.
- For each **missing** file, create the parent directory if needed (`docs/product/`) and write the matching template block **verbatim** to its target path. Do not fill in the `TODO` markers — that is the human's job.
- Write **only** these three files. Specifically, do **not**:
  - scaffold a build-spec file in `docs/specs/` — the buildable spec is authored later by `/optimus:brainstorm` or dropped in by a human, in `docs/specs/`; see the contract;
  - write anything under `.claude/` (settings, hooks, `.optimus-version`, or docs) — agent/project setup is `/optimus:init`'s job, not this skill's;
  - invent product names, technology choices, or any content beyond the neutral templates.

## Step 4 — Report and hand off

- Summarize what was **created** vs. **skipped**.
- Tell the user to fill the `TODO` sections top-down (vision → MVP PRD → target stack), and state the precedence (the canonical rule lives in `$CLAUDE_PLUGIN_ROOT/references/sdd-mapping.md` and is restated in each scaffolded doc's header) so they know how the docs relate: *higher docs set long-term direction; the active build spec governs what to build right now — when they conflict about current work, the active build spec wins.*
- Close with the handoff tip. This is **not** a continuation skill (the human fills the docs out-of-band and `/optimus:brainstorm` gathers its own context), so use the default — Variant C in `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md`:

  > **Next step:** fill in the cascade's `TODO` sections (vision → MVP PRD → target stack). Then run `/optimus:brainstorm` to design the first build — it reads the cascade as steering and writes the engineering spec to `docs/specs/`.
  >
  > **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
