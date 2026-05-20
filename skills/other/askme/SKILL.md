---
name: askme
description: Verbalized Sampling (VS) protocol for intent exploration before planning, mode-aware. Default `exhaustive` runs full VS; `collaborative` runs tip-sharing dialogue; `adversarial` walks the design tree one fork at a time. Auto-detects from phrasing ("help me refine" → collaborative, "poke holes" → adversarial); override via `/askme adversarial|collaborative|exhaustive`. Use for ambiguous tasks or maximum clarifying questions before committing.
---

# Ask Me Command

Before proceeding to ask planning questions, you must *proactively and critically* execute both Verbalized Sampling (VS) and exploration:

- For Verbalized Sampling, sample multiple intent hypotheses, assign each an explicit probability weight (0–1 scale), and identify the specific observation or scenario that would falsify each before selecting a direction. Each hypothesis names which operation (compress / extend / correct) and the rejection category it must avoid (overkill, monkey-patching, overcomplication). Expand hypothesis depth as ambiguity, risk, or architectural surface grows; keep it concise when scope is truly narrow. Explore meaningful edge cases until additional cases stop changing the decision; broaden sampling if no clear leader emerges. Surface decision points early with concrete options and trade-offs. Synthesize surviving hypotheses into one consolidated direction before responding. Output should stay compact and decision-oriented: intent summary, assumptions, and focused questions. Do not proceed on non-trivial changes without visible VS.

**Required VS Output Format:**
```
1. [Weight: 0.42] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]

2. [Weight: 0.28] hypothesis here
   - Falsifier: [observation or scenario that would invalidate this]
```

- For exploration, deliberately seek out unconventional, underexplored, and edge-case possibilities relating to the user's objective, drawing on both the provided context and plausible but non-obvious requirements. Include at least 3 edge cases (at least 5 if architectural), and stop expanding once additional cases no longer change decisions.

Only after completing *both* critical VS and exploration steps, proceed to use the question tool to ask the *maximum possible number* of precise, clarifying, and challenging planning questions that holistically address the problem space, taking into account uncertainty, gaps, and ambiguous requirements.

## Modes [LOAD-BEARING]

`askme` is intentionally one skill with three modes (not split into per-mode skills); callers without a mode arg get `exhaustive` (the original VS protocol) unchanged. The body above describes `exhaustive`; the two new modes share the AskUserQuestion contract and antipattern guidance below but differ in posture.

### Mode-selection (hybrid)

Auto-detect from invoking-context phrasing, with slash-arg override:

- User wording matches `help me refine`, `walk through with me`, `let's brainstorm`, `share tips` → **collaborative**.
- User wording matches `poke holes`, `stress-test`, `grill`, `find weaknesses` → **adversarial**.
- Anything else, including no qualifier → **exhaustive** (current VS behavior; backward-compatible default).
- Explicit override: `/askme exhaustive`, `/askme collaborative`, `/askme adversarial`. The override always wins over auto-detect. Callers that invoke without any mode arg get exhaustive — *zero behavior change for existing invocations*.

### `exhaustive` mode

The VS-shaped protocol described above. Sample multiple intent hypotheses, assign weights, identify the falsifier per hypothesis, then fire the maximum-cardinality clarifying question batch. This is the default when no other signal fires.

### `collaborative` mode

Two-way tip-sharing dialogue. Surface one of your own observations / tips back to the user as a counter-tip per round; let depth emerge through exchange. No scoring, no ranked sample. Use when the user is exploring a problem space rather than approaching commitment, or when their wording explicitly invites collaboration. Stop when the user signals convergence.

### `adversarial` mode

Walk the design tree one fork at a time. Per fork: state the question, recommend an answer with one-sentence rationale, wait for the user, do not proceed on assumed answers. Resolve dependencies parents-first; do not descend into children while a parent is unresolved. Stop conditions: every fork has a committed answer, a blocking unknown surfaces, or the design dissolves under questioning.

### Escalation triggers (collaborative → adversarial)

Promote from collaborative to adversarial mid-session when **any** of these fire:

- **Ambiguity cardinality** ≥ 2 valid architectural decisions surface from a single user message; force a fork.
- **Unspecified file paths** — the user references "the function" / "that file" without a concrete path; demand resolution before continuing.
- **Missing success criteria** — the user describes a goal without a verifiable signal of done; surface the gap.

Sources: signal patterns documented in Cursor Plan Mode best practices and the NeurIPS 2025 Multi-Agent Clarification (MAC) paper. Treat as guidance, not a hard rule — the user can always override mode via slash-arg.

### Mode interactions with the VS preamble

The VS preamble (sample, weight, falsifier-per-hypothesis) is required only in `exhaustive` mode. `collaborative` does not run VS — it foregrounds dialogue. `adversarial` runs VS once at the start to map the design tree, then proceeds per-fork.

## `AskUserQuestion` tool contract (Claude Code reference)

This protocol assumes a single "ask user" tool with the contract below. Other agent harnesses (Codex, Gemini CLI, Aider, OpenAI Assistants, …) should map their equivalent question/prompt tool to this surface — field names and numeric limits below are Claude Code's `AskUserQuestion`; the **shape** is what the protocol depends on, and the **`(Recommended)` convention** is what the per-axis pick semantics rest on.

## Antipattern: override-checklist UI [LOAD-BEARING]

**Bad shape — never generate this:**
```
Which of these defaults should I override before I lock in the plan?
❯ 1. [ ] Diff-only mode
  2. [ ] Include root prompts
  3. [ ] system-prompt-baseline.md wins on conflict
  4. [ ] Bump plugin manifests
```
This is a single `multiSelect: true` question where **unticked = "default stands"**. It collapses four independent axes into one checkbox list. Never generate this shape.

**Correct shape — one single-select question per axis:**
```
Q1 — Scope (single-select)
❯ Diff-only mode (Recommended) — propagate only recently-new baseline
  Full block alignment — full sweep across all blocks

Q2 — Roots (single-select)
❯ Skip root prompts (Recommended) — derivative artifacts
  Include root prompts — also touch ODD/{GENERIC,COMPACTED,MINIMAL}

Q3 — Conflict policy (single-select)
❯ Preserve target policy (Recommended) — non-conflicting only
  system-prompt-baseline.md wins — override divergent target policy

Q4 — Manifests (single-select)
❯ Skip bump (Recommended) — sibling-harness scope
  Bump minor — semver per system-prompt-baseline.md memory note
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
