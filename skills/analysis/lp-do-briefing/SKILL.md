---
name: lp-do-briefing
description: Produce an understanding-only system briefing — how something works now, traced end-to-end with evidence pointers. No planning artifacts or tasks. Use when you need current-behavior understanding without committing to a plan.
---

# Briefing Orchestrator

`/lp-do-briefing` produces concise system briefings: current behavior explained end-to-end with evidence, no planning tasks.

Use this skill when:
- You want to understand a system before deciding whether to change it.
- A stakeholder needs a factual snapshot of current behavior.
- You need evidence pointers before writing a spec or planning a change.

Use `/lp-do-fact-find` instead when you intend to plan or build a change.

## Global Invariants

### Operating mode

**BRIEFING ONLY**

### Allowed actions

- Read/search files and docs.
- Run non-destructive commands (`rg`, targeted lint/typecheck) for evidence.
- Inspect targeted git history.

### Prohibited actions

- Code changes, refactors, or production data writes.
- Destructive shell/git commands.
- Planning/build execution — this skill ends at a briefing note.

### Evidence and quality rules

- Non-trivial claims require file/line pointers.
- Unknowns must include a concrete verification path.
- Omit empty sections or collapse to one-line `Not investigated: <reason>`.

## Required Inputs

- Topic or system area to understand.
- At least one location anchor (path guess, route, endpoint, error/log, or user flow).

If either is missing, ask only the minimum follow-up questions needed to unblock.

## Phase 0: Queue Check Gate

Load and follow: `../_shared/queue-check-gate.md` (briefing mode).

## Phase 1: Topic Selection

### Fast path (argument provided)

- Argument is a topic, file path, or system area → proceed to sufficiency gate.

### Discovery path (no argument)

- Ask the user what system, feature, or behavior they want to understand.

## Phase 2: Sufficiency Gate

Do not start investigation until topic and location anchor are both satisfied.

## Phase 3: Investigate

Load and follow:

- `modules/briefing.md`

## Phase 4: Persist Artifact

- Output path: `docs/briefs/<topic-slug>-briefing.md`
- Fallback: `docs/plans/<topic-slug>-briefing.md`
- Template: `docs/briefs/_templates/briefing-note.md`
- Fill with evidence. Omit empty sections.

## Completion Message

> Briefing complete. Note saved to `<path>`. This documents current behavior and evidence pointers. No planning artifact was produced. Use `/lp-do-fact-find` when you are ready to plan a change.
