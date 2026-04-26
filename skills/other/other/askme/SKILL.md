---
name: askme
description: Verbalized Sampling (VS) protocol for deep intent exploration before planning. Use when starting ambiguous or complex tasks, when multiple interpretations exist, or when you need to explore diverse intent hypotheses and ask maximum clarifying questions before committing to an approach.
---

# Ask Me Command

Before proceeding to ask planning questions, you must *proactively and critically* execute both Verbalized Sampling (VS) and exploration:

- For Verbalized Sampling, generate and *sample* at least N distinct, diverse candidates that represent different possible user intents or directions, ranked by likelihood, where N is dynamic by ambiguity/risk/scope (baseline N>=5; trivial N>=3; high ambiguity/risk N>=7; architectural N>=10; no hard cap). Run actor-critic on each VS sample: explicitly record one weakness, contradiction, and oversight before selecting a direction. VS prevents over-engineering by surfacing simpler alternatives; expand only while new samples materially change planning decisions, and prefer the smallest sufficient N.

**Required VS Output Format:**
```
1. [Most likely] hypothesis here
   - Weakness: [potential flaw]
   - Contradiction: [logical conflict if any]
   - Oversight: [what this misses]

2. [Alternative] hypothesis here
   ...
```

- For exploration, deliberately seek out unconventional, underexplored, and edge-case possibilities relating to the user's objective, drawing on both the provided context and plausible but non-obvious requirements. Include at least 3 edge cases (at least 5 if architectural), and stop expanding once additional cases no longer change decisions.

Only after completing *both* critical VS and exploration steps, proceed to use the question tool to ask the *maximum possible number* of precise, clarifying, and challenging planning questions that holistically address the problem space, taking into account uncertainty, gaps, and ambiguous requirements.

## `AskUserQuestion` tool contract (Claude Code reference)

This protocol assumes a single "ask user" tool with the contract below. Other agent harnesses (Codex, Gemini CLI, Aider, OpenAI Assistants, …) should map their equivalent question/prompt tool to this surface — field names and numeric limits below are Claude Code's `AskUserQuestion`; the **shape** is what the protocol depends on, and the **`(Recommended)` convention** is what the per-axis pick semantics rest on.

## Antipattern: override-checklist UI [LOAD-BEARING]

**Bad shape — never generate this:**
```
Which of these defaults should I override before I lock in the plan?
❯ 1. [ ] Diff-only mode
  2. [ ] Include root prompts
  3. [ ] CLAUDE.md wins on conflict
  4. [ ] Bump plugin manifests
```
This is a single `multiSelect: true` question where **unticked = "default stands"**. It collapses four independent axes into one checkbox list. Never generate this shape.

**Correct shape — one single-select question per axis:**
```
Q1 — Scope (single-select)
❯ Diff-only mode (Recommended) — propagate only recently-new CLAUDE.md
  Full block alignment — full sweep across all blocks

Q2 — Roots (single-select)
❯ Skip root prompts (Recommended) — derivative artifacts
  Include root prompts — also touch ODD/{GENERIC,COMPACTED,MINIMAL}

Q3 — Conflict policy (single-select)
❯ Preserve target policy (Recommended) — non-conflicting only
  CLAUDE.md wins — override divergent target policy

Q4 — Manifests (single-select)
❯ Skip bump (Recommended) — sibling-harness scope
  Bump minor — semver per CLAUDE.md memory note
```

**Positive routing rule:** When the brief calls for the user to *rarely have to type*, route the intent into N per-axis single-select questions (≤4 per fire) — each axis's `(Recommended)` option carries the default. Ticking `(Recommended)` *is* accepting the default.

**Never use `multiSelect` for axis-with-default override semantics.** Reserve `multiSelect` strictly for additive picks (feature toggles, optional sub-tasks).

**Per fire (one tool call):**
- `questions` array — `minItems: 1, maxItems: 4`. All questions in the array render as one batched UI; one user round-trip per fire.

**Per question:**
- `question` — full sentence ending in `?`
- `header` — short chip label, ≤ 12 characters
- `multiSelect` — boolean (default `false`). `false` = single-pick (mutually exclusive options); `true` = subset of additive items (feature toggles, optional sub-tasks)
- `options` — array, `minItems: 2, maxItems: 4`

**Per option:**
- `label` — 1-5 words; the chip text the user sees and ticks. Mark the recommended choice by appending `(Recommended)` to its label and placing it **first** in the array.
- `description` — explanation of the trade-off / consequence; the one-sentence rationale lives here.
- `preview` — optional rendered content (markdown, monospace box). Single-select only (tool constraint). Use for visual comparisons (layout mockups, code diffs, file trees); skip when the difference is purely conceptual.

**Built-in escapes (do not duplicate):**
- The free-text "Other" input is **auto-provided** on every question; never add an explicit "Other" option.
- Users may attach free-text notes via the `annotations` response field.

**Plan-mode caveat:**
- Use this tool only to *clarify requirements* or *choose between approaches* during planning. Do **not** ask "Is the plan ready?" / "Should I proceed?" — that's what `ExitPlanMode` is for.

**askme-specific notes:**
- The "maximum possible number" of questions above is bounded by the tool's per-fire cap (4); for larger question sets, fire multiple sequential batches, ordered by dependency.
- Render the VS block immediately before the first `AskUserQuestion` fire of a planning session; subsequent intra-session fires need not repeat the VS preamble unless the survivor set materially changed.

**Mapping for other harnesses:**
- If the harness exposes only single-question prompts, fire them sequentially in the dependency order — the *shape* (clarifying questions with one Recommended each) is what matters; batching is an optimization.
- Map `(Recommended)` to whatever default-marker convention the harness uses; the rationale belongs in the description body either way.
- Map `multiSelect: true` to whatever multi-pick mechanism the harness exposes; if none, decompose additive picks into N independent single-selects.
