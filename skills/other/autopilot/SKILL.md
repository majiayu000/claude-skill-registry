---
name: autopilot
description: Hands-off end-to-end delivery pipeline that CHAINS existing ODIN skills — plan → proceed → simplify → review → fix → atomic-commit-and-push → gh-fix-ci → report — with review-gated sequencing and an autofix-then-halt posture; it sequences and gates, it never reimplements the skills it calls. Use when the user says "autopilot", "lfg", "take this from plan to shipped", "run the whole pipeline", "hands-off ship it", or "do the end-to-end build". Entry is execution-only (plan onward); strategy and ideation stay upstream and manual. `proceed` is the single execution step inside this chain; `review-fix-grill-loop` is the review/fix loop only — autopilot spans plan through CI.
metadata:
  short-description: Hands-off plan→ship pipeline chaining existing skills
---

# Autopilot — hands-off plan→ship pipeline that chains existing skills

`autopilot` runs a build request from plan to shipped without re-prompting at every step. It is a **chain**: each phase invokes an existing ODIN skill via the Skill tool and gates on the result before the next phase begins. It owns sequencing, the phase gates, and the terminal report — nothing else. It writes no code surface of its own; the chained skills do.

Adapted from EveryInc/compound-engineering-plugin (MIT).

`Op: extend` — a new orchestration capability over skills that already exist. The entropy it adds (sequencing + gates) is load-bearing for the hands-off contract; the work itself is the chained skills', not autopilot's.

## When to Apply

- The user hands an execution-ready task and wants it taken from plan to shipped without step-by-step approval: "autopilot", "lfg", "ship it end to end", "take it from plan to PR".
- A concrete change is specified — enough for `plan` to produce implementation units. The pipeline executes; it does not discover what to build.

## When NOT to Apply

- **No concrete task yet** (vague goal, greenfield discovery) → `askme` / `strategy` / `ideate` upstream first, manually. autopilot never chains those; arriving with an execution-ready task is the entry contract.
- **A single execution step against an existing plan** → `proceed`. autopilot wraps `proceed` with the rest of the arc; if that arc is unwanted, call `proceed` directly.
- **The review→fix loop on a diff until clean** → `review-fix-grill-loop` (multi-iteration, medium floor). autopilot's review→fix is a single bounded pass, not a loop.
- **Ship existing commits only** → `atomic-commit-and-push`. **Fix failing CI only** → `gh-fix-ci`. **Read-only review** → `review`.

## Inputs and Flags

- `[task]` — the execution-ready request handed to `plan` as Phase 1 input. Required; an empty/ambiguous task halts at G1.
- `against <ref>` — base-ref override forwarded to the diff-scoped phases (`simplify`, `review`).
- `mode:local` — force local-only (skip push + CI) even when a remote exists.
- `mode:headless` — non-interactive overlay; pass through to each chained skill's headless variant where it has one. No phase prompts the user; a gate that would prompt instead HALTs with the question in the report.

## The chain

Each row is one phase: the named skill is invoked, not reimplemented. This is the phase map only. The gate that advances each phase, its autofix arm, and the halt action are defined once — in the Validation Gates table below for the in-body summary, and in `references/pipeline-gates.md` for the authoritative pass-criteria, state machine, and halt/report formats.

| # | Phase | Invokes | Note |
|---|-------|---------|------|
| 1 | Plan | `plan` | read-only |
| 2 | Execute | `proceed` | implements the plan |
| 3 | Simplify | `simplify` | compress the new diff |
| 4 | Review | `review` | read-only assessment |
| 5 | Apply fixes | `fix` | **conditional** — runs only when G4 fails; it is the review gate's autofix arm, not an unconditional step |
| 6 | Commit + push | `atomic-commit-and-push` | push half skipped local-only |
| 7 | CI | `gh-fix-ci` | skipped local-only |
| 8 | Report | — | always, on success or HALT |

## Support files — read on demand

Don't bulk-load. Read at the step that needs it.

- `references/pipeline-gates.md` — the authoritative source for every gate's exact pass-criteria, the autofix arm per gate, the autofix-then-halt state machine, local-only detection, and the halt-handoff and report formats. The Validation Gates table below is the in-body summary; read the reference when running any gate or deciding a halt.

## Workflow

The sequence and its halt mechanics; exact pass-criteria per gate are in the Validation Gates table and `references/pipeline-gates.md`.

1. **Phase 1 — Plan.** Invoke `plan` with the task (read-only). G1 fails on an ambiguous request — no autofix exists for "scope unknown"; HALT and hand off to upstream `askme`/`strategy`.
2. **Phase 2 — Execute.** Invoke `proceed` against the plan. G2 red → autofix arm `fix` runs **once**, re-check; still red → HALT.
3. **Phase 3 — Simplify.** Invoke `simplify` on the new diff. `simplify` self-reverts a behavior regression; an unrecoverable exit (new rejection ground / mixed commit) is G3 fail → HALT.
4. **Phase 4 (+5) — Review-gate.** Invoke `review` (read-only). Only if a critical/high finding exists, invoke `fix` **once** on those findings (Phase 5), then re-review the changed files. Residual critical/high after the one pass is G4 fail → HALT.
5. **Phase 6 — Commit + push.** Detect remote via `git remote`. Invoke `atomic-commit-and-push`; local-only → commits only, push half skipped. A push refusal (force/protected) is G6 fail and not autofixable → HALT.
6. **Phase 7 — CI.** Skipped local-only. Otherwise invoke `gh-fix-ci`, which watches PR checks and runs its own fix arm **once**; still red is G7 fail → HALT, hand off failing-check logs/URLs.
7. **Phase 8 — Report.** Always — on success or at the halt point. Phases run, gates passed/failed, residual handoff, commits/PR, the next operator's action.

## Constitutional Rules (Non-Negotiable)

1. **Chain, never reimplement.** Each phase delegates to its named skill via the Skill tool. autopilot owns sequencing, gates, and the report — nothing else. Inlining a phase's logic is Graft.
2. **Execution-only entry.** The chain starts at `plan` and never invokes `strategy` or `ideate`. Greenfield discovery is upstream and manual; auto-chaining it to "be helpful" on a vague request is Excess.
3. **Review-gated sequencing.** A phase begins only after the prior gate passes. No phase starts on a red gate.
4. **Autofix-then-halt.** On a failing gate, run the bounded autofix arm **once** (`fix` for the verifier and review gates, `gh-fix-ci` for the CI gate), then re-check. Still failing → HALT, hand off residual findings, run the report. Never run an autofix arm twice. Never carry a red gate into the next phase — compounding a bad change across phases is the exact failure this rule prevents.
5. **Local-only when no remote.** Detect via `git remote`; empty (or `mode:local`) → skip the push half and the whole CI phase; still commit and still report.
6. **Baseline wins.** On any conflict with `~/.claude/claude/system-prompt-baseline.md`, the baseline governs.

## Validation Gates

Gate id equals phase number; Phase 5 (`fix`, G4's autofix arm) and Phase 8 (Report) are gateless, so there is no G5 or G8.

| Gate | Pass Criteria | Autofix arm (once) | Blocking |
|------|---------------|--------------------|----------|
| G1 Plan | concrete plan + critical files; task not ambiguous | none | Yes — HALT to upstream `askme`/`strategy` |
| G2 Execute | repo-native verifier green after `proceed` | `fix` | Yes — HALT on still-red |
| G3 Simplify | clean exit, behavior preserved | `simplify` self-revert | Yes — HALT on new rejection ground / mixed commit |
| G4 Review | no critical/high finding after one fix pass + re-review | `fix` then re-review | Yes — HALT on residual critical/high |
| G6 Commit/push | atomic commits made; push ok (local-only: commits only) | none | Yes — HALT on push refusal |
| G7 CI | PR checks green | `gh-fix-ci` watch+fix | Yes — HALT on still-red; skipped local-only |
| Report emitted | terminal report produced on success or HALT | — | Yes |

## Anti-patterns

- **Reimplementing a chained skill inline** instead of invoking it. The whole value is composition; inlining is Graft and drift.
- **Chaining strategy/ideate** to rescue a vague request. Greenfield is manual; autopilot refuses to discover scope.
- **Looping an autofix arm until green.** The posture is once-then-halt. A second autofix attempt hides a bad plan and compounds risk; HALT and hand off instead.
- **Carrying a red gate forward** "to fix later". The next phase amplifies the defect over a larger surface.
- **Inventing a remote** to push a local-only repo. No remote → commit and report.
- **Skipping the report on HALT.** When the pipeline stops early, the residual-findings handoff IS the deliverable.

## Disambiguation

- **vs `proceed`** — `proceed` is the single execution step (plan→code, verify each step). It IS Phase 2 of this chain. autopilot wraps it with plan before and simplify/review/ship/CI after.
- **vs `review-fix-grill-loop`** — that skill is a diff-scoped review→resolve→fix **loop** that iterates to a clean floor. autopilot's Phase 4+5 is a **single bounded pass** (review → fix once → re-review → halt), sitting inside the larger plan→ship arc. Want the loop-to-clean on a diff and nothing else → use `review-fix-grill-loop`.
- **vs `simplify` / `fix` / `atomic-commit-and-push` / `gh-fix-ci`** — each is one phase. Call it directly when you want only that phase.
- **vs `strategy` / `ideate`** — upstream, manual, deliberately not chained. autopilot starts where they end.

## Operating surface

autopilot writes no code surface itself. `proceed` and `fix` write the working tree; `atomic-commit-and-push` writes commits and the remote; `plan`/`review` are read-only; `simplify` self-reverts on regression. autopilot owns the phase sequence, the gate decisions, and the terminal report. No writes to undefined or doubly-owned locations.
