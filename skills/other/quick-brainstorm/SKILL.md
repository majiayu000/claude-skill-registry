---
name: quick-brainstorm
description: >
  Lightweight brainstorming for bug fixes, small features, or code improvements
  that need clarification before implementation. Triggers deep questioning to
  ensure accurate output. Use when user asks to fix a bug, add a small feature,
  refactor code, or make targeted improvements — and the scope is small enough
  that a full brainstorm session is unnecessary. Do NOT use for large-scale
  architecture decisions or greenfield projects.
---

# Quick Brainstorm

**MANDATORY: Do NOT call any file-edit, file-create, or code-generation tools until Phase 1 Q&A self-check has passed or Fast Track criteria are met. Reading files for context is allowed. Violation = immediate stop and return to Q&A.**

Lightweight brainstorming → deep Q&A → design confirmation → Plan Mode → execution.

**Core principle:** Only ask deep, non-obvious questions. Goal is accurate output, not question count.

## Optional Parameters

- `--doc` — After design confirmation, write design doc to `docs/plans/YYYY-MM-DD-<topic>.md` using `create_file`.
- `--worktree` — Before starting, create isolated branch via `git worktree add ../quick-brainstorm-<topic> -b quick-brainstorm/<topic>` and work there.
- `--plan-file` — Write implementation plan to `docs/plans/YYYY-MM-DD-<topic>-plan.md` instead of only presenting in chat.

## Process

```
Task → Understand context (read files/code/commits)
     → Q&A (one question at a time, until self-check passes)
     → Multiple approaches? → Compare options with recommendation
     → Present design in sections, confirm each
     → Enter Plan Mode: create implementation plan, wait for approval
     → Execute after user approval
```

## Fast Track

May skip Q&A **only if ALL three conditions are true:**
1. The change is mechanical (single-line fix, typo, rename, or user gave exact code to write)
2. Zero design decisions or trade-offs involved
3. User's instruction leaves no room for interpretation

If any condition fails → go to Phase 1. When in doubt, ask one question to verify.

## Phase 1: Q&A

**Rules:**
- One question at a time, prefer multiple choice
- Skip anything Claude can infer from code/context
- Keep asking until self-check passes — not based on a minimum question count

**Self-check before ending Q&A:**
- [ ] Core functionality approach is clear
- [ ] Edge cases and error handling covered
- [ ] No missing related requirements
- [ ] User has confirmed or implicitly indicated discussion is sufficient (e.g., answered last question with no new concerns)

## Phase 2: Compare Options

**When:** 2+ reasonable approaches exist. **Skip when:** One clearly optimal solution.

Present each option with pros/cons and a recommendation with reasoning. Keep brief.

## Phase 3: Present Design

Present in sections, confirm each before continuing. Trim sections that don't apply.

1. Change overview — What and why
2. Technical approach — Implementation details, files involved
3. Data/API/UI changes — If any
4. Edge cases — Key cases only
5. Implementation steps — Brief execution order

## Phase 4: Plan Mode

After design confirmation, switch to planning-only mode (no code output yet):

1. **Create implementation plan** — List each step: files to change, what to change, expected outcome. If the environment supports a built-in plan mode (e.g. `plan` command, Plan Mode toggle, or `writing-plans` skill), use that; otherwise present the plan as a structured list in chat.
2. **Wait for explicit user approval** before writing any code.
3. **During execution**, pause and ask if encountering scenarios not covered in the plan.

## Guardrails

**STOP and return to the correct phase if any of these occur:**

- Calling edit/create tools before Q&A self-check passed (unless Fast Track criteria met)
- User says "no" but continuing with original approach
- Entering Plan Mode without design confirmation
- Executing without Plan Mode approval
- Judging a task as "obvious" without verifying all three Fast Track conditions
