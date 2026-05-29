---
name: step2
description: "ONLY when user explicitly types /step2. Never auto-trigger on plan, design, or architect."
argument-hint: "[goal description]"
---

# /step2 - Structured Plan for Subagent Execution

Create _step2_plan.md that a fresh `/step3` session can execute with zero prior context.

_step2_plan.md is the **only context bridge** between this session and execution. Everything a subagent needs must be in the plan.

**Design principle:** Maximize safe parallel execution. Design for parallelism from the start, then serialize only where truly necessary.

## Flow

1. **Load context** — FIRST ACTION: read `_step1_decisions.md` at repository root. Do NOT ask the user anything before checking this file.
   - **Found:** Use it as the goal. Apply Scan Integration rules below. If it contains `## Unresolved`, warn the user and ask whether to resolve now or proceed.
   - **Not found:** Fall back to conversation context or ask the user what's being built.
2. **Research** — Read codebase, identify files, patterns, dependencies
3. **Design phases (parallelism-first)** — See Phase Design below
4. **Validate** — See Validation Checklist below
5. **MANDATORY: Write `_step2_plan.md`** — At **repository root** (NEVER in subdirectories) using the Write tool. Use `date` for timestamps. Do this BEFORE any closing remarks. This file is the primary deliverable — without it, /step2 failed.
6. **MANDATORY: Delete `_step1_decisions.md`** — Immediately after writing _step2_plan.md, delete it with Bash `rm`. Leaving it behind causes stale context in future sessions. Verify deletion before continuing.
7. **Confirm** — Only AFTER both file operations are confirmed, show summary and end with `Next: /step3 to execute. Tip: /clear first so /step3 gets a full context window.`

## Scan Integration

**Only applies when `_step1_decisions.md` exists.** Actively transform it — don't just copy:

- **Themed decision groups** → organize phases by theme
- **Pitfalls / Risks** → concrete guardrails placed in the specific phase where they apply
- **Key decisions** → stated in the phase they constrain, so the subagent sees them in context
- **Rejected alternatives** → per-phase guardrails ("Do NOT use X because Y")
- **Scope (what's out)** → restate exclusions in relevant phases to prevent drift

The Rationale section is rewritten for execution, not copied from _step1_decisions.md. A subagent needs: the approach, what NOT to do, and the patterns to follow.

## Phase Design (Parallelism-First)

1. **Identify the work units** — every distinct file or module change
2. **Group by independence** — which units touch completely separate files?
3. **Form parallel groups first** — units that can't conflict go in the same group as separate phases
4. **Serialize only what must be serial** — shared interfaces, types that other phases consume
5. **Split to unlock parallelism** — if a phase touches 4 files but only 1 creates a dependency, split it

**Granularity rule:** Prefer more smaller phases over fewer large ones, as long as each phase remains coherent. More phases = more parallelism. Never split below the point where a phase can't be understood in isolation.

### Phase Requirements

Each phase executes as an **isolated subagent in a fresh context** — must be self-contained:

- **Explicit file paths** — name specific files, never "the file from Phase 2"
- **No cross-phase references** — describe what's needed, don't point to other phases
- **One clear objective** — single responsibility
- **Concrete tasks** — actionable, unambiguous

### Context Budget

/step3 targets 50-150 lines per subagent dispatch. Design phases to fit:
- A phase with 5 Reference files and 8 tasks will blow the budget — split it
- If a phase needs extensive context to execute, it's too big or too vague

### Reference Field

The `**Reference:**` field is how a subagent orients itself without exploring the codebase. Guide attention:

```
**Reference:**
- `src/auth/middleware.ts` — follow the existing guard pattern (line ~30) for new guards
- `src/types/api.ts` — conform to the Response<T> wrapper type
```

What to include: files to read, what pattern to follow, interfaces to conform to. What NOT to include: files the subagent won't need.

### Guardrails Field

Per-phase guardrails derived from _step1_decisions.md pitfalls and codebase constraints:

```
**Guardrails:**
- Do NOT modify the existing User type — extend with a new interface
- All new endpoints must use the validation middleware from src/middleware/validate.ts
```

Only include when a phase has real risks of going wrong. Not every phase needs guardrails.

### Dependencies

- Explicit numeric: "Depends: 2,3"
- No transitive repetition (if 3→2→1, phase 3 lists only "2")
- Document what it provides: "Depends: 2 (creates lib/core.py)" — /step3 passes this verbatim to subagents

### Parallel Safety

- Same group MUST NOT touch same files
- Each phase lists what it modifies via **Modifies:** field
- When truly uncertain after analysis, serialize (safety > speed)

## Validation Checklist

Before writing _step2_plan.md, verify:

1. **Parallel maximization** — could any sequential dependency be broken by splitting a phase? Could any phase's dependencies be reduced?
2. **No file collisions** — scan every parallel group, confirm no two phases in the same group touch the same file
3. **Subagent autonomy** — for each phase: "could a subagent execute this with ONLY the phase text and the Reference files?" If no, add what's missing. Check that dispatch stays within ~150 lines
4. **Guardrail placement** — every _step1_decisions.md pitfall is addressed in a specific phase, not just floating in the Rationale
5. **Completeness** — all decisions are reflected in at least one phase's tasks or guardrails

## Rules

- **NEVER use Task or EnterPlanMode.** This skill IS the planning framework. Subagents lose your context. Plan mode hijacks your flow. Read/Glob/Grep directly.
- **Gate: write before farewell.** Never mention `/step3` or signal completion until `_step2_plan.md` has been written with the Write tool AND `_step1_decisions.md` has been deleted in the current conversation. Both file operations are proof the skill finished. Missing either = skill failed.

## _step2_plan.md Format

```markdown
<!-- @plan: /step2 YYMMDD_HHMM -->
# [Goal Title]

**Goal:** [1-2 sentence description]
**Created:** YYYY-MM-DD

## Rationale

Rewritten for subagent consumption — what approach, what to avoid, what patterns to follow.

**Approach:** [chosen approach]
**Why:** [key reasons grounded in codebase evidence]
**Patterns:** [codebase conventions subagents must follow]
**Non-goals:** [what's explicitly out of scope]

## Phases Overview

| Phase | Name | Depends | Parallel Group | Est. Lines |
|-------|------|---------|----------------|------------|
| 1 | ... | - | A | ~60 |
| 2 | ... | 1 | B | ~80 |
| 3 | ... | 1 | B | ~45 |
| 4 | ... | 2,3 | C | ~70 |

## Phase Details

### Phase 1: [title]
**Modifies:** [file/directory scope]
**Reference:**
- `path/to/file.ts` — [what to look at and why]
**Guardrails:**
- [constraint, if any]
**Tasks:**
- [ ] Task 1
- [ ] Task 2
```

Note: `Depends` and `Parallel Group` live only in the Phases Overview table (for /step3's orchestration). Phase Details sections contain only what subagents need: Modifies, Reference, Guardrails, Tasks.

## Output

```
Plan created: _step2_plan.md
- Phases: N (M can run in parallel)
- Parallel groups: N
- Est. dispatch sizes: all within budget / Phase X may be tight
Next: /step3 to execute. Tip: /clear first so /step3 gets a full context window.
```

## Lifecycle

```
/step1 → _step1_decisions.md written
    ↓ (fresh session)
/step2 → reads _step1_decisions.md → writes _step2_plan.md → deletes _step1_decisions.md
    ↓ (fresh session)
/step3 → checkpoint → executes → deletes _step2_plan.md (or reset to checkpoint on failure)
```

Both `_step1_decisions.md` and `_step2_plan.md` are disposable. Each stage produces an artifact, the next consumes and deletes it. The code changes are the deliverable, not the artifacts.
