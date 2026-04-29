---
name: grill-me
description: Adversarial relentless interview against any plan or design until shared understanding is reached. Walk the decision tree, resolve dependencies one answer at a time, recommend a default per question. Trigger when the user says "grill me", "stress-test this", "interview me about this design", or otherwise asks for hostile-but-fair scrutiny of a proposal. General-purpose — no domain anchor required.
disable-model-invocation: true
---

Adversarial interview. Walk every branch of the design tree; resolve dependencies one decision at a time; recommend an answer per question.

## Modality disambiguation [LOAD-BEARING]

Three adjacent skills — pick the right one before invoking.

| Skill | Shape | Anchor | Output | Use when |
|---|---|---|---|---|
| *clarifying-question protocol* | VS-shaped — sample N intent hypotheses, rank, challenge each, then batch clarifying questions | None — pre-planning ambiguity | Survivor set + clarified scope | User intent is itself unclear |
| **this skill** | Linear adversarial interview, recommendation per question | None — design under test is the only anchor | Shared understanding, decision tree resolved | User has a plan/design and wants it stress-tested |
| *domain-model grilling* | Adversarial interview gated on documented domain language | `CONTEXT.md` + `docs/adr/` | Updated `CONTEXT.md` and/or new ADR | Project has documented domain language to honour |

**Rule of thumb:** intent unclear → clarifying-question protocol. Plan exists, no domain rubric → this skill. Plan exists, domain rubric required → domain-model grilling.

## Process

### 1. Anchor on the design under test

Confirm what the plan is in one sentence. If the user's pitch is too thin to interrogate, pivot to a clarifying-question protocol instead.

### 2. Walk the decision tree

For every fork in the design — scope, boundary, ordering, error surface, contract, naming, public-API shape, irreversibility — ask one question. Order by dependency: parents before children.

For each question:

- State the question precisely (one fact at a time).
- Recommend an answer with a one-sentence rationale.
- Wait for the user; never proceed on assumed answers.

### 3. Explore the codebase before asking when possible

If a question can be resolved by reading the code, read it instead of asking.

- Discovery: `fd -e <ext> <path>`.
- Structural search: `ast-grep run -p '<pattern>' -l <lang> -C 3`.
- Lexical search: `git --no-pager grep -n -C 3 '<pattern>'`.
- Targeted read: `bat -P -p -n -r START:END <path>`.
- Dispatch an Explore agent when the question spans >5 files or >2 directories.

### 4. Resolve dependencies before descending

Do not ask child questions while the parent is unresolved. If a parent answer invalidates a queued child, drop the child.

### 5. Stop conditions

Halt when one of:

- Every fork has a committed answer with a stated rationale.
- A blocking unknown surfaces that the user must investigate offline.
- The plan dissolves under questioning — declare it and recommend pivot.

## Question taxonomy (what counts as a fork worth grilling)

- Public API shape — names, signatures, error modes, ordering.
- Storage / state ownership — single source vs replicated, sync vs async, consistency model.
- Boundary placement — what crosses a process / network / module seam.
- Failure surface — throw vs Result, retry policy, partial-failure semantics.
- Concurrency — ownership of mutable state, lock ordering, backpressure, cancellation.
- Irreversibility — migrations, deletions, deployments, paid calls.
- Performance budget — p50/p95 targets, allocation budget, hot-path constraints.

Skip — pure mechanics: syntax, import order, brace placement, repo-conventional choices.

## Recommendation discipline

- Always recommend. "You decide" is forbidden.
- Render the recommendation by appending `(Recommended)` to the option label and placing it first per the contract below.
- Distinguish recommendation from verdict: the user can override; the rec is taste, not gate.
- If no defensible one-sentence rationale exists, the question is not a real fork — drop it.

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

## Language-neutral examples

**Rust** — Plan: "Add a `RetryClient` wrapper around our HTTP client." Forks: error surface (panic on exhaustion vs `Result<_, RetryError>`), retry policy (fixed vs exponential vs jittered), cancellation (drop-as-cancel vs explicit `CancellationToken`), idempotency contract (caller-asserted vs key-derived). Walk in that order; recommend `Result` + jittered exponential + drop-as-cancel + caller-asserted.

**Java / Spring Boot 3** — Plan: "Introduce a domain event bus for `Order` lifecycle." Forks: synchronous vs async dispatch, in-process vs broker (Kafka/RabbitMQ), at-least-once vs exactly-once semantics, ordering guarantees per aggregate, dead-letter handling. Walk parents first before children; recommend async + in-process for v1 with explicit upgrade path documented.

Forbidden: asking what the codebase already answers, accepting "I don't know" without parking the question.
