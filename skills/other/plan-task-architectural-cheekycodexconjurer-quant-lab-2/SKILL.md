---
name: Plan Task (Architectural)
description: Use when the user asks for a plan or the task is complex/ambiguous. Enforces AGENTS.md workflow and encourages loading other relevant skills.
---

# Plan Task (Architectural)

Use this skill to produce a **fast, phased plan** consistent with `AGENTS.md`.

## When to use

- The user asks for a plan ("plan this", "how would you…", "phased plan").
- The task spans multiple files/subsystems.
- The requirements are ambiguous or risky.

## Protocol

1. Read: `architecture.md`, `README.md`, and the relevant `docs/architecture/*.md`.
2. Load supporting skills from `skills/` (see `skills/README.md`).

## Recommended output structure

### 1) Understanding & Mode

- 1–2 sentence summary of the request.
- Task mode (A/B/C/D/E) and what that implies (plan-only vs implement).

### 2) Investigation

- Files read (only what you opened).
- Current behavior/state (brief).
- Constraints (contracts, UX rules, limits).

### 3) Plan (phased)

Use 2–3 phases when helpful:

- Phase 1: preparation / refactor
- Phase 2: core change
- Phase 3: verification + cleanup + docs

For each phase: **what changes**, **files to touch**, **risks**.

### 4) Verification & Docs

- Commands to run (see `skills/verify_changes/SKILL.md`).
- Docs to update (see `skills/sync_docs/SKILL.md`).

