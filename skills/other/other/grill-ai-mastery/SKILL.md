---
name: grill-ai-mastery
description: Hybrid interview that probes AI-engineering mastery by tip-vocabulary depth — entity referencing, loop closure, observability, harness improvement — not by token usage or LOC. Start collaborative (two-way tip exchange), escalate to adversarial probing when depth is lacking. Trigger when the user says "interview me on AI", "stress-test my Claude usage", "evaluate this candidate's AI engineering", or otherwise asks for an AI-collab skill assessment. User-only — never auto-invoke.
disable-model-invocation: true
---

Probe AI mastery by what the subject *names*, not by how much they *generate*. The premise from the chat that prompted this skill: token usage and LOC are noise; concrete tip vocabulary (URL-as-entity-ref, loop closure, observability) is signal.

## Mode disambiguation

| Skill                    | Anchor                                         | Posture                                         |
| ------------------------ | ---------------------------------------------- | ----------------------------------------------- |
| **`grill-ai-mastery`**   | AI-collab tip vocabulary tree (this file)      | Hybrid: collaborative → adversarial             |
| `grill-me`               | Any plan/design under test                     | Linear adversarial, recommendation per question |
| `request-refactor-plan`  | A refactor in particular                       | Adversarial interview specific to refactoring   |

This skill is the AI-mastery anchor; `grill-me` is the domain-agnostic version. Pick by what's being assessed.

## Phase 1 — Collaborative tip-sharing

Open by asking the subject to *name* a tip they actually use when collaborating with an LLM. Two-way: surface one of yours back as a counter-tip. The exchange is the assessment, not a quiz. Watch for:

- Concrete protocol names (URL-as-entity-ref, AGENTS.md, MCP resources, structured outputs) versus generic platitudes ("I write good prompts").
- Direction-of-travel signals — does the subject describe loops, observability, anchored references? Or do they describe vibes, screenshots, "the function we discussed"?
- Self-correction — when the subject reaches for a vague handle, do they catch themselves and produce a URL?

Stay collaborative as long as the depth matches the level the assessment is calibrated to.

## Phase 2 — Adversarial probe (escalation)

Promote to adversarial questioning when **any** of these signals fire:

- **Vague answers** — "I just use it normally" / "good prompts" / "I check the output" with no protocol name attached.
- **Token-usage / LOC framing** — the explicit anti-pattern from the chat that prompted this skill. Surface the rejection: "those measure quantity, not capability. What do you actually do that someone less skilled does not?"
- **Inability to name three protocols** — when prompted directly, cannot produce three concrete tactics with a why for each.
- **Unanchored entity references** in the conversation itself — the subject says "the PR" / "that bug" without offering a URL.

In adversarial mode, walk the tip-vocabulary tree:

1. **Entity referencing** — how do you point at an entity so a future session can find it? (Looking for: URL permalinks, MCP resources, file:line, symbol paths.)
2. **Durable references** — where does the next session start? (Looking for: PR comment threads, AGENTS.md, structured logs — not chat memory.)
3. **Loop closure** — when work needs N iterations, what does the inner loop look like and where is the human? (Looking for: CLI triggers, file outputs, contract assertions, human at the outer loop only.)
4. **Harness improvement** — what do you do when the loop cannot close? (Looking for: trap-or-abandon — improve the harness, do not babysit.)

Recommend per the `AskUserQuestion` contract below — mark the option with `(Recommended)` and place it first. The recommendation gives the subject a calibration point without grading on a hidden rubric.

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

## Stop conditions

- Tree is walked end-to-end with substantive answers per fork.
- A blocking gap surfaces — the subject lacks a basic protocol vocabulary; halt and recommend `ai-collab-protocols` as a starting point rather than continuing the probe.
- Subject converges with the assessor — depth matches; no further probing changes the verdict.

## Anti-patterns to flag in the subject

- **Token usage as a proxy for skill** — already named above; reject and redirect.
- **LOC as productivity** — comments-as-LOC is the running joke of the source chat; treat as the tell that the subject does not yet think in protocols.
- **"Mindless automation eats the most tokens"** — paraphrase from the chat. If the subject argues automation is the high-skill move, probe whether they distinguish *open-observability autonomous loops* from *babysat scripts*.

## Tab-complete note

`grill-ai-mastery` and `grill-me` share the `grill-` prefix and will tab-complete adjacent. Both exist intentionally: `grill-me` for general design grilling, this skill for AI-collab assessment specifically. Confirm with the user which they meant when invocation is ambiguous.